# *-* encoding= utf-8 *-*

import os
import Crypto.Cipher.AES as AES
import Crypto.Cipher.Blowfish as BF
import Crypto.Random as Random
import Crypto.Hash.SHA256 as SHA256
from random import randrange
from log import Logger

class Caller:

	def __init__(self):
		self.aes= AESEncryptor()
		self.bf= BlowfishEncryptor()

	def encrypt(self, key, algorithm, path, extraction= None):
		
		if path[0] is "folder":
			if algorithm == "AES256":

				self.aes.setKey(key)
				self.aes.encryptAllInPath(path[1], algorithm, extraction)
			else:
				self.bf.setKey(key)
				self.bf.encryptAllInPath(path[1], algorithm, extraction)
		else: 
			if algorithm == "AES256":

				self.aes.setKey(key)
				self.aes.encryptThisFiles(path[1], algorithm,extraction)
			else:
				self.bf.setKey(key)
				self.bf.encryptThisFiles(path[1], algorithm,extraction)

	def decrypt(self, key, algorithm, path, extraction= None):
		if path[0] is "folder":
			if algorithm == "AES256":

				self.aes.setKey(key)
				self.aes.decryptAllInPath(path[1], algorithm, extraction)
			else:
				self.bf.setKey(key)
				self.bf.decryptAllInPath(path[1], algorithm, extraction)
		else: 
			if algorithm == "AES256":

				self.aes.setKey(key)
				self.aes.decryptThisFiles(path[1], algorithm,extraction)
			else:
				self.bf.setKey(key)
				self.bf.decryptThisFiles(path[1], algorithm,extraction)



class BaseEncryptor(object):

	def __init__(self):
		self.key= None
		self.log= Logger()

	def getAllFiles(self, dir_path):
		dirs = []
		for dirName, subdirList, fileList in os.walk(dir_path):
			for fname in fileList:
				dirs.append(os.path.join(dirName,fname))

		return dirs

	
	def buildPathsFromTree(self, tree, string, arreglo):

		#Busca archivos en el arbol recursivamente
		#Suponiendo que el root es el currentNode
		node= tree.currentNode.value.branches.first
		while node:
			if node.type()== "Carpeta":
				st = os.path.join(string,node.getName())
				tree.currentNode= node
				self.buildPathsFromTree(tree, st, arreglo)
				tree.currentNode= node
			else:
				st= os.path.join(string, node.getName())
				arreglo.append(st)
			node= node.next


	def encryptAllInPath(self, path, algorithm, extractionPath=None):
		self.log.openLog()
		self.log.logThis("Encriptando con ", algorithm, takeTime= True)
		self.log.logThis("Path: ", path, "\n")
		if extractionPath:
			dirs= [x for o in path for x in self.getAllFiles(o)]
			array= []
			self.buildPathsFromTree(extractionPath[1], extractionPath[0],array)
			for file in array:
				if os.path.exists(os.path.dirname(file)):
					continue
				else:
					os.makedirs(os.path.dirname(file))
			[[self.log.logThis("Encriptando: ", f),self.encrypt(f,file)] for file in array for f in dirs if os.path.basename(file) == os.path.basename(f)]
		else:
			for p in path:
				dirs = self.getAllFiles(p)
				if len(dirs) > 0:
					for file in dirs:
						self.log.logThis("Encriptando: ", file)
						self.encrypt(file, extractionPath)
				else:
					self.log.logThis("Esta vacio")
		self.log.closeLog()

	def decryptAllInPath(self, path, algorithm, extractionPath= None):
		self.log.openLog()
		self.log.logThis("\t Desencriptando con ", algorithm, takeTime= True)
		self.log.logThis("Path: ",path, "\n")

		# if extractionPath:
		# 	dirs= [x for o in path for x in self.getAllFiles(o)]
		# 	array= []
		# 	self.buildPathsFromTree(extractionPath[1], extractionPath[0],array)
		# 	for file in array:
		# 		if os.path.exists(os.path.dirname(file)):
		# 			continue
		# 		else:
		# 			os.makedirs(os.path.dirname(file))
		# 	[[self.log.logThis("Encriptando: ", f),self.encrypt(f,file)] for file in array for f in dirs if os.path.basename(file) == os.path.basename(f)]

		for p in path:
			dirs= self.getAllFiles(p)
			if len(dirs) > 0:
				for file in dirs:
					if file[-4:] == '.enc':
						self.log.logThis("Desencriptando: ", file)
						self.decrypt(file, extractionPath)
			else:
				self.log.logThis("Esta vacio")
		self.log.closeLog()

	def encryptThisFiles(self, path, algorithm, extractionPath= None):
		self.log.openLog()
		self.log.logThis("Encriptando con ", algorithm, takeTime= True)
		self.log.logThis("Path: ", path, "\n")

		for p in path:
			self.log.logThis("Encriptando: ", p)
			self.encrypt(p, extractionPath[0])
		self.log.closeLog()

	def decryptThisFiles(self, path, algorithm, extractionPath= None):
		self.log.openLog()
		self.log.logThis("\t Desencriptando con ", algorithm, takeTime= True)
		self.log.logThis("Path: ", path, "\n")
		
		for p in path:
			self.log.logThis("Desencriptando: ", p)
			self.decrypt(p, extractionPath[0])
		self.log.closeLog()

	def readFileBytes(self, filename):
		foo= open(filename, 'rb')
		data= foo.read()
		foo.close()
		return data

	def writeFileBytes(self, filename, bufferedData):
		foo= open(filename, 'wb+')
		foo.write(bufferedData)
		foo.close()

class AESEncryptor(BaseEncryptor):

	def __init__(self):
		super(AESEncryptor, self).__init__()

	def setKey(self, key):
		newKey= SHA256.new(key)
		self.key= newKey.digest()

	def pad(self, string):
		length= AES.block_size - (len(string) % AES.block_size)
		string += (chr(length))*length
		return string

	def encrypt(self, filePath, path=None):
		
		file_data= self.readFileBytes(filePath)		
		data= self.pad(file_data)
		iv= Random.new().read(AES.block_size)
		AESCipher= AES.new(self.key, AES.MODE_CBC, iv)
		cipherData= iv + AESCipher.encrypt(data)
		
		if path:
			f_name= path+'.enc'
		else:
			f_name= filePath + '.enc'

		self.writeFileBytes(f_name, cipherData)
		
	def decrypt(self, file, path= None):
		
		enc_data= self.readFileBytes(file)
		iv = enc_data[:16]
		AESCipher= AES.new(self.key, AES.MODE_CBC, iv)
		decryted_data=  AESCipher.decrypt(enc_data[AES.block_size:])
		decryted_data= decryted_data[:-ord(decryted_data[-1])]

		if path:
			basename= os.path.basename(file)
			f_name= path[0].strip(basename) +'/(DEC)'+basename[:-4]
		else:
			f_name= file[:-4]
		
		self.writeFileBytes(f_name, decryted_data)
		
	
class BlowfishEncryptor(BaseEncryptor):

	def __init__(self):
		super(BlowfishEncryptor, self).__init__()
		
	def setKey(self, key):
		self.key= key

	def encrypt(self, filePath, path=None):
		
		file_data= self.readFileBytes(filePath)
		BFcipher= BF.new(self.key)
		cipherData= BFcipher.encrypt(self.pad(file_data))

		if path:
			f_name= path + '.enc'
		else:
			f_name= filePath + '.enc'

		self.writeFileBytes(f_name, cipherData)

	def decrypt(self, filePath, path=None):
		
		enc_data= self.readFileBytes(filePath)
		BFcipher= BF.new(self.key)
		decryted_data= self.depad(BFcipher.decrypt(enc_data))

		if path:
			basename= os.path.basename(filePath)
			f_name= path[0].strip(basename) +'/(DEC)'+basename[:-4]
		else:
			f_name= filePath[:-4]
		
		self.writeFileBytes(f_name, decryted_data)


	def pad(self, file_buffer):
        
		pad_bytes = 8 - (len(file_buffer) % 8)                                 
		for i in range(pad_bytes - 1): file_buffer += chr(randrange(0, 256))
		# final padding byte; % by 8 to get the number of padding bytes
		bflag = randrange(6, 248); bflag -= bflag % 8 - pad_bytes
		file_buffer += chr(bflag)
		return file_buffer

	def depad(self, file_buffer):
		pad_bytes = ord(file_buffer[-1]) % 8
		if not pad_bytes: pad_bytes = 8
		return file_buffer[:-pad_bytes]
		

if __name__== '__main__':
	pass
