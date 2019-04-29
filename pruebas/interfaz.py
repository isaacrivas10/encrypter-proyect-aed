# *-* coding=utf-8 *-*

import sys, os
import json
from Arbol import Arbol
from TDA import Node, Carpeta, Archivo
from PyQt4 import QtGui, QtCore, Qt
from functools import partial
from encrypter import Caller

class Window(QtGui.QWidget):

	def __init__(self):
		super(Window, self).__init__()

		self.currentAlgorithm= "AES256"
		self.workingReadingDir= ""
		self.workingSavingDir= ""
		self.password= "Password"
		self.savePassword= False

		self.caller= Caller()

		self.tree= None
		self.path= None

		self.setGeometry(350,200,700,350)
		self.setWindowTitle("Python Encrypter")
		self.setWindowIcon(QtGui.QIcon("123.jpg"))
		QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(
			'Plastique'))
		self.setStyleSheet("background:#928a37")

		self.home()

	def home(self):
		# ComboBox para seleccion de algoritmos
		comboBox= QtGui.QComboBox(self)
		comboBox.addItem("AES256")
		comboBox.addItem("Blowfish")
		#color
		comboBox.setStyleSheet("background:#c98828")
		

		# TextBox para el almacenamiento de direcciones
		self.readingTextBox= QtGui.QLineEdit(self)
		self.readingTextBox.resize(350,35) 
		self.readingTextBox.setEnabled(False)
		self.savingTextBox= QtGui.QLineEdit(self)
		self.savingTextBox.resize(350,35)
		self.savingTextBox.setEnabled(False)
		self.readingTextBox.setStyleSheet("background:#f7f3cd")
		self.savingTextBox.setStyleSheet("background:#f7f3cd") 
		self.readingTextBox.setText("Direccion a cifrar")
		self.savingTextBox.setText("Almacenamiento de cifrado")

		label= QtGui.QLabel("Algoritmo:")

		self.passTextBox= QtGui.QLineEdit(self)
		self.passTextBox.setText("Password")
		self.passTextBox.textChanged[str].connect(self.setPassword)
		self.passTextBox.resize(30, 10)
		self.passTextBox.setStyleSheet("background: white")

		self.passCheckBox= QtGui.QCheckBox(u"Guardar Contraseña", self)
		self.passCheckBox.stateChanged.connect(self.savePasswordBool)
		self.passCheckBox.setStyleSheet("background: #d4f0f9")

		# Definicion de botones
		readingDirBtn= QtGui.QPushButton(u'\u25bc', self)
		readingDirBtn.clicked.connect(partial(self.openFolder, "1"))
		readingDirBtn.resize(readingDirBtn.minimumSizeHint())
		readingDirBtn.setStyleSheet("background:#c98828")

		savingDirBtn= QtGui.QPushButton(u'\u25bc', self)
		savingDirBtn.clicked.connect(partial(self.openFolder, "2"))
		savingDirBtn.resize(savingDirBtn.minimumSizeHint())
		savingDirBtn.setStyleSheet("background:#c98828")

		encryptBtn= QtGui.QPushButton("Cifrar", self)
		encryptBtn.clicked.connect(self.encrypt)
		encryptBtn.resize(encryptBtn.minimumSizeHint())
		encryptBtn.setStyleSheet("background:#fd9a08")
		
		decryptBtn= QtGui.QPushButton("Descifrar", self)
		decryptBtn.clicked.connect(self.decrypt)
		decryptBtn.resize(decryptBtn.minimumSizeHint())
		decryptBtn.setStyleSheet("background:#fd9a08")

		# Definicion del Tree de directorios
		self.treeWidget= QtGui.QTreeWidget(self)
		self.treeWidget.setHeaderLabels(QtCore.QStringList("Directorios"))
		self.treeWidget.setStyleSheet("background:#f7f3cd")

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
		
		gridLayout.addWidget(encryptBtn, 6,1)
		gridLayout.addWidget(decryptBtn, 7,1)

		gridLayout.addWidget(self.passTextBox, 4, 1, 1, 2)
		gridLayout.addWidget(self.passCheckBox, 5, 1)

		# Establecemos gridLayout como el layout principal
		self.setLayout(gridLayout)

		# Cuando se selecciona un algoritmo desde
		# la comboBox se llama este metodo
		comboBox.activated[str].connect(self.setEncriptionAlgorithm)
		
		self.show()

	def encrypt(self):
		
		extractionPath= str(self.workingSavingDir)
		if extractionPath in (self.path[1][0]):
			self.caller.encrypt(path= self.path, 
				algorithm= self.currentAlgorithm,
				key= self.password)
			self.treeWidget.clear()
			self.treeConstructor(self.path)
		else:
			self.caller.encrypt(path= self.path,
			extraction= [extractionPath, self.tree],
			algorithm= self.currentAlgorithm,
			key= self.password)
						
	def decrypt(self):
		extractionPath= str(self.workingSavingDir)
		if extractionPath in (self.path[1][0]):
			self.caller.decrypt(path= self.path, 
				algorithm= self.currentAlgorithm,
				key= self.password)
			self.treeWidget.clear()
			self.treeConstructor(self.path)
		else:
			self.caller.decrypt(path= self.path,
				extraction= [extractionPath, self.tree],
				algorithm= self.currentAlgorithm,
				key= self.password)

	def savePasswordBool(self):
		if self.passCheckBox.isChecked():
			self.savePassword= True
		else:	
			self.savePassword= False
		print self.cipher.key

	def setPassword(self, text):
		self.password= unicode(self.passTextBox.text())
		
	def setEncriptionAlgorithm(self, algrithm):
		self.currentAlgorithm= algrithm


	def openFolder(self, param):
		openF = FileDialog()
		self.workingReadingDir= ""

		if param == "1":
			openF.exec_()
			output= openF.getFiles()
			self.path= output

			if output is not True:
				if len(output[1]) is 1 and output[0] is "folder":
					self.workingSavingDir= output[1][0]
				else:
					self.workingSavingDir= os.path.dirname(
						os.path.abspath(output[1][0]))
				for x in output[1]:
					path= os.path.join(os.path.dirname(output[1][0]), os.path.basename(x))
					self.workingReadingDir += path + ";" 
				self.savingTextBox.setText(self.workingSavingDir)
				self.readingTextBox.setText(self.workingReadingDir)
				self.treeWidget.clear()

				self.treeConstructor(output)
			else:
				msg= QtGui.QMessageBox()
				msg.setIcon(QtGui.QMessageBox.Warning)
				msg.setWindowTitle("File dialog error")
				msg.setText("Error")
				msg.setDetailedText("Por favor escoger un solo tipo de objeto\nEjemplo:\n\tSolo archivos \n\tSolo carpetas")
				msg.exec_()

		elif param == "2":
			openF.setFileMode(QtGui.QFileDialog.Directory)
			openF.exec_()
			output= openF.getFiles()
			self.workingSavingDir= output[1][0]
			self.savingTextBox.setText(output[1][0])

	def treeConstructor(self, output):

		if len(output[1]) is 1:
			path= output[1][0]
			if output[0] is "folder":
				rootName= os.path.basename(path)
			else:
				rootName= os.path.basename(os.path.dirname(path))
			
			self.tree= Arbol(rootName)
			if output[0] == "folder":
				self.buildTree(path=path, tree=self.tree)
			else:
				self.buildTree(tree=self.tree, rootChilds=output)

		else:
			#crear arbol con las hijos en root
			rootName= os.path.basename(os.path.dirname(output[1][0]))
			
			self.tree= Arbol(rootName)
			self.buildTree(tree=self.tree, rootChilds=output)
		
		self.tree.currentNode= self.tree.root
		self.LoadTreeStructure(self.tree, self.treeWidget)
		self.tree.currentNode= self.tree.root
		self.saveTree(self.tree)
		self.tree.currentNode= self.tree.root

	def LoadTreeStructure(self, tree, treeWidget):
		#Busa archivos en el arbol recursivamente
		#Suponiendo que el root es el currentNode
		#print "Vengo de ", tree.currentNode.getName()
		node= tree.currentNode.value.branches.first

		while node:
			#print "Estoy node:", node.getName()
			treeItem= QtGui.QTreeWidgetItem(treeWidget,
					[node.getName()])
			if node.type()== "Carpeta":
			#	print "Es carpeta"
				tree.currentNode= node
			#	print "Entrando a", tree.currentNode.getName()
				self.LoadTreeStructure(tree, treeItem)
				treeItem.setIcon(0, QtGui.QIcon("folder.ico"))
			else:
			#	print "Es archivo"
				treeItem.setIcon(0, QtGui.QIcon("file.png"))

			node= node.next


	def buildTree(self, tree, path=None, rootChilds=None, _rootNode=False):
		try:
			if path:
				print "Estoy en ", path
				if _rootNode:
					print "root node:", os.path.basename(path) 
					# Si True significa que este path es un nodo hijo de root
					node= Node(Carpeta(os.path.basename(path)))
					tree.root.getValue().add(node)
					tree.currentNode= node
					self.buildTree(tree=tree, path=path)
				else:
					for file in os.listdir(path):
						node= tree.currentNode #Guardamos el node original
						print "Buscando..."
						file_path= path + '/' + file
						if os.path.isdir(file_path):
							print "Carpeta:",file,"Direccion:",file_path
							nodoNuevo=Node(Carpeta(file))#creo el nodo de tipo carpeta y nombre file
							tree.add(nodoNuevo)#agrega al currentNode del arbol
							print file,"agregado a", tree.currentNode.getName()
							tree.currentNode= nodoNuevo
							print "currentNode:",tree.currentNode.getName()
							self.buildTree(path=file_path, tree=tree)
							print "Busqueda finalizada en", tree.currentNode.getName()
							tree.currentNode= node
							print "currentNode:",tree.currentNode.getName()
						else:
							print "Archivo:",file,"Direccion:",file_path
							nodoNuevo=Node(Archivo(file))
							tree.add(nodoNuevo)
			if rootChilds:
				print "Root childs: ", rootChilds
				if rootChilds[0] is "folder":
					for child in rootChilds[1]:
						print "Agregando al root", child
						self.buildTree(path=child, tree=tree, _rootNode=True)
						tree.currentNode= tree.root
				else:
					for child in rootChilds[1]:
						print "Agregando al root", child
						tree.add(Node(Archivo(os.path.basename(child))))
		except Exception as e:
			print 'buildTree Exception: ', e

	def saveTree(self, tree):
		Diccionario = {"name": "<archivoOrigen>","Type":"Carpeta","Children":[]}
		Diccionario["name"] = tree.getRoot()
		self.generateJSON(tree,Diccionario["Children"])
		with open('arbol.json','w') as f:
			f.write(json.dumps(Diccionario))

	def generateJSON(self, tree,arreglo):
		node = tree.currentNode.value.branches.first
		while node:
			if node.type()=="Carpeta":
				tempD = {"name": node.value.name, "type": "folder","children":[]}
				tree.currentNode = node
				self.generateJSON(tree, tempD["children"])
				arreglo.append(tempD)
			else:
				tempD = {"name": node.value.name,"type":"File"}
				arreglo.append(tempD)
			node = node.next

class FileDialog(QtGui.QFileDialog):
	"""docstring for FileDialog"""
	def __init__(self):
		super(FileDialog, self).__init__()
		self.setOption(QtGui.QFileDialog.DontUseNativeDialog, True)
		self.setFileMode(QtGui.QFileDialog.ExistingFiles)
		self.fixedFiles= {"folder": [], "file":[]}

	def accept(self):
		self.handleFiles([str(x) for x in self.selectedFiles()])
		self.done(0)
		
	def handleFiles(self, files):
		for file in files:
			if os.path.isdir(file):
				self.fixedFiles["folder"].append(file)
			else:
				self.fixedFiles["file"].append(file)

	def getFiles(self):
		if len(self.fixedFiles["folder"]) > 0 and len(self.fixedFiles["file"]) > 0:
			return True
		else:
			for k, v in self.fixedFiles.iteritems():
				if len(v) > 0:
					return [k, v]
		self.fixedFiles= {"folder": [], "file":[]}

def run():
	app= QtGui.QApplication(sys.argv)
	GUI= Window()
	sys.exit(app.exec_())

if __name__ == '__main__':
	run()
