# PDS Tarea AWSRekognition
 Uses AWS Rekognition to compare 2 the text of images, and check if both images share the SAME text.

# Requerimientos
Python 3.8.6
Boto3 for Python
AWS Credentials

# Instrucciones de uso
1.- Configurar las credenciales en %HOMEPATH$/.aws/credentials segun su cuenta de AWS
2.- Ejecutar text-detector.py
3.- Ingresar un Bucket valido (debe estar creado previamente y con permisos de acceso)
4.- Ingresar las imagenes segun se solicita:
	4.1.- Estas deben estar en la misma carpeta que text-detector.py o en el bucket.
	4.2.- Si no se encuentra en el Bucket, el archivo sera cargado al mismo.


# Supuestos
- Para que se considere que 2 oraciones tienen el mismo texto, deberan ser 2 oraciones exactamente iguales 
(en orden y simbolos), incluyendo posibles simbolos extraños, los cuales pueden causar diferencias.
Es irrelevante si estan en mayusculas o en minusculas.
Ejemplos:
	"Una botella de agua" y "Una botella de agua" se consideran iguales.
	"Una botella de agua" y "UNA BOTELLA DE AGUA" se consideran iguales, las mayusculas son irrelevantes.
	"Una botella de agua" y "Una! botella! de agua!" se consideran diferentes.
	"Una botella de agua" y "Botella de una agua" se consideran diferentes, al contener las mismas palabras, en distinto orden.
	"Una botella de agua" y "habia una botella de agua vacia", se consideran diferentes, aun que se contenga "Una botella de agua", la 		oracion es distinta.

Made by Khantur - El cronista sin tinta.

