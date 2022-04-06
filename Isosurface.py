#!/usr/bin/env python
from __future__ import print_function

import vtk

#Interactor style that handles mouse and keyboard events

class MyInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
    isovalue=0.5
    def __init__(self,parent=None):
        self.parent = vtk.vtkRenderWindowInteractor()
        if(parent is not None):
          self.parent = parent
        self.AddObserver("KeyPressEvent",self.keyPress)
    
    def keyPress(self,obj,event):
      key = self.parent.GetKeySym()
      if(key == "Up"):
        #TODO: have this increase the isovalue
        MyInteractorStyle.isovalue = MyInteractorStyle.isovalue +0.05
        print("Up ", MyInteractorStyle.isovalue)
      if(key == "Down"):
        #TODO: have this decrease the isovalue
        MyInteractorStyle.isovalue = MyInteractorStyle.isovalue-0.05
        print("Down ", MyInteractorStyle.isovalue)
      


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

#TODO:
#
#Insert isosurfacing, scalebar, and text code here
#
##############################
### QUESTION 1 -ISOSURFACE ###
##############################
#Object
hydrogen=vtk.vtkMarchingCubes()
hydrogen.SetInputConnection(imageReader.GetOutputPort())
hydrogen.SetValue(0, MyInteractorStyle.isovalue) #Could this be hydrogen.SetValue(0, 0.1)?
hydrogen.ComputeNormalsOn()
hydrogen.Update()
#Mapper
hydrogenMapper=vtk.vtkPolyDataMapper()
hydrogenMapper.SetInputConnection(hydrogen.GetOutputPort())
#Actor
hydrogenActor=vtk.vtkActor()
hydrogenActor.SetMapper(hydrogenMapper)

##############################

#A renderer that renders our geometry into the render window
renderer = vtk.vtkRenderer()
renderer.SetBackground(0.1, 0.1, 0.3)

#Add actors to our renderer
renderer.AddActor(outlineActor)
renderer.AddActor(hydrogenActor)
#TODO: You'll probably need to add additional actors to the scene

#The render window
renwin = vtk.vtkRenderWindow()
renwin.SetSize( 512, 512);
renwin.AddRenderer(renderer)

#Interactor to handle mouse and keyboard events
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetInteractorStyle(MyInteractorStyle(parent = interactor))
interactor.SetRenderWindow(renwin)

interactor.Initialize()
interactor.Start()
