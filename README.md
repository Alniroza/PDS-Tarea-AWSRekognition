# PDS Tarea AWSRekognition
 Uses AWS Rekognition to compare 2 the text of images, and check if both images share the SAME text.\
 Developed as a homework for 'Software Tests' on UTFSM.

# Requerimientos
Python 3.8.6\
Boto3 for Python\
AWS Credentials\

# Instrucciones de uso
IMPORTANTE: Si al ejecutar el programa, el Working directory es distinto de la carpeta del text-detector.py.
En la linea 11, debes cambiar __file__ por '__file__' o viceversa.

0.- Verificar que el Working directory corresponda a la ubicacion de text-detector.py (primer print al ejecutar el codigo)
1.- Configurar las credenciales en %HOMEPATH$/.aws/credentials segun su cuenta de AWS\
2.- Ejecutar text-detector.py\
3.- Ingresar un Bucket valido (debe estar creado previamente y con permisos de acceso)\
4.- Ingresar las imagenes segun se solicita:\
	4.1.- Estas deben estar en la misma carpeta que text-detector.py o en el bucket.\
	4.2.- Si no se encuentra en el Bucket, el archivo sera cargado al mismo.\

# Supuestos
- Consideraremos que el texto de la imagen de control, se encuentra en la imagen de prueba, si todas las palabras de la imagen de control se encuentran en la imagen de prueba, y con los mismos simbolos (ignorando mayusculas o minusculas) sin importar si la imagen de prueba tiene texto extra. Si esto se cumple, la funcion "rekognition-comparator()" retornara True (1).\
- Diremos que una palabra, es cualquier conjunto de caracteres separados por espacios ($$Hola123!$% se consideraria como 1 palabra)\

# Ejemplos de resultados:\
	- "Una botella de agua" y "Una botella de agua" se consideran iguales, por lo tanto, la funcion retornara True\
	- "Una botella de agua" y "UNA BOTELLA DE AGUA" se consideran iguales, las mayusculas son irrelevantes y se retornara True.\
	- "Una botella de agua" y "Una botella de agua!" se consideran diferentes, y se retornara False. (agua != agua!)\
	- "Una botella de agua" y "Botella de una agua" se considera contenido en el control. y se retornara true.\
	- "Una botella de agua" y "habia una botella de agua vacia", se consideran valido, ya que se contiene "Una botella de agua" en la\ 
	oracion mas larga de prueba, y se retornara True.
\\
Made by Khantur - El cronista sin tinta.

