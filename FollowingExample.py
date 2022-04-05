#!/usr/bin/env python

#Creation of a pipeline

import vtk


def Frailejon_Ernesto_Perez():
    print("Hola, soy el Frailejon_Ernesto_Perez")
    colors=vtk.vtkNamedColors() #Color names are RGBA (A=alpha)

    #Set background color
    backgroundColor=map(lambda x:x/1, [11, 10, 25, 155])
    #A lambda function can take n number of arfuments but only one expression
    #It is a small anonymous function
    colors.SetColor("BkgColor", *backgroundColor)

    #Creates a poligonal cylinder model, number in set resolution 
    # is the number of faces, more faces more circular
    myCylinder=vtk.vtkCylinderSource()
    myCylinder.SetResolution(25)
    myCylinder2=vtk.vtkCylinderSource()
    myCylinder2.SetResolution(5)

    #Mapper - Push the geometry into the graphics library, also does color mapping 
    myCylinderMapper=vtk.vtkPolyDataMapper() #Class to map polygonal data to graphics primitives
    myCylinderMapper.SetInputConnection(myCylinder.GetOutputPort())
    myCylinderMapper2=vtk.vtkPolyDataMapper() #Class to map polygonal data to graphics primitives
    myCylinderMapper2.SetInputConnection(myCylinder2.GetOutputPort())

    #Actor, this is a grouping mechanism, and allows to insert a transformation matrix and/or
    #texture map.
    myCylinderActor=vtk.vtkActor()
    myCylinderActor.SetMapper(myCylinderMapper)
    myCylinderActor.GetProperty().SetColor(colors.GetColor3d("Green"))
    myCylinderActor.RotateX(0)
    myCylinderActor.RotateY(0)
    myCylinderActor.RotateZ(50)
    myCylinderActor2=vtk.vtkActor()
    myCylinderActor2.SetMapper(myCylinderMapper2)
    myCylinderActor2.GetProperty().SetColor(colors.GetColor3d("Red"))

    #Rederers - creates a graphic structure in the assigned window
    #The render window interactor allows to use the mouse events 
    #to perform camera or actor manipulation depending on the definition of the
    #events
    rendererCylinder=vtk.vtkRenderer()
    rendererWindow=vtk.vtkRenderWindow()
    rendererWindow.AddRenderer(rendererCylinder)
    interactorRenderer=vtk.vtkRenderWindowInteractor()
    interactorRenderer.SetRenderWindow(rendererWindow)

    #Add actors to the rederer and set background and size
    rendererCylinder.AddActor(myCylinderActor)
    rendererCylinder.AddActor(myCylinderActor2)
    rendererCylinder.SetBackground(colors.GetColor3d("BkgColor"))
    rendererWindow.SetSize(500,500)
    rendererWindow.SetWindowName("El Frailejon")

    #Initialize the interactor and must be before the event loop
    interactorRenderer.Initialize()

    #Playing witj zoom 
    rendererCylinder.ResetCamera()
    rendererCylinder.GetActiveCamera().Zoom(0.5)
    rendererWindow.Render()

    #Start event loop
    interactorRenderer.Start()


##if __name__=="__main__" 
##when python runs the __name__ variable it will be set as __main__ if the module is 
##the main program. If the code is imported from another module, then __name__ will be
# set to that module name

if __name__=="__main__":
    Frailejon_Ernesto_Perez()
    print("Hola Frailejon")