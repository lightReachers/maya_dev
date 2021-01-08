
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
        self.ui.cb_prj.currentIndexChanged.connect(self.refresh_episodes)
        
    
    def get_projects(self):
        projects = os.listdir(PRJ_ROOT)
        
        self.ui.cb_prj.addItems(projects)
        
    def get_episodes(self):
        current_prj = self.ui.cb_prj.currentText()
        episode_root = os.path.join(PRJ_ROOT, current_prj, "episodes")
        episodes = os.listdir(episode_root)
        self.ui.epi_list.addItems(episodes) 
        
    def refresh_episodes(self):
        self.get_episodes()
    
   
if __name__ == "__main__":

    try:
        designer_ui.close() # pylint: disable=E0601
        designer_ui.deleteLater()
    except:
        pass

    ui_path = r"E:/project/openfilemaya/open_file.ui"

    designer_ui = DesignerUI(ui_path)
    designer_ui.show()
