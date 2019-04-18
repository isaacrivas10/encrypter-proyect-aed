# *-* encoding= utf-8 *-*

import os
import Crypto.Cipher.AES as AES
import Crypto.Random as Random
import Crypto.Hash.SHA256 as SHA256


class Logger:

	def __init__(self):
		self.name= 'logger.txt'
		self.file= None
		self.openLog()

	def openLog(self):
		self.file= open(self.name, "w")

	def logThis(self, *text):
		text= list(text)
		for t in text:
			self.file.write(str(t))
			self.file.write('\n')

	def closeLog(self):
		if self.file:
			self.file.close()


class Encrypter:

	def __init__(self):
		self.key= None
		self.log = Logger()

	def setKey(self, key):
		newKey= SHA256.new(key)
		self.key= newKey.digest()

	def pad(self, string):
		#return string +  b"\0" * (AES.block_size - len(string) % AES.block_size)
		length= AES.block_size - (len(string) % AES.block_size)
		string += (chr(length))*length
		return string

	def encryptAES(self, filePath, path=None):
		with open(filePath, "rb") as file:
			file_data= file.read()
		
		data= self.pad(file_data)
		iv= Random.new().read(AES.block_size)
		AESCipher= AES.new(self.key, AES.MODE_CBC, iv)
		cipherData= iv + AESCipher.encrypt(data)
		
		if path:
			basename= os.path.basename(file.name)
			f_name= os.path.join(path, basename+ '.enc')
		else:
			f_name= filePath + '.enc'
		with open(f_name, "wb") as encFile:
			encFile.write(cipherData)

	def decryptAES(self, file, path= None):
		with open(file, "rb") as encFile:
			enc_data=  encFile.read()
		
		iv = enc_data[:16]
		AESCipher= AES.new(self.key, AES.MODE_CBC, iv)
		decryted_data=  AESCipher.decrypt(enc_data[AES.block_size:])
		decryted_data= decryted_data[:-ord(decryted_data[-1])]

		if path:
			basename= os.path.basename(file.name)
			f_name= os.path.join(path, '(DEC)'+basename[:-4])
		else:
			f_name= file[:-4]
		with open(f_name, "wb") as decFile:
			decFile.write(decryted_data)

	def encryptAllInPath(self, path, algorithm, 
		extractionPath=None):
		dirs= self.getAllFiles(path)
		for file in dirs:
			print "Encriptando:  ", file
			if algorithm == 'AES256':
				self.encryptAES(str(file), extractionPath)
			else:
				pass

	def decryptAllInPath(self, path, algorithm,
		extractionPath= None):
		dirs= self.getAllFiles(path)
		for file in dirs:
			if file[-4:] == '.enc':
				print "Desencriptando:  ", file
				if algorithm == "AES256":
					self.decryptAES(str(file), extractionPath)
				else:
					pass
		
	def getAllFiles(self, dir_path):
		dirs = []
		for dirName, subdirList, fileList in os.walk(dir_path):
			for fname in fileList:
				dirs.append(os.path.join(dirName,fname))

		return dirs




if __name__== '__main__':
	pass
