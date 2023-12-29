import requests
import http.client
import json
import random
import csv
import os
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
from passlib.hash import pbkdf2_sha256
from datetime import datetime

ARCHIVO = "usuarios.csv"
ARCHIVO2 = "transacciones.csv"

NO_REGISTRADO = 3
REGISTRADO = 1
CONTRASENIA_INCORRECTA = 2

EQUIPO_LOCAL = 'L'
EQUIPO_VISITANTE = 'V'

PAGO_APUESTA_MIN = 2
PAGO_APUESTA_MAX = 5

TIRADA_DADO_MIN = 1
TIRADA_DADO_MAX = 4


def valor_invalido(valor, valores_validos):
    return valor not in valores_validos

def numero_invalido(numero: str):
    return numero.isnumeric()

def cargar_usuarios(archivo):
    """

    PRECONDICION: Se recibe un archivo.csv
    POSTCONDICION: Devuelve una lista en caso de que el archivo no este vacio, de lo contrario devolvera -1
    
    """

    usuarios = []
    directorio = os.getcwd()
    ruta_del_archivo = os.path.join(directorio, archivo)
    if not os.path.exists(ruta_del_archivo):
        return -1
    with open(archivo, newline='', encoding="UTF-8") as archivo_csv:
        csv_reader = csv.reader(archivo_csv, delimiter=',')
        encabezado = next(csv_reader)
        for row in csv_reader:
            usuarios.append(row)

    return usuarios

def cargar_transacciones(archivo):
    """
    
    PRECONDICION: Se recibe un archivo.csv
    POSTCONDICION: Devuelve una lista en caso de que el archivo no este vacio, de lo contrario devolvera -1
    
    """
        
    transacciones = []
    directorio = os.getcwd()
    ruta_del_archivo = os.path.join(directorio, archivo)
    if not os.path.exists(ruta_del_archivo):
        return transacciones 
    with open(archivo, newline='', encoding="UTF-8") as archivo_csv:
        csv_reader = csv.reader(archivo_csv, delimiter=',')
        encabezado = next(csv_reader)
        for row in csv_reader:
            transacciones.append(row)
                    
    return transacciones

def pedir_busqueda():
    """

    PRECONDICION: Se le pide al usuario que ingrese usuario y contraseña.
    POSTCONDICION: Devuelve los dos valores ingresados por el usuario.
    
    """

    id_usuario = input("INGRESE USUARIO (MAIL): ")
    contrasenia = input("INGRESE CONTRASEÑA: ")
    
    return id_usuario, contrasenia

def encriptacion(contrasenia):
    """

    PRECONDICION: Se recibe el valor valido
    POSTCONDICION: Devuelve el valor encriptado
 
    """

    hash = pbkdf2_sha256.hash(contrasenia)

    return hash


def buscar(id_usuario, usuarios, contrasenia):
    """
     
    PRECONDICION: Se reciben datos leidos por consola
    POSTCONDICION: Devolvera un numero dependiendo si estan o no en la lista usuarios, 1: registrado, 3: no registrado, 2: si la contraseña es incorrecta
    
    """

    buscado = NO_REGISTRADO

    for fila in usuarios:
        if(len(fila) > 0):
            if((id_usuario == fila[0]) and (pbkdf2_sha256.verify(contrasenia, fila[2]))):
                buscado = REGISTRADO
            else:
                if(id_usuario == fila[0]): 
                    buscado = CONTRASENIA_INCORRECTA
		
    return buscado

def registrar_usuario(id_usuario, contrasenia, usuarios):
    """
    
    PRECONDICION: Se reciben datos leidos por consola
    POSTCONDICION: Devuelve true si se pudo registrar de lo contrario devuelve false y se le mostrara mensajes al usuario para un control de su registro
    
    """

    registrado = False

    buscado = buscar(id_usuario, usuarios, contrasenia)

    while(buscado != 0):

        if(buscado == REGISTRADO):
            print("Usted se encuentra registrado \n")
            
            registrado = True
            buscado = 0

        elif(buscado == CONTRASENIA_INCORRECTA):
            while(buscado == CONTRASENIA_INCORRECTA):
                print("LA CONTRASEÑA ES INCORRECTA")
                confirmacion = input("DESEA SALIR? (si/no): ")
                while (confirmacion.lower() != "si") and (confirmacion.lower() != "no"):
                    confirmacion = input("INGRESE NUEVAMENTE LA RESPUESTA. DESEA SALIR? (si/no): ")
                
                if (confirmacion.lower() == "no"):
                    contrasenia = input("INGRESE NUEVAMENTE LA CONTRASEÑA: ")
                    buscado = buscar(id_usuario, usuarios, contrasenia)
                else:
                    return None
                
        else:
            print("NO SE ENCUENTRA REGISTRADO")
            respuesta = input("DESEA REGISTRARSE [si/no]: ")
            if(respuesta.lower() != "si"):
                return None

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
    """

    PRECONDICION: Se recibe una lista de usuarios cargada
    POSTCONDICION: Se crea un archivo cargado con la lista de usuarios
     
    """

    with open(archivo, 'w', newline='', encoding="UTF-8") as archivo_csv:
        csv_writer = csv.writer(archivo_csv, delimiter=',',quotechar='"', quoting= csv.QUOTE_NONNUMERIC)
        csv_writer.writerow(["ID", "Nombre Usuario", "Contraseña", "Cantidad Apostada", "Fecha Ultima Apuesta", "Dinero Disponible"])
        csv_writer.writerows(usuarios)

def menu():

    print("---------------MENU DE OPCIONES-----------------------------")
    print("(a) SE LE MUESTRA EL PLANTEL COMPLETO DE TODOS LOS EQUIPOS DE LPF ARGENTINA 2023")
    print("(b) SE LE MUESTRA LA TABLA DE POSICIONES DEL AÑO QUE ELIJA DE LPF ARGENTINA")
    print("(c) SE LE MUESTRA INFORMACION ACERCA DEL ESTADIO Y ESCUDO DE UN EQUIPO ELEGIDO")
    print("(d) SE LE MUESTRA UN GRAFICO DE LOS GOLES POR MINUTO DE UN EQUIPO ELEGIDO")
    print("(e) PERMITIR CARGAR DINERO EN SU CUENTA.")
    print("(f) SE LE MUESTRA EL USUARIO QUE MAS APOSTO HASTA EL MOMENTO")
    print("(g) SE LE MUESTRA EL USUARIO QUE MAS GANO HASTA EL MOMENTO")
    print("(h) APOSTAR")
    print("(i) SALIR DEL PROGRAMA")

def Imprimir_equipos_de_la_liga():
    """

    PRECONDICION: Pide a la API los equipos de la liga Argentina de la temporada 2023
    POSTCONDICION: Y luego imprime en un listado a los equipos que la conforman y crea un diccionario que tiene 
                    como clave a los equipos con sus respectivos id. 

    """
    url= "https://v3.football.api-sports.io/teams?league=128&season=2023"
    payload = {}
    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "c347da80012545f47dd7ac448d329d83"
        }
    response = requests.request("GET", url, headers=headers)
    stri_json = response.text
    diccionario_equipos = json.loads(stri_json)
    print('LOS EQUIPOS QUE CONFORMAN LA LIGA PROFESIONAL SON:')
    diccionario_equipos_y_id={}
    for response in diccionario_equipos["response"]:
        for team in response :
            if team == "team":
                diccionario_equipos_y_id[(response[team]["name"]).capitalize()]=response[team]["id"]
                print(response[team]["name"]) 
    return diccionario_equipos_y_id

def opcion_2():
    """

    PRECONDICION: Pide al usuario un equipo y pide a la API los jugadores que pertenecen a ese equipo.
    POSTCONDICION: Muestra un listado del plantel del equipo ingresado por el usuario.

    """
    diccionario_equipos_y_id=Imprimir_equipos_de_la_liga()
    equipo_ingresado_por_usuario= input('Ingrese el nombre del equipo para ver su plantel:  ').capitalize()
    
    while equipo_ingresado_por_usuario not in diccionario_equipos_y_id:
        print('Ese equipo no esta en esta liga o no existe: ')
        equipo_ingresado_por_usuario= input('Ingrese el nombre del equipo para ver su plantel:  ').capitalize()
    id_equipo=diccionario_equipos_y_id[equipo_ingresado_por_usuario]
    
    url = f"https://v3.football.api-sports.io/players?league=128&season=2023&team={id_equipo}"

    payload = {}
    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "c347da80012545f47dd7ac448d329d83"
        }

    response_2 = requests.request("GET", url, headers=headers)

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
    """

    PRECONDICION: Pide al usuario un equipo y pide a la API los goles de toda la temporada de ese equipo.
    POSTCONDICION: Muestra en un grafico todos los goles que hizo el equipo en toda la temporada  divididos por minutos.

    """      
    diccionario_equipos_y_id=Imprimir_equipos_de_la_liga()
    equipo_ingresado_por_usuario=input('Elija el equipo  al cual que desea verle los goles de la temporada: ').capitalize()
    while equipo_ingresado_por_usuario not in diccionario_equipos_y_id:
        print('Ese equipo no esta en esta liga o no existe: ')
        equipo_ingresado_por_usuario=input('Elija el equipo  al cual que desea verle los goles de la temporada: ').capitalize()
    id_equipo=diccionario_equipos_y_id[equipo_ingresado_por_usuario]
    
    url = f"https://v3.football.api-sports.io/teams/statistics?league=128&season=2023&team={id_equipo}"

    payload = {}    
    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "c347da80012545f47dd7ac448d329d83"
            }
    
    response = requests.request("GET", url, headers=headers)
    str_json= response.text
    diccionario_goles_y_minutos= json.loads(str_json)
    data={}
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

def validar_fecha(fecha_str):
    """
 
    PRECONDICION: Se recibe una fecha en cadena con formato YYYY-MM-DD
    POSTCONDICION: Devuelve true si es la fecha es igual a la fecha actual de lo contrario devuelve false
 
    """
    try:
        datetime.strptime(fecha_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False
def cargar_fecha_actual():
    fecha_actaul=datetime.now()
    fecha_actaul1=datetime.strftime(fecha_actaul,'%Y-%m-%d')
    fecha = input("Ingrese la fecha actual en formato YYYY-MM-DD: ")
    while not validar_fecha(fecha) or fecha != fecha_actaul1:
        print("Fecha no válida. Intente nuevamente.")
        fecha = input("Ingrese la  fecha  actual en formato YYYY-MM-DD: ")
    return fecha
def opcion_6(id_usuario:str, leer_dinero:int, usuarios:list, transacciones:list)->list:
    """
    PRECONDICION: 
    POSTCONDICION: Se cargara una lista con campos validos a la lista transacciones
    """
    linea = []
    fecha= cargar_fecha_actual()

    for fila in usuarios:

        if(id_usuario == fila[0]):
            fila[5] = str(int(fila[5]) + leer_dinero)
            print("SE AGREGO DINERO A SU CUENTA CON EXITO")
            print(f"SU DINERO DISPONIBLE HASTA EL MOMENTO ES {fila[5]}")
            tipo_resultado = "deposita" 
            importe = leer_dinero

            linea.append(id_usuario)
            linea.append(fecha)
            linea.append(tipo_resultado)
            linea.append(importe)
    transacciones.append(linea)

def opcion_7(usuarios:list)->None:
    """
     
    PRECONDICION: Se recibe una lista con datos validos
    POSTCONDICION: Se muestra por pantalla el usuario que mas dinero aposto
    
    """
    max_apostado = -1
    for fila in usuarios:
        if(int(fila[3]) > max_apostado):
            max_apostado = int(fila[3])
    if(max_apostado == 0):
        print("NO HAY INFORMACION, PORQUE AUN NADIE APOSTO")
    elif(max_apostado > 0):
        for fila in usuarios:
            if(int(fila[3]) == max_apostado):
                print(f"EL USUARIO {fila[1]} CON LA CANTIDAD DE ${max_apostado} ES EL QUE MAS DINERO APOSTO HASTA EL MOMENTO")


def opcion_8(transacciones:list, usuarios:list):
    """
    
    PRECONDICION: 
    POSTCONDICION: se mostrara informacion del usuario que mas veces gano
    
    """
    apuestas_usuarios = {}
    acumulador_veces_ganadas = 1
    mayor_cant_veces_ganadas = 0
    id_usuario_mayor_cant_veces_ganadas = "x"

    for fila in transacciones:
        if(len(fila) > 0):
            if((fila[2] == "Pierde") or (fila[2] == "deposita")):
                print("AUN NO HAY GANADORES")
            else:
                if((fila[2] == "Gana") and (fila[0] not in apuestas_usuarios)):
                    apuestas_usuarios[fila[0]] = [acumulador_veces_ganadas]
                else:
                    if((fila[2] == "Gana") and (fila[0] in apuestas_usuarios)):
                        apuestas_usuarios[fila[0]] = [int(" ".join(map(str,apuestas_usuarios[fila[0]]))) + acumulador_veces_ganadas]

    for usuario in apuestas_usuarios:
        str_apuestas = (" ".join(map(str, apuestas_usuarios[usuario])))
        if(int(str_apuestas) > mayor_cant_veces_ganadas):
            mayor_cant_veces_ganadas = int(str_apuestas)
            id_usuario_mayor_cant_veces_ganadas = usuario

    for fila in usuarios:
        if(fila[0] == id_usuario_mayor_cant_veces_ganadas):
            print(f"EL USUARIO QUE MAS VECES APOSTO HASTA EL MOMENTO ES {fila[1]} CON LA CANTIDAD DE {mayor_cant_veces_ganadas} APUESTAS")

    if(len(transacciones) == 0):
        print("AUN NO HAY GANADORES")
                
def lee_informacion(url1):
    url= f"https://v3.football.api-sports.io{url1}"
    payload = {}
    headers = {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': "4f195fbb113f91fc46340162f872b960"
            }
    response = requests.request("GET", url, headers=headers)
    stri_json = response.text
    data= json.loads(stri_json)

    return data

def cargando_equipos():
    """

    PRECONDICION: -----------------------------
    POSTCONDICION: devolvera un diccionario con los equipos

    """
    url1 = ("/teams?league=128&season=2023")
    data = lee_informacion(url1)
  
    equipos = {}
    cantidad_equipos = data['results']

    for resultado in range(cantidad_equipos):
        nombre_equipo = (data['response'][resultado]['team']['name'])
        id_equipo = (data['response'][resultado]['team']['id'])

        equipos[id_equipo] = nombre_equipo
    
    return equipos


def mostrar_equipos_id(equipos:dict):
    """

    PRECONDICION: recibe un diccionario cargado con datos validos.
    POSTCONDICION: Se imprimira por pantalla informacion deL diccionario.

    """
    for id_equipo, nombre_equipo in equipos.items():
        print(f"ID {id_equipo} - {nombre_equipo} ")

def jugada(local_o_visitante):
    """

    PRECONDICION: recibe como valor una cadena 'home' o 'away'
    POSTCONDICION: Se imprimira 'L' si es local o 'V'  si es visitante

    """
    if('home' in local_o_visitante):
            local_o_visitante = EQUIPO_LOCAL
    else:
        if('away' in local_o_visitante):
            local_o_visitante = EQUIPO_VISITANTE
    return local_o_visitante

def cargar_fixture(leer_equipo):
    """

    PRECONDICION: recibe por paramentro un numero entero positivo.
    POSTCONDICION: devolvera un diccionario con los fixtures.

    """
    fixtures = {}
    url1 =  (f"/fixtures?league=128&season=2023&team={leer_equipo}")
    data = lee_informacion(url1)


    cantidad_fixture = data['results']
    for resultado in range(cantidad_fixture):
        id_fixture = (data['response'][resultado]['fixture']['id'])
        fecha = (data['response'][resultado]['fixture']['date'])
        estadio = (data['response'][resultado]['fixture']['venue']['name'])
        local = (data['response'][resultado]['teams']['home']['name'])
        local_o_visitante1 = (list((data['response'][resultado]['teams']).keys())[0])
        local_o_visitante1 = jugada(local_o_visitante1)
        visitante = (data['response'][resultado]['teams']['away']['name'])
        local_o_visitante2 = (list((data['response'][resultado]['teams']).keys())[1])
        local_o_visitante2 = jugada(local_o_visitante2)
        fixtures[id_fixture] = [(local_o_visitante1, local), (local_o_visitante2, visitante), fecha, estadio]

    return fixtures

def mostrar_fixtures(fixtures):
    """

    PRECONDICION: recibe por parametro un diccionario con datos validos.
    POSTCONDICION: mostrara informacion del diccionario.

    """
    for id_fixture in fixtures:
        print(f"ID: {id_fixture} - ({fixtures[id_fixture][0][0]}) {fixtures[id_fixture][0][1]} vs ({fixtures[id_fixture][1][0]}) {fixtures[id_fixture][1][1]} - {fixtures[id_fixture][2]} - {fixtures[id_fixture][3]}")

def pago_x_apuesta():
    """

    PRECONDICION: ----------------------
    POSTCONDICION: Devuelve un valor asignado de forma aleaatoria

    """
    cant_pago_x_apuestas = random.randrange(PAGO_APUESTA_MIN,PAGO_APUESTA_MAX)
    return cant_pago_x_apuestas

def importe_apuesta(id_fixture:int, fixtures:dict, cant_pago_x_apuestas:int, ganador:str, monto_a_apostar:int):
    """

    PRECONDICION: recibe por parametro valores validos
    POSTCONDICION: devuelve un numero positivo, resultado de lo que paga por fixture

    """
    url1 = (f"/predictions?fixture={id_fixture}")
    data = lee_informacion(url1)

    w_o_d = (data['response'][0]['predictions']['win_or_draw'])

    ganador_x_api = (data['response'][0]['predictions']['winner']['name'])

    pago_x_apuestas_wod = cant_pago_x_apuestas * 0.1
    equipo1 = fixtures[id_fixture][0]

    equipo2 = fixtures[id_fixture][1]

    

    if((ganador_x_api == equipo1[1]) and (equipo1[0] in ganador) and (w_o_d)):
        importe = pago_x_apuestas_wod * monto_a_apostar
    
    elif((ganador_x_api == equipo2[1]) and (equipo2[0] in ganador) and (w_o_d)):
        importe = pago_x_apuestas_wod * monto_a_apostar

    elif((ganador_x_api == equipo1[1]) and (equipo1[0] in ganador) and (not(w_o_d))):
        importe = cant_pago_x_apuestas * monto_a_apostar
 
    elif((ganador_x_api == equipo2[1]) and (equipo2[0] in ganador) and (not(w_o_d))):
        importe = cant_pago_x_apuestas * monto_a_apostar
    
    elif((ganador_x_api != equipo1[1]) and (equipo1[0] in ganador) and (w_o_d)):
        importe = cant_pago_x_apuestas * monto_a_apostar

    elif((ganador_x_api != equipo2[1]) and (equipo2[0] in ganador) and (w_o_d)):
        importe = cant_pago_x_apuestas * monto_a_apostar

    elif((ganador_x_api != equipo1[1]) and (equipo1[0] in ganador) and (not(w_o_d))):
        importe = pago_x_apuestas_wod * monto_a_apostar

    elif((ganador_x_api != equipo2[1]) and (equipo2[0] in ganador) and (not(w_o_d))):
        importe = pago_x_apuestas_wod * monto_a_apostar

    elif(ganador == "EMPATE"):
        importe = monto_a_apostar * 0.5
 
    return importe

def mostrar_pago_x_equipo(id_fixture:int, fixtures:dict):
    """

    PRECONDICION: Se recibe id_fixtures y cant_pago_x_apuestas valores enteros positivos
    POSTCONDICION: mostrara informacion de lo que se paga en caso de ganar o empatar

    """
    url1 = (f"/predictions?fixture={id_fixture}")
    data = lee_informacion(url1)

    w_o_d = (data['response'][0]['predictions']['win_or_draw'])
    ganador_x_api = (data['response'][0]['predictions']['winner']['name'])
    
    cant_pago_x_apuestas = pago_x_apuesta()
    pago_x_apuestas_wod = cant_pago_x_apuestas * 0.1
    equipo1 = fixtures[id_fixture][0]

    equipo2 = fixtures[id_fixture][1]

    if((ganador_x_api == equipo1[1]) and (equipo1[0] == 'L') and (w_o_d)):
        print(f"SI APUESTA POR {equipo1[1]} GANADOR  => PAGA {pago_x_apuestas_wod}  VECES LO APOSTADO")
        print(f"SI APUESTA POR {equipo2[1]} GANADOR  => PAGA {cant_pago_x_apuestas} VECES LO APOSTADO")

    if((ganador_x_api == equipo2[1]) and (equipo2[0] == 'L') and (w_o_d)):
        print(f"SI APUESTA POR {equipo2[1]} GANADOR  => PAGA {pago_x_apuestas_wod} VECES LO APOSTADO")
        print(f"SI APUESTA POR {equipo1[1]} GANADOR  => PAGA {cant_pago_x_apuestas}  VECES LO APOSTADO")

    if((ganador_x_api == equipo1[1]) and (equipo1[0] == 'V') and (w_o_d)):
        print(f"SI APUESTA POR {equipo1[1]} GANADOR  => PAGA {pago_x_apuestas_wod}  VECES LO APOSTADO")
        print(f"SI APUESTA POR {equipo2[1]} GANADOR  => PAGA {cant_pago_x_apuestas} VECES LO APOSTADO")

    if((ganador_x_api == equipo2[1]) and (equipo2[0] == 'V') and (w_o_d)):
        print(f"SI APUESTA POR {equipo2[1]} GANADOR  => PAGA {pago_x_apuestas_wod} VECES LO APOSTADO")
        print(f"SI APUESTA POR {equipo1[1]} GANADOR  => PAGA {cant_pago_x_apuestas}  VECES LO APOSTADO")

    if((ganador_x_api == equipo1[1]) and (equipo1[0] == 'L') and (not(w_o_d))):
        print(f"SI APUESTA POR {equipo1[1]} GANADOR  => PAGA {cant_pago_x_apuestas} VECES LO APOSTADO")
        print(f"SI APUESTA POR {equipo2[1]} GANADOR  => PAGA {pago_x_apuestas_wod} VECES LO APOSTADO")

    if((ganador_x_api == equipo2[1]) and (equipo2[0] == 'L') and (not(w_o_d))):
        print(f"SI APUESTA POR {equipo2[1]} GANADOR  => PAGA {cant_pago_x_apuestas} VECES LO APOSTADO")
        print(f"SI APUESTA POR {equipo1[1]} GANADOR  => PAGA {pago_x_apuestas_wod} VECES LO APOSTADO")

    if((ganador_x_api == equipo1[1]) and (equipo1[0] == 'V') and (not(w_o_d))):
        print(f"SI APUESTA POR {equipo1[1]} GANADOR  => PAGA {cant_pago_x_apuestas} VECES LO APOSTADO")
        print(f"SI APUESTA POR {equipo2[1]} GANADOR  => PAGA {pago_x_apuestas_wod} VECES LO APOSTADO")

    if((ganador_x_api == equipo2[1]) and (equipo2[0] == 'V') and (not(w_o_d))):
        print(f"SI APUESTA POR {equipo2[1]} GANADOR  => PAGA {cant_pago_x_apuestas} VECES LO APOSTADO")
        print(f"SI APUESTA POR {equipo1[1]} GANADOR  => PAGA {pago_x_apuestas_wod} VECES LO APOSTADO")

    print("SI APUESTA POR EMPATE PAGA 0.5 VECES LO APOSTADO") 
    return cant_pago_x_apuestas        
def simular_partido():
    """

    PRECONDICION: ---------------
    POSTCONDICION: Devolvera una cadena GANADOR(L):en caso de que gane el equipo local, GANADOR(V):en caso de que gane visitante y EMPATE: si el partido termina en empate

    """
    resultado_apuesta = random.randrange(TIRADA_DADO_MIN,TIRADA_DADO_MAX)
    if(resultado_apuesta == 1):
        ganador = "GANADOR(L)"
    elif(resultado_apuesta == 2):
        ganador = "EMPATE"
    else:
        if(resultado_apuesta == 3):
            ganador = "GANADOR(V)"
    return ganador

def guardar_transacciones(transacciones:list, archivo2):
    """
    
    PRECONDICION: recibe por parametro una lista
    POSTCONDICION: Guarda lista transacciones en un archivo2
    
    """
    with open(archivo2, 'w', newline='', encoding="UTF-8") as archivo_csv:
        csv_writer = csv.writer(archivo_csv, delimiter=',',quotechar='"', quoting= csv.QUOTE_NONNUMERIC)
        csv_writer.writerow(["ID", "Fecha Transaccion", "Tipo resultado", "Importe"])
        csv_writer.writerows(transacciones) #linea tiene que ser una lista

def cantidad_apostada_hasta_el_momento(id_usuario:str, usuarios:list, monto_a_apostar:int)->None:
    """
    
    PRECONDICION: 
    POSTCONDICION: modifica la cantidad apostada (posicion 3 de la lista de usuarios)
    
    """
    for fila in usuarios:
        if(id_usuario == fila[0]):
            fila[3] = str(int(fila[3]) + monto_a_apostar)

def fecha_ultima_apuesta(id_usuario:str, usuarios, fecha:str):
    """
    
    PRECONDICION: 
    POSTCONDICION: modifica la fecha
    
    """
    for fila in usuarios:
        if(id_usuario == fila[0]):
            fila[4] = fecha
                
def validar_monto(id_usuario:str, usuarios:list, monto_a_apostar:int)->bool:
    """
    
    PRECONDICION: 
    POSTCONDICION: devuelve true si el dinero a apostar es mayor o igual al dinero disponible de lo contrario false
    
    """
    monto_superado = False
    for fila in usuarios:
        if(id_usuario == fila[0]):
            if(monto_a_apostar > int(float(fila[5]))):
                monto_superado = True
                print(f"SU DINERO DISPONIBLE ES {fila[5]}")
    return monto_superado

def mostrar_ganador(equipo_ganador:str)->None:
    """
    
    PRECONDICION: Recibe por parametro una cadena con datos validos
    POSTCONDICION: muestra el resultado del partido
    
    """
    if(EQUIPO_VISITANTE in equipo_ganador):
        print("GANO EL EQUIPO VISITANTE")
    elif(EQUIPO_LOCAL in equipo_ganador):
        print("GANO EL EQUIPO LOCAL")
    else:
        print("EL PARTIDO TERMINO EN UN EMPATE")

def modificacion_importe(id_usuario:str, usuarios:list, importe:int,): 
    """
    
    PRECONDICION: 
    POSTCONDICION: modifica su dinero disponible y lo muestra por pantalla
    
    """
    for fila in usuarios:
        if(id_usuario == fila[0]):
            fila[5] = str(int(float(fila[5])) + (int(importe))) 
            print(f"SU DINERO DISPONIBLE ES {fila[5]}")


def validar_apuesta(apuesta):
    """
    
    PRECONDICION: el valor ingresado tiene que ser una cadena
    POSTCONDICION: Devuelve true si el valor recibido por parametro coincide con  uno de los valores compradados, de lo contrario devolvera false
    
    """
    apuesta_valida = False
    if((apuesta == "GANADOR(L)") or (apuesta == "GANADOR(V)") or (apuesta == "EMPATE")):
        apuesta_valida = True
    return apuesta_valida
            
def opcion_9(usuarios, id_usuario, transacciones):
    """

    PRECONDICION: se recibe el id_usuario como una cadena valida, una lista de usuarios y una lista de transacciones
    POSTCONDICION: se cargara la lista de transacciones con datos validos

    """
    linea = []
    print("SE LE MOSTRARA PREVIAMENTE UNA LISTA CON LOS EQUIPOS")
    print("DE LA LIGA PROFESIONAL CORRESPONDIENTE A LA TEMPORADA 2023 CON SUS RESPECTIVOS 'ID' ")
    equipos = cargando_equipos()
    mostrar_equipos_id(equipos)
    
    leer_equipo = input("INGRESE EL ID DEL EQUIPO PARA OBTENER INFORMACION DEL FIXTURE: ")
    while not numero_invalido(leer_equipo) or (int(leer_equipo) not in equipos):
        leer_equipo = input("INGRESE NUEVAMENTE EL ID DEL EQUIPO PARA OBTENER INFORMACION DEL FIXTURE: ")
    leer_equipo = int(leer_equipo)

    fixtures = cargar_fixture(leer_equipo)
    mostrar_fixtures(fixtures)
    importe = 0 
    respuesta = "si"

    while respuesta.lower() == "si":
        
        id_fixture = input("INGRESE EL ID DEL FIXTURE PARA MOSTRARLE LO QUE PAGA: ")
        while not numero_invalido(id_fixture) or (int(id_fixture)  not in fixtures):
            id_fixture = input("PARA APOSTAR POR UN EQUIPO INGRESE NUEVAMENTE, INGRESE UN ID DEL FIXTURE: ")
        id_fixture = int(id_fixture)

        cant_pago_x_apuestas = mostrar_pago_x_equipo(id_fixture, fixtures)
        respuesta = input("INGRESE 'si' SI DESEA VER CUANTO PAGA OTRO PARTIDO O INGRESE 'no' PARA APOSTAR: ")
        while((respuesta.lower() != "si") and (respuesta.lower() != "no")):
            respuesta = input("INGRESE NUEVAMENTE LA RESPUESTA: 'si' SI DESEA VER CUANTO PAGA OTRO PARTIDO O INGRESE 'no' PARA APOSTAR: ")

    print("QUE EMPIECE EL JUEGO")
    fecha=cargar_fecha_actual()
    ganador = simular_partido()

    leer_partido = input("PARA APOSTAR POR UN EQUIPO, INGRESE UN ID DEL FIXTURE: ")
    while not numero_invalido(leer_partido) or (int(leer_partido)  not in fixtures):
        leer_partido = input("PARA APOSTAR POR UN EQUIPO INGRESE NUEVAMENTE, INGRESE UN ID DEL FIXTURE: ")
    leer_partido = int(leer_partido)

    apuesta = input("INGRESE SU APUESTA (GANADOR(L)/EMPATE/GANADOR(V)): ")
    while(not validar_apuesta(apuesta)):
        apuesta = input("INGRESE SU APUESTA (GANADOR(L)/EMPATE/GANADOR(V)): ")

    monto_a_apostar = int(input("INGRESE EL MONTO A APOSTAR: "))
    if(not validar_monto(id_usuario, usuarios, monto_a_apostar)):
        print("\n")
        mostrar_ganador(ganador) 
        if apuesta == ganador:
            print("¡FELICIDADES! ES UN GANADOR")
            importe = importe_apuesta(leer_partido, fixtures, cant_pago_x_apuestas, ganador, monto_a_apostar)
            print(f"POR LA APUESTA GANADA SE LE HIZO UN PAGO DE ${importe} A SU DINERO DISPONIBLE")
            modificacion_importe(id_usuario, usuarios, importe) 
            resultado = "Gana"
        else:
            importe = (-monto_a_apostar) 
            print(f"PERDIO Y SE LE DESCONTO ${monto_a_apostar} DE SU DINERO DISPONIBLE")
            modificacion_importe(id_usuario, usuarios, importe)
            resultado = "Pierde"
    else:
        print(f"LO SENTIMOS  NO PUEDE APOSTAR") 

    if(int(importe) != 0):
        linea.append(id_usuario)
        linea.append(fecha)  
        linea.append(resultado) 
        linea.append(importe)

        transacciones.append(linea)

        cantidad_apostada_hasta_el_momento(id_usuario, usuarios, monto_a_apostar)
        fecha_ultima_apuesta(id_usuario, usuarios, fecha)
                

def seleccionar_opcion():
    menu()

    opcion = input("Ingrese una opcion: ")

    while valor_invalido(opcion, ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']):
        opcion = input(f"La opcion {opcion} es invalida. Por favor, seleccione una opcion valida: ")

    return opcion


def main():
    print("BIENVENIDOS AL PORTAL DE APUESTAS JUGARSELAS.\n")
    usuarios = cargar_usuarios(ARCHIVO)
    if(usuarios == -1):
        print("LO SENTIMOS!! NO SE PUEDE REALIZAR EL JUEGO PORQUE EL ARCHIVO DE USUARIOS NO EXISTE")
        return None
    
    transacciones = cargar_transacciones(ARCHIVO2)
    id_usuario, contrasenia = pedir_busqueda()
    registrado = registrar_usuario(id_usuario, contrasenia, usuarios)

    guardar_usuario(usuarios, ARCHIVO)
    usuarios = cargar_usuarios(ARCHIVO)

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
                opcion_6(id_usuario, leer_dinero,usuarios,transacciones) 
            elif opcion == 'f':
                opcion_7(usuarios)
            elif opcion == 'g':
                opcion_8(transacciones, usuarios)
            elif opcion == 'h':
                opcion_9(usuarios, id_usuario, transacciones)

            guardar_transacciones(transacciones, ARCHIVO2)

            opcion = seleccionar_opcion()

        guardar_usuario(usuarios, ARCHIVO)

main()

