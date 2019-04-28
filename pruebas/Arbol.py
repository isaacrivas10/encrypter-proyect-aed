
from TDA import *

class Arbol:

	def __init__(self,nameroot="/"):
		# El constructor define la raiz de el directorio
		self.root = Node(Carpeta(nameroot)) # Root es un nodo,contiene una carpeta adentro
		self.currentNode= self.root

	def getRoot(self):
		return self.root.getName()

	def add(self, node):
		self.currentNode.getValue().add(node)
		#print "Nodo ", node.getName(), " agregado"