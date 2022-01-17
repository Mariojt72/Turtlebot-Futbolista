#!/usr/bin/env python
import rospy
import cv2
import sys
import numpy as np
import imutils #pip install imutils
from cv_bridge import CvBridge
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image

radius_amarillo_anterior=0
estado=0
derecha=False
izquierda=False

def callback(msg):
	
	#Rangos color rojo
	low_red = np.array([0, 100, 20])
	high_red = np.array([10, 255, 255])
	
	#Rangos color azul
	low_blue = np.array([100, 150, 0])
	high_blue = np.array([140, 255, 255])
	
	#Rangos color amarillo
	low_yellow = np.array([0, 0, 0])
	high_yellow = np.array([180, 255, 30])
	
	#Lectura de la imagen de la camara
	bridge=CvBridge()
	cv_image=bridge.imgmsg_to_cv2(msg,desired_encoding="bgr8")
	
	#Conversion a HSV
	imagen_hsv=cv2.cvtColor(cv_image,cv2.COLOR_BGR2HSV)
	
	#Buscamos el rango de color especificado
	red_img = cv2.inRange(imagen_hsv, low_red, high_red)
	blue_img = cv2.inRange(imagen_hsv, low_blue, high_blue)
	yellow_img = cv2.inRange(imagen_hsv, low_yellow, high_yellow)
	
	#Obtenemos los contornos de la esfera roja
	cnts_r = cv2.findContours(red_img, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	cnts_r = imutils.grab_contours(cnts_r)
	center_r = None
	
	#Obtenemos los contornos de la esfera azul
	cnts_b = cv2.findContours(blue_img, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	cnts_b = imutils.grab_contours(cnts_b)
	center_b = None
	
	#Obtenemos los contornos de la esfera amarilla
	cnts_y = cv2.findContours(yellow_img, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	cnts_y = imutils.grab_contours(cnts_y)
	center_y = None
	
	#Def radios y centro
	global radius_azul
	global radius_rojo
	global radius_amarillo
	global center_rojo
	global center
	global center_amarillo
	global radius_amarillo_anterior
	#Def estado
	global estado
	
	#Booleanos giro
	global derecha
	global izquierda
	
	#Def movimiento
	cmd = Twist() 
	cmd.linear.x = 0
	cmd.angular.z = 0
	
	center=[0,0]
	center_rojo=[0,0]
	center_amarillo=[0,0]
	radius_azul=0
	radius_amarillo=0
	
	#Global radius
	
	#Obtenemos los datos de la imagen
	#height, width, channels= cv_image.shape
	#print(height, width, channels)
	
	#Obtenemos el centroide de la pelota roja
	if len(cnts_r) > 0:
		pelota_roja=True
		c = max(cnts_r, key=cv2.contourArea)
		((x, y), radius_rojo) = cv2.minEnclosingCircle(c)
		#Imprimimos el radio para tener una aproximacion de la distancia a la bola
		print("El radio de la pelota roja es: ",radius_rojo,"\n")
		M = cv2.moments(c)
		center_rojo = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		if radius_rojo > 10:
			cv2.circle(cv_image, center_rojo,5, (255, 255, 255), -1)
		print("Centro rojo: ", center_rojo, "\n")
	else:
		pelota_roja=False
		
	
	#Obtenemos el centroide de la pelota azul		
	if len(cnts_b) > 0:
		pelota_azul=True
		c = max(cnts_b, key=cv2.contourArea)
		((x, y), radius_azul) = cv2.minEnclosingCircle(c)
		#Imprimimos el radio para tener una aproximacion de la distancia a la bola
		print("El radio de la pelota azul es:",radius_azul,"\n")
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		if radius_azul > 10:
			cv2.circle(cv_image, center,5, (255, 255, 255), -1)
		print("Centro azul: ", center, "\n")
	else:
		pelota_azul=False
		
	#Obtenemos el centroide de la pelota amarilla		
	if len(cnts_y) > 0:
		c = max(cnts_y, key=cv2.contourArea)
		((x, y), radius_amarillo) = cv2.minEnclosingCircle(c)
		#Imprimimos el radio para tener una aproximacion de la distancia a la bola
		print("El radio de la pelota amarilla es:",radius_amarillo,"\n")
		M = cv2.moments(c)
		center_amarillo = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))	

	
	#Obtenemos las coordenadas del centroide de la pelota roja	
	x,y = center_rojo
	i,j = center
	n,m = center_amarillo
		
	#Maquina de estados
	
	if estado==0:
	
		if x<250:
			derecha=True
				
		elif x>390:
			izquierda=True
				
		if i>250 and i<390 and x>250 and x<390:
			estado=	5
		
		if derecha:
			cmd.linear.x = 0
			cmd.angular.z= 0.2
			if n>290 and n<350:
				radius_amarillo_anterior=radius_amarillo
				estado=1
				derecha=False
				
		if izquierda:
			cmd.linear.x = 0	
			cmd.angular.z= -0.2
			if n>290 and n<350:
				radius_amarillo_anterior=radius_amarillo
				estado=2
				izquierda=False
			
	elif estado==1:
		cmd.linear.x = 0.2
		cmd.angular.z= 0
		if radius_amarillo-radius_amarillo_anterior > 10:
			estado=3
	
	elif estado==2:
		cmd.linear.x = 0.2
		cmd.angular.z= 0
		if radius_amarillo-radius_amarillo_anterior > 10:
			estado=4
			
	elif estado==3:
		cmd.linear.x = 0
		cmd.angular.z= -0.2
		if x>290 and x<350:
			if i<350 and i>270:
				estado= 5
			else:
				estado=7	
			
	elif estado==4:
		cmd.linear.x = 0
		cmd.angular.z= 0.2
		if x>290 and x<350:
			if i<370 and i>290:
				estado= 5
			else:
				estado=8			
		
	elif estado==5:	
		cmd.linear.x = 0.5
		cmd.angular.z = 0
		if radius_azul>55:
			estado=6
					
	elif estado==6:
		cmd.angular.z= 0
		cmd.linear.x = 0
	
	elif estado==7:
		cmd.linear.x = 0	
		cmd.angular.z= 0.2
		if n>290 and n<350:
			radius_amarillo_anterior=radius_amarillo
			estado=1
	
	elif estado==8:
		cmd.linear.x = 0	
		cmd.angular.z= -0.2
		if n>290 and n<350:
			radius_amarillo_anterior=radius_amarillo
			estado=2
		
	else:
		print("Error en la maquina de estados")
	
	print("El estado es:",estado,"\n")
	print("El valor de radius_amarillo_anterior es:",radius_amarillo_anterior,"\n")	
	#Imprimimos la imagen de la camara		
	#cv2.imshow('Imagen',cv_image)
	#cv2.waitKey(0)
	
	#Publicamos velocidades
	pub.publish(cmd)

rospy.init_node('productor_consumidor')
pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size = 5)
sub = rospy.Subscriber('/camera/rgb/image_raw', Image, callback)
rospy.spin()
