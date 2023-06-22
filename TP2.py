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
		

def obtener_diccionario_tablas(anio):
    """

    PRECONDICION: Solicita a la API info. sobre la temporada elegida por el usuario.
    POSTCONDICION: Devuelve un diccionario con la info. sobre la temporada elegida por el usuario.

    """

    url = f"https://v3.football.api-sports.io/standings?league=128&season={anio}"

    payload = {}
    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "c347da80012545f47dd7ac448d329d83"
        }

    response = requests.request("GET", url, headers=headers, data=payload)

    stri_json = response.text                    
    diccionario_tablas = json.loads(stri_json)         # Pasar de Json a python

    return diccionario_tablas

def opcion_3():
    """

    PRECONDICION: Pide al usuario que ingrese una temporada para consultar la tabla de posiciones.
    POSTCONDICION: Imprime los datos solicitados por el usuario
    
    """

    anio = input("Ingrese una temporada (2015-2023) para consultar su tabla de posiciones: ")
    while valor_invalido(anio, ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023']) :
        anio = input("La temporada ingresada es invalida. Ingrese nuevamente la temporada: ")
    anio = int(anio)
 
    diccionario_tablas = obtener_diccionario_tablas(anio)

    datos_liga = diccionario_tablas['response'][0] 
    posiciones = datos_liga['league']['standings'][0]

    print(f"----Tabla de posiciones LPF Argentina {anio}")

    if (anio == 2015) or (anio == 2016) or (anio == 2017) or (anio == 2018) or (anio == 2019): 
        
        mostrar_tabla_quince_to_diecinueve(anio, posiciones)
    
    elif (anio == 2020): 
        
        mostrar_tabla_veinte(anio, datos_liga)

    elif (anio == 2021) or (anio == 2022): 
        
        mostrar_tabla_veinti_uno_dos(anio, datos_liga)

    elif (anio == 2023):
        
       mostrar_tabla_veinti_tres(anio, datos_liga)

def mostrar_tabla_quince_to_diecinueve(anio:int, posiciones:dict):

    for i in posiciones:
            puesto = i['rank']
            equipo = i['team']['name']
            puntos = i['points']
            jugados = i['all']['played']
            ganados = i['all']['win']
            empatados = i['all']['draw']
            perdidos = i['all']['lose']

            print(f"{puesto}) {equipo}: {puntos} puntos. En {jugados} partidos obtuvo {ganados} victorias, {perdidos} derrotas y {empatados} empates")

def mostrar_tabla_veinti_uno_dos(anio:int, datos_liga:dict):

    posiciones_mostrar_primera_fase = datos_liga['league']['standings'][1]
    posiciones_segunda_fase = datos_liga['league']['standings'][0]
        
    print("Primera Fase")
    for i in posiciones_mostrar_primera_fase:
        puesto = i['rank']
        equipo = i['team']['name']
        puntos = i['points']
        jugados = i['all']['played']
        ganados = i['all']['win']
        empatados = i['all']['draw']
        perdidos = i['all']['lose']
        print(f"{puesto}) {equipo}: {puntos} puntos. En {jugados} partidos obtuvo {ganados} victorias, {perdidos} derrotas y {empatados} empates")
        
    print()
    print("Segunda Fase")
    for i in posiciones_segunda_fase:
        puesto = i['rank']
        equipo = i['team']['name']
        puntos = i['points']
        jugados = i['all']['played']
        ganados = i['all']['win']
        empatados = i['all']['draw']
        perdidos = i['all']['lose']

        print(f"{puesto}) {equipo}: {puntos} puntos. En {jugados} partidos obtuvo {ganados} victorias, {perdidos} derrotas y {empatados} empates")

def mostrar_tabla_veinti_tres(anio:int, datos_liga:dict):

    posiciones_mostrar_primera_fase = datos_liga['league']['standings'][1]
    for i in posiciones_mostrar_primera_fase:
        puesto = i['rank']
        equipo = i['team']['name']
        puntos = i['points']
        jugados = i['all']['played']
        ganados = i['all']['win']
        empatados = i['all']['draw']
        perdidos = i['all']['lose']
        
        print(f"{puesto}) {equipo}: {puntos} puntos. En {jugados} partidos obtuvo {ganados} victorias, {perdidos} derrotas y {empatados} empates")
    print()
    print(f"La segunda fase de la temporada {anio} todavia no se jugo.")

def mostrar_tabla_veinte(anio: int, datos_liga:dict):

    grupo_uno = datos_liga['league']['standings'][4]
    grupo_dos = datos_liga['league']['standings'][5]
    grupo_tres = datos_liga['league']['standings'][6]
    grupo_cuatro = datos_liga['league']['standings'][7]
    grupo_cinco = datos_liga['league']['standings'][8]
    grupo_seis = datos_liga['league']['standings'][9]
    grupo_a_ganadores = datos_liga['league']['standings'][0]
    grupo_b_ganadores = datos_liga['league']['standings'][1]
    grupo_a_perdedores = datos_liga['league']['standings'][2]
    grupo_b_perdedores = datos_liga['league']['standings'][3]

    mostrar_primera_fase(grupo_uno, grupo_dos, grupo_tres, grupo_cuatro, grupo_cinco, grupo_seis)
    print()
    mostrar_segunda_fase(grupo_a_ganadores, grupo_b_ganadores, grupo_a_perdedores, grupo_b_perdedores)
    
def mostrar_primera_fase(grupo_uno:list, grupo_dos:list, grupo_tres:list, grupo_cuatro:list, grupo_cinco:list, grupo_seis:list):

    print("Primera fase")
    print("Grupo 1")
    for i in grupo_uno:
        puesto = i['rank']
        equipo = i['team']['name']
        puntos = i['points']
        jugados = i['all']['played']
        ganados = i['all']['win']
        empatados = i['all']['draw']
        perdidos = i['all']['lose']
        
        print(f"{puesto}) {equipo}: {puntos} puntos. En {jugados} partidos obtuvo {ganados} victorias, {perdidos} derrotas y {empatados} empates")
    
    print()
    print("Grupo 2")
    for i in grupo_dos:
        puesto = i['rank']
        equipo = i['team']['name']
        puntos = i['points']
        jugados = i['all']['played']
        ganados = i['all']['win']
        empatados = i['all']['draw']
        perdidos = i['all']['lose']
        
        print(f"{puesto}) {equipo}: {puntos} puntos. En {jugados} partidos obtuvo {ganados} victorias, {perdidos} derrotas y {empatados} empates")

    print()
    print("Grupo 3")
    for i in grupo_tres:
        puesto = i['rank']
        equipo = i['team']['name']
        puntos = i['points']
        jugados = i['all']['played']
        ganados = i['all']['win']
        empatados = i['all']['draw']
        perdidos = i['all']['lose']
        
        print(f"{puesto}) {equipo}: {puntos} puntos. En {jugados} partidos obtuvo {ganados} victorias, {perdidos} derrotas y {empatados} empates")

    print()
    print("Grupo 4")
    for i in grupo_cuatro:
        puesto = i['rank']
        equipo = i['team']['name']
        puntos = i['points']
        jugados = i['all']['played']
        ganados = i['all']['win']
        empatados = i['all']['draw']
        perdidos = i['all']['lose']
        
        print(f"{puesto}) {equipo}: {puntos} puntos. En {jugados} partidos obtuvo {ganados} victorias, {perdidos} derrotas y {empatados} empates")

    print()
    print("Grupo 5")
    for i in grupo_cinco:
        puesto = i['rank']
        equipo = i['team']['name']
        puntos = i['points']
        jugados = i['all']['played']
        ganados = i['all']['win']
        empatados = i['all']['draw']
        perdidos = i['all']['lose']
        
        print(f"{puesto}) {equipo}: {puntos} puntos. En {jugados} partidos obtuvo {ganados} victorias, {perdidos} derrotas y {empatados} empates")

    print()
    print("Grupo 6")
    for i in grupo_seis:
        puesto = i['rank']
        equipo = i['team']['name']
        puntos = i['points']
        jugados = i['all']['played']
        ganados = i['all']['win']
        empatados = i['all']['draw']
        perdidos = i['all']['lose']
        
        print(f"{puesto}) {equipo}: {puntos} puntos. En {jugados} partidos obtuvo {ganados} victorias, {perdidos} derrotas y {empatados} empates")

def mostrar_segunda_fase(grupo_a_ganadores:list, grupo_b_ganadores:list, grupo_a_perdedores:list, grupo_b_perdedores:list):

    print("Segunda fase")
    print("Grupo A - Ganadores")
    for i in grupo_a_ganadores:
        puesto = i['rank']
        equipo = i['team']['name']
        puntos = i['points']
        jugados = i['all']['played']
        ganados = i['all']['win']
        empatados = i['all']['draw']
        perdidos = i['all']['lose']
        
        print(f"{puesto}) {equipo}: {puntos} puntos. En {jugados} partidos obtuvo {ganados} victorias, {perdidos} derrotas y {empatados} empates")

    print()
    print("Grupo B - Ganadores")
    for i in grupo_b_ganadores:
        puesto = i['rank']
        equipo = i['team']['name']
        puntos = i['points']
        jugados = i['all']['played']
        ganados = i['all']['win']
        empatados = i['all']['draw']
        perdidos = i['all']['lose']
        
        print(f"{puesto}) {equipo}: {puntos} puntos. En {jugados} partidos obtuvo {ganados} victorias, {perdidos} derrotas y {empatados} empates")

    print()
    print("Grupo A - Perdedores")
    for i in grupo_a_perdedores:
        puesto = i['rank']
        equipo = i['team']['name']
        puntos = i['points']
        jugados = i['all']['played']
        ganados = i['all']['win']
        empatados = i['all']['draw']
        perdidos = i['all']['lose']
        
        print(f"{puesto}) {equipo}: {puntos} puntos. En {jugados} partidos obtuvo {ganados} victorias, {perdidos} derrotas y {empatados} empates")

    print()
    print("Grupo B - Perdedores")
    for i in grupo_b_perdedores:
        puesto = i['rank']
        equipo = i['team']['name']
        puntos = i['points']
        jugados = i['all']['played']
        ganados = i['all']['win']
        empatados = i['all']['draw']
        perdidos = i['all']['lose']
        
        print(f"{puesto}) {equipo}: {puntos} puntos. En {jugados} partidos obtuvo {ganados} victorias, {perdidos} derrotas y {empatados} empates")


def obtener_diccionario_equipos():
    """

    PRECONDICION: Solicita a la API info. de los equipos que participan de la LPF 2023.
    POSTCONDICION: Devuelve un diccionario con la info. de los equipos que participan de la LPF 2023.

    """
    
    url = "https://v3.football.api-sports.io/teams?league=128&season=2023"

    payload = {}
    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "c347da80012545f47dd7ac448d329d83"
        }

    response = requests.request("GET", url, headers=headers, data=payload)

    stri_json = response.text
    diccionario_equipos = json.loads(stri_json)  # Pasar de json a dicc de python

    return diccionario_equipos

def opcion_4():
   """

   PRECONDICION: Pide al usuario que elija un equipo de la lista.
   POSTCONDICION: Muestra los datos del estadio y el escudo de ese equipo.
   
   """

   diccionario_equipos = obtener_diccionario_equipos()

   datos_equipos = diccionario_equipos['response']
   
   mostrar_equipos(datos_equipos)

   eleccion = input("Elija un equipo del listado de equipos: ")
   while valor_invalido(eleccion, ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28']) :
      eleccion = input("La eleccion ingresada es invalida. Ingrese nuevamente la eleccion del equipo: ")
   eleccion = int(eleccion)

   choice = datos_equipos[eleccion - 1]
   nombre = choice['team']['name']
   print()
   print(nombre)

   mostrar_datos_estadio(choice)
   
   mostrar_escudo(choice)
   
def mostrar_datos_estadio(choice:dict):
   
   datos_estadio = choice['venue']
   nombre = datos_estadio['name']
   direccion = datos_estadio['address']
   ciudad = datos_estadio['city']
   capacidad = datos_estadio['capacity']
   logo = datos_estadio['image']

   response = requests.get(logo)
   img = Image.open(BytesIO(response.content))
   img.show()
   
   print(f"El {nombre} esta ubicado en la calle {direccion} de la ciudad de {ciudad}. Tiene una capacidad para {capacidad} personas.")

def mostrar_escudo(choice:dict):
   
   escudo = choice['team']['logo']
   response = requests.get(escudo)
   img = Image.open(BytesIO(response.content))
   img.show()

def mostrar_equipos(datos_equipos:dict):
   
   print("---Estos son los equipos que participan en la temporada 2023 de LPF Argentina.")
   
   contador = 0
   
   for i in datos_equipos:
    contador +=1
    equipo = i['team']['name']
    
    print(f"{contador}) {equipo}")


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
		
		opcion = seleccionar_opcion()
		
		while opcion != 'i':
                     
                     if opcion == 'a':
                          opcion_2()
                     
                     elif opcion == 'b':
                          opcion_3()
                     
                     elif opcion == 'c':
                          opcion_4()
                     
                     elif opcion == 'd':
                          opcion_5()
                     
                     elif opcion == 'e':
                          leer_dinero = int(input("CUANTO DINERO DESEA CARGAR (INGRESAR SOLO EL NUMERO): "))
                          opcion_6(id_usuario, leer_dinero, ARCHIVO, usuarios)
                     
                     elif opcion == 'f':
                          opcion_7(ARCHIVO, usuarios)
                     
                     opcion = seleccionar_opcion()
        guardar_usuario(ARCHIVO, usuarios)
		
main()

