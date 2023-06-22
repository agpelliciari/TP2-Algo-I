import requests
import json
import random
import csv
import os
import matplotlib.pyplot as plt
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
def opcion_2():
    url= "https://v3.football.api-sports.io/teams?league=128&season=2023"

    payload = {}
    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "ce6d1b3840dfa8ebcb068e3174297234"
        }

    response = requests.request("GET", url, headers=headers)
    #response.txt es toda la respuesta en texto
    #Pasar de json a dicc de python

    stri_json = response.text
    diccionario_equipos = json.loads(stri_json)
    print('Los Equipos que conforman la Liga profesional son:')
    diccionario_equipos_y_id={}
    for response in diccionario_equipos["response"]: 
    #response ya es el diccionario grande 
        for team in response :
            if team == "team": # Aca le pido que recorra del diccionario grande, la clave team y me de el nombre y el id asi lo guardo en un nuevo diccionario
                diccionario_equipos_y_id[response[team]["name"]]=response[team]["id"]
                print(response[team]["name"]) #imprimo el nombre del equipo
    #PIDO EL EQUIPO AL USUARIO Y VERIFICO SI EXISTE Y BUSCO CUAL ES EL CODIGO DEL EQUIPO 
    equipo_ingresado_por_usuario= input('Ingrese el nombre del equipo para ver su plantel:  ')
    while equipo_ingresado_por_usuario not in diccionario_equipos_y_id:
        print('Ese equipo no esta en esta liga o no existe: ')
        equipo_ingresado_por_usuario= input('Ingrese el nombre del equipo para ver su plantel:  ')
    id_equipo=diccionario_equipos_y_id[equipo_ingresado_por_usuario]
    #HAGO LA PREGUNTA EN LA API PARA QUE ME DUELVA LOS JUGADORES QUE PERTENCEN AL EQUIPO DE DESEE EL USUARIO
    url = f"https://v3.football.api-sports.io/players?league=128&season=2023&team={id_equipo}"

    payload = {}
    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "ce6d1b3840dfa8ebcb068e3174297234"
        }

    response_2 = requests.request("GET", url, headers=headers)

    # Pasar de json a dicc de python
    stri_json_2 = response_2.text
    diccionario_jugadores = json.loads(stri_json_2)
    for response_2 in diccionario_jugadores["response"]:
        for player  in response_2:
            if player == "player":
                print('-',response_2[player]["firstname"],response_2[player]["lastname"])
def opcion_5()->None:
    #DESDE ACA HASTA EL SEGUNDO URL SE PUEDE PONER COMO OTRA FUNCION YA QUE SIRVE PARA EL PUNTO DOS Y EL CINCO
    url= "https://v3.football.api-sports.io/teams?league=128&season=2023"

    payload = {}
    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "ce6d1b3840dfa8ebcb068e3174297234"
        }

    response = requests.request("GET", url, headers=headers)
    #response.txt es toda la respuesta en texto
    # Pasar de json a dicc de python

    stri_json = response.text
    diccionario_equipos = json.loads(stri_json)
    print('Los Equipos que conforman la Liga profesional son:')
    diccionario_equipos_y_id={}
    for response in diccionario_equipos["response"]: 
        #response ya es el diccionario grande 
        for team in response :
            if team == "team": # Aca le pido que recorra del diccionario grande la clave team y me de el nombre y el id asi lo guar en un nuevo diccionario
                print(response[team]["name"])
                diccionario_equipos_y_id[response[team]["name"]]=response[team]["id"]         
    equipo_ingresado_por_usuario=input('Elija el equipo  al cual que desea verle los goles de la temporada: ')
    while equipo_ingresado_por_usuario not in diccionario_equipos_y_id:
        equipo_ingresado_por_usuario=input('Elija el equipo  al caul que desea verle los goles de la temporada: ')
    id_equipo=diccionario_equipos_y_id[equipo_ingresado_por_usuario]
    #HAGO LA PREGUNTA EN LA API PARA QUE ME DUELVA LOS JUGADORES QUE PERTENCEN AL EQUIPO DE DESEE EL USUARIO
    url = f"https://v3.football.api-sports.io/teams/statistics?league=128&season=2023&team={id_equipo}"

    payload = {}    
    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "ce6d1b3840dfa8ebcb068e3174297234"
        }

    response = requests.request("GET", url, headers=headers)
    str_json= response.text
    diccionario_goles_y_minutos= json.loads(str_json)
    data={}
    #print(diccionario_goles_y_minutos)
    for minute in diccionario_goles_y_minutos["response"]["goals"]["for"]:
        if minute=="minute":
            for minutes in diccionario_goles_y_minutos["response"]["goals"]["for"][minute]:
                data[minutes]= diccionario_goles_y_minutos["response"]["goals"]["for"][minute][minutes]["total"]
                if data[minutes]== None:
                    data[minutes]=0
    names=list(data.keys())
    values=list(data.values())
    fig, axs = plt.subplots(1, 1, figsize=(9, 3), sharey=True)
    axs.bar(names,values)
    fig.suptitle('Goles por Minutos Jugados')
    plt.show()
    
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

    while valor_invalido(opcion, ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']):
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
			if opcion == 'a':
				opcion_2()
			elif opcion == 'd':
				opcion_5()
			elif opcion == 'e':
				leer_dinero = int(input("CUANTO DINERO DESEA CARGAR (INGRESAR SOLO EL NUMERO): "))
				opcion_6(id_usuario, leer_dinero, ARCHIVO, usuarios)
			elif opcion == 'f':
				opcion_7(ARCHIVO, usuarios)

			opcion = seleccionar_opcion() 

	guardar_usuario(usuarios, ARCHIVO)
		
main()

