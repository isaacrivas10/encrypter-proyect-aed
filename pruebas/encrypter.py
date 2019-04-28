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

	def encrypt(self, key, algorithm, path, extractionPath= None):

		if algorithm == "AES256":
			self.aes.setKey(key)
			self.aes.encryptAllInPath(path, algorithm, extractionPath)
		else:
			self.bf.setKey(key)
			self.bf.encryptAllInPath(path, algorithm, extractionPath)

	def decrypt(self, key, algorithm, path, extractionPath= None):
		if algorithm == "AES256":
			self.aes.setKey(key)
			self.aes.decryptAllInPath(path, algorithm, extractionPath)
		else:
			self.bf.setKey(key)
			self.bf.decryptAllInPath(path, algorithm, extractionPath)


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

	def encryptAllInPath(self, path, algorithm, extractionPath=None):
		dirs= self.getAllFiles(path)
		self.log.openLog()
		self.log.logThis("Encriptando con ", algorithm, takeTime= True)
		self.log.logThis("Path: ", path, "\n")
		if len(dirs) > 0:
			for file in dirs:
				self.log.logThis("Encriptando: ", file)
				self.encrypt(str(file), extractionPath)
		else:
			self.log.logThis("Esta vacio")
		self.log.closeLog()

	def decryptAllInPath(self, path, algorithm, extractionPath= None):
		dirs= self.getAllFiles(path)
		self.log.openLog()
		self.log.logThis("\t Desencriptando con ", algorithm, takeTime= True)
		self.log.logThis("Path: ",path, "\n")
		if len(dirs) > 0:
			for file in dirs:
				if file[-4:] == '.enc':
					self.log.logThis("Desencriptando: ", file)
					self.decrypt(str(file), extractionPath)
		else:
			self.log.logThis("Esta vacio")
			self.log.closeLog()

	def readFileBytes(self, filename):
		foo= open(filename, 'rb')
		data= foo.read()
		foo.close()
		return data

	def writeFileBytes(self, filename, bufferedData):
		foo= open(filename, 'wb')
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
			basename= os.path.basename(file.name)
			f_name= os.path.join(path, basename+ '.enc')
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
			basename= os.path.basename(file.name)
			f_name= os.path.join(path, '(DEC)'+basename[:-4])
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
			basename= os.path.basename(file.name)
			f_name= os.path.join(path, basename+ '.enc')
		else:
			f_name= filePath + '.enc'

		self.writeFileBytes(f_name, cipherData)

	def decrypt(self, filePath, path=None):
		
		enc_data= self.readFileBytes(filePath)
		BFcipher= BF.new(self.key)
		decryted_data= self.depad(BFcipher.decrypt(enc_data))

		if path:
			basename= os.path.basename(file.name)
			f_name= os.path.join(path, '(DEC)'+basename[:-4])
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
