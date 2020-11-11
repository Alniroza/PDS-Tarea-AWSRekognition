import boto3, sys, io, os
from datetime import datetime

#Bucket Service
s3 = boto3.client('s3')
#Rekognition Service
rekognition = boto3.client("rekognition")

#Working directory is text-detector.py folders
os.chdir(os.path.dirname(os.path.abspath('__file__')))
print(os.getcwd())


def main():
	print(" > text-detector.py utiliza los servicios de AWS, para leer el texto de imagenes y compararlos con una imagen control.\n",
		"> Lea el README.txt para mas detalles de como usar el software.\n",
		"> --------------------------------------------------------------------------\n\n",
		"> Ingrese su Bucket e imagen de Control, luego ingrese imagenes de prueba a comprar con el control.")

	bucket = input(" > Ingrese nombre de su Bucket en AWS: ")

	controlpath = input(" > Ingrese nombre de imagen de Control: ")
	print(" > Ingrese nombres de su imagen de prueba, o 0 para salir.")


	if not image_in_bucket(bucket, controlpath):
		push_bucket(bucket, controlpath)
	controlrekogn = rekognition.detect_text( Image = {'S3Object':{'Bucket': bucket,'Name':controlpath}})
	testpath = ""

	while (1):
		testpath = input(" > Ingrese imagen de Prueba: ")
		if testpath == 0:
			#Terminate while
			break
		if not image_in_bucket(bucket, testpath):
			push_bucket(bucket, testpath)

		testrekogn = rekognition.detect_text( Image = {'S3Object':{'Bucket': bucket,'Name': testpath}} )
		print(testrekogn)
		#we rekognition
		
		pass

	return 0

def rekognition_comparator(data1, data2):
	return 0

def image_in_bucket(bucket, filepath):
	bucketfiles = s3.list_objects_v2(Bucket = bucket)
	for files in bucketfiles['Contents']:
		if files["Key"] == filepath:
			return 1
	return 0
	

def push_bucket(bucket, filepath):
	try:
		#s3.upload_file(filepath, 'bucket', filepath).
		with open(filepath, 'rb') as data:
			s3.upload_fileobj(data, bucket, filepath)

		logger("Subiendo "+ filepath + " al bucket " + bucket)
		return 1
	except:
		print("no se pudo subir el archivo")
	
	return 0


def logger(text):
	logs = open('LOGS.txt', 'a')
	#Obteniendo Hora
	now = datetime.now()
	#Mensaje del log
	logtext = "["+str(now)+"] " + text +"\n"
	#Escribiendo0
	logs.write(logtext)
	return logs.close()


main()