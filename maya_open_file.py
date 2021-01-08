
import os

from PySide2 import QtCore
from PySide2 import QtUiTools
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.cmds as cmds
import maya.OpenMayaUI as omui

PRJ_ROOT = "F:/Projects/PRJ"
def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class DesignerUI(QtWidgets.QDialog):

    def __init__(self, ui_path=None, parent=maya_main_window()):
        super(DesignerUI, self).__init__(parent)

        self.setWindowTitle("Open File")

        self.init_ui(ui_path)
       # self.create_layout()
        
        self.get_projects()
        self.get_episodes()
        self.create_connections()
        
    def init_ui(self, ui_path=None):
      
        print(ui_path)
        f = QtCore.QFile("E:/project/openfilemaya/open_file.ui")
        f.open(QtCore.QFile.ReadOnly)

        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(f)

        f.close()
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addWidget(self.ui)

    def create_layout(self):
        self.ui.layout().setContentsMargins(6, 6, 6, 6)

    def create_connections(self):
        self.ui.open_btn.hide()
        self.ui.cb_prj.currentIndexChanged.connect(self.refresh_episodes)
        self.ui.epi_list.itemClicked.connect(self.get_shots)
        self.ui.shot_list.itemClicked.connect(self.get_files)
        self.ui.file_list.itemClicked.connect(self.get_file_path)
        self.ui.open_btn.clicked.connect(self.open_maya_scene)
    
    def get_projects(self):
        projects = os.listdir(PRJ_ROOT)
        
        self.ui.cb_prj.addItems(projects)
        
    def get_episodes(self):
        current_prj = self.ui.cb_prj.currentText()
        episode_root = os.path.join(PRJ_ROOT, current_prj, "episodes")
        episodes = os.listdir(episode_root)
        self.ui.epi_list.clear()
        self.ui.shot_list.clear()
        self.ui.file_list.clear()
        self.ui.epi_list.addItems(episodes) 
        
    def refresh_episodes(self):
        self.get_episodes()
        
    def get_shots(self):
        self.ui.open_btn.hide()
        shot_root = os.path.join(PRJ_ROOT, self.ui.cb_prj.currentText(), "episodes", self.ui.epi_list.currentItem().text(), "shot")
        shots = os.listdir(shot_root)
        self.ui.shot_list.clear()
        self.ui.shot_list.addItems(shots)
        
    def get_files(self):
        self.ui.open_btn.hide()
        current_shot = self.ui.shot_list.currentItem().text()
        self.file_root = os.path.join(PRJ_ROOT, self.ui.cb_prj.currentText(), "episodes", self.ui.epi_list.currentItem().text(), "shot", current_shot, "lighting\light_char\maya\work")
        self.ui.file_list.clear()
        files = os.listdir(self.file_root)
        for ma_file in files:
            if ma_file.endswith(".ma"):
                self.ui.file_list.addItem(ma_file)
    
    def get_file_path(self):
        scene_filepath = os.path.join(self.file_root, self.ui.file_list.currentItem().text())
        self.ui.open_btn.show()
        return scene_filepath
        
    def open_maya_scene(self):
        scene_file = self.get_file_path()
        fileCheckState = cmds.file(q=True, modified=True)
        # cmds.file(new=True, force=True)
        if fileCheckState: 
            cmds.file(scene_file, o=True, pmt=True, force=True)
            self.close() 
        else:
            input = cmds.confirmDialog( title='Unsaved changes for current scene', message='Are you sure about open new file?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
            if input == "Yes":
               cmds.file(scene_file, o=True, pmt=True, force=True) 
               self.close() 
if __name__ == "__main__":

    try:
        designer_ui.close() # pylint: disable=E0601
        designer_ui.deleteLater()
    except:
        pass

    ui_path = r"E:/project/openfilemaya/open_file.ui"

    designer_ui = DesignerUI(ui_path)
    designer_ui.show()
