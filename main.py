import sys
from utilities import FileHelper
import constants

def readMedidas(file):
	fileHelper = FileHelper()

	try:
		f = fileHelper.openReadOnlyFile(file)

		lineas = f.readlines()

		medidas = []
		for linea in lineas:
			linea = linea.split(",")
			linea[len(linea)-1] = linea[len(linea)-1].strip("\r\n")

			if ( linea != "\r\n" or linea != "\n" ):
				for m in linea:
					muestra = m.split(":")
					medidas.append((muestra[0], muestra[1]))
	except:
		print("Error al leer el fichero")

	return medidas

def k_medidas():
	medidas = readMedidas("medidas.txt")

	print medidas

if __name__ == "__main__":
	import sys

	k_medidas()