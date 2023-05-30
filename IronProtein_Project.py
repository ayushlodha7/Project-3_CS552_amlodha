#importting the vtk
import vtk
# Read the Iron Protein dataset
filename = "ironProt.vtk"
reader = vtk.vtkStructuredPointsReader()
reader.SetFileName(filename)
reader.Update()

min = 0  # Slider minimum value
max = 500  # Slider maximum value

#Isosurface Contour Filter
isosurface = vtk.vtkContourFilter()
isosurface.SetInputConnection(reader.GetOutputPort())
isosurface.SetValue(0, (min + max)/2)

#Cleaning the polyData
clean = vtk.vtkCleanPolyData()
clean.SetInputConnection(isosurface.GetOutputPort())

# Normals of the PolyData
normals = vtk.vtkPolyDataNormals()
normals.SetInputConnection(isosurface.GetOutputPort())
normals.SetFeatureAngle(45)

isosurfaceMapper = vtk.vtkPolyDataMapper()
isosurfaceMapper.SetInputConnection(normals.GetOutputPort())
isosurfaceMapper.SetColorModeToMapScalars()

isosurfaceActor = vtk.vtkActor()
isosurfaceActor.SetMapper(isosurfaceMapper)

outline = vtk.vtkOutlineFilter()
outline.SetInputConnection(reader.GetOutputPort())
outlineMapper = vtk.vtkPolyDataMapper()
outlineMapper.SetInputConnection(outline.GetOutputPort())
outlineActor = vtk.vtkActor()
outlineActor.SetMapper(outlineMapper)
outlineActor.GetProperty().SetColor(0.0, 0.0, 0.0)

ren = vtk.vtkRenderer()
ren.SetBackground(0.88, 0.74, 0.52) # light brown background
renWin = vtk.vtkRenderWindow()
renWin.SetSize(500, 500)
renWin.AddRenderer(ren)

iren = vtk.vtkRenderWindowInteractor()
iren.SetSize(1500, 1500)
iren.SetRenderWindow(renWin)

ren.AddActor(outlineActor)

# Set dark brown color to isosurface actor
isosurfaceActor.GetProperty().SetColor(0.4, 0.2, 0.0)
ren.AddActor(isosurfaceActor)

# Clipping of the dataset which is used for Creating the Sliding Window which 
# shows the cross section
plane = vtk.vtkPlane()
clipper = vtk.vtkClipPolyData()
clipper.SetInputConnection(isosurface.GetOutputPort())
clipper.SetClipFunction(plane)
clipper.InsideOutOn()

selectMapper = vtk.vtkPolyDataMapper()
selectMapper.SetInputConnection(clipper.GetOutputPort())

selectActor = vtk.vtkLODActor()
selectActor.SetMapper(selectMapper)
selectActor.GetProperty().SetColor(0.4, 0.2, 0.0) # dark brown color to select actor
selectActor.SetScale(1.01, 1.01, 1.01)

ren.AddActor(selectActor)

iren.Initialize()

def myCallback(obj, event):
    global plane, selectActor
    obj.GetPlane(plane)
    selectActor.VisibilityOn()

# ImplicitPlaneWidget
planeWidget = vtk.vtkImplicitPlaneWidget()
planeWidget.SetInteractor(iren)
planeWidget.SetPlaceFactor(1)
planeWidget.SetInputConnection(reader.GetOutputPort())
planeWidget.PlaceWidget()
planeWidget.AddObserver("InteractionEvent", myCallback)
planeWidget.On()

# Iso-value slider callback
def vtkSliderCallback2(obj, event):
    sliderRepres = obj.GetRepresentation()
    pos = sliderRepres.GetValue()
    isosurface.SetValue(0, pos)

# Iso-value slider
SliderRepres = vtk.vtkSliderRepresentation2D()
SliderRepres.SetMinimumValue(min)
SliderRepres.SetMaximumValue(max)
SliderRepres.SetValue((min + max) / 2)
SliderRepres.SetTitleText("Iso-value")
SliderRepres.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
SliderRepres.GetPoint1Coordinate().SetValue(0.3, 0.05)
SliderRepres.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
SliderRepres.GetPoint2Coordinate().SetValue(0.7, 0.05)
SliderRepres.SetSliderLength(0.02)
SliderRepres.SetSliderWidth(0.035)
SliderRepres.SetEndCapLength(0.015)
SliderRepres.SetEndCapWidth(0.035)
SliderRepres.SetTubeWidth(0.0060)
SliderRepres.SetLabelFormat("%3.0lf")
SliderRepres.SetTitleHeight(0.02)
SliderRepres.SetLabelHeight(0.02)
SliderRepres.GetSelectedProperty().SetColor(0, 1, 0)

SliderWidget = vtk.vtkSliderWidget()
SliderWidget.SetInteractor(iren)
SliderWidget.SetRepresentation(SliderRepres)
SliderWidget.KeyPressActivationOff()
SliderWidget.SetAnimationModeToAnimate()
SliderWidget.SetEnabled(True)
SliderWidget.AddObserver("EndInteractionEvent", vtkSliderCallback2)

# Execute the Pipeline
renWin.Render()

# initialize and start the interactor
iren.Start()
