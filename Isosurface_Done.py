#!/usr/bin/env python
from __future__ import print_function

import vtk

### Hw 4 - April/8/2022
### Alan Braeley - Carolina Hurtado-Pulido

#Interactor style that handles mouse and keyboard events

class MyInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
    isovalue=0.5
   
    def __init__(self,parent=None):
        self.parent = vtk.vtkRenderWindowInteractor()
        if(parent is not None):
          self.parent = parent
        self.AddObserver("KeyPressEvent",self.keyPress)
    ##############################
    ### QUESTION 2 - ISOVALUES ###
    ##############################
    def keyPress(self,obj,event):
        key = self.parent.GetKeySym()
        if(key == "Up"):
            #TODO: have this increase the isovalue
            MyInteractorStyle.isovalue = MyInteractorStyle.isovalue +0.05 #Change isovalue
            print("Up ", MyInteractorStyle.isovalue)
        if(key == "Down"):
            #TODO: have this decrease the isovalue
            MyInteractorStyle.isovalue = MyInteractorStyle.isovalue-0.05
            print("Down ", MyInteractorStyle.isovalue)
        hydrogen.SetValue(0,MyInteractorStyle.isovalue) #Add isovalue to the object
        txt.SetInput("Isovalue: "+str(MyInteractorStyle.isovalue))
        self.parent.Render()#Update display
     


#Loader for our structured dataset
imageReader = vtk.vtkStructuredPointsReader()
imageReader.SetFileName("./data/hydrogen.vtk")
imageReader.Update()


#Print dimensions and range of the 3d image
dims = imageReader.GetOutput().GetDimensions()
print("Dimensions of image: " + str(dims[0]) + " x "
      + str(dims[1]) + " x " + str(dims[2]))
range = imageReader.GetOutput().GetScalarRange();
print("Range of image: " + str(range[0]) + " to " +  str(range[1]))

#create an outline that shows the bounds of our dataset
outline = vtk.vtkOutlineFilter();
outline.SetInputConnection(imageReader.GetOutputPort());

#mapper to push the outline geometry to the graphics library
outlineMapper = vtk.vtkPolyDataMapper();
outlineMapper.SetInputConnection(outline.GetOutputPort());
#actor for the outline to add to our renderer
outlineActor = vtk.vtkActor();
outlineActor.SetMapper(outlineMapper);
outlineActor.GetProperty().SetLineWidth(2.0);

##############################
### QUESTION 1 -ISOSURFACE ###
##############################
#Source
hydrogen=vtk.vtkMarchingCubes()
hydrogen.SetInputConnection(imageReader.GetOutputPort())
hydrogen.SetValue(0, 0.5) 
hydrogen.ComputeNormalsOn()
#Mapper
hydrogenMapper=vtk.vtkPolyDataMapper()
hydrogenMapper.SetInputConnection(hydrogen.GetOutputPort())
#Actor
hydrogenActor=vtk.vtkActor()
hydrogenActor.SetMapper(hydrogenMapper)
##############################
#
#
##############################
#### QUESTION 3 - TEXT #######
##############################
txt = vtk.vtkTextActor()
txtprop = txt.GetTextProperty()
txtprop.BoldOn()
txtprop.SetFontSize(30)
txt.SetDisplayPosition(15, 30)
txt.SetInput("Isovalue: "+str(0.5))
##############################
#
#
##############################
#### QUESTION 4 - SCALEBAR #######
##############################
isosurface = vtk.vtkContourFilter()
isosurface.SetInputConnection(imageReader.GetOutputPort())
isosurface.SetValue(0,MyInteractorStyle.isovalue)
lookuptable = vtk.vtkColorTransferFunction()
lookuptable.AddRGBPoint(0,1,0,0)
lookuptable.AddRGBPoint(0.5,0,1,0)
lookuptable.AddRGBPoint(0.3,1,1,0)
lookuptable.AddRGBPoint(1,0,0,1)
isosurfaceMapper = vtk.vtkPolyDataMapper()
isosurfaceMapper.SetLookupTable(lookuptable)
isosurfaceMapper.SetInputConnection(isosurface.GetOutputPort())
scalarBar = vtk.vtkScalarBarActor()
scalarBar.SetLookupTable(isosurfaceMapper.GetLookupTable())
scalarBar.SetTitle("Probability")
scalarBar.SetWidth(.1)
scalarBar.SetHeight(.8)
spc = scalarBar.GetPositionCoordinate()
spc.SetCoordinateSystemToNormalizedViewport()
spc.SetValue(0.8,0.05)

##############################

#A renderer that renders our geometry into the render window
renderer = vtk.vtkRenderer()
renderer.SetBackground(0.1, 0.1, 0.3)

#Add actors to our renderer
renderer.AddActor(scalarBar)
renderer.AddActor(outlineActor)
renderer.AddActor(txt)
renderer.AddActor(hydrogenActor)

isosurfaceActor = vtk.vtkActor()
isosurfaceActor.SetMapper(isosurfaceMapper)
#The render window
renwin = vtk.vtkRenderWindow()
renwin.SetSize( 1000, 650);
renwin.AddRenderer(renderer)






#Interactor to handle mouse and keyboard events
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetInteractorStyle(MyInteractorStyle(parent = interactor))
interactor.SetRenderWindow(renwin)


interactor.Initialize()
interactor.Start()