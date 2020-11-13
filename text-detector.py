import boto3, io, os
from statistics import mean
from datetime import datetime

# Bucket Service
s3 = boto3.client('s3')
# Rekognition Service
rekognition = boto3.client("rekognition")

# Working directory is text-detector.py folders
os.chdir(os.path.dirname(os.path.abspath(__file__)))
print('WORKING DIRECTORY: ' + os.getcwd())


def main():
	print(" > text-detector.py utiliza los servicios de AWS, para leer el texto de imagenes y compararlos con una imagen control.\n",
		"> Lea el README.txt para mas detalles de como usar el software.\n",
		"> --------------------------------------------------------------------------\n")

	bucket = input(" > Ingrese nombre de su Bucket en AWS: ")
	controlpath = input(" > Ingrese imagen de Control: ")

	logger('Rekognition text-detection a ' + controlpath + ' en ' + bucket)
	if not image_in_bucket(bucket, controlpath):
		push_bucket(bucket, controlpath)
	controlrekogn = rekognition.detect_text( Image = {'S3Object':{'Bucket': bucket,'Name':controlpath}})
	testpath = ""

	print(" > Ingrese nombres de sus imagenes de prueba, o 0 para salir.")
	while (1):
		testpath = input(" > Ingrese imagen de Prueba: ")
		if testpath == '0':
			# Terminate while
			break

		logger('Rekognition text-detection a ' + testpath + ' en ' + bucket)
		if not image_in_bucket(bucket, testpath):
			push_bucket(bucket, testpath)

		testrekogn = rekognition.detect_text( Image = {'S3Object':{'Bucket': bucket,'Name': testpath}} )
		logger('Comprobando si el texto de' + testpath + 'se encuentra en ' + 'controlpath')
		comparation = rekognition_comparator(controlrekogn, testrekogn)
		# we rekognition
		if comparation:
			print('True')
		else:
			print('False')
		pass
	return 0

def rekognition_comparator(detected_text1, detected_text2):

	text1_list = []
	text1_confidences =[]
	text2_list = []
	text2_confidences = []

	#Lets get all our words and confidences of those words
	#Lets ignore all words with less than 97% confidence.
	for texts in detected_text1['TextDetections']:
		if texts['Type'] == 'WORD' and texts['Confidence'] > 97:
			text1_list.append(texts['DetectedText'].lower())
			text1_confidences.append(texts['Confidence'])
	for texts in detected_text2['TextDetections']:
		if texts['Type'] == 'WORD' and texts['Confidence'] > 97:
			text2_list.append(texts['DetectedText'].lower())
			text2_confidences.append(texts['Confidence'])

	
	mean1_confidences = mean(text1_confidences)
	mean2_confidences = mean(text2_confidences)
	print(mean1_confidences , ' ' , mean2_confidences)

	if (mean1_confidences < 97 or mean2_confidences < 97):
		logger("Confianza insuficiente de textos, media1 = " + mean1_confidences + ', media2 = ' + mean2_confidences)
		return 0

	print(text1_list)
	print(text2_list)

	if len(text1_list) <= len(text2_list):
		for i in range(len(text1_list)):
			if text1_list[i] in text2_list:
				continue
			else:
				logger('Texto NO contenido en imagen de prueba. media1 = ' + mean1_confidences + ', media2 = ' + mean2_confidences)
				return False
		logger('Texto de imagen de control, contenido en prueba.  media1 = ' + mean1_confidences + ', media2 = ' + mean2_confidences)
		return True

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