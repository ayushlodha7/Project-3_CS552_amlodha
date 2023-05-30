import vtk

# 100^3 Sampling dataset of the Quadric function

# F(x,y,z) = 1*x^2 + 0.6*y^2 + 0.2*z^2 + 0*x*y + 0*y*z + 0.1*x*z + 0.2*x + 0*y + 0*z + 0

quadric = vtk.vtkQuadric()
quadric.SetCoefficients(1, 0.6, 0.2, 0, 0, 0.1, 0.2, 0, 0, 0)


sample = vtk.vtkSampleFunction()
sample.SetSampleDimensions(100, 100, 100)
sample.SetImplicitFunction(quadric)

min = 0.05  # Slider minimum value
max = 1.5  # Slider maximum value

# computing a contour of an input data.
isosurface = vtk.vtkContourFilter()
isosurface.SetInputConnection(sample.GetOutputPort())
isosurface.SetValue(0, (min + max) / 2)

isosurfaceMapper = vtk.vtkPolyDataMapper()
isosurfaceMapper.SetInputConnection(isosurface.GetOutputPort())
isosurfaceMapper.SetColorModeToMapScalars()

isosurfaceActor = vtk.vtkActor()
isosurfaceActor.SetMapper(isosurfaceMapper)

# Create the outline
outline = vtk.vtkOutlineFilter()
outline.SetInputConnection(sample.GetOutputPort())

outlineMapper = vtk.vtkPolyDataMapper()
outlineMapper.SetInputConnection(outline.GetOutputPort())

outlineActor = vtk.vtkActor()
outlineActor.SetMapper(outlineMapper)
outlineActor.GetProperty().SetColor(1, 1, 1)

# Sliding window plane feature
plane = vtk.vtkPlane()
clipper = vtk.vtkClipPolyData()
clipper.SetInputConnection(isosurface.GetOutputPort())
clipper.SetClipFunction(plane)
clipper.InsideOutOn()

selectMapper = vtk.vtkPolyDataMapper()
selectMapper.SetInputConnection(clipper.GetOutputPort())

selectActor = vtk.vtkLODActor()
selectActor.SetMapper(selectMapper)
selectActor.GetProperty().SetColor(0, 1, 0)
selectActor.SetScale(1.01, 1.01, 1.01)

ren = vtk.vtkRenderer()
ren.SetBackground(0, 0, 0)
renWin = vtk.vtkRenderWindow()
renWin.SetSize(500, 500)
renWin.AddRenderer(ren)

ren.AddActor(outlineActor)
ren.AddActor(isosurfaceActor)
ren.AddActor(selectActor)

renWinInteractor = vtk.vtkRenderWindowInteractor()
renWinInteractor.SetRenderWindow(renWin)

def myCallback(obj, event):
    global plane, selectActor
    obj.GetPlane(plane)
    selectActor.VisibilityOn() 

planeWidget = vtk.vtkImplicitPlaneWidget()
planeWidget.SetInteractor(renWinInteractor)
planeWidget.SetPlaceFactor(1)
planeWidget.SetInputConnection(isosurface.GetOutputPort())
planeWidget.PlaceWidget()
planeWidget.AddObserver("InteractionEvent", myCallback)
planeWidget.On()  # ImplicitPlaneWidget end


#  Interactive Slider representation
def vtkSliderCallback2(obj, event):
    sliderRepres = obj.GetRepresentation()
    pos = sliderRepres.GetValue()
    isosurface.SetValue(0, pos)

SliderRepres = vtk.vtkSliderRepresentation2D()
SliderRepres.SetMinimumValue(min)
SliderRepres.SetMaximumValue(max)
SliderRepres.SetValue(0.1)
SliderRepres.SetTitleText("Interactive Slider")
SliderRepres.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
SliderRepres.GetPoint1Coordinate().SetValue(0.3, 0.05)
SliderRepres.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
SliderRepres.GetPoint2Coordinate().SetValue(0.7, 0.05)
SliderRepres.SetSliderLength(0.02)
SliderRepres.SetSliderWidth(0.03)
SliderRepres.SetEndCapLength(0.01)
SliderRepres.SetEndCapWidth(0.03)
SliderRepres.SetTubeWidth(0.005)
SliderRepres.SetTitleHeight(0.02)
SliderRepres.SetLabelHeight(0.02)
SliderRepres.GetSelectedProperty().SetColor(0, 1, 0)

SliderWidget = vtk.vtkSliderWidget()
SliderWidget.SetInteractor(renWinInteractor)
SliderWidget.SetRepresentation(SliderRepres)
SliderWidget.KeyPressActivationOff()
SliderWidget.SetAnimationModeToAnimate()
SliderWidget.SetEnabled(True)
SliderWidget.AddObserver("EndInteractionEvent", vtkSliderCallback2)

renWinInteractor.Initialize()
renWin.Render()
SliderWidget.EnabledOn()
renWinInteractor.Start()