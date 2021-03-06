#!/usr/bin/env python
 
import sys
import vtk
import math
from PyQt4 import QtCore, QtGui
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtk.vtkImagingCorePython import vtkImageBlend
from vtk.vtkCommonDataModelPython import vtkPolyData
from math import sqrt
import multiprocessing
import s_rc
import time
from PyQt4.Qt import QPixmap, QThread, QTcpServer
from PyQt4.QtGui import QSplashScreen
 
class MainWindow(QtGui.QMainWindow):
    height = 80*1.78
    splineOrigin= (196,95)
    splineTop = 635
    splineCurvePoints = []
    height_default = {}
    firstlogin = True
    heightValue = 0
    typeIndex =1
    typeTF={}
    typeWords = ["","1.line","2.paracurve","3.Normal Distribution Curve","4.Bezier","5.upper bezier",""]
    cigmaNum = [20,15,50,50,80,80,10]
    bodyfile = "organ.stl"
    viewingType = False
    
    
    
    def initialHeight(self):
        for i in range(0,100):
            self.height_default[i] = 50
#         print(self.height_default[self.perHeight])
        pass
     
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setWindowTitle("FYP")
        #self.statusBar()
        self.initialHeight()
        self.p1 = multiprocessing.Process(target=self.setSliderHValue,args=(2,))
 
        self.frame = QtGui.QFrame()
        self.frame2 = QtGui.QFrame()
        self.frame3 = QtGui.QFrame()
        self.frame4 = QtGui.QFrame()
        
 
        self.vl = QtGui.QVBoxLayout()
        self.vl2 = QtGui.QVBoxLayout()
        self.vl3 = QtGui.QVBoxLayout()
        self.vl4 = QtGui.QVBoxLayout()
        
        self.vl.setContentsMargins(0, 10, 0, 10)
        self.vl2.setContentsMargins(0, 10, 0, 10)
        self.vl3.setContentsMargins(0, 10, 0, 10)
        self.vl4.setContentsMargins(0, 0, 0, 0)
        
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vtkWidget2 = QVTKRenderWindowInteractor(self.frame2)
        self.vtkWidget3 = QVTKRenderWindowInteractor(self.frame3)
        self.vtkWidget4 = QVTKRenderWindowInteractor(self.frame4)
        
        
        sld = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        sld.setValue(self.height/1.78)
        sld.setFocusPolicy(QtCore.Qt.NoFocus)
        sld.setGeometry(30, 40, 100, 30)
        sld.valueChanged[int].connect(self.changeValue)
        
        self.vl.addWidget(self.vtkWidget)
        self.vl.addWidget(sld)
        self.vl2.addWidget(self.vtkWidget2)
        self.vl3.addWidget(self.vtkWidget3)
        self.vl4.addWidget(self.vtkWidget4)
        
        self.ren = vtk.vtkRenderer()
        self.ren2 = vtk.vtkRenderer()
        self.ren3 = vtk.vtkRenderer()
        self.ren4 = vtk.vtkRenderer()
        
        self.ren.SetBackground(0.6, 0.6, 0.6)
        self.ren.SetBackground2(0.95, 0.95, 0.95)
        self.ren.GradientBackgroundOn()
        
        self.ren2.SetBackground(0.8, 0.8, 0.8)
        self.ren2.SetBackground2(0.95, 0.95, 0.95)
        self.ren2.GradientBackgroundOn()
        
        self.ren3.SetBackground(0.8, 0.8, 0.8)
        self.ren3.SetBackground2(0.95, 0.95, 0.95)
        self.ren3.GradientBackgroundOn()
        
        self.ren4.SetBackground(0.8, 0.8, 0.8)
        self.ren4.SetBackground2(0.95, 0.95, 0.95)
        self.ren4.GradientBackgroundOn()
        
        
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.vtkWidget2.GetRenderWindow().AddRenderer(self.ren2)
        self.vtkWidget3.GetRenderWindow().AddRenderer(self.ren3)
        self.vtkWidget4.GetRenderWindow().AddRenderer(self.ren4)
                
        
        self.renderWindowInteractor = self.vtkWidget.GetRenderWindow().GetInteractor()
        self.renderWindowInteractor2 = self.vtkWidget2.GetRenderWindow().GetInteractor()
        self.renderWindowInteractor3 = self.vtkWidget3.GetRenderWindow().GetInteractor()
        self.renderWindowInteractor4 = self.vtkWidget4.GetRenderWindow().GetInteractor()
        
        
        style = vtk.vtkInteractorStyleTrackballCamera()
        style2 =vtk.vtkInteractorStyleAreaSelectHover()
        style3 =vtk.vtkInteractorStyleAreaSelectHover()
        style4 =vtk.vtkInteractorStyleAreaSelectHover()
        
        
        self.renderWindowInteractor.SetInteractorStyle(style)
        self.renderWindowInteractor2.SetInteractorStyle(style2)
        self.renderWindowInteractor3.SetInteractorStyle(style3)
        self.renderWindowInteractor4.SetInteractorStyle(style4)

        
        self.toolbar = self.theToolbar()
        self.body = self.humanBody()
        self.ren.AddActor(self.body)
        self.BodyCut = self.cutPlane(True)
        self.ren.AddActor(self.BodyCut)
        self.splineP = self.spinePlane()
        self.ren.AddActor(self.splineP)
        self.deformTypeWords = self.words("Whole Body")
        self.ren.AddActor(self.deformTypeWords)
        
        self.SecCut = self.cutPlane(False)
        self.ren2.AddActor(self.SecCut)
        self.ren2.AddActor(self.words("cross-section"))
        self.ren2.AddActor(self.wordsL())
        self.ren2.AddActor(self.wordsR())
        
        self.ren3.AddActor(self.spinePlane())
        self.ren3.AddActor(self.words("Create spline curve"))
        self.ren3.AddActor(self.x_ray())
        
        self.splinecur = self.SplineCurve(True)
        self.ren4.AddActor(self.splinecur)
        self.ren4.AddActor(self.words("Spline curve"))

        
        
        self.ren.ResetCamera()
        self.ren2.ResetCamera()
        self.ren3.ResetCamera()
        self.ren4.ResetCamera()
        
        self.frame.setLayout(self.vl)
        self.frame2.setLayout(self.vl2)
        self.frame3.setLayout(self.vl3)
        self.frame4.setLayout(self.vl4)
        
        self.setCentralWidget(self.splitter())
        
        self.p1.start()
        self.show()
        self.AddObserverOfRen3()
        self.speedup()
        self.renderWindowInteractor.Initialize()
        self.renderWindowInteractor2.Initialize()
        self.renderWindowInteractor3.Initialize()
        self.renderWindowInteractor4.Initialize()  
        
        self.showFullScreen()  

    def humanBody(self):
        #Load stl file
        filename = self.bodyfile
        # Create a reader
        self.reader = vtk.vtkSTLReader()
        self.reader.SetFileName(filename)
        
        #make the actor smooth
        smoothFiliter = vtk.vtkSmoothPolyDataFilter()
        if vtk.VTK_MAJOR_VERSION <= 5:
            smoothFiliter.SetInput(self.reader.GetOutput())
        else:
            smoothFiliter.SetInputConnection(self.reader.GetOutputPort())
        smoothFiliter.SetNumberOfIterations(200)
        smoothFiliter.Update()
        #finish smooth      
        
        #compute normal and make the model smooth
        self.normFilter = vtk.vtkPolyDataNormals()
        self.normFilter.SetInputConnection(smoothFiliter.GetOutputPort())
        self.normFilter.SetComputePointNormals(1)
        self.normFilter.SetComputeCellNormals(1)
        self.normFilter.Update()
        #finish compute normal
        
        
        
        if self.firstlogin:
            self.universalEdges = self.normFilter
            EdgesFile = self.normFilter
            self.firstlogin = False
        else:
            EdgesFile = self.universalEdges
            
            
        if self.viewingType:
            extractEdges = vtk.vtkExtractEdges()
            extractEdges.SetInputConnection(self.universalEdges.GetOutputPort())
            extractEdges.Update()
            EdgesFile = extractEdges
            pass
        else:
            EdgesFile = self.universalEdges
            pass
        
        # Create a mapper
        mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(self.reader.GetOutput())
        else:
            mapper.SetInputConnection(EdgesFile.GetOutputPort())
        
        # Create an actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(0.596,0.961,1)
        actor.RotateX(90)
        actor.RotateZ(30)
        actor.RotateY(180)
        
        #Finish loading stl file
        return actor
    
    def AddPoint(self,x,y,z):
        # Create the geometry of a point (the coordinate)
        points = vtk.vtkPoints()
        p = [x, y, z]
 
        # Create the topology of the point (a vertex)
        vertices = vtk.vtkCellArray()
 
        id = points.InsertNextPoint(p)
        vertices.InsertNextCell(1)
        vertices.InsertCellPoint(id)
 
        # Create a polydata object
        point = vtk.vtkPolyData()
 
        # Set the points and vertices we created as the geometry and topology of the polydata
        point.SetPoints(points)
        point.SetVerts(vertices)
 
        # Visualize
        mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(point)
        else:
            mapper.SetInputData(point)
 
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetPointSize(5)
        actor.GetProperty().SetColor(0,0.1,0.9)
        return actor
    
    def x_ray(self):
        #get the image
        reader = vtk.vtkJPEGReader()
        reader.SetFileName('x.JPG')
        reader.Update()
        
        imageBlend = vtkImageBlend()
        imageBlend.SetInputConnection(0,reader.GetOutputPort())
        imageBlend.SetOpacity(0, 0.5)
        imageBlend.Update()
        
        imageActor = vtk.vtkImageActor()
        imageActor.SetInputData(reader.GetOutput())
        imageActor.SetOpacity(0.5)
        #imageActor.SetScale(0.1, 0.1, 0.1)
        
        sliceActor = self.spinePlane()
        #print(sliceActor.GetBounds())
        bs=sliceActor.GetBounds()
        #print bs
        igs = imageActor.GetBounds()
        scaleNum = max((-bs[0]-80+bs[1])/igs[1],(bs[3]-bs[2])/igs[3]/1.1)
        
        imageActor.SetScale(scaleNum, scaleNum, 0.1)
        imageActor.SetOrigin(bs[0]-16, 0+38, 0)
        
        #print(imageActor.GetOrigin())
        return imageActor
    
    def splitter(self):
        #Create layout 

        Form = QtGui.QWidget()
        Form2 = QtGui.QWidget()
        
        splitter1 = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter1.addWidget(self.setupUI2(Form2))
        splitter1.addWidget(self.setupUI1(Form))
        
        splitter2 = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(self.frame4)
        
        splitter3 = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter3.addWidget(splitter2)
        splitter3.addWidget(self.frame2)
        
        splitter4 = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter4.addWidget(self.frame3)
        splitter4.addWidget(self.frame)
        splitter4.addWidget(splitter3)
        #Finish layout
        
        return splitter4

    def theToolbar(self):
        # Toolbar
        exitAction = QtGui.QAction(QtGui.QIcon('exit24.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip("Leave the App")
        exitAction.triggered.connect(self.handleQuit)
        
        loadAction = QtGui.QAction(QtGui.QIcon('5.png'),'Load',self)
        loadAction.setShortcut('Ctrl+S')
        loadAction.triggered.connect(self.handleLoad)
        
        cutAction = QtGui.QAction(QtGui.QIcon('4.png'),'Cut',self)
        cutAction.setShortcut('Ctrl+K')
        cutAction.triggered.connect(self.handleSave)
        
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)
        self.toolbar.addAction(loadAction)
        self.toolbar.addAction(cutAction)
        self.setStyleSheet("""QToolBar {
             background-color: #ffffff;
        }""")
        #Finish Toolbar
        return self.toolbar

    def handleSave(self):
        stlWriter = vtk.vtkSTLWriter()
        triangleFilter = vtk.vtkTriangleFilter()
        clean = vtk.vtkCleanPolyData()
        triangleFilter.SetInputConnection(self.universalEdges.GetOutputPort())
        clean.SetInputConnection(triangleFilter.GetOutputPort())
        stlWriter.SetFileName("out.stl")
        stlWriter.SetInputConnection(clean.GetOutputPort())
        stlWriter.Write()
        print "output success"
        pass
    
    def handleQuit(self):
        choice = QtGui.QMessageBox.question(self,"Extract!","Leave the App?",QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            sys.exit()
        else:
            pass
    
    def handleLoad(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/Users/aaronhu/Desktop', 'STL *.stl')
        self.bodyfile  = fname.__str__()
        
        self.ren.RemoveActor(self.body)
        self.ren.RemoveActor(self.BodyCut)
        self.ren.RemoveActor(self.splineP)
        
        
        self.body = self.humanBody()
        self.ren.AddActor(self.body)
        self.BodyCut = self.cutPlane(True)
        self.ren.AddActor(self.BodyCut)
        self.splineP = self.spinePlane()
        self.ren.AddActor(self.splineP)
        self.ren.ResetCamera()
        print fname
        
        #havent done  
        
    def speedup(self):
        fname = ""
        self.bodyfile  = fname.__str__()
        
        self.ren.RemoveActor(self.body)
        self.ren.RemoveActor(self.BodyCut)
        self.ren.RemoveActor(self.splineP)
        
        
        self.body = self.humanBody()
        self.ren.AddActor(self.body)
        self.BodyCut = self.cutPlane(True)
        self.ren.AddActor(self.BodyCut)
        self.splineP = self.spinePlane()
        self.ren.AddActor(self.splineP)
        self.ren.ResetCamera()
        
    def SplineCurve(self, first):
        polygonActor = vtk.vtkActor()
        if first:
            # Create five points. 
            origin = [0.0, 0.0, 0.0]
            p0 = [0.0, 5.0, 0.0]
            p1 = [0.0, 10.0, 0.0]
   
            # Create a vtkPoints object and store the points in it
            points = vtk.vtkPoints()
            points.InsertNextPoint(origin)
            points.InsertNextPoint(p0)
            points.InsertNextPoint(p1)

            # Create a cell array to store the lines in and add the lines to it
            lines = vtk.vtkCellArray()
            for i in range(2):
              line = vtk.vtkLine()
              line.GetPointIds().SetId(0,i)
              line.GetPointIds().SetId(1,i+1)
              lines.InsertNextCell(line)
             
            # Create a polydata to store everything in
            linesPolyData = vtk.vtkPolyData()
             
            # Add the points to the dataset
            linesPolyData.SetPoints(points)
             
            # Add the lines to the dataset
            linesPolyData.SetLines(lines)
             
            # Setup actor and mapper
            mapper = vtk.vtkPolyDataMapper()
            if vtk.VTK_MAJOR_VERSION <= 5:
                mapper.SetInput(linesPolyData)
            else:
                mapper.SetInputData(linesPolyData)
            polygonActor.GetProperty().SetColor(0,0,0)
            polygonActor.SetMapper(mapper)
            
        else:
            points = vtk.vtkPoints()
            for point in self.splineCurvePoints:
                p = [point[0],point[1],0]
                points.InsertNextPoint(p)
                
            lines = vtk.vtkCellArray()
            #lines.InsertNextCell(len(self.splineCurvePoints))
            for i in range(len(self.splineCurvePoints)-1):
                line = vtk.vtkLine()
                line.GetPointIds().SetId(0,i)
                line.GetPointIds().SetId(1,i+1)
                lines.InsertNextCell(line)
            
            polygon = vtk.vtkPolyData()
            polygon.SetPoints(points)
            polygon.SetLines(lines)
     
            # vtkPolyDataMapper is a class that maps polygonal data (i.e., vtkPolyData)
            # to graphics primitives
            polygonMapper = vtk.vtkPolyDataMapper()
            if vtk.VTK_MAJOR_VERSION <= 5:
                polygonMapper.SetInputConnection(polygon.GetProducerPort())
            else:
                polygonMapper.SetInputData(polygon)
                polygonMapper.Update()
                
            polygonActor.GetProperty().SetColor(255,255,0)
            polygonActor.SetMapper(polygonMapper)
        return polygonActor
    
    def makeSplineCurve(self):
        points = vtk.vtkPoints()
        for point in self.splineCurvePoints:
                p = [point[0],point[1],0]
                points.InsertNextPoint(p)
        
        xSpline = vtk.vtkKochanekSpline()
        spline = vtk.vtkParametricSpline()
        spline.SetXSpline(xSpline)
        spline.SetPoints(points);
        functionSource = vtk.vtkParametricFunctionSource()
        functionSource.SetParametricFunction(spline);
        functionSource.Update();
        
        #create mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(functionSource.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(0,0,255)
        return actor
        
        
        pass
    
    def spinePlane(self):
        plane=vtk.vtkPlane()
        plane.SetOrigin(0,0,0)
        #print(self.height)
        plane.SetNormal(-0.4,0.7,0)
        cutter=vtk.vtkCutter()
        cutter.SetCutFunction(plane)
        cutter.SetInputConnection(self.universalEdges.GetOutputPort())
        cutter.Update()
        cutterMapper=vtk.vtkPolyDataMapper()
        cutterMapper.SetInputConnection( cutter.GetOutputPort())
        #create plane actor
        planeActor=vtk.vtkActor()
        planeActor.GetProperty().SetColor(1,1,0)
        planeActor.GetProperty().SetLineWidth(2)
        planeActor.SetMapper(cutterMapper)
        planeActor.RotateX(90)
        planeActor.RotateZ(30)
        planeActor.RotateY(180)
        return planeActor
    
    def cutPlane(self, human):
        #create slice
        #create an plane
        plane=vtk.vtkPlane()
        plane.SetOrigin(0,0,self.height)
        #print(self.height)
        plane.SetNormal(0,0,1)
        cutter=vtk.vtkCutter()
        cutter.SetCutFunction(plane)
        cutter.SetInputConnection(self.universalEdges.GetOutputPort())
        cutter.Update()
        cutterMapper=vtk.vtkPolyDataMapper()
        cutterMapper.SetInputConnection( cutter.GetOutputPort())
        #create plane actor
        planeActor=vtk.vtkActor()
        planeActor.GetProperty().SetColor(1,0,0)
        if human:
            planeActor.GetProperty().SetLineWidth(4)
        else:
            planeActor.GetProperty().SetLineWidth(1)
        planeActor.SetMapper(cutterMapper) 
        if human:
             planeActor.RotateX(90)
             planeActor.RotateZ(30)
             planeActor.RotateY(180)
        else:
            planeActor.RotateX(0)
            planeActor.RotateZ(150)
            planeActor.RotateY(0)
        #finish slice
        return planeActor
    
    def words(self,content):
        # create a text actor
        txt = vtk.vtkTextActor()
        txt.SetInput(content)
        txtprop=txt.GetTextProperty()
        txtprop.SetFontFamilyToArial()
        txtprop.SetFontSize(18)
        txtprop.SetColor(1,0,0)
        txt.SetDisplayPosition(20,30)
        return txt
    
    def wordsL(self):
        # create a text actor
        txt = vtk.vtkTextActor()
        txt.SetInput("L")
        txtprop=txt.GetTextProperty()
        txtprop.SetFontFamilyToArial()
        txtprop.SetFontSize(10)
        txtprop.SetColor(0.4,0.4,0.4)
        txt.SetDisplayPosition(50,200)
        return txt
    
    def wordsR(self):
        # create a text actor
        txt = vtk.vtkTextActor()
        txt.SetInput("R")
        txtprop=txt.GetTextProperty()
        txtprop.SetFontFamilyToArial()
        txtprop.SetFontSize(10)
        txtprop.SetColor(0.4,0.4,0.4)
        txt.SetDisplayPosition(350,200)
        
        return txt
    
    def changeSpline(self):
        
        if len(self.splineCurvePoints) >1:
            self.ren4.RemoveActor(self.splinecur)
            self.splinecur = self.makeSplineCurve()
            self.ren4.AddActor(self.splinecur)
            self.ren4.ResetCamera()
            self.renderWindowInteractor4.Render()
        else:
            pass
    
    def setSliderHValue(self,interval):
        #print self.height_default[self.heightValue]
        self.horizontalSlider.setValue(self.height_default[self.heightValue])
        pass
     
    def changeValue(self, value):
        self.ren.RemoveActor(self.BodyCut)
        self.ren2.RemoveActor(self.SecCut)
        
        #self.horizontalSlider.setValue(self.height_default[value])
        self.height = value*1.78
        self.heightValue = value
        self.p1.run()
        
        self.BodyCut = self.cutPlane(True)
        self.SecCut = self.cutPlane(False)
        
        self.ren.AddActor(self.BodyCut)
        self.ren2.AddActor(self.SecCut)
        self.ren2.ResetCamera()
        
        self.renderWindowInteractor.Render()
        self.renderWindowInteractor2.Render()
    
    def HandleAddPoints(self, obj, ev):
        mousePosition = self.renderWindowInteractor3.GetEventPosition()
        print(mousePosition)
        origin = self.splineOrigin
        windowSize = (self.frame.width(),self.splineTop - origin[1])
        bounds = self.spinePlane().GetBounds()
        bounds2 = self.x_ray().GetBounds()

        width = bounds2[1]-bounds2[0]
        height = bounds2[3]-bounds[2]
        #print(bounds)
        
        pointX = (mousePosition[0]-origin[0])/(windowSize[0]/width)
        pointY = (mousePosition[1]-origin[1])/(windowSize[1]/height)
        
        print(pointX,pointY)
        if mousePosition[1]>origin[1] and mousePosition[1]<self.splineTop:
            self.ren3.AddActor(self.AddPoint(pointX, pointY, 0))
            self.AddPointToListBySort((int(pointX),int(pointY)))
            
        self.renderWindowInteractor3.Render()
    
    def HandleReleasePoints(self, obj, ev):
        pass
    
    def AddObserverOfRen3(self):
        self.renderWindowInteractor3.RemoveObservers('LeftButtonPressEvent')
        self.renderWindowInteractor3.AddObserver('LeftButtonPressEvent', self.HandleAddPoints, 1.0)
        self.renderWindowInteractor3.AddObserver('LeftButtonPressEvent',self.HandleReleasePoints,-1.0)
    
    def AddPointToListBySort(self,point):
        if(self.splineCurvePoints == []):
            self.splineCurvePoints.append(point)
        else:
            for index in range(len(self.splineCurvePoints)) :
                p = self.splineCurvePoints[index]
                if(p[1]>point[1]):
                    self.splineCurvePoints.insert(index, point)
                    return
            self.splineCurvePoints.append(point)
    
    def handleChangeType(self):
        if(self.viewingType):
            self.viewingType = False
            pass
        else:
            pass
            self.viewingType = True
        
        self.ren.RemoveActor(self.body)
        self.body = self.humanBody()
        self.ren.AddActor(self.body)
        self.renderWindowInteractor.Render()
        
        pass
    
    def setupUI1(self,Form):
        Form.setObjectName("Form")
        Form.resize(130, 170)
        Form.setMouseTracking(False)
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tabWidget = QtGui.QTabWidget(Form)
        self.tabWidget.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.tabWidget.setMouseTracking(True)
        self.tabWidget.setTabPosition(QtGui.QTabWidget.North)
        self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.setElideMode(QtCore.Qt.ElideLeft)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidgetPage1 = QtGui.QWidget()
        #first tab
        self.tabWidgetPage1.setObjectName("tabWidgetPage1")
        self.verticalLayout = QtGui.QVBoxLayout(self.tabWidgetPage1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton = QtGui.QPushButton(self.tabWidgetPage1)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.handleChangeType)
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtGui.QPushButton(self.tabWidgetPage1)
        self.pushButton_2.clicked.connect(self.handleType)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtGui.QPushButton(self.tabWidgetPage1)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.deleteAllPoints)
        self.verticalLayout.addWidget(self.pushButton_3)
        self.pushButton_4 = QtGui.QPushButton(self.tabWidgetPage1)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout.addWidget(self.pushButton_4)
        self.pushButton_4.clicked.connect(self.changeSpline)
        self.tabWidget.addTab(self.tabWidgetPage1, "")
        self.tabWidgetPage2 = QtGui.QWidget()
        self.tabWidgetPage2.setObjectName("tabWidgetPage2")
        #second tab
        self.verticalLayout2 = QtGui.QVBoxLayout(self.tabWidgetPage2)
        self.verticalLayout2.setObjectName("verticalLayout2")
        self.buttonBox = QtGui.QDialogButtonBox(self.tabWidgetPage2)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.clicked.connect(self.initialHeight)
        self.horizontalSlider = QtGui.QSlider(self.tabWidgetPage2)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.setValue(50)
        self.horizontalSlider.valueChanged[int].connect(self.deformSurface)
        
        self.verticalLayout2.addWidget(self.horizontalSlider)
        self.verticalLayout2.addWidget(self.buttonBox)
        self.tabWidget.addTab(self.tabWidgetPage2, "")
        self.horizontalLayout_2.addWidget(self.tabWidget)
        self.horizontalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)
        return Form
    
    def retranslateUi(self, Form):
        self.pushButton.setText("Viewing Type")
        self.pushButton_2.setText("Deform Type")
        self.pushButton_3.setText("Delete All")
        self.pushButton_4.setText("Finish")
    
    def setupUI2(self,Form):
        Form.setObjectName("Form")
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.treeWidget = QtGui.QTreeWidget(Form)
        self.treeWidget.setObjectName("treeWidget")
        self.verticalLayout.addWidget(self.treeWidget)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi2(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        return Form
    
    def retranslateUi2(self, Form):
        self.treeWidget.headerItem().setText(0,"Task")
        self.treeWidget.headerItem().setText(1,"Date")
        self.treeWidget.headerItem().setText(2,"Action")
    
    def deleteAllPoints(self):
        self.ren3.RemoveAllViewProps()
        
        self.ren3.AddActor(self.spinePlane())
        self.ren3.AddActor(self.words("Create spline curve"))
        self.ren3.AddActor(self.x_ray())
        self.splineCurvePoints = []
        
        self.ren4.RemoveActor(self.splinecur)
        self.splinecur = self.SplineCurve(True)
        self.ren4.AddActor(self.splinecur)
        
        self.ren4.ResetCamera()
        self.renderWindowInteractor4.Render()
        self.renderWindowInteractor3.Render()
    
    def handleType(self):
        for i in range(0,6):
            self.typeTF[i]=False
        
        self.typeIndex =self.typeIndex+1
        self.ren.RemoveActor(self.deformTypeWords)
        
        if(self.typeIndex>=6):
            self.typeIndex =1
        
        
        self.cigma = self.cigmaNum[self.typeIndex]
        self.typeTF[self.typeIndex] = True
        
        
        self.deformTypeWords = self.words(self.typeWords[self.typeIndex])
        self.ren.AddActor(self.deformTypeWords)
        self.renderWindowInteractor.Render()
        
        self.initialHeight()
        
        pass
    
    def deformSurface(self,value):
        default = self.height_default[int(self.height/1.78)]
        change = (value - default)/100.0*20
        self.height_default[self.height/1.78] = value
        points = self.universalEdges.GetOutput().GetPoints()
        if len(self.typeTF) ==0:
            line = True
            paracurve = False
            uniparacurve = False
            beizer = False
            upcurve = False
            change = (value - default)/100.0*3
            self.cigma = 15
        else:
            line = self.typeTF[1]
            paracurve = self.typeTF[2]
            uniparacurve = self.typeTF[3]
            beizer = self.typeTF[4]
            upcurve = self.typeTF[5]
        
        for point in range(0,points.GetNumberOfPoints()):
            #unversal paracurve test
            if uniparacurve:
                a = change/(self.height*self.height-178*self.height)
                x = points.GetPoint(point)[2]
                y = a*x*x-178*a*x
                newX = points.GetPoint(point)[0] - y
                newY = points.GetPoint(point)[1] - y/sqrt(3)
                newPoint = [newX,newY,points.GetPoint(point)[2]]
                self.universalEdges.GetOutput().GetPoints().SetPoint(point,newPoint)
                pass
            
            if upcurve:
                if points.GetPoint(point)[2]>self.height:
                    t = (points.GetPoint(point)[2]-self.height+self.cigma)/self.cigma
                    y = change*2*t*(1-t)
                    #print t
                    newX = points.GetPoint(point)[0] - y
                    newY = points.GetPoint(point)[1] - y/sqrt(3)
                else:
                    newX = points.GetPoint(point)[0] 
                    newY = points.GetPoint(point)[1] 
                newPoint = [newX,newY,points.GetPoint(point)[2]]
                self.universalEdges.GetOutput().GetPoints().SetPoint(point,newPoint)
            
            
            elif self.height+self.cigma>points.GetPoint(point)[2]>self.height-self.cigma:
                if paracurve:
                    #test with para-curve
                    x = (points.GetPoint(point)[2]-self.height)
                    y = -change/(self.cigma*self.cigma)*x*x+change
                    newX = points.GetPoint(point)[0] - y
                    newY = points.GetPoint(point)[1] - y/sqrt(3)
                    
                if beizer:
                    t = (points.GetPoint(point)[2]-self.height+self.cigma)/self.cigma/2
                    y = change*2*t*(1-t)
                    #print t
                    newX = points.GetPoint(point)[0] - y
                    newY = points.GetPoint(point)[1] - y/sqrt(3)
                    pass
                
                
                if line:
                    #compute change of two axis
                    change = (value - default)/100.0*3
                    if points.GetPoint(point)[2]>self.height:
                        #not finish
                        newX = points.GetPoint(point)[0] + change*(points.GetPoint(point)[2]-self.height-self.cigma)/3
                        newY = points.GetPoint(point)[1] + change*(points.GetPoint(point)[2]-self.height-self.cigma)/3/sqrt(3)
                    elif points.GetPoint(point)[2]<self.height:
                        newX = points.GetPoint(point)[0] + change*(self.height-self.cigma-points.GetPoint(point)[2])/3
                        newY = points.GetPoint(point)[1] + change*(self.height-self.cigma-points.GetPoint(point)[2])/3/sqrt(3)
                    else:
                        newX = points.GetPoint(point)[0] + change*(points.GetPoint(point)[2]-self.height)
                        newY = points.GetPoint(point)[1] + change*(points.GetPoint(point)[2]-self.height)/sqrt(3)
                    
                    
                newPoint = [newX,newY,points.GetPoint(point)[2]]
                self.universalEdges.GetOutput().GetPoints().SetPoint(point,newPoint)
                
        self.ren.RemoveActor(self.body)
        self.body = self.humanBody()
        self.ren.AddActor(self.body)
        self.renderWindowInteractor.Render()
        pass 
    
        
if __name__ == "__main__":
    
    app = QtGui.QApplication(sys.argv)

    splash= QSplashScreen(QPixmap(":/p/pic.jpg"))
    splash.show()
    str = "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
    app.processEvents()
    splash.showMessage(str+"          Loading...")
    time.sleep(0.2)
    app.processEvents()
    splash.showMessage(str+"          Importing Qt...100%")
    time.sleep(0.2)
    app.processEvents()
    splash.showMessage(str+"          Importing VTK...100%")
    time.sleep(0.2)
    app.processEvents()
    splash.showMessage(str+"          Rendering interface...37%")
    time.sleep(0.2)
    app.processEvents()
    splash.showMessage(str+"          Rendering interface...55%")
    time.sleep(0.3) 
    app.processEvents()  
    splash.showMessage(str+"          Rendering interface...100%")
    time.sleep(0.2)
    app.processEvents()
    splash.showMessage(str+"          Rendering Model...31%")
    time.sleep(0.4)
    app.processEvents()
    splash.showMessage(str+"          Rendering Model...47%")
    time.sleep(0.1)
    app.processEvents()
    splash.showMessage(str+"          Rendering Model...100%")
    time.sleep(0.2)
    app.processEvents()
    splash.showMessage(str+"          Generating Spline Curve...100%")
    time.sleep(0.3)
    app.processEvents()
    splash.showMessage(str+"          Generating Body...23%")
    time.sleep(0.1)
    app.processEvents()
    splash.showMessage(str+"          Generating Body...54%")
    time.sleep(0.3)
    app.processEvents()
    splash.showMessage(str+"          Generating Body...100%")
    time.sleep(0.2)
    app.processEvents()
    
    #window = MainWindow()
    splash.finish(MainWindow())
    sys.exit(app.exec_())
