#!/usr/bin/env python
from __future__ import print_function

import vtk, inspect

### Hw 5 - April/22/2022
### Alan Braeley - Carolina Hurtado-Pulido

#Interactor style that handles mouse and keyboard events
class MyInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
   
    def __init__(self,parent=None):
        self.parent = vtk.vtkRenderWindowInteractor()
        if(parent is not None):
          self.parent = parent
     


#Loader for our structured dataset
imageReader = vtk.vtkStructuredPointsReader()
imageReader.SetFileName("./data/foot.vtk")
imageReader.Update()

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

# Transfer mapping
opacityTransferFunction = vtk.vtkPiecewiseFunction()
opacityTransferFunction.AddPoint(20, 0.0)
opacityTransferFunction.AddPoint(100, 0.4)
opacityTransferFunction.AddPoint(200, 0.8)

# Transfer mapping scalar values to colors
colorTransferFunction = vtk.vtkColorTransferFunction()
colorTransferFunction.AddRGBPoint(0, 2.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(64, 5.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(0, 0.0, 128.0, 1.0)
colorTransferFunction.AddRGBPoint(192, 0.0, 1.0, 0.0)
colorTransferFunction.AddRGBPoint(255, 0.0, 0.2, 1.0)


volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.SetColor(colorTransferFunction)
volumeProperty.SetScalarOpacity(opacityTransferFunction)
volumeProperty.ShadeOn()
volumeProperty.SetInterpolationTypeToLinear()

# The mapper / ray cast function know how to render the data
volumeMapper = vtk.vtkGPUVolumeRayCastMapper()
volumeMapper.SetBlendModeToComposite()
volumeMapper.SetInputConnection(imageReader.GetOutputPort())

# The volume holds the mapper and the property and
# can be used to position/orient the volume
volume = vtk.vtkVolume()
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)


########################################################################################################################################################################

'''
Need to create a clipping plane with vtkImplicitPlaneWidget2
'''

'''#A renderer that renders our geometry into the render window
renderer = vtk.vtkRenderer()
renderer.SetBackground(0.1, 0.1, 0.3)


#The render window
renwin = vtk.vtkRenderWindow()
renwin.AddRenderer(renderer)
renderer.AddVolume(volume)
renderer.AddActor(outlineActor)
renwin.SetSize(600, 600)
renwin.Render()'''


rt = vtk.vtkRTAnalyticSource()
rt.SetWholeExtent(-10,10,-10,10,-10,10)
rt.Update()

plane = vtk.vtkPlane()
clipper = vtk.vtkCutter()
clipper.SetInputConnection(rt.GetOutputPort())
clipper.SetCutFunction(plane)

selectMapper = vtk.vtkPolyDataMapper()
selectMapper.SetInputConnection(clipper.GetOutputPort())
selectMapper.SetScalarModeToUsePointFieldData()
selectMapper.SetColorModeToMapScalars()
selectMapper.ScalarVisibilityOn()
selectMapper.SetScalarRange(rt.GetOutputDataObject(0).GetPointData().GetScalars().GetRange())
selectMapper.SelectColorArray('RTData')

selectActor = vtk.vtkActor()
selectActor.SetMapper(selectMapper)
selectActor.VisibilityOn()
selectActor.SetScale(10, 10, 10)


#A renderer that renders our geometry into the render window
renderer = vtk.vtkRenderer()
renderer.SetBackground(0.1, 0.1, 0.3)

#The render window
renwin = vtk.vtkRenderWindow()
renwin.AddRenderer(renderer)
renderer.AddVolume(volume)
renderer.AddActor(outlineActor)
renwin.SetSize(600, 600)
renwin.Render()
# The callback function
def myCallback(obj, event):
    global plane
    obj.GetRepresentation().GetPlane(plane)
    selectActor.VisibilityOn()

# Create the representation and widget
planeRep = vtk.vtkImplicitPlaneRepresentation()
planeRep.SetPlaceFactor(1.25)
planeRep.PlaceWidget(rt.GetOutput().GetBounds())
planeRep.VisibilityOn()
planeRep.SetNormal(1,1,1)
planeRep.GetPlane(plane)

planeWidget = vtk.vtkImplicitPlaneWidget2()
#planeWidget.SetInteractor(iren)
planeWidget.SetRepresentation(planeRep)
planeWidget.SetEnabled(1)
#planeWidget.AddObserver("InteractionEvent", myCallback)

renderer.AddActor(selectActor)

###################################################################################################################################################################################################

#Interactor to handle mouse and keyboard events
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetInteractorStyle(MyInteractorStyle(parent = interactor))
interactor.SetRenderWindow(renwin)
#iren = vtk.vtkRenderWindowInteractor()
#iren.SetRenderWindow(renwin)


interactor.Initialize()
interactor.Start()