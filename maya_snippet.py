# Copy selection set members and create new selection set

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm

cmds.select('test_sel_set')
a = cmds.ls(sl=True, long=True, tr=True)
print(a)
x = max(a, key=len)
items = cmds.ls(sl=True, long=True)
cmds.select(x.split('|')[2])

print(items)
new = pm.duplicate(pm.ls(sl=True))

pm.select(new, hi=True)
sel_items = pm.ls(sl=True, tr=True, assemblies=False, long=True)
print('sel_items', sel_items)


def is_group(node):
    children = node.getChildren()
    for child in children:
        if type(child) is not pm.nodetypes.Transform:
            return False
    return True


grp_sel = filter(is_group, sel_items)
print('grp', grp_sel)
req_sel = [x for x in sel_items if x not in grp_sel]
pm.select(req_sel)

set = pm.sets()
print(set)
pm.rename(set, 'new_set')
cmds.select('test_sel_set')
wrong_set = cmds.ls(sl=1, long=True)
print('w_set', wrong_set)
print('items', items)
for mesh_t in wrong_set:
    if mesh_t not in items:
        cmds.sets(mesh_t, rm='test_sel_set')

        ##### Set Ranges for maya

        import pymel.core as pm

        # set frame ranges for plackback
    pm.playbackOptions(minTime=in_frame,
                       maxTime=out_frame,
                       animationStartTime=in_frame,
                       animationEndTime=out_frame)

    # set frame ranges for rendering
    defaultRenderGlobals = pm.PyNode('defaultRenderGlobals')
    defaultRenderGlobals.startFrame.set(in_frame)
    defaultRenderGlobals.endFrame.set(out_frame)
    
    # Shader selection from current selection 
    sel = cmds.ls(sl=True)
    cmds.hyperShade( shaderNetworksSelectMaterialNodes=True )
    print "%s -> %s" % (sel[0], cmds.ls(sl=True)[0])    
    
    # Shader export from selection
import maya.cmds as cmds
import maya.mel as mel
import random
import os
import pymel.core as pm
sceneName = cmds.file ( q=True, sn=True, shn=True)
scenePath = cmds.file ( q=True, sn=True).split(sceneName)
path = scenePath[0] + sceneName[0] + "_abcExport/"
if not os.path.exists(path):
    os.makedirs(path)   
selectedObj = pm.ls(sl=1,dag=1,s=1)
shadingGrp = pm.listConnections(selectedObj[0],type='shadingEngine')
print(selectedObj,list(set(shadingGrp)))
for shdGrp in list(set(shadingGrp)):
    print(shdGrp.name())
    shader = (pm.listConnections(shdGrp.name() + '.surfaceShader'))
    pm.select(shader)
    cmds.file(path + 'mat.ma', es=True, type='mayaAscii')
    

# Assign shader to selection

import pymel.core as PM
sel = PM.ls(sl=1)
print(sel)

shr = PM.PyNode('mat_mat_01')
SG = PM.sets (renderable = True, noSurfaceShader = True, empty = True, name = shr.name() + 'SG')
PM.sets('mat_mat_01', sel[0].name())
shr.outColor >> SG.surfaceShader
    
