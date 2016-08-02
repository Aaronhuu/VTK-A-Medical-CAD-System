from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QApplication
import vtk
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import sys
from PyQt4.Qt import QGridLayout


 
class Ui_MainWindow(QtGui.QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 800)
        self.centralWidget = QtGui.QWidget(MainWindow)

        self.gridlayout = QtGui.QGridLayout(self.centralWidget)
        self.vtkWidget = QVTKRenderWindowInteractor(self.centralWidget)
        self.vtkWidget2 = QVTKRenderWindowInteractor(self.centralWidget)
        #self.hbox = QtGui.QHBoxLayout(self.centralWidget)
        
        
        label1= QtGui.QFrame(self)
        label1.setFrameShape(QtGui.QFrame.StyledPanel)
        
        
        label2= QtGui.QFrame(self)
        label2.setFrameShape(QtGui.QFrame.StyledPanel)
        
        
        
        label3= QtGui.QFrame(self)
        label3.setFrameShape(QtGui.QFrame.StyledPanel)
        
        #toolbar
        exitAction = QtGui.QAction(QtGui.QIcon('exit24.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(QtGui.qApp.quit)
        
        saveAction = QtGui.QAction(QtGui.QIcon('4.png'),'Save',self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.triggered.connect(QtGui.qApp.quit)
        
        cutAction = QtGui.QAction(QtGui.QIcon('5.png'),'Cut',self)
        cutAction.setShortcut('Ctrl+K')
        cutAction.triggered.connect(QtGui.qApp.quit)
        
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)
        self.toolbar.addAction(saveAction)
        self.toolbar.addAction(cutAction)
        
        #############image reading 
        label = QtGui.QLabel() 
        pixmap = QtGui.QPixmap('x.JPG')
        scaledpix = pixmap.scaled(430,610)
        label.setPixmap(scaledpix)
        ############## finish img
        
        self.splitter1 = QtGui.QSplitter(QtCore.Qt.Vertical)
        self.splitter1.addWidget(label3)
        self.splitter1.addWidget(label1)
        
        label4= QtGui.QFrame(self)
        label4.setFrameShape(QtGui.QFrame.StyledPanel)
        
        label5 = QtGui.QFrame(self)
        label5.setFrameShape(QtGui.QFrame.StyledPanel)
        
        splitter2 = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter2.addWidget(self.splitter1)
        splitter2.addWidget(label4)
        
        splitter3 = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter3.addWidget(splitter2)
        splitter3.addWidget(label5)
        
        
        
        self.gridlayout.addWidget(label,1,0)
        self.gridlayout.addWidget(self.vtkWidget, 1, 1)
        self.gridlayout.addWidget( self.toolbar , 0, 0, 1, 2)
        self.gridlayout.addWidget( splitter3 , 1, 3 )
        
        MainWindow.setCentralWidget(self.centralWidget)
          
    
    
        
class Example(QtGui.QMainWindow):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
        
    def initUI(self):               
        
        exitAction = QtGui.QAction(QtGui.QIcon('exit24.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(QtGui.qApp.quit)
        
        saveAction = QtGui.QAction(QtGui.QIcon('4.png'),'Save',self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.triggered.connect(QtGui.qApp.quit)
        
        cutAction = QtGui.QAction(QtGui.QIcon('5.png'),'Cut',self)
        cutAction.setShortcut('Ctrl+K')
        cutAction.triggered.connect(QtGui.qApp.quit)
        
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)
        self.toolbar.addAction(saveAction)
        self.toolbar.addAction(cutAction)
        
        self.setGeometry(300, 300, 1280, 720)
        self.setWindowTitle('Toolbar')    
        self.show()

class ViewShape(QtGui.QMainWindow):
 
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ren = vtk.vtkRenderer()
        self.ui.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.ui.vtkWidget.GetRenderWindow().GetInteractor()
        
        
        
        filename = "organ.stl"
        # Create a reader
        reader = vtk.vtkSTLReader()
        reader.SetFileName(filename)
        
 
        # Create a mapper
        mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(reader.GetOutput())
        else:
            mapper.SetInputConnection(reader.GetOutputPort())

        # Create an actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.RotateX(-90)
        
        self.ren.AddActor(actor)
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    #eg = Example()
    window = ViewShape()
    window.show()
    window.iren.Initialize() # Need this line to actually show the render inside Qt
    sys.exit(app.exec_())