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
EMPATE = 'E'

PAGO_APUESTA_MIN = 2
PAGO_APUESTA_MAX = 5

TIRADA_DADO_MIN = 1
TIRADA_DADO_MAX = 4

ID_USUARIO = 0
NOMBRE_USUARIO = 1
CANTIDAD_APOSTADA = 3
ULTIMA_APUESTA = 4
DINERO_DISPONIBLE = 5

RESULTADO = 2

DEPOSITAR = 'deposita'
GANA_APUESTA = 'gana'
PIERDE_APUESTA = 'pierde'

NOMBRE_EQUIPO = 0
ESCUDO_EQUIPO = 1
ESTADIO_EQUIPO = 2

def valor_invalido(valor, valores_validos):
    return valor not in valores_validos

def numero_invalido(numero: str):
    return numero.isnumeric()

def cargar_archivo_usuarios(archivo):
    """

    PRECONDICION: Se recibe un archivo.csv
    POSTCONDICION: Devuelve una lista en caso de que el archivo no este vacio, de lo contrario devolvera -1
    
    """
    usuarios = []
    try:
        with open(archivo, newline='', encoding="UTF-8") as archivo_csv:
            csv_reader = csv.reader(archivo_csv, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                usuarios.append(row)
    except FileNotFoundError:
        print("El archivo no existe")
        return -1

    return usuarios

def guardar_archivo_usuarios(usuarios, archivo):
    """

    PRECONDICION: Se recibe una lista de usuarios cargada
    POSTCONDICION: Se crea un archivo cargado con la lista de usuarios
     
    """

    with open(archivo, 'w', newline='', encoding="UTF-8") as archivo_csv:
        csv_writer = csv.writer(archivo_csv, delimiter=',',quotechar='"', quoting= csv.QUOTE_NONNUMERIC)
        csv_writer.writerow(["ID", "Nombre Usuario", "Contraseña", "Cantidad Apostada", "Fecha Ultima Apuesta", "Dinero Disponible"])
        csv_writer.writerows(usuarios)

def cargar_archivo_transacciones(archivo):
    """
    
    PRECONDICION: Se recibe un archivo.csv
    POSTCONDICION: Devuelve una lista en caso de que el archivo no este vacio, de lo contrario devolvera -1
    
    """    
    transacciones = []
    
    try:
        with open(archivo, newline='', encoding="UTF-8") as archivo_csv:
            csv_reader = csv.reader(archivo_csv, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                transacciones.append(row)
    except FileNotFoundError:
        print("El archivo no existe")
        return -1
                    
    return transacciones

def guardar_archivo_transacciones(transacciones:list, archivo2):
    """
    
    PRECONDICION: recibe por parametro una lista
    POSTCONDICION: Guarda lista transacciones en un archivo2
    
    """
    with open(archivo2, 'w', newline='', encoding="UTF-8") as archivo_csv:
        csv_writer = csv.writer(archivo_csv, delimiter=',',quotechar='"', quoting= csv.QUOTE_NONNUMERIC)
        csv_writer.writerow(["ID", "Fecha Transaccion", "Tipo resultado", "Importe"])
        csv_writer.writerows(transacciones) #linea tiene que ser una lista

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
    encontrado = -1
    i = 0
    
    while((encontrado != 0) and (i < len(usuarios))):

        fila = usuarios[i]

        if((id_usuario == fila[0]) and (pbkdf2_sha256.verify(contrasenia, fila[2]))):
            buscado = REGISTRADO
            encontrado = 0

        elif(id_usuario == fila[0]): 
            buscado = CONTRASENIA_INCORRECTA
            encontrado = 0
        
        else:
            i += 1
	
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

def menu():

    print("---------------MENU DE OPCIONES-----------------------------")
    print("(1) SE LE MUESTRA EL PLANTEL COMPLETO DE TODOS LOS EQUIPOS DE LPF ARGENTINA 2023")
    print("(2) SE LE MUESTRA LA TABLA DE POSICIONES DEL AÑO QUE ELIJA DE LPF ARGENTINA")
    print("(3) SE LE MUESTRA INFORMACION ACERCA DEL ESTADIO Y ESCUDO DE UN EQUIPO ELEGIDO")
    print("(4) SE LE MUESTRA UN GRAFICO DE LOS GOLES POR MINUTO DE UN EQUIPO ELEGIDO")
    print("(5) INGRESAR DINERO EN SU CUENTA")
    print("(6) SE LE MUESTRA EL USUARIO QUE MAS APOSTO HASTA EL MOMENTO")
    print("(7) SE LE MUESTRA EL USUARIO QUE MAS GANO HASTA EL MOMENTO")
    print("(8) APOSTAR")
    print("(9) SALIR DEL PROGRAMA")

def seleccionar_opcion():
    menu()

    opcion = input("Ingrese una opcion: ")

    while valor_invalido(opcion, ['1', '2', '3', '4', '5', '6', '7', '8', '9']):
        opcion = input(f"La opcion {opcion} es invalida. Por favor, seleccione una opcion valida: ")

    return opcion

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

def imprimir_plantel_equipo_seleccionado():
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

def ingresar_anio():
    anio = input("Ingrese una temporada (2015-2023) para consultar su tabla de posiciones: ")
    while valor_invalido(anio, ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023']) :
        anio = input("La temporada ingresada es invalida. Ingrese nuevamente la temporada: ")
    anio = int(anio)

    return anio

def imprimir_tabla_anio_seleccionado():
    """

    PRECONDICION: Pide al usuario que ingrese una temporada para consultar la tabla de posiciones.
    POSTCONDICION: Imprime los datos solicitados por el usuario

    """

    anio = ingresar_anio()

    url = (f"/standings?league=128&season={anio}")
    data_liga_anio_ingresado = lee_informacion(url)

    datos_liga = data_liga_anio_ingresado['response'][0] 
    posiciones = datos_liga['league']['standings'][0]

    print(f"----Tabla de posiciones LPF Argentina {anio}")
    if (anio == 2015) or (anio == 2016) or (anio == 2017) or (anio == 2018) or (anio == 2019): 
        mostrar_tabla_quince_to_diecinueve(posiciones)

    elif (anio == 2020): 
        mostrar_tabla_veinte(datos_liga)

    elif (anio == 2021) or (anio == 2022):
        mostrar_tabla_veinti_uno_dos(datos_liga)

    elif (anio == 2023):        
        mostrar_tabla_veinti_tres(anio, datos_liga)

def mostrar_tabla_quince_to_diecinueve(posiciones:dict):

    for i in posiciones:            
            puesto = i['rank']
            equipo = i['team']['name']
            puntos = i['points']
            jugados = i['all']['played']
            ganados = i['all']['win']
            empatados = i['all']['draw']
            perdidos = i['all']['lose']

            print(f"{puesto}) {equipo}: {puntos} puntos. En {jugados} partidos obtuvo {ganados} victorias, {perdidos} derrotas y {empatados} empates")

def mostrar_tabla_veinti_uno_dos(datos_liga:dict):

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

    posiciones_mostrar_primera_fase = datos_liga['league']['standings'][0]
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

def mostrar_tabla_veinte(datos_liga:dict):
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

def mostrar_escudo_estadio_equipo_seleccionado():
    """
    PRECONDICION: Pide al usuario que elija un equipo de la lista.
    POSTCONDICION: Muestra los datos del estadio y el escudo de ese equipo.

    """ 
    datos_equipos = cargar_equipos()
    mostrar_equipos_id(datos_equipos)
    id_equipo_elegido = validar_equipo_ingresado(datos_equipos)

    datos_equipo_elegido = datos_equipos[id_equipo_elegido]
    nombre_equipo_elegido = datos_equipo_elegido[NOMBRE_EQUIPO]
    print()
    print(nombre_equipo_elegido)

    mostrar_datos_estadio(datos_equipo_elegido)

    mostrar_escudo(datos_equipo_elegido)

def mostrar_datos_estadio(datos_equipo_elegido):
   
    datos_estadio = datos_equipo_elegido[ESTADIO_EQUIPO]
    nombre = datos_estadio['name']
    direccion = datos_estadio['address']
    ciudad = datos_estadio['city']
    capacidad = datos_estadio['capacity']
    logo = datos_estadio['image']

    response = requests.get(logo)
    img = Image.open(BytesIO(response.content))
    img.show()
   
    print(f"El {nombre} esta ubicado en la calle {direccion} de la ciudad de {ciudad}. Tiene una capacidad para {capacidad} personas.")

def mostrar_escudo(datos_equipo_elegido):

    escudo = datos_equipo_elegido[ESCUDO_EQUIPO]
    response = requests.get(escudo)
    img = Image.open(BytesIO(response.content))
    img.show()

def mostrar_grafico_goles_equipo_seleccionado()->None:
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
    
def cargar_fecha_actual():
    fecha_actual = datetime.now()
    fecha = datetime.strftime(fecha_actual,'%Y-%m-%d')
    
    return fecha

def cargar_dinero_ingresado():
    dinero_ingresado = input("CUANTO DINERO DESEA CARGAR (INGRESAR SOLO EL NUMERO): ")
    while not numero_invalido(dinero_ingresado):
        dinero_ingresado = input("VALOR INVALIDO. VUELVA A INGRESAR CUANTO DINERO DESEA CARGAR (INGRESAR SOLO EL NUMERO): ")
    dinero_ingresado = int(dinero_ingresado)

    return dinero_ingresado

def agregar_transaccion(id_usuario, fecha_actual, tipo_resultado, importe, transacciones):
    linea = []
    linea.append(id_usuario)
    linea.append(fecha_actual)
    linea.append(tipo_resultado)
    linea.append(str(importe))

    transacciones.append(linea)

def depositar_dinero_ingresado(dinero_ingresado:int, fecha_actual:str, id_usuario:str, usuarios:list, transacciones:list):
    encontrado = -1
    i = 0
    
    while((encontrado != 0) and (i < len(usuarios))):

        fila = usuarios[i]

        if(id_usuario == fila[ID_USUARIO]):

            fila[DINERO_DISPONIBLE] = str(int(fila[DINERO_DISPONIBLE]) + dinero_ingresado)
            print("SE AGREGO DINERO A SU CUENTA CON EXITO")
            print(f"SU DINERO DISPONIBLE HASTA EL MOMENTO ES {fila[DINERO_DISPONIBLE]}")
            tipo_resultado = DEPOSITAR 
            importe = dinero_ingresado

            agregar_transaccion(id_usuario, fecha_actual, tipo_resultado, importe, transacciones)
            
            encontrado = 0

        else:
            i += 1
    
def ingresar_dinero_cuenta_usuario(id_usuario:str, usuarios:list, transacciones:list):
    """
    PRECONDICION: 
    POSTCONDICION: Se cargara una lista con campos validos a la lista transacciones
    """
    valor_ingresado = cargar_dinero_ingresado()
    fecha = cargar_fecha_actual()

    depositar_dinero_ingresado(valor_ingresado, fecha, id_usuario, usuarios, transacciones)

def mostrar_usuario_mas_apostador(usuarios:list)->None:
    """
    PRECONDICION: Se recibe una lista con datos validos
    POSTCONDICION: Se muestra por pantalla el usuario que mas dinero aposto
    
    """
    max_apostado = -1

    for fila in usuarios:
        if(int(fila[CANTIDAD_APOSTADA]) > max_apostado):
            max_apostado = int(fila[CANTIDAD_APOSTADA])
            usuario_max_apostador = fila[ID_USUARIO]
    
    if(max_apostado == 0):
        print("NO HAY INFORMACION, PORQUE AUN NADIE APOSTO")

    elif(max_apostado > 0):
        print(f"EL USUARIO {usuario_max_apostador} CON LA CANTIDAD DE ${max_apostado} ES EL QUE MAS DINERO APOSTO")

def mostrar_usuario_mas_ganador(transacciones:list, usuarios:list):
    """
    PRECONDICION: 
    POSTCONDICION: se mostrara informacion del usuario que mas veces gano
    
    """
    cantidad_veces_ganadas = {}
    max_cantidad_veces_ganadas = -1
    
    for fila in transacciones:
        nombre_usuario = fila[ID_USUARIO]
        resultado = fila[RESULTADO]

        if(resultado == GANA_APUESTA):
            if(nombre_usuario not in cantidad_veces_ganadas):
                cantidad_veces_ganadas[nombre_usuario] = 1
            else:
                cantidad_veces_ganadas[nombre_usuario] += 1
    
    if(cantidad_veces_ganadas == {}):
        print(f"TODAVIA NO GANO NINGUN USUARIO APOSTANDO")

    else:
        for nombre_usuario in cantidad_veces_ganadas:
            valor = cantidad_veces_ganadas[nombre_usuario]
            
            if(valor > max_cantidad_veces_ganadas):
                mas_ganador = nombre_usuario
                max_cantidad_veces_ganadas = valor
        
        print(f"EL USUARIO QUE MAS VECES GANO APOSTANDO ES {mas_ganador}, HABIENDO GANADO {max_cantidad_veces_ganadas} APUESTAS")
                
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

def cargar_equipos():
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
        escudo = (data['response'][resultado]['team']['logo'])
        datos_estadio = (data['response'][resultado]['venue'])

        equipos[id_equipo] = nombre_equipo, escudo, datos_estadio
    
    return equipos

def mostrar_equipos_id(equipos:dict):
    """

    PRECONDICION: recibe un diccionario cargado con datos validos.
    POSTCONDICION: Se imprimira por pantalla informacion deL diccionario.

    """
    print("EQUIPOS LIGA PROFESIONAL DE FUTBOL 2023")
    for id_equipo in equipos:
        nombre_equipo = equipos[id_equipo][NOMBRE_EQUIPO]
        print(f"ID {id_equipo} - {nombre_equipo} ")

def jugada(local_o_visitante):
    """

    PRECONDICION: recibe como valor una cadena 'home' o 'away'
    POSTCONDICION: Se imprimira 'L' si es local o 'V'  si es visitante

    """
    if('home' in local_o_visitante):
        local_o_visitante = EQUIPO_LOCAL

    elif('away' in local_o_visitante):
        local_o_visitante = EQUIPO_VISITANTE
    
    return local_o_visitante

def cargar_fixture(equipo_ingresado):
    """

    PRECONDICION: recibe por paramentro un numero entero positivo.
    POSTCONDICION: devolvera un diccionario con los fixtures.

    """
    fixtures = {}
    url1 =  (f"/fixtures?league=128&season=2023&team={equipo_ingresado}")
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

def mostrar_fixture_equipo_elegido(fixtures):
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

def importe_apuesta(id_fixture:int, data_fixture:dict, fixtures:dict, cant_pago_x_apuestas:int, resultado_simulado:str, dinero_apostado:int):
    """
    PRECONDICION: recibe por parametro valores validos
    POSTCONDICION: devuelve un numero positivo, resultado de lo que paga por fixture

    """
    prediccion_ganador_api = data_fixture['response'][0]['predictions']['winner']['name']

    pago_x_apuestas_wod = cant_pago_x_apuestas * 0.1

    equipo1 = fixtures[id_fixture][0]
    equipo2 = fixtures[id_fixture][1]

    if((prediccion_ganador_api == equipo1[1]) and (equipo1[0] == resultado_simulado)):
        importe = pago_x_apuestas_wod * dinero_apostado
    
    elif((prediccion_ganador_api == equipo2[1]) and (equipo2[0] == resultado_simulado)):
        importe = pago_x_apuestas_wod * dinero_apostado
    
    elif((prediccion_ganador_api != equipo1[1]) and (equipo1[0] == resultado_simulado)):
        importe = cant_pago_x_apuestas * dinero_apostado

    elif((prediccion_ganador_api != equipo2[1]) and (equipo2[0] == resultado_simulado)):
        importe = cant_pago_x_apuestas * dinero_apostado

    elif(resultado_simulado == EMPATE):
        importe = dinero_apostado * 0.5
 
    return importe

def mostrar_pago_x_equipo(id_fixture:int, fixtures:dict):
    """

    PRECONDICION: Se recibe id_fixtures y cant_pago_x_apuestas valores enteros positivos
    POSTCONDICION: mostrara informacion de lo que se paga en caso de ganar o empatar

    """
    url1 = (f"/predictions?fixture={id_fixture}")
    data = lee_informacion(url1)

    prediccion_ganador_api = (data['response'][0]['predictions']['winner']['name'])
    
    cant_pago_x_apuestas = pago_x_apuesta()
    pago_x_apuestas_wod = cant_pago_x_apuestas * 0.1
    
    equipo1 = fixtures[id_fixture][0]
    equipo2 = fixtures[id_fixture][1]

    if((prediccion_ganador_api == equipo1[1]) and (equipo1[0] == EQUIPO_LOCAL)):
        print(f"SI APUESTA POR {equipo1[1]} ({EQUIPO_LOCAL}) GANADOR  => PAGA {pago_x_apuestas_wod}  VECES LO APOSTADO")
        print(f"SI APUESTA POR {equipo2[1]} ({EQUIPO_VISITANTE}) GANADOR  => PAGA {cant_pago_x_apuestas} VECES LO APOSTADO")

    elif((prediccion_ganador_api == equipo2[1]) and (equipo2[0] == EQUIPO_LOCAL)):
        print(f"SI APUESTA POR {equipo2[1]} ({EQUIPO_LOCAL}) GANADOR  => PAGA {pago_x_apuestas_wod} VECES LO APOSTADO")
        print(f"SI APUESTA POR {equipo1[1]} ({EQUIPO_VISITANTE}) GANADOR  => PAGA {cant_pago_x_apuestas}  VECES LO APOSTADO")

    elif((prediccion_ganador_api == equipo1[1]) and (equipo1[0] == EQUIPO_VISITANTE)):
        print(f"SI APUESTA POR {equipo1[1]} ({EQUIPO_VISITANTE}) GANADOR  => PAGA {pago_x_apuestas_wod}  VECES LO APOSTADO")
        print(f"SI APUESTA POR {equipo2[1]} ({EQUIPO_LOCAL}) GANADOR  => PAGA {cant_pago_x_apuestas} VECES LO APOSTADO")

    elif((prediccion_ganador_api == equipo2[1]) and (equipo2[0] == EQUIPO_VISITANTE)):
        print(f"SI APUESTA POR {equipo2[1]} ({EQUIPO_VISITANTE}) GANADOR  => PAGA {pago_x_apuestas_wod} VECES LO APOSTADO")
        print(f"SI APUESTA POR {equipo1[1]} ({EQUIPO_LOCAL}) GANADOR  => PAGA {cant_pago_x_apuestas}  VECES LO APOSTADO")

    print("SI APUESTA POR EMPATE PAGA 0.5 VECES LO APOSTADO") 

    return cant_pago_x_apuestas, data     

def simular_partido():
    """

    PRECONDICION: ---------------
    POSTCONDICION: Devolvera una cadena GANADOR(L):en caso de que gane el equipo local, GANADOR(V):en caso de que gane visitante y EMPATE: si el partido termina en empate

    """
    resultado_partido = random.randrange(TIRADA_DADO_MIN, TIRADA_DADO_MAX)

    if(resultado_partido == 1):
        resultado_simulado = EQUIPO_LOCAL

    elif(resultado_partido == 2):
        resultado_simulado = EMPATE

    elif(resultado_partido == 3):
        resultado_simulado = EQUIPO_VISITANTE
    
    return resultado_simulado

def modificar_cantidad_apostada(id_usuario:str, usuarios:list, dinero_apostado:int)->None:
    """
    PRECONDICION: 
    POSTCONDICION: modifica la cantidad apostada (posicion 3 de la lista de usuarios)
    
    """
    encontrado = -1
    i = 0
    
    while((encontrado != 0) and (i < len(usuarios))):

        fila = usuarios[i]

        if(id_usuario == fila[ID_USUARIO]):
            encontrado = 0
            fila[CANTIDAD_APOSTADA] = str(int(fila[CANTIDAD_APOSTADA]) + dinero_apostado)
            print(f"SU TOTAL DE DINERO APOSTADO ES ${fila[CANTIDAD_APOSTADA]}")
        else:
            i += 1

def modificar_fecha_ultima_apuesta(id_usuario:str, usuarios:list, fecha:str):
    """
    PRECONDICION: 
    POSTCONDICION: modifica la fecha
    
    """
    encontrado = -1
    i = 0
    
    while((encontrado != 0) and (i < len(usuarios))):

        fila = usuarios[i]

        if(id_usuario == fila[ID_USUARIO]):
            encontrado = 0
            fila[ULTIMA_APUESTA] = fecha
        else:
            i += 1
                
def monto_excedido(id_usuario:str, usuarios:list, dinero_apostado:int)->bool:
    """
    PRECONDICION: 
    POSTCONDICION: devuelve true si el dinero a apostar es mayor o igual al dinero disponible de lo contrario false

    """
    monto_superado = False
    encontrado = -1
    i = 0
    
    while((encontrado != 0) and (i < len(usuarios))):

        fila = usuarios[i]

        if(id_usuario == fila[ID_USUARIO]):
            encontrado = 0

            if(dinero_apostado > int(fila[DINERO_DISPONIBLE])):
                monto_superado = True
                print(f"SU DINERO DISPONIBLE ES {fila[DINERO_DISPONIBLE]}")
        else:
            i += 1
	
    return monto_superado

def mostrar_ganador(equipo_ganador:str)->None:
    """
    PRECONDICION: Recibe por parametro una cadena con datos validos
    POSTCONDICION: muestra el resultado del partido
    
    """
    if(EQUIPO_VISITANTE == equipo_ganador):
        print("GANO EL EQUIPO VISITANTE")

    elif(EQUIPO_LOCAL == equipo_ganador):
        print("GANO EL EQUIPO LOCAL")

    elif(EMPATE == equipo_ganador):
        print("EL PARTIDO TERMINO EN UN EMPATE")

def modificar_dinero_disponible(id_usuario:str, usuarios:list, importe:int,): 
    """
    PRECONDICION: 
    POSTCONDICION: modifica su dinero disponible y lo muestra por pantalla
    
    """
    encontrado = -1
    i = 0
    
    while((encontrado != 0) and (i < len(usuarios))):

        fila = usuarios[i]

        if(id_usuario == fila[ID_USUARIO]):
            encontrado = 0
            fila[DINERO_DISPONIBLE] = str(int(fila[DINERO_DISPONIBLE]) + (int(importe)))
            print(f"SU DINERO DISPONIBLE ES ${fila[DINERO_DISPONIBLE]}")

        else:
            i += 1
            
def validar_equipo_ingresado(equipos:dict):
    equipo_ingresado = input("INGRESE EL ID DEL EQUIPO: ")
    while not numero_invalido(equipo_ingresado) or (int(equipo_ingresado) not in equipos):
        equipo_ingresado = input("INGRESE NUEVAMENTE EL ID DEL EQUIPO: ")
    equipo_ingresado = int(equipo_ingresado)

    return equipo_ingresado

def mostrar_cuotas_fixture(fixtures:dict):
    respuesta = "si"

    while respuesta.lower() == "si":
        
        id_fixture = input("INGRESE EL ID DEL FIXTURE PARA MOSTRARLE LO QUE PAGA: ")
        while not numero_invalido(id_fixture) or (int(id_fixture)  not in fixtures):
            id_fixture = input("PARA APOSTAR POR UN EQUIPO INGRESE NUEVAMENTE, INGRESE UN ID DEL FIXTURE: ")
        id_fixture = int(id_fixture)

        cant_pago_x_apuestas, data_fixture = mostrar_pago_x_equipo(id_fixture, fixtures)
        respuesta = input("INGRESE 'si' SI DESEA VER CUANTO PAGA OTRO PARTIDO O INGRESE 'no' PARA APOSTAR: ")
        while((respuesta.lower() != "si") and (respuesta.lower() != "no")):
            respuesta = input("INGRESE NUEVAMENTE LA RESPUESTA: 'si' SI DESEA VER CUANTO PAGA OTRO PARTIDO O INGRESE 'no' PARA APOSTAR: ")

    return id_fixture, cant_pago_x_apuestas, data_fixture

def elegir_resultado():
    resultado = input("INGRESE SU APUESTA (GANADOR (L)/ EMPATE (E)/ GANADOR (V)): ").upper()
    while valor_invalido(resultado, [EQUIPO_LOCAL, EQUIPO_VISITANTE, EMPATE]):
        resultado = input("VUELVA A INGRESAR SU APUESTA (GANADOR (L)/ EMPATE (E)/ GANADOR (V)): ").upper()
    
    return resultado

def elegir_monto():
    dinero_apostado = input("INGRESE EL MONTO A APOSTAR: ")
    while not numero_invalido(dinero_apostado):
        dinero_apostado = input("VUELVA A INGRESAR EL MONTO A APOSTAR: ")
    dinero_apostado = int(dinero_apostado)

    return dinero_apostado

def apostar(usuarios, id_usuario, transacciones):
    """

    PRECONDICION: se recibe el id_usuario como una cadena valida, una lista de usuarios y una lista de transacciones
    POSTCONDICION: se cargara la lista de transacciones con datos validos

    """
    equipos = cargar_equipos()
    mostrar_equipos_id(equipos)
    
    id_equipo_ingresado = validar_equipo_ingresado(equipos)

    fixtures = cargar_fixture(id_equipo_ingresado)
    mostrar_fixture_equipo_elegido(fixtures)

    id_fixture, pago_por_apuesta, data_fixture = mostrar_cuotas_fixture(fixtures)

    fecha = cargar_fecha_actual()

    resultado_simulado = simular_partido()

    resultado_apostado = elegir_resultado()
    dinero_apostado = elegir_monto()

    importe = 0

    if not monto_excedido(id_usuario, usuarios, dinero_apostado):
        print("\n")

        mostrar_ganador(resultado_simulado) 

        if (resultado_apostado == resultado_simulado):
            importe = importe_apuesta(id_fixture, data_fixture, fixtures, pago_por_apuesta, resultado_simulado, dinero_apostado)

            print(f"POR LA APUESTA GANADA SE LE HIZO UN PAGO DE ${importe} A SU DINERO DISPONIBLE")
            
            resultado = GANA_APUESTA
        else:
            importe = (-dinero_apostado) 

            print(f"PERDIO Y SE LE DESCONTO ${dinero_apostado} DE SU DINERO DISPONIBLE")

            resultado = PIERDE_APUESTA
    else:
        print(f"LO SENTIMOS NO PUEDE APOSTAR, INGRESE DINERO EN SU CUENTA") 

    importe = int(importe)

    if(importe != 0):

        agregar_transaccion(id_usuario, fecha, resultado, importe, transacciones)

        modificar_dinero_disponible(id_usuario, usuarios, importe)

        modificar_cantidad_apostada(id_usuario, usuarios, dinero_apostado)

        modificar_fecha_ultima_apuesta(id_usuario, usuarios, fecha)
                
def main():
    print("INICIANDO APLICACION...\n")
    usuarios = cargar_archivo_usuarios(ARCHIVO)
    if(usuarios == -1):
        print("CERRANDO APLICACION...")
        return 0
    
    transacciones = cargar_archivo_transacciones(ARCHIVO2)
    #id_usuario, contrasenia = pedir_busqueda()
    id_usuario = "agustinpelliciari@gmail.com"
    contrasenia = "Riverplate"
    registrado = registrar_usuario(id_usuario, contrasenia, usuarios)

    if(registrado):

        opcion = seleccionar_opcion()		

        while opcion != '9':

            if opcion == '1':
                imprimir_plantel_equipo_seleccionado()                     
            elif opcion == '2':
                imprimir_tabla_anio_seleccionado()                     
            elif opcion == '3':
                mostrar_escudo_estadio_equipo_seleccionado()                     
            elif opcion == '4':
                mostrar_grafico_goles_equipo_seleccionado()                     
            elif opcion == '5':
                ingresar_dinero_cuenta_usuario(id_usuario, usuarios, transacciones) 
            elif opcion == '6':
                mostrar_usuario_mas_apostador(usuarios)
            elif opcion == '7':
                mostrar_usuario_mas_ganador(transacciones, usuarios)
            elif opcion == '8':
                apostar(usuarios, id_usuario, transacciones)

            guardar_archivo_transacciones(transacciones, ARCHIVO2)

            opcion = seleccionar_opcion()

        guardar_archivo_usuarios(usuarios, ARCHIVO)

main()

