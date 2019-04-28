from tempArbol import *
import sys, os
path="/home/drunkenboy_/python2/3parcial/pruebas/graphs"#seria el path que seleccionas en la interfaz
pathToTree=path.split("/")#este se le mandaria al arbol
a=Arbol(pathToTree[len(pathToTree)-1])#creo la instancia del arbol

# def buildTheTree( path, NodeRoot):
# 	try:
# 		for file in os.listdir(path):
# 			file_path= path + '/' + file
# 			if os.path.isdir(file_path):
# 				nodoNuevo=Node(Carpeta(file))#creo el nodo de tipo carpeta y nombre file
# 				a.add(nodoNuevo,"-c")#agrega al currentNode del arbol
# 				buildTheTree(file_path,nodoNuevo)
# 			else:
# 				nodoNuevo=Node(Archivo(file))
# 				a.add(nodoNuevo,"-f")
			
# 	except Exception as e:
# 		print 'Exception: ', e

def buildTree(path, tree):
		try:
			for file in os.listdir(path):
				file_path= path + '/' + file
				if os.path.isdir(file_path):
					nodoNuevo=Node(Carpeta(file))#creo el nodo de tipo carpeta y nombre file
					tree.add(nodoNuevo,"-c")#agrega al currentNode del arbol
					tree.currentNode= nodoNuevo
					buildTree(file_path, tree)
				else:
					nodoNuevo=Node(Archivo(file))
					tree.add(nodoNuevo,"-f")
				
		except Exception as e:
			print 'Exception: ', e

def saveTree(tree):
    Diccionario = {"name": "<archivoorigen>","Type":"Carpeta","Children":[]}
    Diccionario["name"] = tree.root.getName()
    generateJSON(tree,Diccionario["Children"])
    with open('arbol.json','w') as f:
         f.write(json.dumps(Diccionario))

def generateJSON(treeRoot,arreglo):
    tempNode = treeRoot.value.branches.first
    while tempNode:
        if tempNode.type()=="Carpeta":
            tempD = {"name": tempNode.value.name, "type": tempNode.type(),"children":[]}
            tree = tempNode
            generateJSON(tree, tempD["children"])
            arreglo.append(tempD)
        else:
            tempD = {"name": tempNode.value.name,"type":tempNode.type()}
            arreglo.append(tempD)
        tempNode = tempNode.next


f=buildTree(path,a)

Diccionario = {"name": "<archivoorigen>","Type":"Carpeta","Children":[]}
Diccionario["name"] = a.root.getName()
generateJSON(a.root,Diccionario["Children"])
print Diccionario

