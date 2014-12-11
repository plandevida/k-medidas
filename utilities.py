'''
	Script con utilidades: manejo de ficheros, ...
'''

class FileHelper:

	def openReadOnlyFile(self, fileName):

		return self.openFile(fileName, 'r')

	def openFile(self, fileName, mode):

		try:
			return open(fileName, mode)
		except:
			print "Error opening the file {f}!".format(f=fileName)

	def closeStream(self, stream):

		if stream:
			stream.close()
			return True
		else:
			return False