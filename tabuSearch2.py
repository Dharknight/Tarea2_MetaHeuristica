import random
import copy

def leer(archivo):
    drones = []
    with open(archivo,'r+') as file:
        count = 0
        uav = {}
        id = 1 
        tiempos = []
        times = []
        for lines in file.readlines():
            lines = lines.split(' ')

            ######Correccion de texto ##### 
            if('\n' in lines[-1]):
                if(lines[-1] == '\n'): 
                    lines.pop()
                else:
                    lines[-1] = (lines[-1])[:-1] ## corta los números o palabras con un \n
            
            ##### Ingreso al diccionario #####
            if count == 0: ### Ingreso datos Cantidad de uavs
                uav['cantidad'] = int(lines[0])
                limit = int(lines[0])
                count = 1
                continue

                ### Ingreso informacion de tiempos
            if count == 1 and len(lines) == 3:
                uav = {
                    'id_uav': id,
                    'botTime':0,
                    'midTime':0,
                    'topTime':0,
                    'times':[]
                }
                times = []
                uav['id_uav'] = id
                uav['botTime'] = int(lines[0])
                uav['midTime'] = int(lines[1])
                uav['topTime'] = int(lines[-1])
                uav['times'] = times

                id = id + 1
                count = 2
                continue
                
                ###Ingreso los tiempos asociados a la cantidad y de cada uav.
            if(count == 2 ):
                if 'times' in uav: ## Reviso si ya existe la seccion de registros de tiempos en el diccionario
                    if len(times) < limit: #Los voy ingresando si es que no cumplen con la cantidad dedatos dichos.
                        for datos in lines: 
                            tiempos.append(int(datos))
                        times.extend(tiempos)
                        tiempos.clear()
                        if len(times) == limit:
                            count = 1  
                            uav['times'] = times
                            drones.append(uav)
    return drones

def gDeterminista(uavs):
    cost = 0
    uav_ant_id = 0
    uavs_orden = sorted(uavs, key=lambda uavs: uavs['midTime'], reverse=False) #UAVs ordenados de menor a mayor por medio del tiempo preferente
    
    for index, uav in enumerate(uavs_orden):
        if index == 0: #Primer UAV en aterrizar asumiendo que cae en su tiempo preferente
            uav['tiempo_aterrizaje'] = uav['midTime']
            cost = cost + 0
            uav_ant_id = uav['id_uav']
        else:
            tiempo_aterrizaje = uavs[uav_ant_id-1]['tiempo_aterrizaje'] + uav['times'][uav_ant_id-1]      #uav['midTime'] + uavs_orden[index-1]['times'][index]
            if tiempo_aterrizaje <= uav['topTime'] and tiempo_aterrizaje >= uav['botTime']: #Los uavs no pueden caer mas allá del tiempo máximo de aterrizaje
                uav['tiempo_aterrizaje'] = tiempo_aterrizaje
                cost = cost + abs(tiempo_aterrizaje - uav['midTime'])
                uav_ant_id = uav['id_uav']
            else:
                tiempo_aterrizaje =  abs(uavs[uav_ant_id-1]['tiempo_aterrizaje'] + uav['times'][uav_ant_id-1] - uav['midTime']) #uavs[uav_ant_id-1]['tiempo_aterrizaje'] + uav['times'][uav_ant_id-1]
                uav['tiempo_aterrizaje'] = uav['botTime']
                cost = cost + tiempo_aterrizaje
    return uavs_orden, cost

def gEstocastico(uavs):
    ##Vamos a generar una lista con los ids de cada uav para despues acceder de forma aleatoria a ellos mediante el greedy estocastico.
    cost = 0
    cant = len(uavs)
    uav_result = []
    tmpAterrizaje = 0
    i = 0 
    midTime = []
    midTimeTotal = 0 
    for uav in uavs: 
        midTime.append(uav['midTime'])
        midTimeTotal = midTimeTotal + uav['midTime']

    premium = False
    premiumID = 0
    for uav in uavs: 
        if uav['midTime'] == 0 or uav['topTime'] == 0 or uav['botTime'] == 0: 
            premium = True
            premiumID = uav['id_uav']
            break
    while((len(uavs)) != 0):
        if i == 0 and premium == False: # el primer uav me permite darle el tiempo de aterrizaje que yo quiera
            SEED = 0 #Genero un numero aleatorio para acceder a un uav de la lista de uavs ordenados
            this_uav = uavs[SEED]
            this_uav['tiempo_aterrizaje'] = this_uav['midTime']
            uav_ant = this_uav
            uavs.remove(this_uav)
            i =  1 
            #Calculamos las probabilidades de cada uav segun midtime/ midtimetotal
            probUavs = []
            for uav in uavs:
                probUavs.append(uav['midTime']/midTimeTotal)
            continue
        elif i == 0 and premium == True:
            this_uav = uavs[premiumID-1]
            this_uav['tiempo_aterrizaje'] = this_uav['midTime']
            uav_ant = this_uav
            uavs.remove(this_uav)
            i =  1
            #Calculamos las probabilidades de cada uav segun midtime/ midtimetotal
            probUavs = []
            for uav in uavs:
                probUavs.append(uav['midTime']/midTimeTotal)
            continue
        else:
            nextMidtime= random.choices(uavs,probUavs)[0]
            #ahora teniendo el midtime, sacamos el id del uav a escoger
            for uav in uavs:
                if uav['midTime'] == nextMidtime['midTime']:
                    this_uav = uav
                    break
            tmpAterrizaje = uav_ant['tiempo_aterrizaje'] + this_uav['times'][uav_ant['id_uav']-1]
            if(tmpAterrizaje <= this_uav['topTime'] and tmpAterrizaje >= this_uav['botTime']): # si esta dentro de los rangos, lo uso
                this_uav['tiempo_aterrizaje'] = tmpAterrizaje                
                cost = cost + abs(tmpAterrizaje - this_uav['midTime']) # calculo los costos
                uav_ant = this_uav # Guardo en una temporal la informacion de uav
                uavs.remove(this_uav) # Elimino el uav usado para no repetirlo
                probUavs = [] # Reinicio la probabilidad de los uavs.
                for uav in uavs:
                    probUavs.append(uav['midTime']/midTimeTotal)
            else:
                tmpAterrizaje =  abs(uav_ant['tiempo_aterrizaje']-this_uav['midTime'])
                this_uav['tiempo_aterrizaje'] = this_uav['botTime']
                cost = cost + tmpAterrizaje
                uav_ant = this_uav
                uavs.remove(this_uav)
                probUavs = [] # Reinicio la probabilidad de los uavs.
                for uav in uavs:
                    probUavs.append(uav['midTime']/midTimeTotal)
            i = i + 1
            uav_result.append(this_uav)
        #print("Se leyeron ",i, " uavs")
    return uav_result, cost

def generar_vecino(solucion):
    # Copiar la solución
    vecino = copy.deepcopy(solucion)

    # Seleccionar una posición aleatoria
    pos = random.randint(0, len(vecino) - 1)

    # Obtener el UAV en la posición seleccionada
    uav = vecino[pos]

    # Generar un nuevo tiempo de aterrizaje dentro del rango permitido
    nuevo_tiempo = random.randint(uav['botTime'], uav['topTime'])

    # Actualizar el tiempo de aterrizaje del UAV en el vecino
    uav['tiempo_aterrizaje'] = nuevo_tiempo

    return vecino


def evaluar(solucion):
    # Calcular el costo de la solución
    costo = 0
    for i in range(len(solucion) - 1):
        costo += abs(solucion[i]['tiempo_aterrizaje'] - solucion[i + 1]['tiempo_aterrizaje'])
    return costo

def tabu_search(solucion_inicial, lista_tabu_size, num_iteraciones):
    mejor_solucion = copy.deepcopy(solucion_inicial)
    mejor_costo = evaluar(mejor_solucion)
    lista_tabu = [copy.deepcopy(mejor_solucion)]  # Agregamos la solución inicial a la lista tabú
    list_t2 = []
    for uavs in mejor_solucion:
        list_t2.append(uavs.get('id_uav'))

    iteracion = 0
    while iteracion < num_iteraciones:
        vecinos = []
        for _ in range(lista_tabu_size):
            vecino = generar_vecino(mejor_solucion)
            while vecino in lista_tabu:  # Evitamos generar vecinos repetidos
                vecino = generar_vecino(mejor_solucion)
            vecinos.append(copy.deepcopy(vecino))

        mejor_vecino = min(vecinos, key=lambda x: evaluar(x))
        costo_vecino = evaluar(mejor_vecino)

        if costo_vecino < mejor_costo:
            mejor_solucion = copy.deepcopy(mejor_vecino)
            mejor_costo = costo_vecino

        lista_tabu.append(copy.deepcopy(mejor_vecino))
        list_t2.append(copy.deepcopy(mejor_vecino[0].get('id_uav')))
        if len(lista_tabu) > lista_tabu_size:
            lista_tabu.pop(0)
            list_t2.pop(0)
        #print(list_t2)
        iteracion += 1

    return mejor_solucion, mejor_costo



if __name__ == '__main__':
    
   
    print("1.- Deimos.txt")    
    print("2.- Europa.txt")
    print("3.- Titan.txt")
    choose = input("ingrese que texto quiere analizar para el algoritmo Hill Climbing Alguna_mejora:  ")
    match choose:
        case '1':
            ar = 't2_Deimos.txt'
        case '2':
            ar = 't2_Europa.txt'
        case '3':
            ar = 't2_Titan.txt'
    uavs = leer(ar)
    caminoDeterminista, costoDeterminista = gEstocastico(uavs)
    print("Costo Estocastico:",costoDeterminista)
    #ahora ejecutamos el tabu y mostramos sus resultados
    solucion_inicial = caminoDeterminista
    lista_tabu_size = 10
    num_iteraciones = 1000
    solucion, costo = tabu_search(copy.deepcopy(caminoDeterminista), lista_tabu_size, num_iteraciones)

    print("Costo Tabu Search:",costo)
    #if(caminoDeterminista != solucion):
    #    print("Camino Determinista:",caminoDeterminista)
    #    print("Camino Tabu Search:",solucion)
    #else: 
    #    print("son iguales los caminos.") 
    #print("Diferencia de Costos:",costoDeterminista-costo)

    

