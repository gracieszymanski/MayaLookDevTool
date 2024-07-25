# SP24_V313_P06_SzymaskiGracie_lighting_tool_v01
# A tool to create a maya scene with render layers to test lighting on an object
# By Gracie Szymanski
# Created 5/14/24

#imports
import sys
import maya.cmds as cmds
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance
from PySide2.QtWidgets import QMainWindow, QFileDialog
from PySide2.QtUiTools import QUiLoader

#allows maya to access the folder where the files imported are located
#without this maya cannot import other files
MAYA_PATH = r"C:\Users\aspen\OneDrive\Documents\P06_PersonalProject"
sys.path.insert(0, MAYA_PATH)
import SP24_V313_P06_SzymaskiGracie_lighting_functions_v01 as lf

#UI Path
PATH = r"C:\Users\aspen\OneDrive\Documents\P06_PersonalProject\SP24_V313_P06_SzymaskiGracie_lighting_GUI_v01.ui"
loader = QUiLoader()

class MainWindow(QMainWindow):

    def __init__(self, parent = None):

        super(MainWindow, self).__init__(parent)
        gui = loader.load(PATH, parent) #loads in ui file with main window design

        #Calls the functions that check if arnold and redshift is properly installed and loaded on device
        self.render_tabs = gui.render_tabs
        self.redshift = True
        self.check_redshift()
        self.arnold = True
        self.check_arnold()

        """TAB ONE MAYA TAB"""
        ###KEY LIGHT####
        self.maya_key_cone_label = gui.maya_key_cone_label
        self.maya_key_cone_spinBox = gui.maya_key_cone_spinBox

        self.maya_key_type = 0
        gui.maya_key_type_comboBox.currentIndexChanged.connect(self.update_maya_key_type)

        self.maya_key_cone = 90
        gui.maya_key_cone_spinBox.valueChanged.connect(self.update_maya_key_dist)

        self.maya_key_int = 1
        gui.maya_key_intense_spinBox.valueChanged.connect(self.update_maya_key_int)

        self.maya_key_R = 1 
        self.maya_key_G = 1 
        self.maya_key_B = 1
        gui.maya_key_R_spinBox.valueChanged.connect(self.update_maya_key_R)
        gui.maya_key_G_spinBox.valueChanged.connect(self.update_maya_key_G)
        gui.maya_key_B_spinBox.valueChanged.connect(self.update_maya_key_B)

        ###FILL LIGHT###
        #default variables and signals to update them for attributes
        self.maya_fill_cone_label = gui.maya_fill_cone_label
        self.maya_fill_cone_spinBox = gui.maya_fill_cone_spinBox

        self.maya_fill_type = 0 
        gui.maya_fill_type_comboBox.currentIndexChanged.connect(self.update_maya_fill_type)

        self.maya_fill_cone = 90
        gui.maya_fill_cone_spinBox.valueChanged.connect(self.update_maya_fill_cone)

        self.maya_fill_int = .8
        gui.maya_fill_intense_spinBox.valueChanged.connect(self.update_maya_fill_int)

        self.maya_fill_R = 1
        self.maya_fill_G = 1
        self.maya_fill_B = 1
        gui.maya_fill_R_spinBox.valueChanged.connect(self.update_maya_fill_R)
        gui.maya_fill_G_spinBox.valueChanged.connect(self.update_maya_fill_G)
        gui.maya_fill_B_spinBox.valueChanged.connect(self.update_maya_fill_B)

        ###BOUNCE LIGHT####
        #default variables and signals to update them for attributes
        self.maya_bounce_cone_spinBox = gui.maya_bounce_cone_spinBox
        self.maya_bounce_cone_label = gui.maya_bounce_cone_label

        self.maya_bounce_type = 0
        gui.maya_bounce_type_comboBox.currentIndexChanged.connect(self.update_maya_bounce_type)

        self.maya_bounce_cone = 90 
        gui.maya_bounce_cone_spinBox.valueChanged.connect(self.update_maya_bounce_cone)

        self.maya_bounce_int = .7 
        gui.maya_bounce_intense_spinBox.valueChanged.connect(self.update_maya_bounce_int)

        self.maya_bounce_R = 1
        self.maya_bounce_G = 1
        self.maya_bounce_B = 1
        gui.maya_bounce_R_spinBox.valueChanged.connect(self.update_maya_bounce_R)
        gui.maya_bounce_G_spinBox.valueChanged.connect(self.update_maya_bounce_G)
        gui.maya_bounce_B_spinBox.valueChanged.connect(self.update_maya_bounce_B)

        """TAB TWO ARNOLD TAB"""
        ###KEY LIGHT###
        #default variables and signals to update them for attributes
        self.arn_cone_spinBox = gui.arn_cone_spinBox
        self.arn_cone_label = gui.arn_cone_label

        self.arn_type = 0
        gui.arn_type_comboBox.currentIndexChanged.connect(self.update_arn_type)

        self.arn_cone = 90
        gui.arn_cone_spinBox.valueChanged.connect(self.update_arn_cone)

        self.arn_int = 1000
        gui.arn_intense_spinBox.valueChanged.connect(self.update_arn_int)

        self.arn_R = 1
        self.arn_G = 1 
        self.arn_B = 1
        gui.arn_R_spinBox.valueChanged.connect(self.update_arn_R)
        gui.arn_G_spinBox.valueChanged.connect(self.update_arn_G)
        gui.arn_B_spinBox.valueChanged.connect(self.update_arn_B)

        """TAB THREE HDRI"""
        ###HDRI DOME###
        #variables and signal for folder opener
        self.hdri_path = 0
        self.hdri_folder_label = gui.hdri_folder_label
        gui.hdri_browse_button.clicked.connect(self.update_path)

        """TAB FOUR REDSHIFT"""
        ###KEY LIGHT###
        #default variables and signals to update them for attributes
        self.red_cone_spinBox = gui.red_cone_spinBox
        self.red_cone_label = gui.red_cone_label

        self.red_type = 0
        gui.red_type_comboBox.currentIndexChanged.connect(self.update_red_type)

        self.red_cone = 90
        gui.red_cone_spinBox.valueChanged.connect(self.update_red_cone)

        self.red_int = 1
        gui.red_intense_spinBox.valueChanged.connect(self.update_red_int)

        self.red_R = 1
        self.red_G = 1 
        self.red_B = 1
        gui.red_R_spinBox.valueChanged.connect(self.update_red_R)
        gui.red_G_spinBox.valueChanged.connect(self.update_red_G)
        gui.red_B_spinBox.valueChanged.connect(self.update_red_B)

        """REST OF APP"""
        #stage size signal and variable
        self.stage_size = 8
        gui.stage_size_spinBox.valueChanged.connect(self.update_stage_size)

        #cornell box signal and variable
        self.cornell_value = 0
        gui.cornell_check.stateChanged.connect(self.update_cornell)

        #look dev spheres signal and variable
        self.spheres_value = 0
        gui.spheres_check.stateChanged.connect(self.update_spheres)

        #maya shaders signal and variable
        self.maya_shd_value = 0
        gui.maya_shd_check.stateChanged.connect(self.update_maya_shd)

        #arnold shaders signal and variable
        self.arn_shd_value = 0
        gui.arn_shd_check.stateChanged.connect(self.update_arn_shd)

        #redshift shaders signal and variable
        self.red_shd_value = 0
        gui.red_shd_check.stateChanged.connect(self.update_red_shd)

        ###BUTTONS###
        gui.run_button.clicked.connect(self.create_scene)
        gui.delete_button.clicked.connect(self.delete_scene)

        self.setCentralWidget(gui)

    """SOFTWARE CHECKS"""

    def check_redshift(self): #checks to see if redshift is installed on to computer

        red_check = cmds.pluginInfo('redshift4maya', query=True, loaded=True)

        if red_check == False: #tries to load redshift
            try:
                cmds.loadPlugin('redshift4maya')

            except Exception as e:
                print("Error loading Redshift: ", e)
                self.render_tabs.setTabEnabled(3, False)
                self.redshift = False #if redshift not loaded properly, the tab is disabled on the GUI

    def check_arnold(self): #checks to see if arnold is installed on to computer

        arnold_check = cmds.pluginInfo('mtoa', query=True, loaded=True)

        if arnold_check == False: #tries to load arnold 
            try:
                cmds.loadPlugin('mtoa')

            except Exception as e:
                print("Error loading Arnold: ", e)
                self.render_tabs.setTabEnabled(1, False)
                self.render_tabs.setTabEnabled(2, False)
                self.arnold = False #if arnold not loaded properly, the arnold and hdri tab is disabled on the GUI

    """TAB ONE MAYA"""
    ###KEY LIGHT###
    #functions to update the key light attributes based on user input

    def update_maya_key_type(self, index):
        
        self.maya_key_type = index

        #sets the cone size attribute to invisible if the user only wants an area light
        if self.maya_key_type == 0 or self.maya_key_type == 2:
            self.maya_key_cone_label.setVisible(True)
            self.maya_key_cone_spinBox.setVisible(True)

        if self.maya_key_type == 1:
            self.maya_key_cone_label.setVisible(False)
            self.maya_key_cone_spinBox.setVisible(False)   

    def update_maya_key_dist(self, value):  

        self.maya_key_cone = value  

    def update_maya_key_int(self, value):

        self.maya_key_int = value

    def update_maya_key_R(self, value):

        self.maya_key_R = value

    def update_maya_key_G(self, value):

        self.maya_key_G = value

    def update_maya_key_B(self, value):

        self.maya_key_B = value

    ###FILL LIGHT###
    #functions to update the fill light attributes based on user input

    def update_maya_fill_type(self, index): 
        
        self.maya_fill_type = index
        
        #sets the cone size attribute to invisible if the user only wants an area light
        if self.maya_fill_type == 0 or self.maya_fill_type == 2:
            self.maya_fill_cone_label.setVisible(True)
            self.maya_fill_cone_spinBox.setVisible(True)

        if self.maya_fill_type == 1:
            self.maya_fill_cone_label.setVisible(False)
            self.maya_fill_cone_spinBox.setVisible(False)   

    def update_maya_fill_cone(self, value):

        self.maya_fill_cone = value

    def update_maya_fill_int(self, value):

        self.maya_fill_int = value

    def update_maya_fill_R(self, value):

        self.maya_fill_R = value

    def update_maya_fill_G(self, value):

        self.maya_fill_G = value

    def update_maya_fill_B(self, value):

        self.maya_fill_B = value
        
    ###BOUNCE LIGHT###
    #functions to update the bounce light attributes based on user input

    def update_maya_bounce_type(self, index):

        self.maya_bounce_type = index

        #sets the cone size attribute to invisible if the user only wants an area light
        if self.maya_bounce_type == 0 or self.maya_bounce_type == 2:
            self.maya_bounce_cone_label.setVisible(True)
            self.maya_bounce_cone_spinBox.setVisible(True)

        if self.maya_bounce_type == 1:
            self.maya_bounce_cone_label.setVisible(False)
            self.maya_bounce_cone_spinBox.setVisible(False)   

    def update_maya_bounce_cone(self, value):

        self.maya_bounce_cone = value
    
    def update_maya_bounce_int(self, value):

        self.maya_bounce_int = value

    def update_maya_bounce_R(self, value):

        self.maya_bounce_R = value

    def update_maya_bounce_G(self, value):

        self.maya_bounce_G = value

    def update_maya_bounce_B(self, value):

        self.maya_bounce_B = value

    """TAB TWO ARNOLD"""
    ###KEY LIGHT###
    #functions to update the key light attributes based on user input
    
    def update_arn_type(self, index):

        self.arn_type = index

        #sets the cone size attribute to invisible if the user only wants an area light
        if self.arn_type == 0 or self.arn_type == 2:
            self.arn_cone_spinBox.setVisible(True)
            self.arn_cone_label.setVisible(True)

        if self.arn_type == 1:
            self.arn_cone_spinBox.setVisible(False)
            self.arn_cone_label.setVisible(False)   

    def update_arn_cone(self, value):

        self.arn_cone = value

    def update_arn_int(self, value):

        self.arn_int = value

    def update_arn_R(self, value):

        self.arn_R = value
    
    def update_arn_G(self, value):

        self.arn_G = value
    
    def update_arn_B(self, value):

        self.arn_B = value

    """TAB THREE HDRI"""
    #opens up a pop up for the user to pick the hdri file
    def update_path(self):

        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFile)

        if file_dialog.exec():
            path = file_dialog.selectedFiles()
            if path:
                self.hdri_folder_label.setText(path[0]) #sets the label to show the user which file they chose
                self.hdri_path = path[0]
 
    """TAB FOUR REDSHIFT"""
    ##KEY LIGHT###
    #functions to update the key light attributes based on user input

    def update_red_type(self, index):

        self.red_type = index

        #sets the cone size attribute to invisible if the user only wants an area light
        if self.red_type == 0 or self.red_type == 2:
            self.red_cone_spinBox.setVisible(True)
            self.red_cone_label.setVisible(True)

        if self.red_type == 1:
            self.red_cone_spinBox.setVisible(False)
            self.red_cone_label.setVisible(False)   

    def update_red_cone(self, value):

        self.red_cone = value

    def update_red_int(self, value):

        self.red_int = value

    def update_red_R(self, value):

        self.red_R = value
    
    def update_red_G(self, value):

        self.red_G = value
    
    def update_red_B(self, value):

        self.red_B = value

    '''REST OF APP'''
    #functions to define if a box is checked or not
    #value = 2 if checked and 0 if unchecked

    def update_stage_size(self, value):

        self.stage_size = value

    def update_cornell(self, state):

        self.cornell_value = state

    def update_spheres(self, state):

        self.spheres_value = state

    def update_maya_shd(self, state):

        self.maya_shd_value = state

    def update_arn_shd(self, state):

        self.arn_shd_value = state

    def update_red_shd(self, state):

        self.red_shd_value = state


    """BUTTONS"""
    #the main function that runs the whole program
    #calls upon the functions file to fulfill commands

    def create_scene(self):

        lf.delete() #deletes any past runs of the app before creating more
        
        #maya layer
        lf.make_maya_layer()
        lf.make_stage()
        lf.make_camera()
        lf.make_maya_key(self.maya_key_type, self.maya_key_cone, self.maya_key_int, self.maya_key_R, self.maya_key_G, self.maya_key_B)
        lf.make_maya_fill(self.maya_fill_type, self.maya_fill_cone, self.maya_fill_int, self.maya_fill_R, self.maya_fill_G, self.maya_fill_B)
        lf.make_maya_bounce(self.maya_bounce_type, self.maya_bounce_cone, self.maya_bounce_int, self.maya_bounce_R, self.maya_bounce_G, self.maya_bounce_B)

        if self.spheres_value == 2:
            lf.make_spheres()
            lf.add_spheres_maya()

        if self.cornell_value == 2:
            lf.make_cornell_box()
            lf.add_cornell_maya()
        
        if self.maya_shd_value == 2:
            lf.make_maya_shaders()

        #arnold layer
        #only runs if arnold was found to be loaded
        if self.arnold == True:
            lf.make_arn_layer()
            lf.make_arn_key(self.arn_type, self.arn_cone, self.arn_int, self.arn_R, self.arn_G, self.arn_B)

            if self.spheres_value == 2:
                lf.add_spheres_arn()

            if self.cornell_value == 2:
                lf.add_cornell_arn()
            
            if self.arn_shd_value == 2:
                lf.make_arn_shaders()
            
            #hdri layer within the arnold if statement since it required arnold to run
            lf.make_hdri_layer()
            lf.make_hdri_dome(self.hdri_path)

            if self.spheres_value == 2:
                lf.add_spheres_hdri()
        
            if self.cornell_value == 2:
                lf.add_cornell_hdri()
        
        #redshift layer
        #only runs if redshift was found to be loaded
        if self.redshift == True:
            lf.make_red_layer()
            lf.make_red_key(self.red_type, self.red_cone, self.red_int, self.red_R, self.red_G, self.red_B)

            if self.spheres_value == 2:
                lf.add_spheres_red()

            if self.cornell_value == 2:
                lf.add_cornell_red()

            if self.red_shd_value == 2:
                lf.make_red_shaders()

        #resizes the whole scene based on user input
        lf.resize(self.stage_size)

    #delete button function
    def delete_scene(self):

        lf.delete()
                       
def main(): #open and run the GUI

    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QMainWindow)
    mw = MainWindow(parent = mayaMainWindow)
    mw.show()

def create_shelf(): #create a maya shelf for the application to easily be used
    
    if cmds.shelfLayout("Lighting_Setup_Tool", exists=True):
        cmds.deleteUI("Lighting_Setup_Tool")
    
    cmds.shelfLayout("Lighting_Setup_Tool", parent="ShelfLayout")

    cmds.shelfButton(label= "button",
    command= main,
    image= "spotlight.png",
    parent="Lighting_Setup_Tool")
        
create_shelf() 
