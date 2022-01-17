# Turtlebot-Futbolista

Enlace al catkin_ws:

https://drive.google.com/file/d/1TLPnmj1ieh550rdAv38lMvMtF19Ewi7M/view?usp=sharing

Instrucciones de ejecución:

0º Compilar el catkin_ws

1º Ejecutar gazebo cargando el archivo playground.wolrd -> roslaunch turtlebot_gazebo turtlebot_world.launch world_file="Direccion del archivo"

2º Opcionalmente se podria ejecutar el siguiente comando para tener vision de la camara ya que en nuestro caso gazebo solia fallar con frecuencia al estar trabajando en una maquina virtual -> rosrun image_view image_view image:=/camera/rgb/image_raw

3º En una nueva terminal ejecutar el archivo elbicho.py

4º Para mayor informacion sobre la practica consultar el documento con la memoria de esta.

Practica realizada por:

	-Pedro Díaz García
	-Jose García Javega
	-Mario Jerez Tallón
	-Santiago Perez Gisbert
