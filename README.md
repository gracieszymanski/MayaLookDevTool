# MayaLookDevTool
# Code that generates in Maya a look dev tool for lighting.

# User Guide:

# To work the app you need two files:
#  ● SP24_V313_P06_SzymaskiGracie_lighting_tool_v01.py
#  ● SP24_V313_P06_SzymaskiGracie_lighting_functions_v01.py
#  The user will run the SP24_V313_P06_SzymaskiGracie_lighting_tool_v01.py file in Maya.
#  ● Before running, the user needs to update two paths: The path of the ui file, and 
# the path of the folder where the 
# P24_V313_P06_SzymaskiGracie_lighting_functions_v01.py file is located so that 
# Maya can find and import it.

#  After running this file, a shelf is created with the tool. To run the tool’s GUI, click the light 
# icon. This then launches the GUI and the user just has to click the run buttons in order to 
# build the scene. This can happen on a new file or on an already existing Maya file. Like 
# the description says, the user must have Legacy Render Layers turned on in Maya 
# Preferences in order for the tool to work since it relies on render layers. The code is also 
# specifically designed for Maya 2024 as some Maya commands are unique to that version.
