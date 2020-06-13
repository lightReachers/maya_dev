import sys
import os

print(sys.path)
import maya.cmds as cmds
import maya.mel as mel
import pprint
from pymongo import MongoClient


class export(object):
    def __init__(self):
        # self.maya_file = sys.argv[1]
        self.data = {'pco': 'GAB'}

    # def init_maya(self):
    #     import maya.standalone
    #     maya.standalone.initialize()

    # def _test_raise_exception(fileObject, clientData):
    # #pretending that a file ref failed below. Ref path validation code would go here.
    #     clientData['exception'] = RuntimeError('bad ref {}'.format(fileObject.expandedFullName()))
    #     return False
    def save_shot_data(self, shot_data):
        client = MongoClient('serverName', 27010) # mongo server
        db = client['project']
        collection = db['data']
        id_inserted = collection.insert_one(post).inserted_id
        print('Shot data is submitted to database with id [ {} ]'.format(id_inserted))

    def export_cache(self):
        print(' \n ')
        print(' \n ')
        print('###################----------------------##################')
        # get file path for database
        current_file = cmds.file(q=True, sn=True)
        self.data['anim_file'] = current_file

        cache_keys = ['_pro_', '_veh_', '_cha_']
        allRefs_path = []
        allRefs = pm.listReferences()
        for r in allRefs:
            allRefs_path.append(r.path)  # for database
            if not r.isLoaded():
                for key_word in cache_keys:
                    if key_word in r.path:
                        if os.path.isfile(r.path):
                            r.load()
                        else:
                            print("Ref path does not exist for [ {} ]".format(r.path))

            if r.isLoaded():
                r.importContents(removeNamespace=False)

        sel_sets = cmds.ls(sets=True)

        set_data = {}
        patterns = ['_sel_set', '_selset', '_Sel_Set']
        selected = []
        for pattern in patterns:
            for sel_set in sel_sets:
                if sel_set.endswith(pattern):
                    selected.append(sel_set)
                    cmds.select(sel_set, add=True)
        print('Total Character : ', len(selected))

        all_transform = cmds.ls(selection=True)
        print('all_transform', all_transform)
        # print(pm.ls(transforms=True))
        prob_camera = [cam for cam in cmds.ls(assemblies=True) if 'CAMERA_RIG_DNA' in str(cam)]
        if prob_camera and len(prob_camera) > 0:
            render_cam = prob_camera[0]
            print('render_cam', render_cam)
            all_transform.append(render_cam)
            print(all_transform)
        else:
            print("*" * 5 + "NO RENDER CAM FOUND" + "*" * 5)
        print('Total shape count for baking : {}'.format(len(all_transform)))

        for n in selected:
            name = n.replace(':', '___')
            print(name)

        start = cmds.playbackOptions(q=True, min=True)
        end = cmds.playbackOptions(q=True, max=True)

        self.data['frames'] = [start, end]

        bake_frame = str(int(start)) + ':' + str(int(end))
        mel.eval('bakeResults -simulation true -t "%s" -hierarchy below -sampleBy'
                 ' 1 -oversamplingRate 1 -disableImplicitControl true -preserveOutsideKeys true'
                 ' -sparseAnimCurveBake false -removeBakedAttributeFromLayer false -removeBakedAnimFromLayer '
                 'false -bakeOnOverrideLayer false -minimizeRotation true -controlPoints false -shape true { %s }'
                 % (bake_frame, ', '.join('"%s"' % x for x in all_transform)))

        maya_file = pm.sceneName()

        basename = os.path.basename(maya_file)
        basename_list = basename.split('_')
        ###target = "G:\PRODUCTION\05_Cache\EP_013B\SC 005\SH_006\ANIM_0"

        CACHE_ROOT = r'Z:\PRODUCTION\Anim_Cache\GAB'
        episode = basename_list[1]
        # seq = basename_list[2].replace('sc', 'SC_')
        shot = basename_list[2]

        CACHE_PATH = os.path.normpath(os.path.join(CACHE_ROOT, episode, shot))
        print('Cache path : ', CACHE_PATH)
        out_dir = CACHE_PATH

        if render_cam:
            cam_root = "-root |{}".format(render_cam)
            cam_output_dir = os.path.normpath(os.path.join(out_dir, 'camera_publish'))
            if not os.path.isdir(cam_output_dir):
                os.makedirs(cam_output_dir)

            cam_export_path = os.path.normpath(os.path.join(cam_output_dir, 'shot_camera.abc'))
            cam_export_exp = 'AbcExport -j "-frameRange %s %s %s -worldSpace -dataFormat ogawa -writeVisibility -file \\\"%s\\\""' % (
                start, end, cam_root, cam_export_path.replace("\\", "\\\\\\\\"))
            try:
                mel.eval(cam_export_exp)
                self.data['cam_path'] = cam_export_path
                print("Shot camera exported to  : {}".format(cam_export_path))
            except:
                err_string = "Error: Unable to export camera"
                self.data['cam_path'] = err_string
                print(err_string)
        new_folder_list = []

        for char in selected:
            name = char
            if ":" in char:
                name = char.split(':')[-1]
                name_sel_set = name
                for s in patterns:
                    if s in name:
                        name = name.replace(s, '')
                        name_orig = name
                        if not name in new_folder_list:
                            new_folder_list.append(name)
                        else:
                            name = '{}__{}'.format(name, str(1))
                            while name in new_folder_list:
                                name_pre = name.split('_')[-1]
                                new_pre = int(name_pre) + 1
                                name = '{}__{}'.format(name_orig, str(new_pre))
                            new_folder_list.append(name)

            dir = os.path.join(out_dir, name)
            full_cache_path = os.path.join(dir, (name + '.xml'))
            set_data.setdefault(name_sel_set, [])
            paths_list_sel_set = set_data[name_sel_set]

            if full_cache_path not in paths_list_sel_set:
                paths_list_sel_set.append(full_cache_path)
                set_data[name_sel_set] = paths_list_sel_set
            print('paths_list_sel_set', paths_list_sel_set)

            print(name, dir)
            cmds.select(char)

            if not os.path.isdir(dir):
                os.makedirs(dir)
            print('Caching is started to ----- >>>>> [ {} ]'.format(dir))
            # outputName = dir + '{k}.abc'.format(k=key)
            # expStr = 'AbcExport -j "-frameRange %s %s %s -worldSpace -uvWrite -writeVisibility -file \\\"%s\\\""' % (start, end, rootString, outputName.replace("\\","\\\\\\\\"))
            # mel.eval(expStr)
            dir = dir.replace('\\', '\\\\\\\\')
            args = [
                0,  # 0 -> Use provided start/end frame.
                start,
                end,
                "OneFilePerFrame",  # File distribution mode.
                0,  # Refresh during caching?
                dir,  # Directory for cache files.
                0,  # Create cache per geometry?
                name,  # Name of cache file.
                0,  # Is that name a prefix?
                "export",  # Action to perform.
                1,  # Force overwrites?
                1,  # Simulation rate.
                1,  # Sample multiplier.
                0,  # Inherit modifications from cache to be replaced?
                1,  # Save as floats.
                "mcx",
                1
            ]
            try:
                cmds.select(char)
                selected_geos = cmds.ls(sl=True)

                for geo in selected_geos:
                    if ':' in geo:
                        new_name = geo.split(':')[-1]
                        cmds.rename(geo, new_name)

                mel.eval('doCreateGeometryCache %s { %s }' % (
                    6,
                    ', '.join('"%s"' % x for x in args),
                ))

                print('-----------[ CACHING DONE ]-----------')
            except:
                print('Error has occured: Try manually to cache for {}'.format(char))
                pass

        self.data['set_data'] = set_data
        self.save_shot_data(self.data)
        pprint.pprint(self.data)
# if __name__ == "__main__":
#     e = export()
#     e.export_cache()


# print('Starting caching for file ------->>>> ', self.maya_file)
# refs_path = ["Z:/PROJECT/GAB/episodes/EP_018B/asset/", "Z:/PROJECT/GAB/asset/"]
# for target in refs_path:
#     for root, dirnames, filenames in os.walk(target):
#         for filename in fnmatch.filter(filenames, '*.ma'):
#             file_path = os.path.join(root, filename)
#             if "rig\publish" in file_path:
#                 self.maya_refs[filename] = file_path
# print self.maya_refs
# self.init_maya()

# try:
#     outData = {}
# cId = OpenM.MSceneMessage.addCheckFileCallback(OpenM.MSceneMessage.kBeforeCreateReferenceCheck, self._test_raise_exception, clientData=outData)
# cmds.file(self.maya_file, o=1, f=1, pmt=1, buildLoadSettings=True)
# loadSettings='implicitLoadSettings'

#     OpenM.MSceneMessage.removeCallback(cId)
#     if 'exception' in outData: #check if an exception was set, if so, raise it
#         raise outData['exception']

# except:
#     #handle the exception here
#     print 'load cancelled due to error'
#     pass
# ref_list = pm.listReferences()

# for r in ref_list:
#     print r.namespace, r.refNode, r.path
#     ref_path = r.path
#     print ref_path
#     if not os.path.isfile(ref_path):
#         basename = os.path.basename(ref_path)
#         print 'Reference found for: ', basename

#         if basename in self.maya_refs.keys():
#             ref_file = self.maya_refs[basename]

#             print ref_file
#             try:
#                 r.replaceWith(ref_file)
#             except:

# cmds.file(save=True, type="mayaAscii")
# unknownNodes = cmds.ls(type="unknown")
# for item in unknownNodes:
#     if cmds.objExists(item):
#         print item
#         cmds.delete(item)