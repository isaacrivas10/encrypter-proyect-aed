# *-* encoding= utf-8 *-*

import os
import Crypto.Cipher.AES as AES
import Crypto.Random as Random
import Crypto.Hash.SHA256 as SHA256


class Encrypter:

	def __init__(self):
		self.key= None

	def setKey(self, key):
		newKey= SHA256.new(key)
		self.key= newKey.digest()

	def pad(self, string):
		return string +  b"\0" * (AES.block_size - len(string) % AES.block_size)

	def encryptAES(self, file, path=None):
		with open(file, "rb") as file:
			file_data= file.read()
		
		data= self.pad(file_data)
		iv= Random.new().read(AES.block_size)
		AESCipher= AES.new(self.key, AES.MODE_CBC, iv)
		cipherData= iv + AESCipher.encrypt(data)
		
		if path:
			basename= os.path.basename(file.name)
			f_name= os.path.join(path, basename+ '.enc')
		else:
			f_name= file.name + '.enc'
		with open(f_name, "wb") as encFile:
			encFile.write(cipherData)

	def decryptAES(self, file, path= None):
		with open(file, "rb") as encFile:
			enc_data=  encFile.read()
		
		iv = enc_data[:AES.block_size]
		AESCipher= AES.new(self.key, AES.MODE_CBC, iv)
		decryted_data=  AESCipher.decrypt(enc_data[AES.block_size:])
		
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
	dir_path = os.path.dirname(os.path.realpath(__file__))
	print dir_path