import boto3, io, os
from datetime import datetime

# Bucket Service
s3 = boto3.client('s3')
# Rekognition Service
rekognition = boto3.client("rekognition")

# Working directory is text-detector.py folders
os.chdir(os.path.dirname(os.path.abspath('__file__')))
print(os.getcwd())


def main():
	print(" > text-detector.py utiliza los servicios de AWS, para leer el texto de imagenes y compararlos con una imagen control.\n",
		"> Lea el README.txt para mas detalles de como usar el software.\n",
		"> --------------------------------------------------------------------------\n\n",
		"> Ingrese su Bucket e imagen de Control, luego ingrese imagenes de prueba a comprar con el control.")

	bucket = input(" > Ingrese nombre de su Bucket en AWS: ")
	controlpath = input(" > Ingrese nombre de imagen de Control: ")

	logger('Analizando ' + controlpath + ' en ' + bucket)
	if not image_in_bucket(bucket, controlpath):
		push_bucket(bucket, controlpath)
	controlrekogn = rekognition.detect_text( Image = {'S3Object':{'Bucket': bucket,'Name':controlpath}})
	testpath = ""

	print(" > Ingrese nombres de sus imagenes de prueba, o 0 para salir.")
	while (1):
		testpath = input(" > Ingrese imagen de Prueba: ")
		if testpath == 0:
			# Terminate while
			break

		logger('Analizando ' + testpath + ' en ' + bucket)
		if not image_in_bucket(bucket, testpath):
			push_bucket(bucket, testpath)

		testrekogn = rekognition.detect_text( Image = {'S3Object':{'Bucket': bucket,'Name': testpath}} )
		
		print(rekognition_comparator(controlrekogn, testrekogn))
		# we rekognition
		
		pass

	while 1:
		pass
	return 0

def rekognition_comparator(detected_text1, detected_text2):
	text1_list = []
	text1_confidences =[]
	text2_list = []
	text2_confidences = []
	#Lets get all our words and confidences of those words
	for texts in detected_text1['TextDetections']:
		if texts['Type'] == 'WORD':
			text1_list.append(texts['DetectedText'].lower())
			text1_confidences.append(texts['Confidence'])
	for texts in detected_text2['TextDetections']:
		if texts['Type'] == 'WORD':
			text2_list.append(texts['DetectedText'].lower())
			text2_confidences.append(texts['Confidence'])

	print(text1_list)
	print(text2_list)

	if len(text1_list) == len(text2_list):
		for i in range(len(text1_list)):
			if text1_list[i] != text2_list[i]:
				return 0
		return 1

	return 0

#Checks if filepath is in bucket
def image_in_bucket(bucket, filepath):
	bucketfiles = s3.list_objects_v2(Bucket = bucket)
	for files in bucketfiles['Contents']:
		if files["Key"] == filepath:
			return 1
	return 0
	
#Upload filepath to buchet
def push_bucket(bucket, filepath):
	try:
		#s3.upload_file(filepath, 'bucket', filepath).
		with open(filepath, 'rb') as data:
			s3.upload_fileobj(data, bucket, filepath)	

		logger("Subiendo "+ filepath + " al bucket " + bucket)
		return 1
	except BaseException as err:
		logger(err)
	
	return 0


#Just logs whats passed as text
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