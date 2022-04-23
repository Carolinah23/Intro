#!/usr/bin/env python
from __future__ import print_function

import vtk

### Hw 5 - April/22/2022
### Alan Braeley - Carolina Hurtado-Pulido

#Interactor style that handles mouse and keyboard events
class MyInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
   
    def __init__(self,parent=None):
        self.parent = vtk.vtkRenderWindowInteractor()
        if(parent is not None):
          self.parent = parent
     
#Loads the data
imageReader = vtk.vtkStructuredPointsReader()
imageReader.SetFileName("./data/foot.vtk")
imageReader.Update()

'''
Question 1
'''
# Transfer mapping to control how opaque the tissue is
opacityTransferFunction = vtk.vtkPiecewiseFunction()
opacityTransferFunction.AddPoint(20, 0.0)
opacityTransferFunction.AddPoint(255, 0.5)

# Transfer mapping to control the colors
colorTransferFunction = vtk.vtkColorTransferFunction()
colorTransferFunction.AddRGBPoint(32.0, 0.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(64.0, 1.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(100.0, 0.0, 0.6, 0.5)
colorTransferFunction.AddRGBPoint(255.0, 1.0, 1.0, 1.0)


volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.SetColor(colorTransferFunction)
volumeProperty.SetScalarOpacity(opacityTransferFunction)
volumeProperty.ShadeOn()
volumeProperty.SetInterpolationTypeToLinear()

# The mapper / ray cast function know how to render the data
volumeMapper = vtk.vtkGPUVolumeRayCastMapper()
volumeMapper.SetBlendModeToComposite()
volumeMapper.SetInputConnection(imageReader.GetOutputPort())

# The volume holds the mapper and the property and also controls the position
volume = vtk.vtkVolume()
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)
'''
End of question 1
'''



'''
Question 2
'''
#A renderer that renders our geometry into the render window
renderer = vtk.vtkRenderer()
renderer.SetBackground(0.1, 0.1, 0.3)

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

#The render window
renwin = vtk.vtkRenderWindow()
renwin.AddRenderer(renderer)
renderer.AddVolume(volume)

renwin.SetSize(1000, 1000)
renwin.Render()

#Interactor to handle mouse and keyboard events
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetInteractorStyle(MyInteractorStyle(parent = interactor))
interactor.SetRenderWindow(renwin)

# Cut the volume
rta = vtk.vtkRTAnalyticSource()
rta.SetWholeExtent(0, 255, 0, 255, 0, 255)
rta.Update()

plane = vtk.vtkPlane()
plane.SetOrigin(10,10,10)
plane.SetNormal(2,1,1.5)
volumeMapper.AddClippingPlane(plane)

# Widget to manipulate the plane
# The cut plane
def MovePlane(widget, event_string):
    rep.GetPlane(plane)

rep = vtk.vtkImplicitPlaneRepresentation()
rep.SetPlaceFactor(1.0);
rep.PlaceWidget(rta.GetOutput().GetBounds())
rep.DrawPlaneOff()
rep.SetPlane(plane)

planeWidget = vtk.vtkImplicitPlaneWidget2()
planeWidget.SetInteractor(interactor)
planeWidget.SetRepresentation(rep);
planeWidget.AddObserver("InteractionEvent",MovePlane);
planeWidget.On()

renderer.AddActor(outlineActor)
renderer.ResetCamera()
'''
End of question 2
'''

interactor.Initialize()
interactor.Start()
