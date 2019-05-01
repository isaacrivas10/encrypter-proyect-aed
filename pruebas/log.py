import datetime

class Logger:

	def __init__(self):
		self.name= 'logger.txt'
		self.file= None
		self.timer= datetime.datetime
		self.executionTime= ExecutionTime()

	def openLog(self):
		self.file= open(self.name, "a")
		self.file.write('\n')

	# Param 0 = jump, 1= takeTime, 3+ texto
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


class ExecutionTime:
    
    def getTime(self):
        return datetime.datetime.now()
    
    def diff(self,i,f):
        diff=f-i

        #produce milisegundos
        m=diff.days*24*60*60*1000
        m+=diff.seconds*1000
        m+=diff.microseconds/100
        return m
    

