# *-* coding=utf-8 *-*

import sys, os
from PyQt4 import QtGui, QtCore, Qt
from functools import partial

class Window(QtGui.QWidget):

	def __init__(self):
		super(Window, self).__init__()

		self.currentAlgorithm= "AES256"
		self.workingReadingDir= ""
		self.workingSavingDir= ""
		self.password= "Password"

		self.setGeometry(350,200,700,350)
		self.setWindowTitle("Python bad-Encripter")
		QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(
			'Plastique'))

		self.home()

	def home(self):
		# ComboBox para seleccion de algoritmos
		comboBox= QtGui.QComboBox(self)
		comboBox.addItem("AES256")
		comboBox.addItem("Algoritmo")
		

		# TextBox para el almacenamiento de direcciones
		self.readingTextBox= QtGui.QLineEdit(self)
		self.readingTextBox.resize(350,35) 
		self.readingTextBox.setEnabled(False)
		self.savingTextBox= QtGui.QLineEdit(self)
		self.savingTextBox.resize(350,35)
		self.savingTextBox.setEnabled(False)
		self.readingTextBox.setText("Seleccionar una direccion")
		self.savingTextBox.setText("Seleccionar una direccion")

		label= QtGui.QLabel("Algoritmo:")

		self.passTextBox= QtGui.QLineEdit(self)
		self.passTextBox.setText("Password")
		self.passTextBox.textChanged[str].connect(self.setPassword)
		self.passTextBox.resize(30, 10)

		# passCheckBox= QtGui.QCheckBox("Guardar", self)
		# passCheckBox.stateChanged.connect(self.savePasswordOnFile)

		# Definicion de botones
		readingDirBtn= QtGui.QPushButton(u'\u25bc', self)
		readingDirBtn.clicked.connect(partial(self.openFolder, "1"))
		readingDirBtn.resize(readingDirBtn.minimumSizeHint())

		savingDirBtn= QtGui.QPushButton(u'\u25bc', self)
		savingDirBtn.clicked.connect(partial(self.openFolder, "2"))
		savingDirBtn.resize(savingDirBtn.minimumSizeHint())

		encriptBtn= QtGui.QPushButton("Encriptar", self)
		encriptBtn.clicked.connect(self.encript)
		encriptBtn.resize(encriptBtn.minimumSizeHint())
		
		decriptBtn= QtGui.QPushButton("Desencriptar", self)
		decriptBtn.clicked.connect(self.decript)
		decriptBtn.resize(decriptBtn.minimumSizeHint())

		# Definicion del Tree de directorios
		self.treeWidget= QtGui.QTreeWidget(self)
		self.treeWidget.setHeaderLabels(QtCore.QStringList("Directorios"))

		# Definicion del Layout de la Ventana
		gridLayout= QtGui.QGridLayout()
		gridLayout.setSpacing(10)
		
		# Agregamos los widgets al Layout
		gridLayout.addWidget(self.readingTextBox, 1, 0)
		gridLayout.addWidget(readingDirBtn, 1, 1)

		gridLayout.addWidget(self.savingTextBox, 2, 0)
		gridLayout.addWidget(savingDirBtn, 2, 1)

		gridLayout.addWidget(self.treeWidget, 3, 0, 5, 1)

		gridLayout.addWidget(comboBox, 3, 1)
		
		gridLayout.addWidget(encriptBtn, 4,1)
		gridLayout.addWidget(decriptBtn, 5,1)

		gridLayout.addWidget(self.passTextBox, 6, 1, 1, 2)
		#gridLayout.addWidget(passCheckBox, 7, 1)

		# Establecemos gridLayout como el layout principal
		self.setLayout(gridLayout)

		# Cuando se selecciona un algoritmo desde
		# la comboBox se llama este metodo
		comboBox.activated[str].connect(self.setEncriptionAlgorithm)
		
		self.show()

	def encript(self):
		print 'Has encriptado %s con %s' % (self.workingSavingDir, 
			self.currentAlgorithm)

	def decript(self):
		print 'Has desencriptado %s con %s' % (self.workingSavingDir, 
			self.currentAlgorithm)

	def savePasswordOnFile(self):
		pass

	def setPassword(self, text):
		self.password= self.passTextBox.text()

	def setEncriptionAlgorithm(self, algrithm):
		self.currentAlgorithm= algrithm

	def openFolder(self, *param):
		params= list(param)
		openF = QtGui.QFileDialog(self)
		openF.setFileMode(QtGui.QFileDialog.Directory)
		if openF.exec_(): 
			folderDirPath= openF.selectedFiles()
			if param[0] == "1":
				self.workingSavingDir= folderDirPath[0]
				self.workingReadingDir= folderDirPath[0]
				self.savingTextBox.setText(folderDirPath[0])
				self.readingTextBox.setText(folderDirPath[0])
				self.treeWidget.clear()
				self.loadTreeStructure(str(self.workingReadingDir), 
					self.treeWidget)
			elif param[0] == "2":
				self.workingSavingDir= folderDirPath[0]
				self.savingTextBox.setText(folderDirPath[0])

	def loadTreeStructure(self, path, treeWidget):
		# Para cada cosa que exista en path
		try:
			for file in os.listdir(path):
				file_path= path + '/' + file
				treeItem= QtGui.QTreeWidgetItem(treeWidget,
											[os.path.basename(file_path)])
				if os.path.isdir(file_path):
					self.loadTreeStructure(file_path, treeItem)
					treeItem.setIcon(0, QtGui.QIcon("assets/forlder.ico"))
				else:
					treeItem.setIcon(0, QtGui.QIcon("assets/file.ico"))
		except:
			pass
			# Nada mas para evitar que no se muera


def run():
	app= QtGui.QApplication(sys.argv)
	GUI= Window()
	sys.exit(app.exec_())

run()
