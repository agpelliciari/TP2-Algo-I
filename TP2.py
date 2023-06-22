import requests
import json
import random
import csv
import os

from PIL import Image
from io import BytesIO
from passlib.hash import pbkdf2_sha256

ARCHIVO = "usuarios.csv"



def valor_invalido(valor, valores_validos):
    return valor not in valores_validos

def cargar_usuarios(archivo):
	usuarios = []
	directorio = os.getcwd()
	ruta_del_archivo = os.path.join(directorio, archivo)
	if not os.path.exists(ruta_del_archivo):
		return usuarios
	with open(archivo, newline='', encoding="UTF-8") as archivo_csv:
		csv_reader = csv.reader(archivo_csv, delimiter=',')
		encabezado = next(csv_reader)
		for row in csv_reader:
			usuarios.append(row)
	
	return usuarios

def pedir_busqueda():
	id_usuario = input("INGRESE USUARIO: ")
	contrasenia = input("INGRESE CONTRASENIA: ")
	return id_usuario, contrasenia

def encriptacion(contrasenia):
	hash = pbkdf2_sha256.hash(contrasenia)
	
	return hash
	

def buscar(id_usuario, usuarios, contrasenia):
	buscado = 3
	
	for fila in usuarios:
		
		if((id_usuario == fila[0]) and (pbkdf2_sha256.verify(contrasenia, fila[2]))):
			buscado = 1
		else:
			if(id_usuario == fila[0]): 
				buscado = 2
	
	return buscado

def registrar_usuario(id_usuario, contrasenia, usuarios):
	registrado = False
	
	buscado = buscar(id_usuario, usuarios, contrasenia)

	while(buscado != 0):

		if(buscado == 1):
			print("Usted se encuentra registrado \n")
			
			registrado = True
			buscado = 0

		elif(buscado == 2):
			while(buscado == 2):
				print("LA CONTRASEÑA ES INCORRECTA")
				contrasenia = input("INGRESE NUEVAMENTE LA CONTRASEÑA: ")
		
				buscado = buscar(id_usuario, usuarios, contrasenia)
		else:
			print("No se encuentra registrado")
			respuesta = input("DESEA REGISTRARSE [S/N]: ")
			if(respuesta.lower() != "s"):
				registrado = False

			cantidad_apostada = "0"
			fecha_apostada = "0000/00/00"
			dinero_disponible = "0"

			nombre_usuario = input("INGRESE SU NOMBRE COMPLETO: ")
			contrasenia_encriptada = encriptacion(contrasenia) 
			usuarios.append([id_usuario, nombre_usuario, contrasenia_encriptada, cantidad_apostada, fecha_apostada, dinero_disponible])
			
			
			registrado = True
			buscado = 0
			print("FELICIDADES!! USTED ES USUARIO NUEVO")

	return registrado

def guardar_usuario(usuarios, archivo):
	with open(archivo, 'w', newline='', encoding="UTF-8") as archivo_csv:
		csv_writer = csv.writer(archivo_csv, delimiter=',',quotechar='"', quoting= csv.QUOTE_NONNUMERIC)
		csv_writer.writerow(["ID", "Nombre Usuario", "Contraseña", "Cantidad Apostada", "Fecha Ultima Apuesta", "Dinero Disponible"])
		csv_writer.writerows(usuarios)

def menu():
	
    print("---------------MENU DE OPCIONES-----------------------------")
    print("(a) SE LE MUESTRA EL PLANTEL COMPLETO DE TODOS LOS EQUIPOS DE LPF ARGENTINA 2023")
    print("(b) SE LE MUESTRA LA TABLA DE POSICIONES DEL AÑO QUE ELIJA DE LPF ARGENTINA")
    print("(c) SE LE MUESTRA INFORMACION ACERCA DEL ESTADIO Y ESCUDO DE UN EQUIPO ELEGIDO")
    print("(d) SE LE MUESTRA EL USUARIO QUE MAS APOSTO HASTA EL MOMENTO")
    print("(e) PERMITIR CARGAR DINERO EN SU CUENTA.")
    print("(f) SE LE MUESTRA EL USUARIO QUE MAS APOSTO HASTA EL MOMENTO")
    print("(g) SE LE MUESTRA EL USUARIO QUE MAS GANO HASTA EL MOMENTO")
    print("(h) APOSTAR")
    print("(i) SALIR DEL PROGRAMA")
	
def opcion_6(id_usuario, leer_dinero, archivo, usuarios):
	for fila in usuarios:
		if(id_usuario == fila[0]):
			fila[5] = str(int(fila[5]) + leer_dinero)
			print("SE AGREGO DINERO A SU CUENTA CON EXITO")
			print(f"SU DINERO DISPONIBLE HASTA EL MOMENTO ES {fila[5]}")

def opcion_7(archivo, usuarios):
	max_apostado = -1
	for fila in usuarios:
		if(int(fila[3]) > max_apostado):
			max_apostado = int(fila[3])
	for fila in usuarios:
		if(int(fila[3]) == max_apostado):
			print(f"EL USUARIO {fila[1]} CON LA CANTIDAD DE ${max_apostado} ES EL QUE MAS DINERO APOSTO HASTA EL MOMENTO")
			
def seleccionar_opcion():
    menu()

    opcion = input("Ingrese una opcion: ")

    while valor_invalido(opcion, ['a', 'b', 'c', 'd', 'e', 'f', 'g']):
        opcion = input(f"La opcion {opcion} es invalida. Por favor, seleccione una opcion valida: ")

    return opcion
	

def main():
	
	print("BIENVENIDOS AL PORTAL DE APUESTAS JUGARSELAS.\n")
	usuarios = cargar_usuarios(ARCHIVO)
	id_usuario, contrasenia = pedir_busqueda()
	registrado = registrar_usuario(id_usuario, contrasenia, usuarios)
	

	if(registrado):
	
		print("ACONTINUACION SE LE MOSTRARA UN MENU DE OPCIONES PARA EL USO DE SU CUENTA. ")
		menu()
		
		opcion = seleccionar_opcion()
		
		while opcion != 'i':
			if opcion == 'e':
				leer_dinero = int(input("CUANTO DINERO DESEA CARGAR (INGRESAR SOLO EL NUMERO): "))
				opcion_6(id_usuario, leer_dinero, ARCHIVO, usuarios)
			elif opcion == 'f':
				opcion_7(ARCHIVO, usuarios)
            
            opcion = seleccionar_opcion()    

	guardar_usuario(usuarios, ARCHIVO)
		
main()

