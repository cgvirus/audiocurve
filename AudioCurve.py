# -*- coding: utf-8 -*-

# @olear: I suck at python, but adapted the pyplug from @rcspam, works but need some love

#Note that Viewers are never exported
#This file was automatically generated by Natron PyPlug exporter version 1.
import NatronEngine

# extra lib added
import os, time, tempfile
from os import *

def getPluginID():
    return "AudioCurve"

def getLabel():
    return "AudioCurve"

def getVersion():
    return 1

def getIconPath():
    return "audiocurve.png"

def getGrouping():
    return "Read"

def getDescription():
    return "Generate curves from audio in Natron.\n\nWritten by @olear and @rcspam.\nPowered by SoX."
    
# extra defs added

def audioCurve(audioFileATA, asciiFileATA, dimATA, fpsATA, durationATA, xHeightATA, yHeightATA):
    ret_a2a = os.system(str(os.path.dirname(os.path.realpath(__file__)))+"/AudioCurve/audiocurve -input \""+str(audioFileATA)+"\" -output \""+str(asciiFileATA)+"\" -"+str(dimATA)+" -fps "+str(fpsATA)+" -frames "+str(durationATA)+" -cX "+str(xHeightATA)+" -cY "+str(yHeightATA));
    return ret_a2a

def animCurves(thisParam, fileAC, dimAC, durationAC ,frameStartAC):
    # ascii file #TODO delete file when done
    asciiAC = open(fileAC, "r")
    # end frame
    lineAC = int(durationAC) + int(frameStartAC)
    # anim x
    if dimAC == 0:
        # reset x before recalculate
        thisParam.removeAnimation(0)
        for frameC in range(int(frameStartAC),lineAC + int(frameStartAC)):
            x = asciiAC.readline()
            thisParam.setValueAtTime(float(x), frameC, 0)
    # anim y
    elif dimAC == 1:
        # reset y before recalculate
        thisParam.removeAnimation(1)
        for frameC in range(int(frameStartAC),lineAC):
            y = asciiAC.readline()
            thisParam.setValueAtTime(float(y), frameC, 1)
    # anim yx
    else:
        # reset x and y before recalculate
        thisParam.removeAnimation(0)
        thisParam.removeAnimation(1)
        for frameC in range(int(frameStartAC),lineAC):
            x, y = asciiAC.readline().split ("_")
            thisParam.setValueAtTime(float(x), frameC, 0)
            thisParam.setValueAtTime(float(y), frameC, 1)

def paramHasChanged(thisParam, thisNode, thisGroup, app, userEdited):
    # audio input file
    audio_file = thisNode.inputFile.get()
    # ascii output file
    ascii_file = thisNode.curveFile.get()
    
    # convert dimension in comprehensive thing for audio2ascii script 
    dim = thisNode.dimEnsion.get()
    if dim == 0:
        dimension = "x"
    elif dim == 1:
        dimension = "y"
    elif dim == 2:
        dimension = "xy" 

    # Import Curve
    if ascii_file is not None and audio_file is not None and thisParam == thisNode.importCurve:
        ret_exec = audioCurve(audio_file, ascii_file, dimension, thisNode.framesPerSec.get(), thisNode.duraTion.get(), thisNode.xHeight.get(), thisNode.yHeight.get())
        # test and wait end of audio2ascii 
        if ret_exec == 0:
            # calculate animation 
            animCurves(thisNode.curveIn, ascii_file, thisNode.dimEnsion.get(), thisNode.duraTion.get(), thisNode.atFrameNum.get())
            

## / extra defs

def createInstance(app,group):

    #Create all nodes in the group
    lastNode = app.createNode("fr.inria.built-in.Output", 1, group)
    lastNode.setScriptName("Output1")
    lastNode.setLabel("Output1")
    lastNode.setPosition(758.75, 325.125)
    lastNode.setSize(104, 44)
    lastNode.setColor(0.699992, 0.699992, 0.699992)
    groupOutput1 = lastNode

    param = lastNode.getParam("Output_layer_name")
    if param is not None:
        param.setValue("RGBA")
        param.setVisible(False)
        del param

    param = lastNode.getParam("highDefUpstream")
    if param is not None:
        param.setVisible(False)
        del param

    del lastNode



    lastNode = app.createNode("fr.inria.built-in.Input", 1, group)
    lastNode.setScriptName("Input1")
    lastNode.setLabel("Input1")
    lastNode.setPosition(758.75, 161.125)
    lastNode.setSize(104, 44)
    lastNode.setColor(0.300008, 0.500008, 0.2)
    groupInput1 = lastNode

    param = lastNode.getParam("Output_layer_name")
    if param is not None:
        param.setValue("RGBA")
        param.setVisible(False)
        del param

    param = lastNode.getParam("highDefUpstream")
    if param is not None:
        param.setVisible(False)
        del param

    del lastNode

    #Create the parameters of the group node the same way we did for all internal nodes
    lastNode = group
    param = lastNode.getParam("highDefUpstream")
    if param is not None:
        param.setVisible(False)
        del param

    param = lastNode.getParam("onParamChanged")
    if param is not None:
        param.setValue("AudioCurve.paramHasChanged")
        del param


    #Create the user-parameters
    lastNode.userNatron = lastNode.createPageParam("userNatron", "Settings")
    param = lastNode.createFileParam("inputFile", "Audio")
    param.setSequenceEnabled(False)

    #Add the param to the page
    lastNode.userNatron.addParam(param)

    #Set param properties
    param.setHelp("")
    param.setAddNewLine(True)
    param.setAnimationEnabled(False)
    lastNode.inputFile = param
    del param

    param = lastNode.createFileParam("curveFile", "CurveFile")
    param.setSequenceEnabled(False)

    #Add the param to the page
    lastNode.userNatron.addParam(param)

    #Set param properties
    param.setHelp("")
    param.setVisible(False)
    param.setAddNewLine(True)
    param.setAnimationEnabled(False)
    tf = tempfile.NamedTemporaryFile()
    param.setDefaultValue(tf.name)
    lastNode.curveFile = param
    del param

    param = lastNode.createChoiceParam("dimEnsion", "Dimension")
    entries = [ ("x", ""),
    ("y", ""),
    ("xy", "")]
    param.setOptions(entries)
    del entries

    #Add the param to the page
    lastNode.userNatron.addParam(param)

    #Set param properties
    param.setHelp("Dimension curve X/Y (left/right)")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    options = param.getOptions()
    foundOption = False
    for i in range(len(options)):
        if options[i] == "x":
            param.setValue(i)
            foundOption = True
            break
    if not foundOption:
        app.writeToScriptEditor("Could not set option for parameter dimension on node AudioCurve")
    lastNode.dimEnsion = param
    del param

    param = lastNode.createIntParam("framesPerSec", "FPS")
    param.setDisplayMinimum(0, 0)
    param.setDisplayMaximum(100, 0)
    param.setDefaultValue(24, 0)

    #Add the param to the page
    lastNode.userNatron.addParam(param)

    #Set param properties
    param.setHelp("Calculate curve with this frame rate")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    lastNode.framesPerSec = param
    del param

    param = lastNode.createIntParam("duraTion", "Frames")
    param.setDisplayMinimum(0, 0)
    param.setDisplayMaximum(10000, 0)
    param.setDefaultValue(240, 0)

    #Add the param to the page
    lastNode.userNatron.addParam(param)

    #Set param properties
    param.setHelp("Duration in frames")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    lastNode.duraTion = param
    del param

    param = lastNode.createIntParam("xHeight", "Height X")
    param.setDisplayMinimum(0, 0)
    param.setDisplayMaximum(500, 0)
    param.setDefaultValue(100, 0)

    #Add the param to the page
    lastNode.userNatron.addParam(param)

    #Set param properties
    param.setHelp("Height of X deviation in pixels")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    lastNode.xHeight = param
    del param

    param = lastNode.createIntParam("yHeight", "Height Y")
    param.setDisplayMinimum(0, 0)
    param.setDisplayMaximum(500, 0)
    param.setDefaultValue(100, 0)

    #Add the param to the page
    lastNode.userNatron.addParam(param)

    #Set param properties
    param.setHelp("Height of Y deviation in pixels")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    lastNode.yHeight = param
    del param

    param = lastNode.createIntParam("atFrameNum", "Start at frame")
    param.setDisplayMinimum(1, 0)
    param.setDisplayMaximum(500, 0)
    param.setDefaultValue(1, 0)

    #Add the param to the page
    lastNode.userNatron.addParam(param)

    #Set param properties
    param.setHelp("Start the curve at this frame")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    lastNode.atFrameNum = param
    del param

    param = lastNode.createButtonParam("importCurve", "Generate curve(s)")

    #Add the param to the page
    lastNode.userNatron.addParam(param)

    #Set param properties
    param.setHelp("Generate curve from parameters")
    param.setAddNewLine(True)
    param.setPersistant(False)
    param.setEvaluateOnChange(False)
    lastNode.importCurve = param
    del param
    
    param = lastNode.createDouble2DParam("curveIn", "Curve ")
    param.setMinimum(-2.14748e+09, 0)
    param.setMaximum(2.14748e+09, 0)
    param.setDisplayMinimum(0, 0)
    param.setDisplayMaximum(500, 0)
    param.setMinimum(-2.14748e+09, 1)
    param.setMaximum(2.14748e+09, 1)
    param.setDisplayMinimum(0, 1)
    param.setDisplayMaximum(500, 1)

    #Add the param to the page
    lastNode.userNatron.addParam(param)

    #Set param properties
    param.setHelp("Curve X/Y result")
    param.setAddNewLine(True)
    param.setAnimationEnabled(True)
    lastNode.curveIn = param
    del param

    # extra callback added
    app.AudioCurve1.onParamChanged.set("AudioCurve.paramHasChanged")    

    #Refresh the GUI with the newly created parameters
    lastNode.refreshUserParamsGUI()
    del lastNode

    #Now that all nodes are created we can connect them together, restore expressions
    groupOutput1.connectInput(0, groupInput1)

