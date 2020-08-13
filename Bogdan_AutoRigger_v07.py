import maya.cmds as cmds

# ui dimensions
winWidth = 300
winHeight = 487

# button colours
layoutStep0 = (.35,0,0.7)
layoutStep1 = (.3,0,0.6)
layoutStep2 = (.25,0,0.5)
layoutStep3 = (.2,0,0.4)
layoutStep4 = (.15,0,0.3)
layoutStep5 = (.1,0,0.2)

# instance window name
UiMain = "MainInterface"
enableUiElements = False

### Utility Functions ###

def updateValues(primaryVar, secondaryVar, uiType):

    if uiType == "field":
        if not cmds.intField(primaryVar, q=True, v=True) < 6:
            cmds.intSlider(secondaryVar, e=True, max=cmds.intField(primaryVar, q=True, v=True))
        cmds.intSlider(secondaryVar, e=True, v=cmds.intField(primaryVar, q=True, v=True))
    if uiType == "slider":
        cmds.intField(secondaryVar, e=True, v=cmds.intSlider(primaryVar, q=True, v=True))

# function to combine commands from gui
# take functions from command line and fills is "*funcs" ex: combine_funcs(func1(args), func2(args))
def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        # for each function added to command line
        for f in funcs:
            # run function with its arguements
            f(*args, **kwargs)

def measuringTool(group_name, startLocation, endLocation):
    
    group = cmds.group(em=True, n=group_name)
    cmds.parent(group,  createCore.rig_name)
    
    # create measuring tool using 2 locators
    measuringTool.start = cmds.spaceLocator(n="measure_start")[0]
    cmds.setAttr("{}.v".format(measuringTool.start), 0)
    cmds.parent(measuringTool.start, group)
    measuringTool.end = cmds.spaceLocator(n="measure_end")[0]
    cmds.setAttr("{}.v".format(measuringTool.end), 0)
    cmds.parent(measuringTool.end, measuringTool.start)
    cmds.pointConstraint(startLocation, measuringTool.start)
    cmds.pointConstraint(endLocation, measuringTool.end)
    cmds.aimConstraint(endLocation, measuringTool.start)
    
def createCurve(name, start, end):
    # create curve
    createCurve.curvee = cmds.curve(d=1, p=[(0,0,0),(1,0,0)], k=[0,1], n=name)
    cmds.setAttr("{}.template".format(createCurve.curvee), 1)
    cmds.parent(createCurve.curvee, createCore.curve_grp)
    # parent edit points of curve to locators, then hide locators
    createCurve.curveLocator_start = cmds.pointCurveConstraint("{}.ep[0]".format(createCurve.curvee), rpo=True, w=1)[0]
    cmds.setAttr("{}.v".format(createCurve.curveLocator_start), 0)
    cmds.parent(createCurve.curveLocator_start, createCore.curve_grp)
    createCurve.curveLocator_end = cmds.pointCurveConstraint("{}.ep[1]".format(createCurve.curvee), rpo=True, w=1)[0]
    cmds.CenterPivot(createCurve.curveLocator_end)
    cmds.setAttr("{}.v".format(createCurve.curveLocator_end), 0)
    cmds.parent(createCurve.curveLocator_end, createCore.curve_grp)
    # constrain locators to start joint and end joint
    cmds.parentConstraint(start, createCurve.curveLocator_start)
    cmds.parentConstraint(end, createCurve.curveLocator_end)
    
### ================= ###

# check whether window: "Main Interface" already exists
if (cmds.window(UiMain, q=True, ex=True)):
    cmds.deleteUI(UiMain)

# create main ui
cmds.window(UiMain, t="Main Interface", s=False, wh=(winWidth,winHeight), rtf=True)
tabs = cmds.tabLayout()

#################################
## Proxy tab
#################################

prox_parent = cmds.columnLayout()
# frame laying out step 1.0: to generate the proxy
cmds.frameLayout(l="Step 1.0 Name Rig", bv=True, bgc=layoutStep0, w=winWidth*.975, h=winHeight/11)

rigName = cmds.textField(pht="rig_name")
# setting parent to top column layout
cmds.setParent(prox_parent)

# frame laying out step 1.1: to generate the proxy
cmds.frameLayout(l="Step 1.1 Initialize Proxy", bv=True, bgc=layoutStep1, w=winWidth*.975, h=winHeight/6.5)

cmds.rowColumnLayout(nc=2, cw=[(1,winWidth*.5),(2,winWidth*.5)])
createButton = cmds.button(l="Generate Proxy", bgc=(0.5,0.5,0.5), w=winWidth/2, h=winHeight/10, c="createCore()")
resetButton = cmds.button(l="Reset Proxy", bgc=(0.4,0.4,0.4), w=winWidth/2, h=winHeight/10, c="resetCore()", en=False)
# setting parent to top column layout
cmds.setParent(prox_parent)

# frame laying out step 1.2: to customize spine and neck
frameLayout1_2 = cmds.frameLayout(l="Step 1.2 Spine and Neck", bv=True, bgc=layoutStep2, w=winWidth*.975, en=False)

cmds.rowColumnLayout(nc=3, cw=[(1,winWidth*.30),(2,winWidth*.20),(3,winWidth*.45)])
# how many spine joints
cmds.text(l="Spine joints:")
spineIntField = cmds.intField(v=3, cc="combine_funcs(updateValues(spineIntField, spineIntSlider, 'field'), createFromSlider('spine'))")
spineIntSlider = cmds.intSlider(min=1, max=6, v=3, dc="combine_funcs(updateValues(spineIntSlider, spineIntField, 'slider'), createFromSlider('spine'))")
# how many neck joints
cmds.text(l="Neck joints:")
neckIntField = cmds.intField(v=1, cc="combine_funcs(updateValues(neckIntField, neckIntSlider, 'field'), createFromSlider('neck'))")
neckIntSlider = cmds.intSlider(min=1, max=5, v=1, dc="combine_funcs(updateValues(neckIntSlider, neckIntField, 'slider'), createFromSlider('neck'))")

# setting parent to top column layout
cmds.setParent(prox_parent)

# frame laying out step 1.3: to customize hands and feet
frameLayout1_3 = cmds.frameLayout(l="Step 1.3 Arms", bv=True, bgc=layoutStep3, w=winWidth*.975, en=False)

cmds.rowColumnLayout(nc=3, cw=[(1,winWidth*.30),(2,winWidth*.20),(3,winWidth*.45)])
# ask if user wants thumbs
cmds.text(l="Thumbs?")
thumbCheckBox = cmds.checkBox(l="", v=True, h=20, cc="createFromSlider('thumb')")
cmds.separator(vis=False)
# how many fingers
cmds.text(l="Fingers:")
fingerIntField = cmds.intField(v=4, cc="combine_funcs(updateValues(fingerIntField, fingerIntSlider, 'field'), createFromSlider('finger'))")
fingerIntSlider = cmds.intSlider(min=1, max=4, v=4, dc="combine_funcs(updateValues(fingerIntSlider, fingerIntField, 'slider'), createFromSlider('finger'))")
# how many elbows
cmds.text(l="Elbows:")
elbowIntField = cmds.intField(v=1, cc="combine_funcs(updateValues(elbowIntField, elbowIntSlider, 'field'), createFromSlider('elbow'))")
elbowIntSlider = cmds.intSlider(min=1, max=6, v=1, dc="combine_funcs(updateValues(elbowIntSlider, elbowIntField, 'slider'), createFromSlider('elbow'))")
# setting parent to top column layout
cmds.setParent(prox_parent)

# frame laying out step 1.4: to customize hands and feet
frameLayout1_4 = cmds.frameLayout(l="Step 1.4 Legs", bv=True, bgc=layoutStep4, w=winWidth*.975, en=False)

cmds.rowColumnLayout(nc=3, cw=[(1,winWidth*.30),(2,winWidth*.20),(3,winWidth*.45)])
# ask if user wants toes
cmds.text(l="Toes?")
toeCheckBox = cmds.checkBox(l="", onc="enableToes()", ofc="disableToes()", v=False, h=20)
cmds.separator(vis=False)
# how many toes
toeText = cmds.text(l="Toes:", en=False)
toeIntField = cmds.intField(v=1, cc="combine_funcs(updateValues(toeIntField, toeIntSlider, 'field'), createFromSlider())", en=False)
toeIntSlider = cmds.intSlider(min=1, max=6, v=1, dc="combine_funcs(updateValues(toeIntSlider, toeIntField, 'slider'), createFromSlider())", en=False)
# how many elbows
cmds.text(l="Knees:")
kneeIntField = cmds.intField(v=1, cc="combine_funcs(updateValues(kneeIntField, kneeIntSlider, 'field'), createFromSlider('knee'))")
kneeIntSlider = cmds.intSlider(min=1, max=6, v=1, dc="combine_funcs(updateValues(kneeIntSlider, kneeIntField, 'slider'), createFromSlider('knee'))")

cmds.setParent(prox_parent)
# frame laying out step 1.5: to customize hands and feet
frameLayout1_5 = cmds.frameLayout(l="Step 1.5 Mirror/Reset Pose", bv=True, bgc=layoutStep5, w=winWidth*.975, en=False)

cmds.rowColumnLayout(nc=1, cw=[(1,winWidth*.975)], h=35)
cmds.text(l="Reset is based on selection - Resets selected and all children."
            " Have nothing selected to reset all", ww=True)

cmds.setParent(frameLayout1_5)
cmds.rowColumnLayout(nc=3, cw=[(1,winWidth*.33),(2,winWidth*.33),(3,winWidth*.3)])
LtoR_Button = cmds.button(l="Left to Right", bgc=(0.5,0.5,0.5), w=winWidth/3, h=winHeight/12, c="mirrorProxyPose('L2R')")
RtoL_Button = cmds.button(l="Right to Left", bgc=(0.47,0.47,0.47), w=winWidth/3, h=winHeight/12, c="mirrorProxyPose('R2L')")
resetPos_Button = cmds.button(l="Reset", bgc=(0.4,0.4,0.4), w=winWidth/4, h=winHeight/12, c="zeroProxy()")


#################################
## Joint/Controls tab
#################################
cmds.setParent(tabs)

jntCtrl_parent = cmds.columnLayout()
# 2.0: joint naming conventions
cmds.frameLayout(l="Step 2.0 Naming convention", bv=True, bgc=layoutStep0, w=winWidth*.975)
cmds.rowColumnLayout(nc=3, cw=[(1,winWidth*.40),(2,winWidth*.30),(3,winWidth*.30)], h=62)

# textfield to get suffix preferences from user
cmds.text(l="Joint Suffix : ")
# joint suffices
jnt_suffix = cmds.textField(pht="_jnt")
cmds.separator(vis=False)

cmds.text(l="Control Suffix : ")
# ctrl suffices
ctrl_suffix = cmds.textField(pht="_ctrl")
ctrlGrp_suffix = cmds.textField(pht="_ctrlGrp")

cmds.text(l="Left/Right : ")
# side naming conventions
left_naming = cmds.textField(pht="_L")
right_naming = cmds.textField(pht="_R")

# 2.1 create rig and hide proxy
cmds.setParent(jntCtrl_parent)
frameLayout2_1 = cmds.frameLayout(l="Step 2.1 Create rig", bv=True, bgc=layoutStep1, w=winWidth*.975, en=False)

cmds.rowColumnLayout(nc=2, cw=[(1,winWidth*.5),(2,winWidth*.5)])
createSkeletonButton = cmds.button(l="Generate Rig", bgc=(0.5,0.5,0.5), w=winWidth/2, h=winHeight/10, c="combine_funcs(createSkeletonCore(), createRigControls())", en=True)
resetSkeletonButton = cmds.button(l="Reset Rig", bgc=(0.4,0.4,0.4), w=winWidth/2, h=winHeight/10, c="resetRig()", en=False)

# setting parent to top column layout
## allow user to choose rig colours
cmds.setParent(jntCtrl_parent)
frameLayout2_2 = cmds.frameLayout(l="Step 2.2 Change Rig Colors", bv=True, bgc=layoutStep2, w=winWidth*.975, en=False)
'''
cmds.rowColumnLayout(nc=3, cw=[(1,winWidth*.50),(2,winWidth*.25),(3,winWidth*.25)])
createControlsButton = cmds.button(l="Create Controls", bgc=(0.5,0.5,0.5), w=winWidth/2, h=winHeight/10, c="createRigControls()", en=True)
leftColorsButton = cmds.button(l="Left", bgc=(0.0,0.5,0.0), w=winWidth/4, h=winHeight/10, c="createRigControls()", en=True)
rightColorsButton = cmds.button(l="Right", bgc=(0.5,0.0,0.0), w=winWidth/4, h=winHeight/10, c="createRigControls()", en=True)
'''
# setting parent to top column layout
## allow user to adjust control shape and size
cmds.setParent(jntCtrl_parent)
frameLayout2_3 = cmds.frameLayout(l="Step 2.3 Adjust Controller Shape and Size", bv=True, bgc=layoutStep3, w=winWidth*.975, en=False)

cmds.tabLayout( tabs, e=True, tabLabel=((prox_parent, "Step 1: Proxy"),(jntCtrl_parent, "Step 2: Joints/Controls")) )

cmds.window(UiMain, e=True, wh=(winWidth,winHeight))
cmds.showWindow()
        
def enableUi(enabled=False):
    if enabled == False:
        cmds.button(createButton, e=True, en=True)
    cmds.button(createButton, e=True, en=False)
    cmds.button(resetButton, e=True, en=enabled)
    cmds.frameLayout(frameLayout1_2, e=True, en=enabled)
    cmds.frameLayout(frameLayout1_3, e=True, en=enabled)
    cmds.frameLayout(frameLayout1_4, e=True, en=enabled)
    cmds.frameLayout(frameLayout1_5, e=True, en=enabled)
    
    cmds.frameLayout(frameLayout2_1, e=True, en=enabled)
    
    cmds.button(createSkeletonButton, e=True, en=enabled)

def enableToes():
    cmds.text(toeText, e=True, en=True)
    cmds.intField(toeIntField, e=True, en=True)
    cmds.intSlider(toeIntSlider, e=True, en=True)
def disableToes():
    cmds.text(toeText, e=True, en=False)
    cmds.intField(toeIntField, e=True, en=False)
    cmds.intSlider(toeIntSlider, e=True, en=False)

# creates proxy joint #
def proxyJoint( group_name, name, radius, color=1 ):
    # create empty transform
    prxyJnt = cmds.group(em=True, n=name)

    # create nurbs circles
    cNorms = [(1,0,0),(0,1,0),(0,0,1)]
    for c in range(0,3):
        circle = cmds.circle(r=radius, nr=cNorms[c])
        circleShape = cmds.listRelatives(s=True)[0]
        cmds.setAttr("{}.overrideEnabled".format(circleShape), 1) # enable color override
        cmds.setAttr("{}.overrideColor".format(circleShape), color) # change color of circles to black
        cmds.parent(circleShape, prxyJnt, r=True, s=True)
        cmds.delete(circle)
    
    cmds.select(prxyJnt)
    proxyJoint.prxyJnt_Grp = cmds.group(n=group_name)
        
    
#######################

def resetRig():
    cmds.delete( "spine_base_jnt", "cog_ctrlGrp")
    for ctrl in [ "thumb", "index", "middle", "ring", "pinky", "finger", "wrist", "elbow", "arm", "knee", "leg"]:
        if cmds.objExists("{}*".format(ctrl)):
            cmds.delete("{}*".format(ctrl))
    
    cmds.setAttr("{}.visibility".format(createCore.rig_name), 1)
    cmds.setAttr("proxy_joint_grp.visibility".format(createCore.rig_name), 1)
    
    cmds.button(resetSkeletonButton, e=True, en=False)
    cmds.button(createSkeletonButton, e=True, en=True)
    

def resetCore():
    grp_suff = cmds.textField(ctrlGrp_suffix, q=True, pht=True)
    if cmds.textField(ctrlGrp_suffix, q=True, tx=True):
        grp_suff = cmds.textField(ctrlGrp_suffix, q=True, tx=True)
    
    cmds.delete( "{}_main{}".format(createCore.rig_name, grp_suff) )
    createCore()
    
    
#############################
##### Proxy Creation
#############################

def createCore():
    # create empty transform
    createCore.rig_name = cmds.textField(rigName, q=True, pht=True)
    if cmds.textField(rigName, q=True, tx=True):
        createCore.rig_name = cmds.textField(rigName, q=True, tx=True)
    group = cmds.group(em=True, n=createCore.rig_name)
    
    createCore.curve_grp = cmds.group(em=True, n="TEMP_curves_grp")
    cmds.parent(createCore.curve_grp, createCore.rig_name)
    
    # base of spine
    proxyJoint("TEMP_spineBase_grp","TEMP_spineBase_jnt",0.35)
    cmds.select(proxyJoint.prxyJnt_Grp)
    cmds.xform(t=(0,8,0))
    cmds.parent(proxyJoint.prxyJnt_Grp, createCore.rig_name)
    # top of spine
    proxyJoint("TEMP_spineTop_grp","TEMP_spineTop_jnt",0.35)
    cmds.select(proxyJoint.prxyJnt_Grp)
    cmds.xform(t=(0,12,0))
    cmds.parent(proxyJoint.prxyJnt_Grp, "TEMP_spineBase_jnt")
    
    # create curve between spine base and top
    createCurve("TEMP_spine_curve", "TEMP_spineBase_jnt", "TEMP_spineTop_jnt")
    
    # create spine joints between spine base and top
    createSpine()
    
    # create base of neck
    proxyJoint("TEMP_neckBase_grp", "TEMP_neckBase_jnt", 0.2)
    cmds.select(proxyJoint.prxyJnt_Grp)
    cmds.xform(t=(0,13,0))
    cmds.parent(proxyJoint.prxyJnt_Grp, "TEMP_spineTop_jnt")
    # create curve between spine top and neck base
    createCurve("TEMP_spineNeck_curve", "TEMP_spineTop_jnt", "TEMP_neckBase_jnt")
    
    # create base of head
    proxyJoint("TEMP_headBase_grp", "TEMP_headBase_jnt", 0.2)
    cmds.select(proxyJoint.prxyJnt_Grp)
    cmds.xform(t=(0,14,0))
    cmds.parent(proxyJoint.prxyJnt_Grp, "TEMP_neckBase_jnt")
    # create curve between neck base and head base
    createCurve("TEMP_neck_curve", "TEMP_neckBase_jnt", "TEMP_headBase_jnt")
    
    # create top of head
    proxyJoint("TEMP_headTop_grp", "TEMP_headTop_jnt", 0.2)
    cmds.select(proxyJoint.prxyJnt_Grp)
    cmds.xform(t=(0,16,0))
    cmds.parent(proxyJoint.prxyJnt_Grp, "TEMP_headBase_jnt")
    # create curve between neck base and head base
    createCurve("TEMP_head_curve", "TEMP_headBase_jnt", "TEMP_headTop_jnt")
    
    # create neck joints between neck base and top
    createNeck()
    
    # create jaw
    proxyJoint("TEMP_jaw_grp", "TEMP_jaw_jnt", 0.2)
    cmds.select(proxyJoint.prxyJnt_Grp)
    cmds.xform(t=(0,14.5,.42))
    cmds.parent(proxyJoint.prxyJnt_Grp, "TEMP_headBase_jnt")
    # create curve between neck base and head base
    createCurve("TEMP_jaw_curve", "TEMP_headBase_jnt", "TEMP_jaw_jnt")
    
    proxyJoint("TEMP_jaw_end_grp", "TEMP_jaw_end_jnt", 0.2)
    cmds.select(proxyJoint.prxyJnt_Grp)
    cmds.xform(t=(0,14,1.15))
    cmds.parent(proxyJoint.prxyJnt_Grp, "TEMP_jaw_jnt")
    # create curve between neck base and head base
    createCurve("TEMP_jaw_end_curve", "TEMP_jaw_jnt", "TEMP_jaw_end_jnt")
    
    # create eyes
    proxyJoint("TEMP_eye_r_grp", "TEMP_eye_r_jnt", 0.2)
    cmds.select(proxyJoint.prxyJnt_Grp)
    cmds.xform(t=(-0.4,15.25,1.1))
    cmds.parent(proxyJoint.prxyJnt_Grp, "TEMP_headBase_jnt")
    # create curve between neck base and head base
    createCurve("TEMP_eye_r_curve", "TEMP_headBase_jnt", "TEMP_eye_r_jnt")
    
    proxyJoint("TEMP_eye_l_grp", "TEMP_eye_l_jnt", 0.2)
    cmds.select(proxyJoint.prxyJnt_Grp)
    cmds.xform(t=(0.4,15.25,1.1))
    cmds.parent(proxyJoint.prxyJnt_Grp, "TEMP_headBase_jnt")
    # create curve between neck base and head base
    createCurve("TEMP_eye_l_curve", "TEMP_headBase_jnt", "TEMP_eye_l_jnt")
    
    #################
    # left clavicle #
    proxyJoint("TEMP_clavicle_l_grp", "TEMP_clavicle_l_jnt", 0.2)
    cmds.select(proxyJoint.prxyJnt_Grp)
    cmds.xform(t=(1,11.5,0))
    cmds.parent(proxyJoint.prxyJnt_Grp, "TEMP_spineTop_jnt")
    # create curve between spine and clavicle
    createCurve("TEMP_clavicle_l_curve", "TEMP_spineTop_jnt", "TEMP_clavicle_l_jnt")
    # left shoulder #
    proxyJoint("TEMP_shoulder_l_grp", "TEMP_shoulder_l_jnt", 0.35)
    cmds.select(proxyJoint.prxyJnt_Grp)
    cmds.xform(t=(2,12,0))
    cmds.parent(proxyJoint.prxyJnt_Grp, "TEMP_clavicle_l_jnt")
    # create curve between neck base and head base
    createCurve("TEMP_shoulder_l_curve", "TEMP_clavicle_l_jnt", "TEMP_shoulder_l_jnt")
    # left wrist #
    proxyJoint("TEMP_wrist_l_grp", "TEMP_wrist_l_jnt", 0.2)
    cmds.select(proxyJoint.prxyJnt_Grp)
    cmds.xform(t=(6.5,12,0))
    cmds.parent(proxyJoint.prxyJnt_Grp, "TEMP_shoulder_l_jnt")
    # create curve between neck base and head base
    createCurve("TEMP_arm_l_curve", "TEMP_shoulder_l_jnt", "TEMP_wrist_l_jnt")
    
    # create elbow joints between shoulder and wrist
    createElbow("l")
    
    createThumb('l')
    createFinger("l")
    
    ##################
    # right clavicle #
    proxyJoint("TEMP_clavicle_r_grp", "TEMP_clavicle_r_jnt", 0.2)
    cmds.select(proxyJoint.prxyJnt_Grp)
    cmds.xform(t=(-1,11.5,0))
    cmds.parent(proxyJoint.prxyJnt_Grp, "TEMP_spineTop_jnt")
    # create curve between spine and clavicle
    createCurve("TEMP_clavicle_r_curve", "TEMP_spineTop_jnt", "TEMP_clavicle_r_jnt")
    # right shoulder #
    proxyJoint("TEMP_shoulder_r_grp", "TEMP_shoulder_r_jnt", 0.35)
    cmds.select(proxyJoint.prxyJnt_Grp)
    cmds.xform(t=(-2,12,0))
    cmds.parent(proxyJoint.prxyJnt_Grp, "TEMP_clavicle_r_jnt")
    # create curve between neck base and head base
    createCurve("TEMP_shoulder_r_curve", "TEMP_clavicle_r_jnt", "TEMP_shoulder_r_jnt")
    # right wrist
    proxyJoint("TEMP_wrist_r_grp", "TEMP_wrist_r_jnt", 0.2)
    cmds.select(proxyJoint.prxyJnt_Grp)
    cmds.xform(t=(-6.5,12,0))
    cmds.parent(proxyJoint.prxyJnt_Grp, "TEMP_shoulder_r_jnt")
    # create curve between neck base and head base
    createCurve("TEMP_arm_r_curve", "TEMP_shoulder_r_jnt", "TEMP_wrist_r_jnt")
    
    # create elbow joints between shoulder and wrist
    createElbow("r")
    
    createThumb('r')
    createFinger("r")
    
    ############
    # left hip #
    proxyJoint("TEMP_hip_l_grp", "TEMP_hip_l_jnt", 0.35)
    cmds.select(proxyJoint.prxyJnt_Grp)
    cmds.xform(t=(1.1,7,0))
    cmds.parent(proxyJoint.prxyJnt_Grp, "TEMP_spineBase_jnt")
    # create curve between neck base and head base
    createCurve("TEMP_hip_l_curve", "TEMP_spineBase_jnt", "TEMP_hip_l_jnt")
    # foot wrist #
    createFoot("l")
    cmds.parent("TEMP_foot_l_grp", "TEMP_hip_l_jnt")
    # create curve between neck base and head base
    createCurve("TEMP_leg_l_curve", "TEMP_hip_l_jnt", "TEMP_foot_l_jnt")
    
    createKnee('l')
    
    #############
    # right hip #
    proxyJoint("TEMP_hip_r_grp", "TEMP_hip_r_jnt", 0.35)
    cmds.select(proxyJoint.prxyJnt_Grp)
    cmds.xform(t=(-1.1,7,0))
    cmds.parent(proxyJoint.prxyJnt_Grp, "TEMP_spineBase_jnt")
    # create curve between neck base and head base
    createCurve("TEMP_hip_r_curve", "TEMP_spineBase_jnt", "TEMP_hip_r_jnt")
    # foot wrist #
    createFoot("r")
    cmds.parent("TEMP_foot_r_grp", "TEMP_hip_r_jnt")
    # create curve between neck base and head base
    createCurve("TEMP_leg_r_curve", "TEMP_hip_r_jnt", "TEMP_foot_r_jnt")
    
    createKnee('r')
    
    createProxyControls()
    cmds.parent(createCore.rig_name, createProxyControls.main_control)
    
    proxy_grp = cmds.group(em=True, n="proxy_joint_grp")
    cmds.parent( proxy_grp, createProxyControls.main_ctrl_group )
    
    cmds.parent("TEMP_{}_grp".format( "spines" ), proxy_grp )
    cmds.parent("TEMP_{}_grp".format( "necks" ), proxy_grp )
    
    for jntGrp in [ "elbows", "knees" ]:
        for side in [ "l", "r" ]:
            cmds.parent("TEMP_{}_{}_grp".format( jntGrp, side ), proxy_grp )
    
    cmds.select(cl=True)
    enableUi(True)

def createFromSlider(slider=None):
    if slider == 'neck':
        if createNeck.neck_Grp:
            cmds.delete(createNeck.neck_Grp)
        createNeck()
    if slider == 'spine':
        if createSpine.spine_Grp:
            cmds.delete(createSpine.spine_Grp)
        createSpine()
    if slider == 'elbow':
        if createElbow.elbow_Grp:
            cmds.delete("TEMP_elbows_l_grp")
            cmds.delete("TEMP_elbows_r_grp")
        createElbow('l')
        createElbow('r')
    if slider == 'knee':
        if createKnee.knee_Grp:
            cmds.delete("TEMP_knees_l_grp")
            cmds.delete("TEMP_knees_r_grp")
        createKnee('l')
        createKnee('r')
    if slider == 'finger':
        if cmds.objExists("TEMP_finger*"):
            cmds.delete("TEMP_finger*")
        createFinger('l')
        createFinger('r')
    if slider == 'thumb':
        if cmds.objExists("TEMP_thumb*"):
            cmds.delete("TEMP_thumb*")
        createThumb('l')
        createThumb('r')
        
        

def createSpine():
    # query number of desired spine joints
    numSpines = cmds.intField(spineIntField, q=True, v=True)
    # create group
    createSpine.spine_Grp = cmds.group(em=True, n="TEMP_spines_grp")
    cmds.parent(createSpine.spine_Grp, createCore.rig_name)
    
    # create and place joints at intervals
    if not numSpines == 0:
        jntInterval = float(1.0/(numSpines+1))
        
        for spine in range(numSpines):
            proxyJoint("TEMP_spine_{}_grp".format(spine+1), "TEMP_spine_{}_jnt".format(spine+1), 0.15)
            
            cmds.select(proxyJoint.prxyJnt_Grp, "TEMP_spine_curve", r=True)
            cmds.pathAnimation(su=jntInterval*(spine+1), stu=spine+1)
            
            cmds.parent(proxyJoint.prxyJnt_Grp, createSpine.spine_Grp)
            
            # hide spine curve
            ## create seperate curves between each joint
            cmds.setAttr( "TEMP_spine_curve.v", 0 )
            if spine > 0:
                createCurve( "TEMP_spine_{}_curve".format(spine+1), "TEMP_spine_{}_jnt".format(spine), "TEMP_spine_{}_jnt".format(spine+1) )
                cmds.parent(createCurve.curvee, createCurve.curveLocator_start, createCurve.curveLocator_end, createSpine.spine_Grp)
        
        createCurve( "TEMP_spine_1_curve", "TEMP_spineBase_jnt", "TEMP_spine_1_jnt" )
        cmds.parent(createCurve.curvee, createCurve.curveLocator_start, createCurve.curveLocator_end, createSpine.spine_Grp)
        createCurve( "TEMP_spine_{}_curve".format(numSpines+1), "TEMP_spine_{}_jnt".format(numSpines), "TEMP_spineTop_jnt" )
        cmds.parent(createCurve.curvee, createCurve.curveLocator_start, createCurve.curveLocator_end, createSpine.spine_Grp)
    
    cmds.select(cl=True)

def createNeck():
    # query number of desired neck joints
    numNecks = cmds.intField(neckIntField, q=True, v=True)
    # create group
    createNeck.neck_Grp = cmds.group(em=True, n="TEMP_necks_grp")
    cmds.parent(createNeck.neck_Grp, createCore.rig_name)
    # create and place joints at intervals
    if not numNecks == 0:
        jntInterval = float(1.0/(numNecks+1))
        
        for neck in range(numNecks):
            proxyJoint("TEMP_neck_{}_grp".format(neck+1), "TEMP_neck_{}_jnt".format(neck+1), 0.1)
            
            cmds.select(proxyJoint.prxyJnt_Grp, "TEMP_neck_curve", r=True)
            cmds.pathAnimation(su=jntInterval*(neck+1), stu=neck+1)
            
            cmds.parent(proxyJoint.prxyJnt_Grp, createNeck.neck_Grp)
            
            # hide neck curve
            ## create seperate curves between each joint
            cmds.setAttr( "TEMP_neck_curve.v", 0 )
            if neck > 0:
                createCurve( "TEMP_neck_{}_curve".format(neck+1), "TEMP_neck_{}_jnt".format(neck), "TEMP_neck_{}_jnt".format(neck+1) )
                cmds.parent(createCurve.curvee, createCurve.curveLocator_start, createCurve.curveLocator_end, createNeck.neck_Grp)
        
        createCurve( "TEMP_neck_1_curve", "TEMP_neckBase_jnt", "TEMP_neck_1_jnt" )
        cmds.parent(createCurve.curvee, createCurve.curveLocator_start, createCurve.curveLocator_end, createNeck.neck_Grp)
        createCurve( "TEMP_neck_{}_curve".format(numNecks+1), "TEMP_neck_{}_jnt".format(numNecks), "TEMP_headBase_jnt" )
        cmds.parent(createCurve.curvee, createCurve.curveLocator_start, createCurve.curveLocator_end, createNeck.neck_Grp)
        
    cmds.select(cl=True)

def createElbow(side):
    # query number of desired neck joints
    numElbows = cmds.intField(elbowIntField, q=True, v=True)
                                                            
    # create group
    createElbow.elbow_Grp = cmds.group(em=True, n="TEMP_elbows_{}_grp".format(side))
    cmds.parent(createElbow.elbow_Grp, createCore.rig_name)
    # create and place joints at intervals
    if not numElbows == 0:
        jntInterval = float(1.0/(numElbows+1))
        
        for elbow in range(numElbows):
            proxyJoint("TEMP_elbow_{}_{}_grp".format(elbow+1, side), "TEMP_elbow_{}_{}_jnt".format(elbow+1, side), 0.2)
            
            cmds.select(proxyJoint.prxyJnt_Grp, "TEMP_arm_{}_curve".format(side), r=True)
            cmds.pathAnimation(su=jntInterval*(elbow+1), stu=elbow+1, f=True, fa='x')
            
            cmds.parent(proxyJoint.prxyJnt_Grp, createElbow.elbow_Grp)
            
            # hide arm curve
            ## create seperate curves between each joint
            cmds.setAttr( "TEMP_arm_{}_curve.v".format(side), 0 )
            if elbow > 0:
                createCurve( "TEMP_elbow_{}_{}_curve".format(side, elbow+1), "TEMP_elbow_{}_{}_jnt".format(elbow, side), "TEMP_elbow_{}_{}_jnt".format(elbow+1, side) )
                cmds.parent(createCurve.curvee, createCurve.curveLocator_start, createCurve.curveLocator_end, createElbow.elbow_Grp)
        
        createCurve( "TEMP_elbow_{}_{}_curve".format(side, 1), "TEMP_shoulder_{}_jnt".format(side), "TEMP_elbow_{}_{}_jnt".format(1, side) )
        cmds.parent(createCurve.curvee, createCurve.curveLocator_start, createCurve.curveLocator_end, createElbow.elbow_Grp)
        createCurve( "TEMP_elbow_{}_{}_curve".format(side, numElbows+1), "TEMP_elbow_{}_{}_jnt".format(numElbows, side), "TEMP_wrist_{}_jnt".format(side) )
        cmds.parent(createCurve.curvee, createCurve.curveLocator_start, createCurve.curveLocator_end, createElbow.elbow_Grp)
            
    cmds.select(cl=True)


def createThumb(side):
    hasThumbs = cmds.checkBox(thumbCheckBox, q=True, v=True)
    
    if hasThumbs:
        for thumb_knuckle in range(4):
            thumb_knuckle = thumb_knuckle + 1
            name = "TEMP_thumb_{}_{}_jnt".format(thumb_knuckle, side)
            group_name = "TEMP_thumb_{}_{}_grp".format(thumb_knuckle, side)
            
            proxyJoint(group_name,name,0.1)
            cmds.select(proxyJoint.prxyJnt_Grp)
            
            cmds.xform(t=(0,0,thumb_knuckle*.4))
            
            if thumb_knuckle > 1:
                cmds.parent(proxyJoint.prxyJnt_Grp, "TEMP_thumb_{}_{}_jnt".format(thumb_knuckle-1, side))
                createCurve("TEMP_thumb_{}_{}_to_{}".format(side, thumb_knuckle-1, thumb_knuckle), "TEMP_thumb_{}_{}_jnt".format(thumb_knuckle-1, side), "TEMP_thumb_{}_{}_jnt".format(thumb_knuckle, side))
        
        cmds.delete( cmds.parentConstraint("TEMP_wrist_{}_jnt".format(side), "TEMP_thumb_{}_{}_grp".format(1, side)) )
        cmds.parent("TEMP_thumb_{}_{}_grp".format(1, side), "TEMP_wrist_{}_jnt".format(side))
        
        if side == "l":
            cmds.xform(t=(0.45,0,.45), os=True)
            cmds.xform(ro=(0,45,0))
        if side == "r":
            cmds.xform(t=(-.45,0,.45), os=True)
            cmds.xform(ro=(0,-45,0))
            
        createCurve("TEMP_thumb_{}_curve".format(side), "TEMP_thumb_{}_{}_jnt".format(1, side), "TEMP_wrist_{}_jnt".format(side))
    cmds.select(cl=True)
    
            
def createFinger(side):
    numFingers = cmds.intField(fingerIntField, q=True, v=True)
    finger_pos_Offset = .45
    
    for finger in range(numFingers):
        finger = finger + 1
        for finger_knuckle in range(4):
            finger_knuckle = finger_knuckle + 1
            name = "TEMP_finger{}_{}_{}_jnt".format(finger, finger_knuckle, side)
            group_name = "TEMP_finger{}_{}_{}_grp".format(finger, finger_knuckle, side)

            proxyJoint(group_name,name,0.1)
            cmds.select(proxyJoint.prxyJnt_Grp)
            if side == "l":
                offset = 1.25
                cmds.xform(t=(finger_knuckle*.4,0,0))
            if side == "r":
                offset = -1.25
                cmds.xform(t=(-(finger_knuckle*.4),0,0))
            
            if finger_knuckle > 1:
                cmds.parent(proxyJoint.prxyJnt_Grp, "TEMP_finger{}_{}_{}_jnt".format(finger, finger_knuckle-1, side))
                createCurve("TEMP_finger{}_{}_{}_to_{}".format(finger, side, finger_knuckle-1, finger_knuckle), "TEMP_finger{}_{}_{}_jnt".format(finger, finger_knuckle-1, side), "TEMP_finger{}_{}_{}_jnt".format(finger, finger_knuckle, side))

        cmds.delete( cmds.parentConstraint("TEMP_wrist_{}_jnt".format(side), "TEMP_finger{}_{}_{}_grp".format(finger, 1, side)) )
        cmds.parent("TEMP_finger{}_{}_{}_grp".format(finger, 1, side), "TEMP_wrist_{}_jnt".format(side))
        cmds.xform(t=(offset,0,0+finger_pos_Offset), os=True)
        
        
        createCurve("TEMP_finger{}_{}_curve".format(finger, side), "TEMP_finger{}_{}_{}_jnt".format(finger, 1, side), "TEMP_wrist_{}_jnt".format(side))
        finger_pos_Offset = finger_pos_Offset-.26
        
    cmds.select(cl=True)


def createFoot(side):

    leg_names = ["foot", "ball", "toe"]
    if side == "l":
        leg_pos = [(1.1,0.75,0),(1.1,0,1),(1.1,0,1.5)]
    if side == "r":
        leg_pos = [(-1.1,0.75,0),(-1.1,0,1),(-1.1,0,1.5)]
    
    for leg_part in range(0,len(leg_names)):
        name = "TEMP_{}_{}_jnt".format(leg_names[leg_part], side)
        group_name = "TEMP_{}_{}_grp".format(leg_names[leg_part], side)
        position = leg_pos[leg_part]

        proxyJoint(group_name,name,0.25)
        cmds.select(proxyJoint.prxyJnt_Grp)
        cmds.xform(t=position)
        
        if leg_part > 0:
            cmds.parent(proxyJoint.prxyJnt_Grp, "TEMP_{}_{}_jnt".format(leg_names[leg_part-1], side))
            createCurve("TEMP_foot_{}_{}_to_{}".format(side, leg_names[leg_part-1], leg_names[leg_part]), "TEMP_{}_{}_jnt".format(leg_names[leg_part-1], side), "TEMP_{}_{}_jnt".format(leg_names[leg_part], side))
    #createCurve("leg_{}_{}2hip".format(side, "spine"), "spine_base_temp", "hip_{}_temp".format(side))

def createKnee(side):
    
    # query number of desired neck joints
    numKnees = cmds.intField(kneeIntField, q=True, v=True)
    # create group
    createKnee.knee_Grp = cmds.group(em=True, n="TEMP_knees_{}_grp".format(side))
    cmds.parent(createKnee.knee_Grp, createCore.rig_name)
    # create and place joints at intervals
    if not numKnees == 0:
        jntInterval = float(1.0/(numKnees+1))
        
        for knee in range(numKnees):
            proxyJoint("TEMP_knee_{}_{}_grp".format(knee+1, side), "TEMP_knee_{}_{}_jnt".format(knee+1, side), 0.2)
            
            cmds.select(proxyJoint.prxyJnt_Grp, "TEMP_leg_{}_curve".format(side), r=True)
            cmds.pathAnimation(su=jntInterval*(knee+1), stu=knee+1)
            
            cmds.parent(proxyJoint.prxyJnt_Grp, createKnee.knee_Grp)
            
            # hide leg curve
            ## create seperate curves between each joint
            cmds.setAttr( "TEMP_leg_{}_curve.v".format(side), 0 )
            if knee > 0:
                createCurve( "TEMP_knee_{}_{}_curve".format(side, knee+1), "TEMP_knee_{}_{}_jnt".format(knee, side), "TEMP_knee_{}_{}_jnt".format(knee+1, side) )
                cmds.parent(createCurve.curvee, createCurve.curveLocator_start, createCurve.curveLocator_end, createKnee.knee_Grp)
        
        createCurve( "TEMP_knee_{}_{}_curve".format(side, 1), "TEMP_hip_{}_jnt".format(side), "TEMP_knee_{}_{}_jnt".format(1, side) )
        cmds.parent(createCurve.curvee, createCurve.curveLocator_start, createCurve.curveLocator_end, createKnee.knee_Grp)
        createCurve( "TEMP_knee_{}_{}_curve".format(side, numKnees+1), "TEMP_knee_{}_{}_jnt".format(numKnees, side), "TEMP_foot_{}_jnt".format(side) )
        cmds.parent(createCurve.curvee, createCurve.curveLocator_start, createCurve.curveLocator_end, createKnee.knee_Grp)
        
    cmds.select(cl=True)
    
def createProxyControls():
    
    ctrl_suff = cmds.textField(ctrl_suffix, q=True, pht=True)
    if cmds.textField(ctrl_suffix, q=True, tx=True):
        ctrl_suff = cmds.textField(ctrl_suffix, q=True, tx=True)
    
    ctrlGrp_suff = cmds.textField(ctrlGrp_suffix, q=True, pht=True)
    if cmds.textField(ctrlGrp_suffix, q=True, tx=True):
        ctrlGrp_suff = cmds.textField(ctrlGrp_suffix, q=True, tx=True)
    
    n_left = cmds.textField(left_naming, q=True, pht=True)
    if cmds.textField(left_naming, q=True, tx=True):
        n_left = cmds.textField(left_naming, q=True, tx=True)
        
    n_right = cmds.textField(right_naming, q=True, pht=True)
    if cmds.textField(right_naming, q=True, tx=True):
        n_right = cmds.textField(right_naming, q=True, tx=True)
    
    
    # create main control to position and scale proxy
    createControl( "{}_main".format(createCore.rig_name), 4, (0,1,0), 17)
    createProxyControls.main_control = createControl.newCtrl
    
    # create extra shape for main control
    createControl( "{}_main".format(createCore.rig_name), 4.2, (0,1,0), 17)
    ctrlShape = cmds.listRelatives(createControl.newCtrl, c=True, s=True)[0]
    cmds.select(ctrlShape, createProxyControls.main_control)
    cmds.parent(r=True, s=True)
    cmds.delete(createControl.newCtrl)
    
    main_extra_shape = cmds.curve(d=1, p=[(0,0,5),(2,0,2),(0,0,3),(-2,0,2),(0,0,5)], k=[0,1,2,3,4])
    ctrlShape = cmds.listRelatives(main_extra_shape, c=True, s=True)[0]

    cmds.setAttr("{}.overrideEnabled".format(ctrlShape), 1) # enable color override
    cmds.setAttr("{}.overrideColor".format(ctrlShape), 17) # change color of circle

    cmds.CenterPivot()
    cmds.move(0,0,6, rpr=True)

    cmds.makeIdentity(a=True, t=1, r=1, s=1)

    cmds.select(ctrlShape, createProxyControls.main_control)
    cmds.parent(r=True, s=True)
    cmds.delete(main_extra_shape)
    
    createProxyControls.main_ctrl_group = cmds.group(createProxyControls.main_control, n="{}_main{}".format(createCore.rig_name, ctrlGrp_suff))
    cmds.move( 0,0,0, "{}.scalePivot".format(createProxyControls.main_ctrl_group), "{}.rotatePivot".format(createProxyControls.main_ctrl_group))
    
    ### create feet controls
    f_naming = [ n_left, n_right ]
    for foot_side in range(2):
        if foot_side == 0:
            color = 14
        else:
            color = 13
        createControl( "foot{}".format(f_naming[foot_side]), 2, (0,1,0), color)
        
        cmds.scale(1, 1, 0, "{}.cv[0:2]".format(createControl.newCtrl),  r=True, p=(0, 0, -0.946))
        cmds.scale(0, 1, 1, "{}.cv[0]".format(createControl.newCtrl), "{}.cv[6:7]".format(createControl.newCtrl), r=True, p=(0.946, 0, -0.081))
        cmds.scale(1, 1, 0, "{}.cv[4:6]".format(createControl.newCtrl), r=True, p=(0.081, 0, 0.946))
        cmds.scale(0, 1, 1, "{}.cv[2:4]".format(createControl.newCtrl), r=True, p=(-0.946, 0, -0.003))
        
        cmds.scale(.9, 1, 2, createControl.newCtrl)
        cmds.makeIdentity(createControl.newCtrl, a=True, s=True)
        cmds.delete(createControl.newCtrl, ch=True)
        
        newCtrlGrp = cmds.group(createControl.newCtrl, n="foot{}{}".format(f_naming[foot_side], ctrlGrp_suff))
        if foot_side == 0:
            cmds.matchTransform(newCtrlGrp, "TEMP_ball_l_jnt", pos=True, rot=True)
            foot_pos = cmds.xform("TEMP_foot_l_jnt", q=True, t=True, ws=True)
            cmds.move(foot_pos[0], 0, foot_pos[2], "foot{}{}.scalePivot".format(f_naming[foot_side], ctrl_suff), "foot{}{}.rotatePivot".format(f_naming[foot_side], ctrl_suff), a=True)
            
            cmds.parentConstraint(createControl.newCtrl, "TEMP_foot_l_grp", mo=True)
            cmds.pointConstraint(createControl.newCtrl, "TEMP_hip_l_grp", skip="y", mo=True)
            
        if foot_side == 1:
            cmds.matchTransform(newCtrlGrp, "TEMP_ball_r_jnt", pos=True, rot=True)
            foot_pos = cmds.xform("TEMP_foot_r_jnt", q=True, t=True, ws=True)
            cmds.move(foot_pos[0], 0, foot_pos[2], "foot{}{}.scalePivot".format(f_naming[foot_side], ctrl_suff), "foot{}{}.rotatePivot".format(f_naming[foot_side], ctrl_suff), a=True)

            cmds.parentConstraint(createControl.newCtrl, "TEMP_foot_r_grp", mo=True)
            cmds.pointConstraint(createControl.newCtrl, "TEMP_hip_r_grp", skip="y", mo=True)
            
        cmds.parent(newCtrlGrp, createProxyControls.main_control)


def mirrorProxyPose(mirrorDir):
    n_left = cmds.textField(left_naming, q=True, pht=True)
    if cmds.textField(left_naming, q=True, tx=True):
        n_left = cmds.textField(left_naming, q=True, tx=True)
        
    n_right = cmds.textField(right_naming, q=True, pht=True)
    if cmds.textField(right_naming, q=True, tx=True):
        n_right = cmds.textField(right_naming, q=True, tx=True)
    
    leftJoints = cmds.ls("TEMP_*_l_*jnt")    
    rightJoints = cmds.ls("TEMP_*_r_*jnt")
    
    leftControls = cmds.ls("*{}_ctrl".format(n_left))
    rightControls = cmds.ls("*{}_ctrl".format(n_right))
        
    if mirrorDir == "L2R":
        for ctrl in range(len(leftControls)):
            pos = cmds.xform(leftControls[ctrl], q=True, t=True)
            rot = cmds.xform(leftControls[ctrl], q=True, ro=True)
            
            cmds.xform(rightControls[ctrl], t=( -(pos[0]), pos[1], pos[2] ), ro=( rot[0], -(rot[1]), -(rot[2]) ))
            
        for jnt in range(len(leftJoints)):
            
            pos = cmds.xform(leftJoints[jnt], q=True, t=True)
            rot = cmds.xform(leftJoints[jnt], q=True, ro=True)
            
            cmds.xform(rightJoints[jnt], t=( -(pos[0]), pos[1], pos[2] ), ro=( rot[0], -(rot[1]), -(rot[2]) ))
        
        
    if mirrorDir == "R2L":
        for ctrl in range(len(leftControls)):
            pos = cmds.xform(rightControls[ctrl], q=True, t=True)
            rot = cmds.xform(rightControls[ctrl], q=True, ro=True)
            
            cmds.xform(leftControls[ctrl], t=( -(pos[0]), pos[1], pos[2] ), ro=( rot[0], -(rot[1]), -(rot[2]) ))
            
        for jnt in range(len(rightJoints)):
        
            pos = cmds.xform(rightJoints[jnt], q=True, t=True)
            rot = cmds.xform(rightJoints[jnt], q=True, ro=True)
            
            cmds.xform(leftJoints[jnt], t=( -(pos[0]), pos[1], pos[2] ), ro=( rot[0], -(rot[1]), -(rot[2]) ))
    

def zeroProxy():
    sel = cmds.ls(sl=True)
    if sel:
        numOfChild = cmds.listRelatives(sel, ad=True, typ="transform")
        
        if numOfChild:
            numOfChild.append(cmds.ls(sl=True)[0])
        
            for i in numOfChild:
                if "_grp" in i:
                    numOfChild.remove(i)
        
        cmds.xform(numOfChild, t=(0,0,0), ro=(0,0,0), s=(1,1,1))
        return

    numOfJoints = cmds.ls("TEMP_*_jnt")
    numOfCtrls = cmds.ls("*_ctrl".format())
    
    cmds.xform(numOfCtrls, t=(0,0,0), ro=(0,0,0), s=(1,1,1))
    cmds.xform(numOfJoints, t=(0,0,0), ro=(0,0,0), s=(1,1,1))

#############################
##### Joint Creation
#############################

def createSkeletonCore():
    
    ctrlGrp_suff = cmds.textField(ctrlGrp_suffix, q=True, pht=True)
    if cmds.textField(ctrlGrp_suffix, q=True, tx=True):
        ctrlGrp_suff = cmds.textField(ctrlGrp_suffix, q=True, tx=True)
        
    ctrl_suff = cmds.textField(ctrl_suffix, q=True, pht=True)
    if cmds.textField(ctrl_suffix, q=True, tx=True):
        ctrl_suff = cmds.textField(ctrl_suffix, q=True, tx=True)

    jnt_suff = cmds.textField(jnt_suffix, q=True, pht=True)
    if cmds.textField(jnt_suffix, q=True, tx=True):
        jnt_suff = cmds.textField(jnt_suffix, q=True, tx=True)
    
    n_left = cmds.textField(left_naming, q=True, pht=True)
    if cmds.textField(left_naming, q=True, tx=True):
        n_left = cmds.textField(left_naming, q=True, tx=True)
        
    n_right = cmds.textField(right_naming, q=True, pht=True)
    if cmds.textField(right_naming, q=True, tx=True):
        n_right = cmds.textField(right_naming, q=True, tx=True)
    
    cmds.rename( "{}_main_ctrlGrp".format(createCore.rig_name), "{}_main{}".format(createCore.rig_name, ctrlGrp_suff) )
    cmds.rename( "{}_main_ctrl".format(createCore.rig_name), "{}_main{}".format(createCore.rig_name, ctrl_suff) )
    
    foot_ctrl_rename = cmds.ls("foot*", typ="transform")
    side = n_left
    for foot in range(len(foot_ctrl_rename)/2):
        if foot == 1:
            side = n_right
            foot = 2
            
        cmds.rename( foot_ctrl_rename[foot], "foot{}_IK{}".format(side, ctrl_suff) )
        cmds.rename( foot_ctrl_rename[foot+1], "foot{}_IK{}".format(side, ctrlGrp_suff) )
    
    createSkeletonCore.end_Joints = []
    createSkeletonCore.mirror_Joints = []
    
    # spine joints
    cmds.select(cl=True)
    spine_joints = cmds.ls("TEMP_*spine*_jnt")
    pos = cmds.xform("TEMP_spineBase_jnt", q=True, t=True, ws=True)
    cmds.joint(n="spine_base{}".format(jnt_suff), p=pos, rad=.3)
    
    spineNum = 1
    for sJnt in spine_joints[2:]:
        
        pos = cmds.xform(sJnt, q=True, t=True, ws=True)
        cmds.joint(n="spine_{}{}".format(spineNum, jnt_suff), p=pos, rad=.3)
        spineNum = spineNum + 1
    
    pos = cmds.xform("TEMP_spineTop_jnt", q=True, t=True, ws=True)
    cmds.joint(n="spine_top{}".format(jnt_suff), p=pos, rad=.3)
    
    # neck joints
    neck_joints = cmds.ls("TEMP_*neck*_jnt")
    pos = cmds.xform("TEMP_neckBase_jnt", q=True, t=True, ws=True)
    cmds.joint(n="neck_1{}".format(jnt_suff), p=pos, rad=.3)
    
    neckNum = 2
    for nJnt in neck_joints[1:]:
        
        pos = cmds.xform(nJnt, q=True, t=True, ws=True)
        cmds.joint(n="neck_{}{}".format(neckNum, jnt_suff), p=pos, rad=.3)
        neckNum = neckNum + 1

    pos = cmds.xform("TEMP_headBase_jnt", q=True, t=True, ws=True)
    cmds.joint(n="head_base{}".format(jnt_suff), p=pos, rad=.3)
        
    # head joints
    pos = cmds.xform("TEMP_headTop_jnt", q=True, t=True, ws=True)
    createSkeletonCore.end_Joints.append(cmds.joint(n="head_top{}".format(jnt_suff), p=pos, rad=.3))
    
    cmds.select("head_base{}".format(jnt_suff))
    jaw_joints = cmds.ls("TEMP_*jaw*_jnt")
    jaw_joints.reverse()
    for jJnt in range(len(jaw_joints)):
        pos = cmds.xform(jaw_joints[jJnt], q=True, t=True, ws=True)
        if jJnt == 0:
            cmds.joint(n="jaw{}".format(jnt_suff), p=pos, rad=.3)
        else:
            createSkeletonCore.end_Joints.append(cmds.joint(n="jaw_end{}".format(jnt_suff), p=pos, rad=.3))
    
    cmds.select("head_base{}".format(jnt_suff))
    pos = cmds.xform("TEMP_eye_l_jnt", q=True, t=True, ws=True)
    createSkeletonCore.end_Joints.append(cmds.joint(n="eye{}{}".format(n_left, jnt_suff), p=pos, rad=.3))
    
    cmds.select("head_base{}".format(jnt_suff))
    pos = cmds.xform("TEMP_eye_r_jnt", q=True, t=True, ws=True)
    createSkeletonCore.end_Joints.append(cmds.joint(n="eye{}{}".format(n_right, jnt_suff), p=pos, rad=.3))
    
    # create locator for inbetween eyes
    cmds.parentConstraint( "eye{}{}".format(n_left, jnt_suff), "eye{}{}".format(n_right, jnt_suff), cmds.spaceLocator(n="eye_inbewteen") )
    cmds.setAttr("eye_inbewteen.v", 0)
    
    # orient joints 
    cmds.joint("spine_base{}".format(jnt_suff), e=True, oj="xyz", sao="xup", ch=True, zso=True)
    
    createSkeletonArm(jnt_suff, '_l', n_left)
    createSkeletonLeg(jnt_suff, '_l', n_left)
    
    for end in createSkeletonCore.end_Joints:
        cmds.setAttr("{}.jointOrientZ".format(end), 0)
        cmds.setAttr("{}.jointOrientY".format(end), 0)
        cmds.setAttr("{}.jointOrientX".format(end), 0)
    
    for mirror in createSkeletonCore.mirror_Joints:
        cmds.select(mirror, r=True)
        cmds.mirrorJoint(myz=True, mb=True, sr=("{}".format(n_left),"{}".format(n_right)))

    cmds.setAttr("{}.visibility".format(createCore.rig_name), 0)
    cmds.setAttr("proxy_joint_grp.visibility".format(createCore.rig_name), 0)
    cmds.select(cl=True)
    
    # create ik handles for arms and legs
    for body_part in ( "arm", "leg" ):
        if body_part == "arm":
            ikJoints = [ "shoulder", "wrist" ]
        if body_part == "leg":
            ikJoints = [ "hip", "ankle" ]
            
        for side in ( n_left, n_right ):
            base = "{}{}_IK{}".format(ikJoints[0], side, jnt_suff)
            end = "{}{}_IK{}".format(ikJoints[1],  side, jnt_suff)
            createIK( base, end, body_part, side )
    
    cmds.select(cl=True)
    

def createSkeletonArm(jnt_suff, side, side_naming):
    cmds.select("spine_top{}".format(jnt_suff))
    
    # clavicle
    pos = cmds.xform("TEMP_clavicle{}_jnt".format(side), q=True, t=True, ws=True)
    createSkeletonArm.clavicle = cmds.joint(n="clavicle{}{}".format(side_naming, jnt_suff), p=pos, rad=.3)
    
    createSkeletonCore.mirror_Joints.append(createSkeletonArm.clavicle)
    
    IK_FK = ['_IK','_FK','']
    for i in range(3):
        
        cmds.select(createSkeletonArm.clavicle)
        # shoulder
        pos = cmds.xform("TEMP_shoulder{}_jnt".format(side), q=True, t=True, ws=True)
        shoulder = cmds.joint(n="shoulder{}{}{}".format(side_naming, IK_FK[i], jnt_suff), p=pos, rad=.3)
        
        # elbows
        elbow_joints = cmds.ls("TEMP_*elbow*{}_jnt".format(side))
        elbowNum = 1
        for eJnt in elbow_joints:
            if len(elbow_joints) > 1:
                pos = cmds.xform(eJnt, q=True, t=True, ws=True)
                elbow = cmds.joint(n="elbow{}{}{}{}".format(side_naming, elbowNum, IK_FK[i], jnt_suff), p=pos, rad=.3)
                elbowNum = elbowNum + 1
            else:
                pos = cmds.xform(eJnt, q=True, t=True, ws=True)
                elbow = cmds.joint(n="elbow{}{}{}".format(side_naming, IK_FK[i], jnt_suff), p=pos, rad=.3 )
        
        # wrist
        pos = cmds.xform("TEMP_wrist{}_jnt".format(side), q=True, t=True, ws=True)
        wrist = cmds.joint(n="wrist{}{}{}".format(side_naming, IK_FK[i], jnt_suff), p=pos, rad=.3)

        cmds.joint(shoulder, e=True, oj="xyz", sao="yup", ch=True, zso=True )
        
        cmds.setAttr("{}.jointOrientX".format(wrist), 0)
        cmds.setAttr("{}.jointOrientX".format(wrist), 0)
        cmds.setAttr("{}.jointOrientZ".format(wrist), 0)
        
        if i < 2:
            cmds.setAttr( "{}.v".format(shoulder), 0 )
        
    cmds.setAttr("elbow{}_IK{}.preferredAngleY".format( side_naming, jnt_suff ), -90)
    
    last_elbow = cmds.listRelatives(wrist, p=True)
    cmds.select(last_elbow)
    forearm = cmds.joint(n="forearm{}{}".format(side_naming, jnt_suff), rad=.15)
    
    cmds.delete( cmds.parentConstraint(last_elbow, wrist, forearm, mo=False) )
    # create node connection that has forearm follow wrist x rotation
    ## rotation should be halved
    forearm_math = cmds.shadingNode( "multiplyDivide", au=True)
    cmds.setAttr( "{}.input2X".format(forearm_math), 0.5 )
    
    cmds.connectAttr( "{}.rotate.rotateX".format(wrist), "{}.input1.input1X".format(forearm_math) )
    cmds.connectAttr( "{}.output.outputX".format(forearm_math), "{}.rotate.rotateX".format(forearm) )
    
    
    # thumb
    cmds.select("wrist{}{}".format(side_naming, jnt_suff))
    thumb = cmds.checkBox(thumbCheckBox, q=True, v=True)
    
    if thumb:
        sel = cmds.ls("TEMP_thumb_1{}_jnt".format(side))
        numOfThumbKnucles = cmds.listRelatives(sel, ad=True, typ="transform")
        
        for i in numOfThumbKnucles:
                if "_grp" in i:
                    numOfThumbKnucles.remove(i)
        
        first = True  
        for thumb_knuckle in range(len(numOfThumbKnucles)+1):
            pos = cmds.xform("TEMP_thumb_{}{}_jnt".format(thumb_knuckle+1, side), q=True, t=True, ws=True)
            thumbKnuckle = cmds.joint(n="thumb_{}{}{}".format(thumb_knuckle+1, side_naming, jnt_suff), p=pos, rad=.22)
            if first:
                firstThumbJoint = thumbKnuckle
                
                first = False
                
            if thumb_knuckle+1 == len(numOfThumbKnucles)+1:
                createSkeletonCore.end_Joints.append(thumbKnuckle)
                    
        cmds.joint(firstThumbJoint, e=True, oj="xyz", sao="zup", ch=True, zso=True)
    
    # fingers
    cmds.select(cl=True)
    numFingers = cmds.intField(fingerIntField, q=True, v=True)
    
    finger_names = ["index", "middle", "ring", "pinky"]
    finger_number = 1
    for finger in range(numFingers):
        cmds.select("wrist{}{}".format(side_naming, jnt_suff))
        
        if finger > 3:
            finger_names = "finger_{}".format(finger_number)
            finger = 0
        
        sel = cmds.ls("TEMP_finger{}_1{}_jnt".format(finger+1, side))
        numOfKnucles = cmds.listRelatives(sel, ad=True, typ="transform")
        for i in numOfKnucles:
                if "_grp" in i:
                    numOfKnucles.remove(i)
        
        first = True    
        for finger_knuckle in range(len(numOfKnucles)+1):
            pos = cmds.xform("TEMP_finger{}_{}{}_jnt".format(finger+1, finger_knuckle+1, side), q=True, t=True, ws=True)
            fingerKnuckle = cmds.joint(n="{}_{}{}{}".format(str(finger_names[finger]), finger_knuckle+1, side_naming, jnt_suff), p=pos, rad=.22)
            if first:
                firstFingerJoint = fingerKnuckle
                
                first = False
            
            if finger_knuckle+1 == len(numOfKnucles)+1:
                createSkeletonCore.end_Joints.append(fingerKnuckle)
            
        finger_number = finger_number + 1
        cmds.joint(firstFingerJoint, e=True, oj="xyz", sao="zup", ch=True, zso=True)
    
        
def createSkeletonLeg(jnt_suff, side, side_naming):
    cmds.select("spine_base{}".format(jnt_suff), r=True)
    
    IK_FK = ['_IK','_FK', '']
    for i in range(3):
        
        cmds.select("spine_base{}".format(jnt_suff), r=True)
        # hip
        pos = cmds.xform("TEMP_hip{}_jnt".format(side), q=True, t=True, ws=True)
        createSkeletonLeg.hip = cmds.joint(n="hip{}{}{}".format(side_naming, IK_FK[i], jnt_suff), p=pos, rad=.3)
        
        createSkeletonCore.mirror_Joints.append(createSkeletonLeg.hip)
        
        # knees
        knee_joints = cmds.ls("TEMP_*knee*{}_jnt".format(side))
        kneeNum = 1
        for kJnt in knee_joints:
            if len(knee_joints) > 1:
                pos = cmds.xform(kJnt, q=True, t=True, ws=True)
                knee = cmds.joint(n="knee{}{}{}{}".format(side_naming, kneeNum, IK_FK[i], jnt_suff), p=pos, rad=.3)
                kneeNum = kneeNum + 1
            else:
                pos = cmds.xform(kJnt, q=True, t=True, ws=True)
                knee = cmds.joint(n="knee{}{}{}".format(side_naming, IK_FK[i], jnt_suff), p=pos, rad=.3)
        
        # ankle
        pos = cmds.xform("TEMP_foot{}_jnt".format(side), q=True, t=True, ws=True)
        cmds.joint(n="ankle{}{}{}".format(side_naming, IK_FK[i], jnt_suff), p=pos, rad=.3)
        
        # ball
        pos = cmds.xform("TEMP_ball{}_jnt".format(side), q=True, t=True, ws=True)
        cmds.joint(n="ball{}{}{}".format(side_naming, IK_FK[i], jnt_suff), p=pos, rad=.3)
        
        # toe
        pos = cmds.xform("TEMP_toe{}_jnt".format(side), q=True, t=True, ws=True)
        createSkeletonCore.end_Joints.append(cmds.joint(n="toe{}{}{}".format(side_naming, IK_FK[i], jnt_suff), p=pos, rad=.3))
    
        cmds.joint(createSkeletonLeg.hip, e=True, oj="xyz", sao="xup", ch=True, zso=True, spa=True)
        
        if i < 2:
            cmds.setAttr( "{}.v".format(createSkeletonLeg.hip), 0 )
    
    cmds.setAttr("knee{}_IK{}.preferredAngleY".format( side_naming, jnt_suff ), 90)

def createControl( name, radius, normal, color, sweep=360, ctrlType="circle" ):
    
    ctrl_suff = cmds.textField(ctrl_suffix, q=True, pht=True)
    if cmds.textField(ctrl_suffix, q=True, tx=True):
        ctrl_suff = cmds.textField(ctrl_suffix, q=True, tx=True)
    
    if ctrlType == "circle":
        # create circle with specifications
        createControl.newCtrl = cmds.circle( n="{}{}".format(name, ctrl_suff), r=radius,  nr=normal, sw=sweep )[0]
        
        ctrlShape = cmds.listRelatives(createControl.newCtrl, c=True, s=True)[0]
        
        cmds.setAttr("{}.overrideEnabled".format(ctrlShape), 1) # enable color override
        cmds.setAttr("{}.overrideColor".format(ctrlShape), color) # change color of circle
    
    if ctrlType == "key":
        radius = .1
        normal = (1,0,0)
        # create key shaped control --O
        createControl.newCtrl = cmds.circle( n="{}{}".format(name, ctrl_suff), r=radius,  nr=normal, sw=sweep )[0]
        cmds.move( 0, 0.5, 0 )
        # change colour
        ctrlShape = cmds.listRelatives(createControl.newCtrl, c=True, s=True)[0]
        cmds.setAttr("{}.overrideEnabled".format(ctrlShape), 1) # enable color override
        cmds.setAttr("{}.overrideColor".format(ctrlShape), color) # change color of circle
        
        cmds.makeIdentity(a=True, t=True, r=True, s=True)
        cmds.move(0,0,0, "{}.scalePivot".format(createControl.newCtrl), "{}.rotatePivot".format(createControl.newCtrl), rpr=True)
        ###
        # create handle
        handle = cmds.curve(d=1, p=[(0,-.05,0),(0,.4,0)], k=[0,1])
        # change colour and parent shape node to circle
        ctrlShape = cmds.listRelatives(handle, c=True, s=True)[0]
        cmds.setAttr("{}.overrideEnabled".format(ctrlShape), 1) # enable color override
        cmds.setAttr("{}.overrideColor".format(ctrlShape), color) # change color of circle
        
        cmds.makeIdentity(a=True, t=True, r=True, s=True)
        cmds.move(0,0,0, "{}.scalePivot".format(handle), "{}.rotatePivot".format(handle), rpr=True)
        
        cmds.parent( ctrlShape, createControl.newCtrl, s=True, r=True)
        cmds.delete( handle )
    
    if ctrlType == "cone":
        # create base
        createControl.cone_control = cmds.curve( d=1, p=[( -0.20, 0, 0.45),( 0.20, 0, 0.45),( 0.45, 0, 0.20),
                            ( 0.45, 0, -0.20),( 0.20, 0, -0.45),( -0.20, 0, -0.45),
                            ( -0.45, 0, -0.20),( -0.45, 0, 0.20),( -0.20, 0, 0.45)], 
                    k=[0,1,2,3,4,5,6,7,8], n="{}{}".format(name, ctrl_suff))
        
        ctrlShape = cmds.listRelatives(createControl.cone_control, c=True, s=True)[0]
        cmds.setAttr("{}.overrideEnabled".format(ctrlShape), 1) # enable color override
        cmds.setAttr("{}.overrideColor".format(ctrlShape), color) # change color of circle
        
        curve_transform = []
        curve_shape_list = []
        for ep in range(8):
            ep_pos = cmds.xform("{}.ep[{}]".format(createControl.cone_control, ep), q=True, t=True )
            
            curve_line = cmds.curve( d=1, p=[( 0,1,0 ), ( ep_pos[0],ep_pos[1],ep_pos[2] )], k=[0,1] )
            curve_transform.append(curve_line)
            
            curveShape = cmds.listRelatives(curve_line, c=True, s=True)[0]
            curve_shape_list.append(curveShape)
            
            cmds.setAttr("{}.overrideEnabled".format(curveShape), 1) # enable color override
            cmds.setAttr("{}.overrideColor".format(curveShape), color) # change color of circle
        
        for line in curve_shape_list:
            cmds.parent( line, createControl.cone_control, s=True, r=True)
        cmds.delete(curve_transform)
        
        
def createIK( base, end, body_part, side ):
    
    ctrl_suff = cmds.textField(ctrl_suffix, q=True, pht=True)
    if cmds.textField(ctrl_suffix, q=True, tx=True):
        ctrl_suff = cmds.textField(ctrl_suffix, q=True, tx=True)
    
    # create ikHandle based on either arm or leg and which side it is
    ## select the base joint followed by the end joint to create the handle
        ## for legs this will need a second step to create the single chain iks
    ### for now the pole vectors for the arms will be pointing on -Z
    ### and the pole vectors for the legs will be point on Z
    
    new_ik = cmds.ikHandle( cmds.select(base, end), n="{}{}_ikHandle".format(body_part, side), solver="ikRPsolver" )[0]
    
    cmds.setAttr("{}.v".format(new_ik), 0)
    
    if "leg" in body_part:
        #cmds.setAttr("{}.poleVectorZ".format(new_ik), 2)
        
        ### creating extra plane solvers for foot ik
        ankle_joint = cmds.listRelatives( end, c=True, typ="joint" )
        ball_ik = cmds.ikHandle( cmds.select(end, ankle_joint), n="{}{}_ikHandle".format("ankle", side), solver="ikSCsolver" )[0]
        cmds.setAttr("{}.v".format(ball_ik), 0)
        
        ball_joint = cmds.listRelatives( ankle_joint, c=True, typ="joint" )
        toe_ik = cmds.ikHandle( cmds.select(ankle_joint, ball_joint), n="{}{}_ikHandle".format("ball", side), solver="ikSCsolver" )[0]
        cmds.setAttr("{}.v".format(toe_ik), 0)
        
        cmds.parent( new_ik, ball_ik, toe_ik, "foot{}_IK{}".format(side, ctrl_suff) )

def createRigControls():
    
    ctrlGrp_suff = cmds.textField(ctrlGrp_suffix, q=True, pht=True)
    if cmds.textField(ctrlGrp_suffix, q=True, tx=True):
        ctrlGrp_suff = cmds.textField(ctrlGrp_suffix, q=True, tx=True)
    
    ctrl_suff = cmds.textField(ctrl_suffix, q=True, pht=True)
    if cmds.textField(ctrl_suffix, q=True, tx=True):
        ctrl_suff = cmds.textField(ctrl_suffix, q=True, tx=True)
    
    jnt_suff = cmds.textField(jnt_suffix, q=True, pht=True)
    if cmds.textField(jnt_suffix, q=True, tx=True):
        jnt_suff = cmds.textField(jnt_suffix, q=True, tx=True)
        
    n_left = cmds.textField(left_naming, q=True, pht=True)
    if cmds.textField(left_naming, q=True, tx=True):
        n_left = cmds.textField(left_naming, q=True, tx=True)
        
    n_right = cmds.textField(right_naming, q=True, pht=True)
    if cmds.textField(right_naming, q=True, tx=True):
        n_right = cmds.textField(right_naming, q=True, tx=True)
        
    
    # create controls for entire rig
    ## split into multiple functions based on which body part is getting the controls
    ### some joints will require unique controls:
        ### Clavicle, fingers, eyes, pole vectors, hips control
    
    spineRigControls( jnt_suff, ctrl_suff, ctrlGrp_suff )
    neckRigControls( jnt_suff, ctrl_suff, ctrlGrp_suff )
    headRigControls( jnt_suff, ctrl_suff, ctrlGrp_suff, n_left, n_right )
    
    # arm controls
    createRigControls.arm_side = "left"
    armRigControls( jnt_suff, ctrl_suff, ctrlGrp_suff, n_left, 14 )
    createRigControls.arm_side = "right"
    armRigControls( jnt_suff, ctrl_suff, ctrlGrp_suff, n_right, 13 )

    # leg controls
    createRigControls.leg_side = "left"
    legRigControl( jnt_suff, ctrl_suff, ctrlGrp_suff, n_left, 14 )
    createRigControls.leg_side = "right"
    legRigControl( jnt_suff, ctrl_suff, ctrlGrp_suff, n_right, 13 )
    
    # set up IK/FK switch per limb
    IKFK_Switch( jnt_suff, ctrl_suff, ctrlGrp_suff, n_left )
    IKFK_Switch( jnt_suff, ctrl_suff, ctrlGrp_suff, n_right )
    
    # hip controls!
    ## these will influence both the hips of the IK and FK
    ### parent contraint the control groups of the FK, and directly contrain the joints of IK
    createControl( "hips", 2.33, (0,1,0), 21 )
    main_hips_control = createControl.newCtrl
    ctrlShape = cmds.listRelatives(main_hips_control, c=True, s=True)[0]
    cmds.rotate( 0, 0, -90, r=True, os=True)
    cmds.xform(ctrlShape, t=(0,-0.4,0), s=(1, 1, 0.8), r=True, os=True)
    
    main_hips_ctrlGrp = cmds.group(main_hips_control, n="hips{}".format(ctrlGrp_suff))
    
    cmds.select( "{}.cv[1]".format(main_hips_control), "{}.cv[5]".format(main_hips_control), r=True )
    cmds.move( 0, -1.66, 0, r=True, os=True)
    
    cmds.select( "{}.cv[0:2]".format(main_hips_control) )
    cmds.scale( 1, 1, 0, p=( 0, 7.250023, 1.493485), r=True)
    
    cmds.select( "{}.cv[4:6]".format(main_hips_control) )
    cmds.scale( 1, 1, 0, p=( 0, 7.250023, -1.493485), r=True)
    
    cmds.delete( cmds.parentConstraint( "spine_base{}".format(jnt_suff), main_hips_ctrlGrp) )
    #### set up contraints
    for side in (n_left, n_right):
        cmds.parentConstraint( main_hips_control, "hip{}_FK{}".format( side, ctrlGrp_suff ), mo=True )
        cmds.parentConstraint( main_hips_control, "hip{}_IK{}".format( side, jnt_suff ), mo=True )
    
    cmds.parent( main_hips_ctrlGrp, "cog{}".format(ctrl_suff) )
    
    cmds.parent( spineRigControls.main_cog_ctrlGrp, "{}_main{}".format(createCore.rig_name, ctrl_suff) )
    #cmds.delete(createCore.rig_name)
    cmds.button(resetSkeletonButton, e=True, en=True)
    cmds.button(createSkeletonButton, e=True, en=False)
    
    cmds.select(cl=True)
    
def spineRigControls( jnt_suff, ctrl_suff, ctrlGrp_suff ):
    # createCore.rig_name
    # createControl( name, radius, normal, color, sweep degree )
    
    # create COG controls
    createControl( "cog", 2.66, (0,1,0), 17 )
    main_cog_control = createControl.newCtrl
    
    spineRigControls.main_cog_ctrlGrp = cmds.group(main_cog_control, n="cog{}".format(ctrlGrp_suff))
    
    # create extra shape for COG
    createControl( "cog_extra", 2.66, (0,1,0), 17 )
    ctrlShape = cmds.listRelatives(createControl.newCtrl, c=True, s=True)[0]
    cmds.select("{}.ep[0:8]".format(ctrlShape))
    cmds.move(0,-0.2,0, r=True)
    
    cmds.select(ctrlShape, main_cog_control)
    cmds.parent(r=True, s=True)
    cmds.delete(createControl.newCtrl)
    
    cmds.delete( cmds.parentConstraint("spine_base{}".format(jnt_suff), spineRigControls.main_cog_ctrlGrp) )
    cmds.delete( cmds.orientConstraint("spine_base{}".format(jnt_suff), spineRigControls.main_cog_ctrlGrp, o=(0,180,-90)) )
    cmds.parentConstraint( main_cog_control, "spine_base{}".format(jnt_suff), mo=True )
    
    # create spine controls
    spine_joints = cmds.ls("spine_*_jnt")
    
    numbering = 1
    for spine in spine_joints:
        if not "base" in spine:
            if not "top" in spine:
                # create spine control and use variable numbering to count
                createControl( "spine_{}".format(numbering), 2, (0,1,0), 17 )
                last_spine_ctrl = createControl.newCtrl
                control_group = cmds.group(createControl.newCtrl, n="spine_{}{}".format(numbering, ctrlGrp_suff))
                cmds.delete( cmds.pointConstraint(spine, control_group) )
                cmds.delete( cmds.orientConstraint("spine_base{}".format(jnt_suff), control_group, o=(0,180,-90)) )
                
                # create hierarchy
                if numbering > 1:
                    cmds.parent( control_group, "spine_{}{}".format(numbering-1, ctrl_suff) )

                cmds.parentConstraint( createControl.newCtrl, spine, mo=True)
                numbering = numbering + 1
            
    cmds.parent( "spine_{}{}".format(1, ctrlGrp_suff), main_cog_control )

    # create control for top of spine
    ## it'll be a secondary control that shouldn't have to be animated too often
    ## so it'll look unique
    createControl( "spine_top", 1, (0,1,0), 21, 180 )
    spineRigControls.spine_top_control = createControl.newCtrl
    
    cmds.rotate(0,90,0)
    cmds.select("{}.ep[0:8]".format(createControl.newCtrl))
    cmds.move(0,0,1, r=True)
    cmds.select( spineRigControls.spine_top_control )
    cmds.makeIdentity( a=True, t=1, r=1, s=1)
    
    # create extra shape for top control
    dupe = cmds.duplicate( spineRigControls.spine_top_control )
    cmds.rotate(0,180,0)
    cmds.select( dupe )
    cmds.makeIdentity( a=True, t=1, r=1, s=1)
    
    ctrlShape = cmds.listRelatives( c=True, s=True)[0]
    cmds.select(ctrlShape, spineRigControls.spine_top_control)
    cmds.parent(r=True, s=True)
    cmds.delete(dupe)
    
    spine_top_ctrlGrp = cmds.group( spineRigControls.spine_top_control, n="spine_top{}".format(ctrlGrp_suff) )
    
    cmds.delete( cmds.pointConstraint( "spine_top{}".format(jnt_suff) , spine_top_ctrlGrp) )
    cmds.delete( cmds.orientConstraint("spine_base{}".format(jnt_suff), spine_top_ctrlGrp, o=(0,180,-90)) )
    cmds.parent( spine_top_ctrlGrp, last_spine_ctrl )
    
    cmds.parentConstraint( spineRigControls.spine_top_control, "spine_top{}".format(jnt_suff), mo=True )
    

def neckRigControls( jnt_suff, ctrl_suff, ctrlGrp_suff ):
    # createCore.rig_name
    # createControl( name, radius, normal, color, sweep degree )
    
    # create neck controls
    neck_joints = cmds.ls("neck_*_jnt")
    
    numbering = 1
    for neck in neck_joints:
        # create neck control and use variable "numbering" to count
        createControl( "neck_{}".format(numbering), .75, (0,1,0), 17 )
        neckRigControls.last_neck_ctrl = createControl.newCtrl
        control_group = cmds.group(createControl.newCtrl, n="neck_{}{}".format(numbering, ctrlGrp_suff))
        cmds.delete( cmds.pointConstraint(neck, control_group) )
        
        # create hierarchy
        if numbering > 1:
            cmds.parent( control_group, "neck_{}{}".format(numbering-1, ctrl_suff) )
        
        cmds.parentConstraint( createControl.newCtrl, neck, mo=True)
        numbering = numbering + 1
            
    cmds.parent( "neck_{}{}".format(1, ctrlGrp_suff), spineRigControls.spine_top_control )
    
def headRigControls( jnt_suff, ctrl_suff, ctrlGrp_suff, n_left, n_right ):
    # createCore.rig_name
    # createControl( name, radius, normal, color, sweep degree )
    
    # create head control
    createControl( "head", 1.25, (0,1,0), 17, 270 )
    headRigControls.head_control = createControl.newCtrl
    cmds.rotate(0,-135,0)
    cmds.makeIdentity( a=True, t=1, r=1, s=1)
    
    # create head control extra
    createControl( "head_extra", 1.25, (0,1,0), 17, 270 )
    cmds.rotate(0,-135,0)
    cmds.move(0,.09,0)
    cmds.makeIdentity( a=True, t=1, r=1, s=1)
    
    ctrlShape = cmds.listRelatives(createControl.newCtrl, c=True, s=True)[0]
    cmds.select(ctrlShape, headRigControls.head_control)
    cmds.parent(r=True, s=True)
    cmds.delete(createControl.newCtrl)

    head_ctrl_group = cmds.group(headRigControls.head_control, n="head_{}".format(ctrlGrp_suff))
    cmds.move(0,0,0, "{}.scalePivot".format(head_ctrl_group), "{}.rotatePivot".format(head_ctrl_group), rpr=True)
    
    cmds.delete( cmds.pointConstraint( "head_base{}".format(jnt_suff), head_ctrl_group) )
    cmds.parent( head_ctrl_group, neckRigControls.last_neck_ctrl )
    
    cmds.parentConstraint( headRigControls.head_control, "head_base{}".format(jnt_suff), mo=True )
    cmds.parent( "eye_inbewteen", headRigControls.head_control)
    
    # create jaw control
    createControl( "jaw", .33, (1,0,0), 17 )
    jaw_ctrl_group = cmds.group(createControl.newCtrl, n="jaw{}".format(ctrlGrp_suff))
    
    cmds.delete( cmds.parentConstraint( "jaw{}".format(jnt_suff), jaw_ctrl_group) )
    cmds.select( "{}.ep[0:8]".format(createControl.newCtrl) )
    
    jaw_end_distance = cmds.getAttr("jaw_end{}.tx".format(jnt_suff))
    
    cmds.move( (jaw_end_distance+.5), 0, 0, r=True, os=True )
    cmds.select( "{}.cv[1:5]".format(createControl.newCtrl) )
    cmds.scale(1,1,0, r=True, os=True)
    
    cmds.parent( jaw_ctrl_group, headRigControls.head_control )
    cmds.parentConstraint( createControl.newCtrl, "jaw{}".format(jnt_suff), mo=True )
    
    # create eye controls
    eye_ctrl_color = [14, 13]
    color_index = 0
    eye_loc_pos = .5
    for eye in ( n_left, n_right ):
        createControl( "eye{}".format(eye), .25, (0,0,1), eye_ctrl_color[color_index])
        eye_ctrl_group = cmds.group(createControl.newCtrl, n="eye{}{}".format(eye, ctrlGrp_suff))
        
        cmds.parent( cmds.spaceLocator(n="eye{}_loc".format(eye)), createControl.newCtrl )
        cmds.move(0,eye_loc_pos,0)
        cmds.setAttr( "eye{}_loc.v".format(eye), 0 )
        cmds.CenterPivot("eye{}_loc".format(eye))
        
        eye_loc_pos = -.5
        color_index = color_index + 1
    
        # move eye control group to associated eye
        cmds.delete( cmds.parentConstraint( "eye{}{}".format(eye, jnt_suff), eye_ctrl_group) )
        cmds.move(0,0,6.66, eye_ctrl_group, r=True)
            
    # create main eye control
    measuringTool( "eye_width_measure", "eye{}_loc".format(n_left), "eye{}_loc".format(n_right))
    eye_diameter = cmds.getAttr("{}.tx".format(measuringTool.end))
    
    radius = eye_diameter / 2
    createControl( "eye_main", radius, (0,0,1), 18)
    cmds.delete( "eye_width_measure" )
       
    #cmds.scale(1, 0, 1, "{}.cv[0:2]".format(createControl.newCtrl),  r=True, p=(0, 0.851313, 0))
    cmds.scale(0, 1, 1, "{}.cv[0]".format(createControl.newCtrl), "{}.cv[6:7]".format(createControl.newCtrl), r=True, p=(0.851313, 0, 0.0730303))
    #cmds.scale(1, 0, 1, "{}.cv[4:6]".format(createControl.newCtrl), r=True, p=(0.0730303, -0.851313, 0))
    cmds.scale(0, 1, 1, "{}.cv[2:4]".format(createControl.newCtrl), r=True, p=(-0.851313, 0, 0))

    cmds.scale(.5, 1, 1, createControl.newCtrl)
    cmds.makeIdentity(createControl.newCtrl, a=True, s=True)
    cmds.delete(createControl.newCtrl, ch=True)
    
    eye_mainctrl_group = cmds.group(createControl.newCtrl, n="eye{}".format(ctrlGrp_suff))
    cmds.delete( cmds.parentConstraint( "eye{}{}".format(n_left, ctrl_suff), "eye{}{}".format(n_right, ctrl_suff), eye_mainctrl_group ) )
    
    cmds.parent( "eye{}{}".format(n_left, ctrlGrp_suff), "eye{}{}".format(n_right, ctrlGrp_suff), createControl.newCtrl )
    cmds.parent( eye_mainctrl_group, headRigControls.head_control )
    cmds.aimConstraint( "eye_inbewteen", createControl.newCtrl, mo=True)
    
def armRigControls( jnt_suff, ctrl_suff, ctrlGrp_suff, side, color ):
    # this will need to loop twice to do both IK and FK -- haha nope
    ## the clavicle will require a unique control
    ### the fingers could use "sour key" like controls for better selection
        ### ( --O ) <--- like this
    
    # create clavicle control
    # create head control
    createControl( "clavicle{}".format(side), 1.2, (1,0,0), color, 270 )
    armRigControls.clavicle_control = createControl.newCtrl
    cmds.rotate(-135,0,0)
    cmds.makeIdentity( a=True, t=1, r=1, s=1)
    
    # create head control extra
    createControl( "clavicle{}".format(side), 1.2, (1,0,0), color, 270 )
    cmds.rotate(-135,0,0)
    cmds.move(.2,0,0)
    cmds.makeIdentity( a=True, t=1, r=1, s=1)
    
    ctrlShape = cmds.listRelatives(createControl.newCtrl, c=True, s=True)[0]
    cmds.select(ctrlShape, armRigControls.clavicle_control)
    cmds.parent(r=True, s=True)
    cmds.delete(createControl.newCtrl)

    clav_ctrl_group = cmds.group( armRigControls.clavicle_control, n="clavicle{}{}".format(side, ctrlGrp_suff) )
    cmds.move( 0,0,0, "{}.scalePivot".format(clav_ctrl_group), "{}.rotatePivot".format(clav_ctrl_group), rpr=True )
    
    if createRigControls.arm_side == "right":
        cmds.rotate(0,0,0, clav_ctrl_group)
        cmds.scale(-1,1,1, clav_ctrl_group)
        #cmds.makeIdentity(a=True, t=True, r=True, s=True)
    else:
        cmds.rotate(0,0,0, clav_ctrl_group)
    
    cmds.delete( cmds.pointConstraint( "clavicle{}{}".format( side, jnt_suff), clav_ctrl_group) )
    cmds.parent( clav_ctrl_group, "spine_top{}".format(ctrl_suff) )
    
    cmds.parentConstraint( armRigControls.clavicle_control, "clavicle{}{}".format( side, jnt_suff), mo=True )
    
    # ARM TIME!
    ## create fk controls along: Shoulder_fk, elbow(s)_fk, and wrist_fk
    
    # shoulder
    createControl( "shoulder{}_FK".format(side), 1, (1,0,0), color )
    armRigControls.shoulder_control = createControl.newCtrl
    shoulder_ctrl_group = cmds.group( n="shoulder{}_FK{}".format(side, ctrlGrp_suff) )
    
    cmds.delete( cmds.parentConstraint( "shoulder{}_FK{}".format( side, jnt_suff), shoulder_ctrl_group) )
    cmds.parent( shoulder_ctrl_group, armRigControls.clavicle_control )
    
    cmds.parentConstraint( armRigControls.shoulder_control, "shoulder{}_FK{}".format( side, jnt_suff), mo=True )
    
    # elbows
    elbow_joints = cmds.ls("elbow{}_FK{}".format(side, jnt_suff))
    elbowNum = 1
    for eJnt in elbow_joints:
        if len(elbow_joints) > 1:
            createControl( "elbow{}_{}_FK".format(side, elbowNum), .8, (1,0,0), color )
            armRigControls.elbow_control = createControl.newCtrl
            elbow_ctrl_group = cmds.group( n="elbow{}_{}_FK{}".format(side, elbowNum, ctrlGrp_suff) )
            
            cmds.delete( cmds.parentConstraint( "elbow{}{}_FK{}".format( side, elbowNum, jnt_suff), elbow_ctrl_group) )
            cmds.parentConstraint( armRigControls.elbow_control, "elbow{}{}_FK{}".format( side, elbowNum, jnt_suff), mo=True )
            
            elbowNum = elbowNum + 1
        else:
            createControl( "elbow{}_FK".format(side), .8, (1,0,0), color )
            armRigControls.elbow_control = createControl.newCtrl
            elbow_ctrl_group = cmds.group( n="elbow{}_FK{}".format(side, ctrlGrp_suff) )
            
            cmds.delete( cmds.parentConstraint( "elbow{}_FK{}".format( side, jnt_suff), elbow_ctrl_group) )
            cmds.parentConstraint( armRigControls.elbow_control, "elbow{}_FK{}".format( side, jnt_suff), mo=True )
            
        cmds.parent( elbow_ctrl_group, armRigControls.shoulder_control )
            
    # wrist
    createControl( "wrist{}_FK".format(side), .8, (1,0,0), color )
    wrist_ctrl_group = cmds.group( n="wrist{}_FK{}".format(side, ctrlGrp_suff) )

    cmds.delete( cmds.parentConstraint( "wrist{}_FK{}".format( side, jnt_suff), wrist_ctrl_group) )
    cmds.parent( wrist_ctrl_group, armRigControls.elbow_control )
    
    cmds.parentConstraint( createControl.newCtrl, "wrist{}_FK{}".format( side, jnt_suff), mo=True )

    # fingers and thumbs
    finger_joint_list = [ "thumb", "index", "middle", "ring", "pinky", "finger" ]
        
    for finger_joint in finger_joint_list:
        # first check if finger joing exist
        if cmds.objExists("{}_1{}{}".format(finger_joint, side, jnt_suff)):
            ## put each knuckle of that finger in a list
            joint_kunckles = cmds.ls("{}*{}{}".format(finger_joint, side, jnt_suff))
            
            for knuckle in range(len(joint_kunckles)-1):
                createControl( "{}_{}{}".format(finger_joint, knuckle+1, side), .8, (1,0,0), color, 360, "key" )
                finger_control = createControl.newCtrl
                
                finger_ctrl_group = cmds.group( n="{}_{}{}{}".format(finger_joint, knuckle+1, side, ctrlGrp_suff) )
                cmds.move(0,0,0, "{}.scalePivot".format(finger_ctrl_group), "{}.rotatePivot".format(finger_ctrl_group), rpr=True)
                
                if createRigControls.arm_side == "right":
                    cmds.rotate(-270,0,0, finger_control)
                else:
                    cmds.rotate(-90,0,0, finger_control)
                    
                cmds.makeIdentity( a=True, t=True, r=True, s=True)
                
                cmds.delete( cmds.parentConstraint( "{}_{}{}{}".format( finger_joint, knuckle+1, side, jnt_suff), finger_ctrl_group) )
                cmds.parentConstraint( finger_control, "{}_{}{}{}".format(finger_joint, knuckle+1, side, jnt_suff), mo=True )
                
                if knuckle > 0:
                    cmds.parent( finger_ctrl_group, "{}_{}{}{}".format(finger_joint, knuckle, side, ctrl_suff) )
        
            cmds.parentConstraint( "wrist{}{}".format(side, jnt_suff), "{}_{}{}{}".format(finger_joint, 1, side, ctrlGrp_suff), mo=True)
            cmds.parent( "{}_{}{}{}".format(finger_joint, 1, side, ctrlGrp_suff), "{}_main{}".format(createCore.rig_name, ctrl_suff))
    
    ##############################
    #### create IK control for arm
        #### as well as control to toggle switch
        # proxyJoint( group_name, name, radius, color=1 )
        # proxyJoint.prxyJnt_Grp
        
    proxyJoint( "wrist{}_IK{}".format( side, ctrlGrp_suff), "wrist{}_IK{}".format( side, ctrl_suff), .8, color )
    # scale control for asthetic
    cmds.scale( .3,1,1, proxyJoint.prxyJnt_Grp )
    cmds.makeIdentity( a=True, s=True )
    # snap to wrist joint
    cmds.delete( cmds.parentConstraint( "wrist{}_IK{}".format( side, jnt_suff), proxyJoint.prxyJnt_Grp) )
    cmds.makeIdentity( proxyJoint.prxyJnt_Grp, a=True, t=True, r=True, s=True )
    
    cmds.orientConstraint( "wrist{}_IK{}".format( side, ctrl_suff), "wrist{}_IK{}".format( side, jnt_suff), mo=True )
    cmds.parent( "arm{}_ikHandle".format(side), "wrist{}_IK{}".format( side, ctrl_suff) )
    cmds.parent( proxyJoint.prxyJnt_Grp, "{}_main{}".format(createCore.rig_name, ctrl_suff))
    
    cmds.setAttr( "wrist{}_IK{}.v".format( side, ctrl_suff), 0 )
    
    # create ik elbow control
    createControl( "elbow{}_IK".format( side), None, None, color, None, 'cone' )
    cmds.scale( 0.66, 0.25, 0.66, createControl.cone_control )
    cmds.makeIdentity( a=True, s=True )
    
    elbow_cone_ctrl_group = cmds.group(createControl.cone_control, n="elbow{}_IK{}".format( side, ctrlGrp_suff))
        
    cmds.delete( cmds.parentConstraint( "elbow{}_IK{}".format( side, jnt_suff), elbow_cone_ctrl_group) )
    cmds.rotate( -90, 0, 0, elbow_cone_ctrl_group)
    cmds.makeIdentity( elbow_cone_ctrl_group, a=True, t=True, r=True, s=True)
    cmds.move( 0, 0, -4, ls=True, os=True, r=True )
    
    cmds.poleVectorConstraint( createControl.cone_control, "arm{}_ikHandle".format(side) )
    cmds.parent( elbow_cone_ctrl_group, "{}_main{}".format(createCore.rig_name, ctrl_suff))
    
    cmds.setAttr( "{}.v".format( createControl.cone_control), 0 )
    
    # create toggle control for IK/FK swtich and potential other attribute
        ## createControl( name, radius, normal, color, sweep=360, ctrlType="circle" )
    createControl( "arm{}_IKFK".format(side), None, None, color, None, 'cone' )
    cmds.scale( 0.6, 0.75, 0.6, createControl.cone_control )
    cone_control_group = cmds.group(createControl.cone_control, n="arm{}_IK/FK{}".format(side, ctrlGrp_suff))
    if createRigControls.arm_side == "right":
        cmds.scale(1,-1,1, cone_control_group)
    
    cmds.delete( cmds.parentConstraint( "wrist{}{}".format( side, jnt_suff), cone_control_group) )
    cmds.move( 0, 2, 0, ls=True, os=True, r=True )
    
    cmds.parentConstraint( "wrist{}{}".format( side, jnt_suff), cone_control_group, mo=True )
    cmds.parent( cone_control_group, "{}_main{}".format(createCore.rig_name, ctrl_suff))
    
    # setup attributes
    for attr in ("tx","ty","tz","rx","ry","rz","sx","sy","sz","v"):
        cmds.setAttr( "{}.{}".format( createControl.cone_control, attr ), lock=True, keyable=False )

    cmds.addAttr( createControl.cone_control, ln="IK_FK_Switch", at="float", min=0, max=1, dv=1 )
    cmds.setAttr( "{}.IK_FK_Switch".format(createControl.cone_control), e=True, keyable=True)

def legRigControl( jnt_suff, ctrl_suff, ctrlGrp_suff, side, color ):
    
    ##### FK CONTROLS #####
    # hip
    createControl( "hip{}_FK".format(side), 1.1, (1,0,0), color )
    legRigControl.hip_control = createControl.newCtrl
    hip_ctrl_group = cmds.group( n="hip{}_FK{}".format(side, ctrlGrp_suff) )
    
    cmds.delete( cmds.parentConstraint( "hip{}_FK{}".format( side, jnt_suff), hip_ctrl_group) )
    cmds.parent( hip_ctrl_group, "cog{}".format(ctrl_suff) )
    
    cmds.parentConstraint( legRigControl.hip_control, "hip{}_FK{}".format( side, jnt_suff), mo=True )
    
    # knee
    knee_joints = cmds.ls("knee{}_FK{}".format(side, jnt_suff))
    kneeNum = 1
    for kJnt in knee_joints:
        if len(knee_joints) > 1:
            createControl( "knee{}_{}_FK".format(side, kneeNum), .8, (1,0,0), color )
            legRigControl.knee_control = createControl.newCtrl
            knee_ctrl_group = cmds.group( n="knee{}_{}_FK{}".format(side, kneeNum, ctrlGrp_suff) )
            
            cmds.delete( cmds.parentConstraint( "knee{}{}_FK{}".format( side, kneeNum, jnt_suff), knee_ctrl_group) )
            cmds.parentConstraint( legRigControl.knee_control, "knee{}{}_FK{}".format( side, kneeNum, jnt_suff), mo=True )
            
            kneeNum = kneeNum + 1
        else:
            createControl( "knee{}_FK".format(side), .8, (1,0,0), color )
            legRigControl.knee_control = createControl.newCtrl
            knee_ctrl_group = cmds.group( n="knee{}_FK{}".format(side, ctrlGrp_suff) )
            
            cmds.delete( cmds.parentConstraint( "knee{}_FK{}".format( side, jnt_suff), knee_ctrl_group) )
            cmds.parentConstraint( legRigControl.knee_control, "knee{}_FK{}".format( side, jnt_suff), mo=True )
            
        cmds.parent( knee_ctrl_group, legRigControl.hip_control )
            
    # ankle
    createControl( "ankle{}_FK".format(side), .8, (1,0,0), color )
    legRigControl.ankle_control = createControl.newCtrl
    ankle_ctrl_group = cmds.group( n="ankle{}_FK{}".format(side, ctrlGrp_suff) )

    cmds.delete( cmds.parentConstraint( "ankle{}_FK{}".format( side, jnt_suff), ankle_ctrl_group) )
    cmds.parent( ankle_ctrl_group, legRigControl.knee_control )
    
    cmds.parentConstraint( createControl.newCtrl, "ankle{}_FK{}".format( side, jnt_suff), mo=True )

    # ball
    createControl( "ball{}_FK".format(side), .6, (1,0,0), color )
    legRigControl.ball_control = createControl.newCtrl
    ball_ctrl_group = cmds.group( n="ball{}_FK{}".format(side, ctrlGrp_suff) )
    
    cmds.delete( cmds.parentConstraint( "ball{}_FK{}".format( side, jnt_suff), ball_ctrl_group) )
    cmds.parent( ball_ctrl_group, legRigControl.ankle_control )
    
    # toe
    createControl( "toe{}_FK".format(side), .6, (1,0,0), color )
    legRigControl.toe_control = createControl.newCtrl
    toe_ctrl_group = cmds.group( n="toe{}_FK{}".format(side, ctrlGrp_suff) )
    
    cmds.delete( cmds.parentConstraint( "toe{}_FK{}".format( side, jnt_suff), toe_ctrl_group) )
    cmds.parent( toe_ctrl_group, legRigControl.ball_control )
    
    cmds.setAttr( "{}.v".format(legRigControl.hip_control), 0 )
    
    #### IK CONTROLS ####
    ## create ik knee control
    createControl( "knee{}_IK".format( side), None, None, color, None, 'cone' )
    cmds.scale( 0.66, 0.25, 0.66, createControl.cone_control )
    cmds.makeIdentity( a=True, s=True )
    
    knee_cone_ctrl_group = cmds.group(createControl.cone_control, n="knee{}_IK{}".format( side, ctrlGrp_suff))
        
    cmds.delete( cmds.parentConstraint( "knee{}_IK{}".format( side, jnt_suff), knee_cone_ctrl_group) )
    cmds.rotate(90,0,0, knee_cone_ctrl_group)
    cmds.makeIdentity( knee_cone_ctrl_group, a=True, t=True, r=True, s=True)
    cmds.move( 0, 0, 4, ls=True, os=True, r=True )
    
    cmds.poleVectorConstraint( createControl.cone_control, "leg{}_ikHandle".format(side) )
    cmds.parent( knee_cone_ctrl_group, "{}_main{}".format(createCore.rig_name, ctrl_suff))
    
    # create toggle control for IK/FK swtich and potential other attribute
        ## createControl( name, radius, normal, color, sweep=360, ctrlType="circle" )
    createControl( "leg{}_IKFK".format(side), None, None, color, None, 'cone' )
    cmds.scale( 0.6, 0.75, 0.6, createControl.cone_control )
    cone_control_group = cmds.group(createControl.cone_control, n="leg{}_IK/FK{}".format(side, ctrlGrp_suff))

    cmds.delete( cmds.parentConstraint( "ankle{}{}".format( side, jnt_suff), cone_control_group) )
    cmds.rotate( -90, 0, 0, cone_control_group)
    cmds.makeIdentity( cone_control_group, a=True, t=True, r=True, s=True)
    cmds.move( 0, 0, -2, ls=True, os=True, r=True )
    
    cmds.parentConstraint( "ankle{}{}".format( side, jnt_suff), cone_control_group, mo=True )
    cmds.parent( cone_control_group, "{}_main{}".format(createCore.rig_name, ctrl_suff))
    
    # setup attributes
    for attr in ("tx","ty","tz","rx","ry","rz","sx","sy","sz","v"):
        cmds.setAttr( "{}.{}".format( createControl.cone_control, attr ), lock=True, keyable=False )

    cmds.addAttr( createControl.cone_control, ln="IK_FK_Switch", at="float", min=0, max=1, dv=0 )
    cmds.setAttr( "{}.IK_FK_Switch".format(createControl.cone_control), e=True, keyable=True)
    
def IKFK_Switch( jnt_suff, ctrl_suff, ctrlGrp_suff, side ):
    # create connections for ik/fk setup
        # skinning skeleton follows either ik or fk using a blend
        ## when in fk, ik controls are hidden. And vice versa.
        ### create switch on cone toggles
    
    #############################
    ##### ARM
    #############################
    
    #### shoulder connection ####
    # create pair blend node #
    pair_blend = cmds.createNode( "pairBlend" )

    ## connect IK in translate/rotate 1 and FK into translate/rotate 2 ##
    # IK to pair blend
    cmds.connectAttr( "shoulder{}_IK{}.translate".format( side, jnt_suff ), "{}.inTranslate1".format( pair_blend ), f=True )
    cmds.connectAttr( "shoulder{}_IK{}.rotate".format( side, jnt_suff ), "{}.inRotate1".format( pair_blend ), f=True )
    # FK to pair blend
    cmds.connectAttr( "shoulder{}_FK{}.translate".format( side, jnt_suff ), "{}.inTranslate2".format( pair_blend ), f=True )
    cmds.connectAttr( "shoulder{}_FK{}.rotate".format( side, jnt_suff ), "{}.inRotate2".format( pair_blend ), f=True )
    # pair blend to skinning joint
    cmds.connectAttr( "{}.outTranslate".format( pair_blend ), "shoulder{}{}.translate".format( side,jnt_suff ), f=True )
    cmds.connectAttr( "{}.outRotate".format( pair_blend ), "shoulder{}{}.rotate".format( side,jnt_suff ), f=True )
    
    ## connect blend attribute from switch with pair blend
    cmds.connectAttr( "arm{}_IKFK{}.IK_FK_Switch".format( side, ctrl_suff ), "{}.weight".format(pair_blend) )
    
    #### elbow connection ####
    # create pair blend node #
    pair_blend = cmds.createNode( "pairBlend" )

    ## connect IK in translate/rotate 1 and FK into translate/rotate 2 ##
    # IK to pair blend
    cmds.connectAttr( "elbow{}_IK{}.translate".format( side, jnt_suff ), "{}.inTranslate1".format( pair_blend ), f=True )
    cmds.connectAttr( "elbow{}_IK{}.rotate".format( side, jnt_suff ), "{}.inRotate1".format( pair_blend ), f=True )
    # FK to pair blend
    cmds.connectAttr( "elbow{}_FK{}.translate".format( side, jnt_suff ), "{}.inTranslate2".format( pair_blend ), f=True )
    cmds.connectAttr( "elbow{}_FK{}.rotate".format( side, jnt_suff ), "{}.inRotate2".format( pair_blend ), f=True )
    # pair blend to skinning joint

    cmds.connectAttr( "{}.outTranslate".format( pair_blend ), "elbow{}{}.translate".format( side, jnt_suff ), f=True )
    cmds.connectAttr( "{}.outRotate".format( pair_blend ), "elbow{}{}.rotate".format( side, jnt_suff ), f=True )
    
    ## connect blend attribute from switch with pair blend
    cmds.connectAttr( "arm{}_IKFK{}.IK_FK_Switch".format( side, ctrl_suff ), "{}.weight".format(pair_blend) )
    
    #### wrist connection ####
    # create pair blend node #
    pair_blend = cmds.createNode( "pairBlend" )

    ## connect IK in translate/rotate 1 and FK into translate/rotate 2 ##
    # IK to pair blend
    cmds.connectAttr( "wrist{}_IK{}.translate".format( side, jnt_suff ), "{}.inTranslate1".format( pair_blend ), f=True )
    cmds.connectAttr( "wrist{}_IK{}.rotate".format( side, jnt_suff ), "{}.inRotate1".format( pair_blend ), f=True )
    # FK to pair blend
    cmds.connectAttr( "wrist{}_FK{}.translate".format( side, jnt_suff ), "{}.inTranslate2".format( pair_blend ), f=True )
    cmds.connectAttr( "wrist{}_FK{}.rotate".format( side, jnt_suff ), "{}.inRotate2".format( pair_blend ), f=True )
    # pair blend to skinning joint
    cmds.connectAttr( "{}.outTranslate".format( pair_blend ), "wrist{}{}.translate".format( side,jnt_suff ), f=True )
    cmds.connectAttr( "{}.outRotate".format( pair_blend ), "wrist{}{}.rotate".format( side,jnt_suff ), f=True )
    
    ## connect blend attribute from switch with pair blend
    cmds.connectAttr( "arm{}_IKFK{}.IK_FK_Switch".format( side, ctrl_suff ), "{}.weight".format(pair_blend) )
    
    ### toggle FK visibility
    condition_node = cmds.shadingNode( "condition", au=True )
    cmds.setAttr( "{}.operation".format(condition_node), 2 )
    cmds.setAttr( "{}.colorIfTrueR".format(condition_node), 1 )
    cmds.setAttr( "{}.colorIfFalseR".format(condition_node), 0 )
    
    cmds.connectAttr( "arm{}_IKFK{}.IK_FK_Switch".format( side, ctrl_suff ), "{}.firstTerm".format( condition_node ), f=True)
    cmds.connectAttr( "{}.outColorR".format( condition_node ), "shoulder{}_FK{}.v".format( side, ctrl_suff ), f=True)
    
    ### toggle IK visibility
    condition_node = cmds.shadingNode( "condition", au=True )
    cmds.setAttr( "{}.operation".format(condition_node), 4 )
    cmds.setAttr( "{}.secondTerm".format(condition_node), 1 )
    cmds.setAttr( "{}.colorIfTrueR".format(condition_node), 1 )
    cmds.setAttr( "{}.colorIfFalseR".format(condition_node), 0 )
    
    cmds.connectAttr( "arm{}_IKFK{}.IK_FK_Switch".format( side, ctrl_suff ), "{}.firstTerm".format( condition_node ), f=True)
    cmds.connectAttr( "{}.outColorR".format( condition_node ), "wrist{}_IK{}.v".format( side, ctrl_suff ), f=True)
    cmds.connectAttr( "{}.outColorR".format( condition_node ), "elbow{}_IK{}.v".format( side, ctrl_suff ), f=True)
    
    
    #############################
    ##### LEG
    #############################
    
    #### hip connection ####
    # create pair blend node #
    pair_blend = cmds.createNode( "pairBlend" )

    ## connect IK in translate/rotate 1 and FK into translate/rotate 2 ##
    # IK to pair blend
    cmds.connectAttr( "hip{}_IK{}.translate".format( side, jnt_suff ), "{}.inTranslate1".format( pair_blend ), f=True )
    cmds.connectAttr( "hip{}_IK{}.rotate".format( side, jnt_suff ), "{}.inRotate1".format( pair_blend ), f=True )
    # FK to pair blend
    cmds.connectAttr( "hip{}_FK{}.translate".format( side, jnt_suff ), "{}.inTranslate2".format( pair_blend ), f=True )
    cmds.connectAttr( "hip{}_FK{}.rotate".format( side, jnt_suff ), "{}.inRotate2".format( pair_blend ), f=True )
    # pair blend to skinning joint
    cmds.connectAttr( "{}.outTranslate".format( pair_blend ), "hip{}{}.translate".format( side,jnt_suff ), f=True )
    cmds.connectAttr( "{}.outRotate".format( pair_blend ), "hip{}{}.rotate".format( side,jnt_suff ), f=True )
    
    ## connect blend attribute from switch with pair blend
    cmds.connectAttr( "leg{}_IKFK{}.IK_FK_Switch".format( side, ctrl_suff ), "{}.weight".format(pair_blend) )
    
    #### knee connection ####
    # create pair blend node #
    pair_blend = cmds.createNode( "pairBlend" )

    ## connect IK in translate/rotate 1 and FK into translate/rotate 2 ##
    # IK to pair blend
    cmds.connectAttr( "knee{}_IK{}.translate".format( side, jnt_suff ), "{}.inTranslate1".format( pair_blend ), f=True )
    cmds.connectAttr( "knee{}_IK{}.rotate".format( side, jnt_suff ), "{}.inRotate1".format( pair_blend ), f=True )
    # FK to pair blend
    cmds.connectAttr( "knee{}_FK{}.translate".format( side, jnt_suff ), "{}.inTranslate2".format( pair_blend ), f=True )
    cmds.connectAttr( "knee{}_FK{}.rotate".format( side, jnt_suff ), "{}.inRotate2".format( pair_blend ), f=True )
    # pair blend to skinning joint

    cmds.connectAttr( "{}.outTranslate".format( pair_blend ), "knee{}{}.translate".format( side, jnt_suff ), f=True )
    cmds.connectAttr( "{}.outRotate".format( pair_blend ), "knee{}{}.rotate".format( side, jnt_suff ), f=True )
    
    ## connect blend attribute from switch with pair blend
    cmds.connectAttr( "leg{}_IKFK{}.IK_FK_Switch".format( side, ctrl_suff ), "{}.weight".format(pair_blend) )
    
    #### ankle connection ####
    # create pair blend node #
    pair_blend = cmds.createNode( "pairBlend" )

    ## connect IK in translate/rotate 1 and FK into translate/rotate 2 ##
    # IK to pair blend
    cmds.connectAttr( "ankle{}_IK{}.translate".format( side, jnt_suff ), "{}.inTranslate1".format( pair_blend ), f=True )
    cmds.connectAttr( "ankle{}_IK{}.rotate".format( side, jnt_suff ), "{}.inRotate1".format( pair_blend ), f=True )
    # FK to pair blend
    cmds.connectAttr( "ankle{}_FK{}.translate".format( side, jnt_suff ), "{}.inTranslate2".format( pair_blend ), f=True )
    cmds.connectAttr( "ankle{}_FK{}.rotate".format( side, jnt_suff ), "{}.inRotate2".format( pair_blend ), f=True )
    # pair blend to skinning joint
    cmds.connectAttr( "{}.outTranslate".format( pair_blend ), "ankle{}{}.translate".format( side,jnt_suff ), f=True )
    cmds.connectAttr( "{}.outRotate".format( pair_blend ), "ankle{}{}.rotate".format( side,jnt_suff ), f=True )
    
    ## connect blend attribute from switch with pair blend
    cmds.connectAttr( "leg{}_IKFK{}.IK_FK_Switch".format( side, ctrl_suff ), "{}.weight".format(pair_blend) )
    
    #### ball connection ####
    # create pair blend node #
    pair_blend = cmds.createNode( "pairBlend" )

    ## connect IK in translate/rotate 1 and FK into translate/rotate 2 ##
    # IK to pair blend
    cmds.connectAttr( "ball{}_IK{}.translate".format( side, jnt_suff ), "{}.inTranslate1".format( pair_blend ), f=True )
    cmds.connectAttr( "ball{}_IK{}.rotate".format( side, jnt_suff ), "{}.inRotate1".format( pair_blend ), f=True )
    # FK to pair blend
    cmds.connectAttr( "ball{}_FK{}.translate".format( side, jnt_suff ), "{}.inTranslate2".format( pair_blend ), f=True )
    cmds.connectAttr( "ball{}_FK{}.rotate".format( side, jnt_suff ), "{}.inRotate2".format( pair_blend ), f=True )
    # pair blend to skinning joint
    cmds.connectAttr( "{}.outTranslate".format( pair_blend ), "ball{}{}.translate".format( side,jnt_suff ), f=True )
    cmds.connectAttr( "{}.outRotate".format( pair_blend ), "ball{}{}.rotate".format( side,jnt_suff ), f=True )
    
    ## connect blend attribute from switch with pair blend
    cmds.connectAttr( "leg{}_IKFK{}.IK_FK_Switch".format( side, ctrl_suff ), "{}.weight".format(pair_blend) )
    
    #### toe connection ####
    # create pair blend node #
    pair_blend = cmds.createNode( "pairBlend" )

    ## connect IK in translate/rotate 1 and FK into translate/rotate 2 ##
    # IK to pair blend
    cmds.connectAttr( "toe{}_IK{}.translate".format( side, jnt_suff ), "{}.inTranslate1".format( pair_blend ), f=True )
    cmds.connectAttr( "toe{}_IK{}.rotate".format( side, jnt_suff ), "{}.inRotate1".format( pair_blend ), f=True )
    # FK to pair blend
    cmds.connectAttr( "toe{}_FK{}.translate".format( side, jnt_suff ), "{}.inTranslate2".format( pair_blend ), f=True )
    cmds.connectAttr( "toe{}_FK{}.rotate".format( side, jnt_suff ), "{}.inRotate2".format( pair_blend ), f=True )
    # pair blend to skinning joint
    cmds.connectAttr( "{}.outTranslate".format( pair_blend ), "toe{}{}.translate".format( side,jnt_suff ), f=True )
    cmds.connectAttr( "{}.outRotate".format( pair_blend ), "toe{}{}.rotate".format( side,jnt_suff ), f=True )
    
    ## connect blend attribute from switch with pair blend
    cmds.connectAttr( "leg{}_IKFK{}.IK_FK_Switch".format( side, ctrl_suff ), "{}.weight".format(pair_blend) )
    
    ### toggle FK visibility
    condition_node = cmds.shadingNode( "condition", au=True )
    cmds.setAttr( "{}.operation".format(condition_node), 2 )
    cmds.setAttr( "{}.colorIfTrueR".format(condition_node), 1 )
    cmds.setAttr( "{}.colorIfFalseR".format(condition_node), 0 )
    
    cmds.connectAttr( "leg{}_IKFK{}.IK_FK_Switch".format( side, ctrl_suff ), "{}.firstTerm".format( condition_node ), f=True)
    cmds.connectAttr( "{}.outColorR".format( condition_node ), "hip{}_FK{}.v".format( side, ctrl_suff ), f=True)
    
    ### toggle IK visibility
    condition_node = cmds.shadingNode( "condition", au=True )
    cmds.setAttr( "{}.operation".format(condition_node), 4 )
    cmds.setAttr( "{}.secondTerm".format(condition_node), 1 )
    cmds.setAttr( "{}.colorIfTrueR".format(condition_node), 1 )
    cmds.setAttr( "{}.colorIfFalseR".format(condition_node), 0 )
    
    cmds.connectAttr( "leg{}_IKFK{}.IK_FK_Switch".format( side, ctrl_suff ), "{}.firstTerm".format( condition_node ), f=True)
    cmds.connectAttr( "{}.outColorR".format( condition_node ), "foot{}_IK{}.v".format( side, ctrl_suff ), f=True)
    cmds.connectAttr( "{}.outColorR".format( condition_node ), "knee{}_IK{}.v".format( side, ctrl_suff ), f=True)