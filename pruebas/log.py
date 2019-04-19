import datetime

class Logger:

	def __init__(self):
		self.name= 'logger.txt'
		self.file= None
		self.timer= datetime.datetime

	def openLog(self):
		self.file= open(self.name, "a")
		self.file.write('\n')

	# Param 0 = jump, 1= takeTime, 3+
	def logThis(self, *argv, **kwargs):
		text= list(argv)

		if kwargs.get("takeTime"):
				self.file.write(self.timer.now().strftime('%Y-%m-%d %H:%M:%S')+ '\t')
		for t in text:
			self.file.write(str(t))
			if kwargs.get("jump"):
				self.file.write('\n')
		self.file.write('\n')

	def closeLog(self):
		if self.file:
			self.file.close()
