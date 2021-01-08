
import os

from PySide2 import QtCore
from PySide2 import QtUiTools
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.cmds as cmds
import maya.OpenMayaUI as omui


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
        # self.create_connections()

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
        # self.ui.cancelButton.clicked.connect(self.close)
        pass
    
    def get_projects(self):
        pass
        
        
    
   
if __name__ == "__main__":

    try:
        designer_ui.close() # pylint: disable=E0601
        designer_ui.deleteLater()
    except:
        pass

    ui_path = r"E:/project/openfilemaya/open_file.ui"

    designer_ui = DesignerUI(ui_path)
    designer_ui.show()
