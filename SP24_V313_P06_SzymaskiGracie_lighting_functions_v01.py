# SP24_V313_P06_SzymaskiGracie_lighting_functions_v01
# A tool to create a maya scene with render layers to test lighting on an object
# functions file
# By Gracie Szymanski
# Created 5/14/24

#impots
import maya.cmds as cmds
import mtoa.utils as mutils 

#Prefix infront of all maya objects so they can easily be deleted
PFX = "GS_"

#a function that deletes any objects in a scene with the prefix in front of it
#used to start fresh or when the user is done
def delete():

    cmds.editRenderLayerGlobals(crl ="defaultRenderLayer")

    if cmds.objExists(PFX+"*"):
        cmds.delete(PFX+"*")

"""LOOKDEV SPHERES AND SPHERE SHADERS"""
#creates the lookdev spheres
def make_spheres():

    cmds.polySphere(n = PFX + "Chrome_Sphere")
    cmds.move(3,6,0)
    cmds.polySphere(n = PFX + "White_Sphere")
    cmds.move(3,8.5,0)

def add_spheres_maya():

    #creates the maya sphere shaders
    white = cmds.shadingNode("blinn", n = PFX + "Sphere_Blinn_White", asShader=True)
    cmds.setAttr (white + ".color", 1,1,1)
    cmds.setAttr (white + ".diffuse", 1)
    cmds.setAttr (white + ".specularColor", .1,.1,.1)
    cmds.setAttr (white + ".eccentricity", .9)
    cmds.setAttr (white + ".specularRollOff", .1)
    cmds.setAttr (white + ".reflectivity", 0)
    chrome = cmds.shadingNode("blinn", n = PFX + "Sphere_Blinn_Chrome", asShader=True)
    cmds.setAttr (chrome + ".color", 0, 0, 0)
    cmds.setAttr (chrome + ".diffuse", 0)
    cmds.setAttr (chrome + ".specularColor", 1,1,1)
    cmds.setAttr (chrome + ".eccentricity", 0)
    cmds.setAttr (chrome + ".specularRollOff", 1)
    cmds.setAttr (chrome + ".reflectivity", 1)

    #creates the shading groups
    shading_grp_white = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name="Sphere_Blinn_WhiteSG")
    cmds.connectAttr(white + ".outColor", shading_grp_white + ".surfaceShader", force=True)
    shading_grp_chrome = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name="Sphere_Blinn_ChromeSG")
    cmds.connectAttr(chrome + ".outColor", shading_grp_chrome + ".surfaceShader", force=True)

    #assigns shader to spheres on that layer
    cmds.select(PFX + "Chrome_Sphere")
    cmds.hyperShade(assign= chrome)
    cmds.select(PFX + "White_Sphere")
    cmds.hyperShade(assign = white)

def add_spheres_arn():

    #adds spheres to arnold layer
    cmds.editRenderLayerMembers(PFX + "Arnold_Layer", PFX + "Chrome_Sphere", PFX + "White_Sphere")
    
    #creates the arnold sphere shaders
    white = cmds.shadingNode("aiStandardSurface", n = PFX + "Sphere_AI_White", asShader=True)
    cmds.setAttr (white + ".baseColor", 1,1,1)
    cmds.setAttr (white + ".specularRoughness", .4)
    cmds.setAttr (white + ".specularIOR", 1.05)
    chrome = cmds.shadingNode("aiStandardSurface", n = PFX + "Sphere_AI_Chrome", asShader=True)
    cmds.setAttr (chrome + ".base", 0)
    cmds.setAttr (chrome + ".specularRoughness", 0.05)
    cmds.setAttr (chrome + ".specularIOR", 5)

    #creates the shading groups
    shading_grp_white = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name="Sphere_AI_WhiteSG")
    cmds.connectAttr(white + ".outColor", shading_grp_white + ".surfaceShader", force=True)
    shading_grp_chrome = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name="Sphere_AI_ChromeSG")
    cmds.connectAttr(chrome + ".outColor", shading_grp_chrome + ".surfaceShader", force=True)
    
    #assigns shader to spheres on that layer
    cmds.select(PFX + "Chrome_Sphere")
    cmds.hyperShade(assign= chrome)
    cmds.select(PFX + "White_Sphere")
    cmds.hyperShade(assign = white)

def add_spheres_hdri():

    #add spheres to hdri layer
    cmds.editRenderLayerMembers(PFX + "HDRI_Layer", PFX + "Chrome_Sphere", PFX + "White_Sphere")
 
    #assign spheres arnold shaders already creates
    cmds.select(PFX + "Chrome_Sphere")
    cmds.hyperShade(assign= PFX + "Sphere_AI_Chrome")
    cmds.select(PFX + "White_Sphere")
    cmds.hyperShade(assign = PFX + "Sphere_AI_White")

def add_spheres_red():

    #adds spheres to redshift layer
    cmds.editRenderLayerMembers(PFX + "Redshift_Layer", PFX + "Chrome_Sphere", PFX + "White_Sphere")

    #creates the redshift spheres shaders
    white = cmds.shadingNode("RedshiftMaterial", n = PFX + "Sphere_RS_White", asShader=True)
    cmds.setAttr (white + ".diffuse_color", 1,1,1)
    cmds.setAttr (white + ".refl_color", .1, .1, .1)
    cmds.setAttr (white + ".refl_roughness", .4)
    chrome = cmds.shadingNode("RedshiftMaterial", n =  PFX + "Sphere_RS_Chrome", asShader=True)
    cmds.setAttr (chrome + ".diffuse_color", 0, 0, 0)
    cmds.setAttr (chrome + ".refl_ior", 50)

    #creates shading group
    shading_grp_white = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name="Sphere_RS_WhiteSG")
    cmds.connectAttr(white + ".outColor", shading_grp_white + ".surfaceShader", force=True)
    shading_grp_chrome = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name="Sphere_RS_ChromeSG")
    cmds.connectAttr(chrome + ".outColor", shading_grp_chrome + ".surfaceShader", force=True)

    #assigns shader to spheres on that layer
    cmds.select(PFX + "Chrome_Sphere")
    cmds.hyperShade(assign= chrome)
    cmds.select(PFX + "White_Sphere")
    cmds.hyperShade(assign = white)

"""LOOK DEV CORNELL BOX AND SHADERS"""
#create the cornell box and cube
def make_cornell_box():
    
    cmds.polyCube(h = 25, w = 25, d = 88, n = PFX + "Cornell_Box")
    cmds.setAttr(PFX + "Cornell_Box" + ".castsShadows", 0)

    cmds.polyCube(n = PFX + "Cornell_Cube")
    cmds.scale(2,2,2)
    cmds.move(3, 3, 0)


def add_cornell_maya():

    #add cornell box to maya layer
    cmds.editRenderLayerMembers(PFX + "Maya_Software_Layer", PFX + "Cornell_Box", PFX + "Cornell_Cube")

    #create blinn shaders for box and cube
    blue = cmds.shadingNode("blinn", n = PFX + "CB_Blue", asShader=True)
    cmds.setAttr(blue + ".color", 0, 0, 1)
    cmds.setAttr(blue + ".specularColor", 0, 0, 0)
    cmds.setAttr(blue + ".reflectivity", 0)
    red = cmds.shadingNode("blinn", n = PFX + "CB_Red", asShader=True)
    cmds.setAttr(red + ".reflectivity", 0)
    cmds.setAttr(red + ".specularColor", 0, 0, 0)
    cmds.setAttr(red + ".color", 1, 0, 0)
    yellow = cmds.shadingNode("blinn", n = PFX + "CB_Yellow", asShader=True)
    cmds.setAttr(yellow + ".reflectivity", 0)
    cmds.setAttr(yellow + ".specularColor", 0, 0, 0)
    cmds.setAttr(yellow + ".color", 1, 1, 0)
    white = cmds.shadingNode("blinn", n = PFX + "CB_White", asShader=True)
    cmds.setAttr(white + ".reflectivity", 0)
    cmds.setAttr(white + ".specularColor", 0, 0, 0)
    cmds.setAttr(white + ".color", 1, 1, 1)
    
    #create shading groups
    shading_grp_blue = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name="CB_BlueSG")
    cmds.connectAttr(blue + ".outColor", shading_grp_blue + ".surfaceShader", force=True)
    shading_grp_red = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name="CB_RedSG")
    cmds.connectAttr(red + ".outColor", shading_grp_red + ".surfaceShader", force=True)
    shading_grp_yellow = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name="CB_YellowSG")
    cmds.connectAttr(yellow + ".outColor", shading_grp_yellow + ".surfaceShader", force=True)
    shading_grp_white = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name="CB_WhiteSG")
    cmds.connectAttr(white + ".outColor", shading_grp_white + ".surfaceShader", force=True)

    #assign correct sides the correct shaders
    cmds.select(PFX + "Cornell_Box.f[0:3]")
    cmds.hyperShade(assign = white)
    cmds.select(PFX+ "Cornell_Box.f[5]")
    cmds.hyperShade(assign = red)
    cmds.select(PFX + "Cornell_Box.f[4]")
    cmds.hyperShade(assign = blue)
    cmds.select(PFX + "Cornell_Cube")
    cmds.hyperShade(assign = yellow)

def add_cornell_arn():

    #add cornell box to arnold layer
    cmds.editRenderLayerMembers(PFX + "Arnold_Layer", PFX + "Cornell_Box", PFX + "Cornell_Cube")

    #assign correct sides the correct blinn shaders
    cmds.select(PFX + "Cornell_Box.f[0:3]")
    cmds.hyperShade(assign = PFX + "CB_White")
    cmds.select(PFX+ "Cornell_Box.f[5]")
    cmds.hyperShade(assign = PFX + "CB_Red")
    cmds.select(PFX + "Cornell_Box.f[4]")
    cmds.hyperShade(assign = PFX + "CB_Blue")
    cmds.select(PFX + "Cornell_Cube")
    cmds.hyperShade(assign = PFX + "CB_Yellow")

def add_cornell_hdri():

    #add cornell box to arnold layer
    cmds.editRenderLayerMembers(PFX + "HDRI_Layer", PFX + "Cornell_Box", PFX + "Cornell_Cube")

    #assign correct sides the correct blinn shaders
    cmds.select(PFX + "Cornell_Box.f[0:3]")
    cmds.hyperShade(assign = PFX + "CB_White")
    cmds.select(PFX+ "Cornell_Box.f[5]")
    cmds.hyperShade(assign = PFX + "CB_Red")
    cmds.select(PFX + "Cornell_Box.f[4]")
    cmds.hyperShade(assign = PFX + "CB_Blue")
    cmds.select(PFX + "Cornell_Cube")
    cmds.hyperShade(assign = PFX + "CB_Yellow")


def add_cornell_red():

    #add cornell box to arnold layer
    cmds.editRenderLayerMembers(PFX + "Redshift_Layer", PFX + "Cornell_Box", PFX + "Cornell_Cube")

    #create redshift shaders for the box
    blue = cmds.shadingNode("RedshiftMaterial", n = PFX + "CB_RS_Blue", asShader=True)
    cmds.setAttr (blue + ".diffuse_color", 0,0,1)
    cmds.setAttr (blue + ".refl_color", .1, .1, .1)
    cmds.setAttr (blue + ".refl_roughness", .4)
    red = cmds.shadingNode("RedshiftMaterial", n = PFX + "CB_RS_Red", asShader=True)
    cmds.setAttr (red + ".diffuse_color", 1,0,0)
    cmds.setAttr (red + ".refl_color", .1, .1, .1)
    cmds.setAttr (red + ".refl_roughness", .4)
    yellow = cmds.shadingNode("RedshiftMaterial", n = PFX + "CB_RS_Yellow", asShader=True)
    cmds.setAttr (yellow + ".diffuse_color", 1,1,0)
    cmds.setAttr (yellow + ".refl_color", .1, .1, .1)
    cmds.setAttr (yellow + ".refl_roughness", .4)
    white = cmds.shadingNode("RedshiftMaterial", n = PFX + "CB_RS_White", asShader=True)
    cmds.setAttr (white + ".diffuse_color", 1,1,1)
    cmds.setAttr (white + ".refl_color", .1, .1, .1)
    cmds.setAttr (white + ".refl_roughness", .4)

    #create shading groups
    shading_grp_blue = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name="CB_RS_BlueSG")
    cmds.connectAttr(blue + ".outColor", shading_grp_blue + ".surfaceShader", force=True)
    shading_grp_red = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name="CB_RS_RedSG")
    cmds.connectAttr(red + ".outColor", shading_grp_red + ".surfaceShader", force=True)
    shading_grp_yellow = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name="CB_RS_YellowSG")
    cmds.connectAttr(yellow + ".outColor", shading_grp_yellow + ".surfaceShader", force=True)
    shading_grp_white = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name="CB_RS_WhiteSG")
    cmds.connectAttr(white + ".outColor", shading_grp_white + ".surfaceShader", force=True)

    #assign correct sides the correct redshift shaders
    cmds.select(PFX + "Cornell_Box.f[0:3]")
    cmds.hyperShade(assign = white)
    cmds.select(PFX+ "Cornell_Box.f[5]")
    cmds.hyperShade(assign = red)
    cmds.select(PFX + "Cornell_Box.f[4]")
    cmds.hyperShade(assign = blue)
    cmds.select(PFX + "Cornell_Cube")
    cmds.hyperShade(assign = yellow)

"""BASIC SHADERS FOR LOOK DEV"""
#create 5 basic arnold shaders for testing
def make_arn_shaders():

    #ai standard surface 
    cmds.shadingNode("aiStandardSurface", n = PFX + "Ai_Standard_Surface", asShader = True)

    #ceramic ai standard surface
    ceramic_shader = cmds.shadingNode("aiStandardSurface", n = PFX + "Ai_Basic_Ceramic", asShader = True)
    cmds.setAttr(ceramic_shader + ".specularRoughness", 0)
    cmds.setAttr(ceramic_shader + ".specularAnisotropy", 0.5)
    cmds.setAttr(ceramic_shader + ".subsurface", 0.1)
    cmds.setAttr(ceramic_shader + ".coatIOR", 1)
    cmds.setAttr(ceramic_shader + ".baseColor", 0.855, 0.817, 0.836)

    #ai car paint
    cmds.shadingNode("aiCarPaint", n = PFX + "Ai_Basic_Car_Paint", asShader = True)

    #glass ai standard surface
    glass_shader = cmds.shadingNode("aiStandardSurface", n = PFX + "Ai_Basic_Glass", asShader = True)
    cmds.setAttr(glass_shader + ".base", 0)
    cmds.setAttr(glass_shader + ".specularRoughness", 0)
    cmds.setAttr(glass_shader + ".specularAnisotropy", 0.5)
    cmds.setAttr(glass_shader + ".specularAnisotropy", 0.5)
    cmds.setAttr(glass_shader + ".transmission", 1)
    cmds.setAttr(glass_shader + ".coatRoughness", 0.1)
    cmds.setAttr(glass_shader + ".coatAffectRoughness", 1)

    #plastic ai standard surface
    plastic_shader = cmds.shadingNode("aiStandardSurface", n = PFX + "Ai_Basic_Plastic", asShader = True)
    cmds.setAttr(plastic_shader + ".baseColor", 0.105, .242, .818)
    cmds.setAttr(plastic_shader + ".specularRoughness", 0.325)
    cmds.setAttr(plastic_shader + ".subsurface", 0.2)
    cmds.setAttr(plastic_shader + ".subsurfaceColor", 0.105, .242, .818)
    cmds.setAttr(plastic_shader + ".coatRoughness", 0)
    cmds.setAttr(plastic_shader + ".coatIOR", 1)
    cmds.setAttr(plastic_shader + ".coatAffectRoughness", 1)
    cmds.setAttr(plastic_shader + ".coatAffectColor", 1)

#create 5 basic maya shaders for testing
def make_maya_shaders():

    #lambert
    cmds.shadingNode("lambert", n = PFX + "Basic_Lambert", asShader = True)

    #phong
    cmds.shadingNode("phong", n = PFX + "Basic_Phong", asShader = True)

    #blinn shaders in different colors
    blinn1 = cmds.shadingNode("blinn", n = PFX + "Basic_Blinn_One", asShader = True)
    cmds.setAttr(blinn1 + ".color", 0, 0, 1)
    blinn2 = cmds.shadingNode("blinn", n = PFX + "Basic_Blinn_Two", asShader = True)
    cmds.setAttr(blinn2 + ".color", 1, 0, 0)
    blinn3 = cmds.shadingNode("blinn", n = PFX + "Basic_Blinn_Three", asShader = True)
    cmds.setAttr(blinn3 + ".color", 0, 1, 0)


#create 5 basic redshift shaders for testing
def make_red_shaders():

    #rs standard material in different colors
    rs1 = cmds.shadingNode("RedshiftStandardMaterial", n = PFX + "RS_Basic_One", asShader = True)
    cmds.setAttr(rs1 + ".base_color", 0, 0, 1)
    rs2 = cmds.shadingNode("RedshiftStandardMaterial", n = PFX + "RS_Basic_Two", asShader = True)
    cmds.setAttr(rs2 + ".base_color", 1, 0, 1)
    rs3 = cmds.shadingNode("RedshiftStandardMaterial", n = PFX + "RS_Basic_Three", asShader = True)
    cmds.setAttr(rs3 + ".base_color", 0, 1, 0)
    rs4 = cmds.shadingNode("RedshiftStandardMaterial", n = PFX + "RS_Basic_Four", asShader = True)
    cmds.setAttr(rs4 + ".base_color", 1, 0, 0)

    #rs car paint
    cmds.shadingNode("RedshiftCarPaint", n = PFX + "RS_Basic_Car_Paint", asShader = True)

"""CREATE TOOL OBJECTS"""
#creates the cirular stage for user to place their objects on to test
def make_stage():

    cmds.polyCylinder(n = "Stage_Part1", r = 8, h = .15, sa = 100)
    cmds.polyCylinder(n = "Stage_Part2", r = 7.95, h = .4, sa = 100)
    cmds.move(0,0.250, 0)
    cmds.polyBevel("Stage_Part2.e[100:199]", o = .06)
    cmds.polyCylinder(n = "Stage_Part3", r = 7.75, h = .3, sa = 100)
    cmds.move(0,0.431, 0)
    cmds.polyBevel("Stage_Part3.e[100:199]", o = .06)
    cmds.polyBooleanCmd( ["Stage_Part1", "Stage_Part2"], op = 1 )
    cmds.polyBooleanCmd( "polySurface1", edit=True, addMesh="Stage_Part3", op = 1 )
    cmds.DeleteHistory()
    cmds.rename("polySurface1", PFX + "Turn_Table")

#creates the render cam
def make_camera():
    
    cmds.camera(n = PFX + "Render_Cam")[0]
    cmds.move(0, 8, 32)
    cmds.rotate(-10,0, 0)

"""CREATE RENDER LAYERS"""
#create layer and layer override
def make_maya_layer():
    
    cmds.createRenderLayer(e = True, mc = True, nr = True, n = PFX + "Maya_Software_Layer")
    cmds.editRenderLayerAdjustment('defaultRenderGlobals.currentRenderer')
    cmds.setAttr('defaultRenderGlobals.currentRenderer', 'mayaSoftware', type='string')

#create layer and layer override
def make_arn_layer():

    cmds.createRenderLayer(PFX + "Turn_Table", PFX + "Render_Cam1", nr = True, mc = True, n = PFX + "Arnold_Layer")
    cmds.editRenderLayerAdjustment('defaultRenderGlobals.currentRenderer')
    cmds.setAttr('defaultRenderGlobals.currentRenderer', 'arnold', type='string')

#create layer and layer override
def make_hdri_layer():

    cmds.createRenderLayer(PFX + "Turn_Table", PFX + "Render_Cam1", nr = True,  mc = True, n = PFX + "HDRI_Layer")
    cmds.editRenderLayerAdjustment('defaultRenderGlobals.currentRenderer')
    cmds.setAttr('defaultRenderGlobals.currentRenderer', 'arnold', type='string')

#create layer and layer override
def make_red_layer():
        
    cmds.createRenderLayer(PFX + "Turn_Table", PFX + "Render_Cam1", nr = True, mc = True, n = PFX + "Redshift_Layer")
    cmds.editRenderLayerAdjustment('defaultRenderGlobals.currentRenderer')
    cmds.setAttr('defaultRenderGlobals.currentRenderer', 'redshift', type='string')

"""CREATE MAYA LIGHTS"""
#creates lights based on variables gotten from user input from GUI 
###KEY LIGHT###
def make_maya_key(maya_key_type, maya_key_cone, maya_key_int, maya_key_R, maya_key_G, maya_key_B):

    if maya_key_type == 0:
        cmds.spotLight(ca = maya_key_cone, i = maya_key_int, pos = (-12,12,3.7), rgb = (maya_key_R, maya_key_G, maya_key_B), rot = (-30,-60, 0), n = PFX + "Maya_Key_Light")
        
    if maya_key_type == 1:
        maya_keyarea_light = cmds.shadingNode("areaLight", asLight = True)
        cmds.move(-12, 12, 3.7)
        cmds.rotate(-30, -60, 0)
        cmds.setAttr(maya_keyarea_light + ".intensity", maya_key_int)
        cmds.setAttr(maya_keyarea_light + ".color", maya_key_R, maya_key_G, maya_key_G)
        cmds.rename(maya_keyarea_light, PFX + "Maya_Key_Light")

    if maya_key_type == 2:
        cmds.spotLight(ca = maya_key_cone, i = maya_key_int, pos = (-12,12,3.7), rgb = (maya_key_R, maya_key_G, maya_key_B), rot = (-30,-60, 0), n = PFX + "Maya_Key_Light")
        
        maya_keyarea_light = cmds.shadingNode("areaLight", asLight = True)
        cmds.move(-12, 12, 3.7)
        cmds.rotate(-30, -60, 0)
        cmds.setAttr(maya_keyarea_light + ".intensity", maya_key_int)
        cmds.setAttr(maya_keyarea_light + ".color", maya_key_R, maya_key_G, maya_key_G)
        cmds.hide(maya_keyarea_light)
        cmds.rename(maya_keyarea_light, PFX + "Maya_Key_Light_2")

###FILL LIGHT###
def make_maya_fill(maya_fill_type, maya_fill_cone, maya_fill_int, maya_fill_R, maya_fill_G, maya_fill_B):

    if maya_fill_type == 0:
        cmds.spotLight(ca = maya_fill_cone, i = maya_fill_int, pos = (7.13,6.6,7.8), rgb = (maya_fill_R, maya_fill_G, maya_fill_B), rot = (-26.8,45.7, -1), n = PFX + "Maya_Fill_Light")

    if maya_fill_type == 1:
        maya_fillarea_light = cmds.shadingNode("areaLight", asLight = True)
        cmds.move(7.13,6.6,7.8)
        cmds.rotate(-26.8,45.7, -1)
        cmds.setAttr(maya_fillarea_light + ".intensity", maya_fill_int)
        cmds.setAttr(maya_fillarea_light + ".color", maya_fill_R, maya_fill_G, maya_fill_G)
        cmds.rename(maya_fillarea_light, PFX + "Maya_Fill_Light")

    if maya_fill_type == 2:
        cmds.spotLight(ca = maya_fill_cone, i = maya_fill_int, pos = (7.13,6.6,7.8), rgb = (maya_fill_R, maya_fill_G, maya_fill_B), rot = (-26.8,45.7, -1), n = PFX + "Maya_Fill_Light")
        
        maya_fillarea_light = cmds.shadingNode("areaLight", asLight = True)
        cmds.move(7.13,6.6,7.8)
        cmds.rotate(-26.8,45.7, -1)
        cmds.setAttr(maya_fillarea_light + ".intensity", maya_fill_int)
        cmds.setAttr(maya_fillarea_light + ".color", maya_fill_R, maya_fill_G, maya_fill_G)
        cmds.hide(maya_fillarea_light)
        cmds.rename(maya_fillarea_light, PFX + "Maya_Fill_Light_2")

###BOUNCE LIGHT###
def make_maya_bounce(maya_bounce_type, maya_bounce_cone, maya_bounce_int, maya_bounce_R, maya_bounce_G, maya_bounce_B):

    if maya_bounce_type == 0:
        cmds.spotLight(ca = maya_bounce_cone, i = maya_bounce_int, pos = (3.3,-3.3,6.4), rgb = (maya_bounce_R, maya_bounce_G, maya_bounce_B), rot = (42,19.6, 0), rs = False, n = PFX + "Maya_Bounce_Light")

    if maya_bounce_type == 1:
        maya_bouncearea_light = cmds.shadingNode("areaLight", asLight = True)
        cmds.move(3.3,-3.3,6.48)
        cmds.rotate(42,19.6, 0)
        cmds.setAttr(maya_bouncearea_light + ".intensity", maya_bounce_int)
        cmds.setAttr(maya_bouncearea_light + ".color", maya_bounce_R, maya_bounce_G, maya_bounce_G)
        cmds.setAttr(maya_bouncearea_light + ".useRayTraceShadows", 0)
        cmds.rename(maya_bouncearea_light, PFX + "Maya_Bounce_Light")

    if maya_bounce_type == 2:

        cmds.spotLight(ca = maya_bounce_cone, i = maya_bounce_int, pos = (3.3,-3.3,6.4), rgb = (maya_bounce_R, maya_bounce_G, maya_bounce_B), rot = (42,19.6, 0), rs = False, n = PFX + "Maya_Bounce_Light")
        
        maya_bouncearea_light = cmds.shadingNode("areaLight", asLight = True)
        cmds.move(3.3,-3.3,6.4)
        cmds.rotate(42,19.6, 0)
        cmds.setAttr(maya_bouncearea_light + ".intensity", maya_bounce_int)
        cmds.setAttr(maya_bouncearea_light + ".color", maya_bounce_R, maya_bounce_G, maya_bounce_G)
        cmds.setAttr(maya_bouncearea_light + ".useRayTraceShadows", 0)
        cmds.hide(maya_bouncearea_light)
        cmds.rename(maya_bouncearea_light, PFX + "Maya_Bounce_Light_2")

"""CREATE ARNOLD LIGHT"""
###KEY LIGHT###
#creates light based on variables gotten from user input from GUI 
def make_arn_key(arn_type, arn_cone, arn_int, arn_R, arn_G, arn_B):

    if arn_type == 0:
        cmds.spotLight(ca = arn_cone, i = arn_int, rgb = (arn_R, arn_G, arn_B), n = PFX + "Arnold_Key_Light")
        cmds.rotate(-30,-60,0)
        cmds.move(-12,12,3.7)

    if arn_type == 1:
        arn_area_light = cmds.shadingNode("areaLight", asLight = True)
        cmds.move(-12, 12, 3.7)
        cmds.rotate(-30, -60, 0)
        cmds.setAttr(arn_area_light + ".intensity", arn_int)
        cmds.setAttr(arn_area_light + ".color", arn_R, arn_G, arn_G)
        cmds.rename(arn_area_light, PFX + "Arnold_Key_Light")

    if arn_type == 2:
        cmds.spotLight(ca = arn_cone, i = arn_int, pos = (-12,12,3.7), rgb = (arn_R, arn_G, arn_B), rot = (-30,-60, 0), n = PFX + "Arnold_Key_Light")
        
        arn_area_light = cmds.shadingNode("areaLight", asLight = True)
        cmds.move(-12, 12, 3.7)
        cmds.rotate(-30, -60, 0)
        cmds.setAttr(arn_area_light + ".intensity", arn_int)
        cmds.setAttr(arn_area_light + ".color", arn_R, arn_G, arn_B)
        cmds.hide(arn_area_light)
        cmds.rename(arn_area_light, PFX + "Arnold_Key_Light_2")

"""MAKE HDRI DOME"""
#uses the file path given to create the hdri dome
#if no file is given a dome is still created just without an hdri attached

def make_hdri_dome(hdri_path):

    if hdri_path == 0:
        mutils.createLocator("aiSkyDomeLight", asLight = True)
        skydome = cmds.rename("aiSkyDomeLight1", PFX + "HDRI_Light")

    else:
        mutils.createLocator("aiSkyDomeLight", asLight = True)
        skydome = cmds.rename("aiSkyDomeLight1", PFX + "HDRI_Light")
        file_txt = cmds.shadingNode("file", asTexture = True, n= "fileTxt")
        cmds.setAttr(file_txt + ".fileTextureName", hdri_path, type="string")
        cmds.connectAttr(file_txt + ".outColor", skydome +".color", force = True)

"""CREATE REDSHIFT LIGHT"""
###KEY LIGHT###
#creates lights based on variables gotten from user input from GUI 
def make_red_key(red_type, red_cone, red_int, red_R, red_G, red_B):
    
    if red_type == 0:
        cmds.spotLight(ca = red_cone, i = red_int, pos = (-12,12,3.7), rgb = (red_R, red_G, red_B), rot = (-30,-60, 0), n = PFX + "Redshift_Key_Light")

    if red_type == 1:
        red_area_light = cmds.shadingNode("areaLight", asLight = True)
        cmds.move(-12, 12, 3.7)
        cmds.rotate(-30, -60, 0)
        cmds.setAttr(red_area_light + ".intensity", red_int)
        cmds.setAttr(red_area_light + ".color", red_R, red_G, red_G)
        cmds.rename(red_area_light, PFX + "Redshift_Key_Light")

    if red_type == 2:
        cmds.spotLight(ca = red_cone, i = red_int, pos = (-12,12,3.7), rgb = (red_R, red_G, red_B), rot = (-30,-60, 0), n = PFX + "Redshift_Key_Light")
        
        red_area_light = cmds.shadingNode("areaLight", asLight = True)
        cmds.move(-12, 12, 3.7)
        cmds.rotate(-30, -60, 0)
        cmds.setAttr(red_area_light + ".intensity", red_int)
        cmds.setAttr(red_area_light + ".color", red_R, red_G, red_G)
        cmds.hide(red_area_light)
        cmds.rename(red_area_light, PFX + "Redshift_Key_Light_2")

"""FINAL ADJUSTMENTS"""
#groups everything together for easy organization
#resizes as a group so camera, lights, and extra items are properly scaled up as well
def resize(stage_size):

    size = stage_size / 8
    group = cmds.group(PFX + "*", n = PFX + "Lighting_Tool_Objects")
    cmds.move(0, 0, 0, group +".scalePivot")
    cmds.scale(size, size, size)
    cmds.lookThru(PFX + "Render_Cam1") #final look thru after resize
