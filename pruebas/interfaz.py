# *-* coding=utf-8 *-*

import sys, os
from PyQt4 import QtGui, QtCore, Qt
from functools import partial
from encrypter import Encrypter

class Window(QtGui.QWidget):

	def __init__(self):
		super(Window, self).__init__()

		self.currentAlgorithm= "AES256"
		self.workingReadingDir= ""
		self.workingSavingDir= ""
		self.password= "Password"
		self.savePassword= False

		self.cipher= Encrypter()
		self.cipher.setKey(self.password)

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
		self.readingTextBox.setText("Direccion a cifrar")
		self.savingTextBox.setText("Almacenamiento de cifrado")

		label= QtGui.QLabel("Algoritmo:")

		self.passTextBox= QtGui.QLineEdit(self)
		self.passTextBox.setText("Password")
		self.passTextBox.textChanged[str].connect(self.setPassword)
		self.passTextBox.resize(30, 10)

		self.passCheckBox= QtGui.QCheckBox(u"Guardar Contraseña", self)
		self.passCheckBox.stateChanged.connect(self.savePasswordBool)

		# Definicion de botones
		readingDirBtn= QtGui.QPushButton(u'\u25bc', self)
		readingDirBtn.clicked.connect(partial(self.openFolder, "1"))
		readingDirBtn.resize(readingDirBtn.minimumSizeHint())

		savingDirBtn= QtGui.QPushButton(u'\u25bc', self)
		savingDirBtn.clicked.connect(partial(self.openFolder, "2"))
		savingDirBtn.resize(savingDirBtn.minimumSizeHint())

		encriptBtn= QtGui.QPushButton("Cifrar", self)
		encriptBtn.clicked.connect(self.encript)
		encriptBtn.resize(encriptBtn.minimumSizeHint())
		
		decriptBtn= QtGui.QPushButton("Descifrar", self)
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

		gridLayout.addWidget(self.treeWidget, 3, 0, 6, 1)

		gridLayout.addWidget(comboBox, 3, 1)
		
		gridLayout.addWidget(encriptBtn, 6,1)
		gridLayout.addWidget(decriptBtn, 7,1)

		gridLayout.addWidget(self.passTextBox, 4, 1, 1, 2)
		gridLayout.addWidget(self.passCheckBox, 5, 1)

		# Establecemos gridLayout como el layout principal
		self.setLayout(gridLayout)

		# Cuando se selecciona un algoritmo desde
		# la comboBox se llama este metodo
		comboBox.activated[str].connect(self.setEncriptionAlgorithm)
		
		self.show()

	def encript(self):
		path= str(self.workingReadingDir)
		extractionPath= str(self.workingSavingDir)
		if path == extractionPath:
			self.cipher.encryptAllInPath(path= path, 
				algorithm= self.currentAlgorithm)
		else:
			self.cipher.encryptAllInPath(path= path,
			extractionPath= extractionPath,
			algorithm= self.currentAlgorithm)
		self.treeWidget.clear()
		self.loadTreeStructure(str(self.workingReadingDir), 
		self.treeWidget)
		
		
		
	def decript(self):
		path= str(self.workingReadingDir)
		extractionPath= str(self.workingSavingDir)
		if path == extractionPath:
			self.cipher.decryptAllInPath(path= path, 
				algorithm= self.currentAlgorithm)
		else:
			self.cipher.decryptAllInPath(path= path,
			extractionPath= extractionPath,
			algorithm= self.currentAlgorithm)
		self.treeWidget.clear()
		self.loadTreeStructure(str(self.workingReadingDir), 
		self.treeWidget)
		

	def savePasswordBool(self):
		if self.passCheckBox.isChecked():
			self.savePassword= True
		else:
			self.savePassword= False
		print self.cipher.key

	def setPassword(self, text):
		self.password= unicode(self.passTextBox.text())
		self.cipher.setKey(self.passTextBox.text())

	def setEncriptionAlgorithm(self, algrithm):
		self.cipher.currentAlgorithm= algrithm


	def openFolder(self, param):
		openF = QtGui.QFileDialog(self)
		openF.setFileMode(QtGui.QFileDialog.Directory)
		if openF.exec_(): 
			folderDirPath= openF.selectedFiles()
			if param == "1":
				self.workingSavingDir= folderDirPath[0]
				self.workingReadingDir= folderDirPath[0]
				self.savingTextBox.setText(folderDirPath[0])
				self.readingTextBox.setText(folderDirPath[0])
				self.treeWidget.clear()
				self.loadTreeStructure(str(self.workingReadingDir), 
					self.treeWidget)
			elif param == "2":
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
					word= treeItem.setIcon(0, QtGui.QIcon("folder.ico"))
				else:
					treeItem.setIcon(0, QtGui.QIcon("file.png"))
		except Exception as e:
			print e
			# Nada mas para evitar que no se muera

	def closeEvent(self, event):
		self.cipher.log.closeLog()


def run():
	app= QtGui.QApplication(sys.argv)
	GUI= Window()
	sys.exit(app.exec_())

if __name__ == '__main__':
	run()
