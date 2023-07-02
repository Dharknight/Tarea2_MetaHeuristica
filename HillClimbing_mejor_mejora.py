import random
import copy

#FUNCIÓN QUE LEE Y EXTRAE LOS DATOS DE LOS ARCHIVOS.
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

#FUNCIÓN DEL GREEDY DETERMINISTA.
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

#FUNCIÓN DEL GREEDY ESTOCÁSTICO.
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

#FUNCIÓN QUE EJECUTA EL ALGORITMO HILL CLIMBING MEJOR-MEJORA.
def hill_climbing_mejor_mejora(caminoDeterminista, costoDeterminista, count_neighbors):
    mejorCostoVecino = costoDeterminista
    tmp_mejorVecino = caminoDeterminista
    while True: #AL EJECUTARSE EL HILL CLIMBING ITER VECES, SE ACABA EL ALGORITMO CON LA MEJOR SOLUCIÓN ENCONTRADA BAJO ESA CANTIDAD DE ITERACIONES
        a = 0
        for nei in tmp_mejorVecino: #SE LIMPIA AL IGUAL QUE EN LOS DEMÁS ALGORITMOS LA LISTA DE UAVS A ATERRIZAR PARA PODER REALIZAR EL CALCULO DE ATERRIZAJE Y COSTO DE FORMA CORRECTA
            if 'tiempo_aterrizaje' in nei:
                del nei['tiempo_aterrizaje']
        if tmp_mejorVecino[0]['botTime'] == 0 and tmp_mejorVecino[0]['midTime'] == 0 and tmp_mejorVecino[0]['topTime'] == 0: #CASO ESPECÍFICO QUE SE ESTÉ TRABAJANDO CON EL ARHCHIVO 2.
            vecinos = generar_todos_los_vecinos(tmp_mejorVecino,0, count_neighbors)  #GENERACIÓN DE VECINOS
        else:
            vecinos = generar_todos_los_vecinos(tmp_mejorVecino,1, count_neighbors)  #GENERACIÓN DE VECINOS
        for vecino in vecinos:  #SE RECORRE EL VECINDARIO DE LA SOLUCIÓN
            costoVecino, Vecino = calcular_costo(vecino)    #SE CALCULA EL COSTO DE LA POSIBLE SOLUCIÓN
            if costoVecino < mejorCostoVecino:  #SI LA SOLUCIÓN POSEE UN COSTO MENOR QUE ANTES ENTONCES SE TRANSFORMA EN LA NUEVA MEJOR SOLUCIÓN
                print('Estoy ', costoVecino)
                tmp_mejorVecino= Vecino
                mejorVecino = copy.deepcopy(Vecino)
                mejorCostoVecino = costoVecino
            else:
                a = a + 1
        if a == len(vecinos) and tmp_mejorVecino != caminoDeterminista: #SI SE RECORRIÓ TODO EL VECINDARIO Y SI EXISTE SOLUCIÓN MEJOR QUE LA INICIAL.
            return mejorVecino, mejorCostoVecino
        elif a == len(vecinos) and tmp_mejorVecino == caminoDeterminista: #SI SE RECORRIÓ TODO EL VECINDARIO Y NO EXISTE SOLUCIÓN MEJOR QUE LA INICIAL.
            return tmp_mejorVecino, mejorCostoVecino
        
#FUNCIÓN QUE GENERA count_neighbor cantidad de VECINOS.
def generar_todos_los_vecinos(camino, premium, count_neighbor): 
    vecinos = []    #LISTA QUE ALMACENARÁ EL VECINDARIO DE UNA SOLUCIÓN.
    a = 0
    if premium == 0:    #EN CASO EXCEPCIONAL QUE SE ESTÉ TRABAJANDO CON EL ARCHIVO 2. YA QUE EN ESTE EL PRIMER UAV EMPIEZA EN EL TIEMPO 0.
        while a < count_neighbor:
            vecino = copy.deepcopy(camino)
            p = random.randint(0,len(camino)-1)
            k = random.randint(0,len(camino)-1)
            if p != k:
                vecino[p] , vecino[k] = vecino[k], vecino[p]
                vecinos.append(vecino)
                a = a + 1
    else:   #LO MISMO QUE EN EL IF, SOLO QUE ACÁ ES CUANDO SE ESTÉ TRABAJANDO CON OTROS ARCHIVOS QUE NO SEAN EL 2.
        while a < count_neighbor:
            vecino = copy.deepcopy(camino)
            p = random.randint(0,len(camino)-1)
            k = random.randint(0,len(camino)-1)
            if p != k:
                vecino[p] , vecino[k] = vecino[k], vecino[p]
                vecinos.append(vecino)
                a = a + 1
    return vecinos

#FUNCIÓN QUE CALCULA EL COSTO DE LA SECUENCIA DE ATERRIZAJE DE LOS UAVS.
def calcular_costo(camino):
    cost = 0
    uav_ant = None
    for index, uav in enumerate(camino):    #SE RECORRE LA LISTA DE UAVS A ATERRIZAR EN ORDEN.
        if index == 0:  #EL PRIMERO EN CAER, AL IGUAL QUE EN EL CÓDIGO GREEDY SE ESTABLECE EN SU TIEMPO PREFERENTE SU ATERRIZAJE.
            uav['tiempo_aterrizaje'] = uav['midTime']
            cost = cost + 0
            uav_ant = uav
        else: #SE REALIZA EL MISMO CÁLCULO QUE EN EL CÓDIGO GREEDY
            tiempo_aterrizaje = uav_ant['tiempo_aterrizaje'] + uav['times'][uav_ant['id_uav']-1] 
            if tiempo_aterrizaje <= uav['topTime'] and tiempo_aterrizaje >= uav['botTime']: #SI EL TIEMPO DE ATERRIZAJE CORRESPONDE DENTRO DE LOS RANGOS ESTABLECIDOS POR EL ARCHIVO PARA EL UAV
                uav['tiempo_aterrizaje'] = tiempo_aterrizaje
                cost = cost + abs(tiempo_aterrizaje - uav['midTime'])
            else: #SI NO, SE LE OBLIGA A ATERRIZAR EN EL TIEMPO MENOR Y ESO CONLLEVA A UNA PENALIZACIÓN MAYOR
                tiempo_aterrizaje = abs(uav_ant['tiempo_aterrizaje'] + uav['times'][uav_ant['id_uav']-1] - uav['midTime'])
                uav['tiempo_aterrizaje'] = uav['botTime']
                cost = cost + tiempo_aterrizaje
            uav_ant = uav
    return cost, camino

#MAIN DEL PROGRAMA.
if __name__ == '__main__':
    #hacemos un match para saber que texto escoger
    print('1.- Trabajar t2_Deimos.txt '+
          '\n 2.- Trabajar t2_Europa.txt'+
          '\n 3.- Trabajar t2_Titan.txt')
    choose = input()
    match choose:
        case '1':
            ar = 't2_Deimos.txt'
            print('1.- Aplicar Hill Climbing Mejor-Mejora con Greedy Determinista' + 
                  ' \n 2.- Aplicar Hill Climbing Mejor-Mejora con Greedy Estocástico')
            choose2 = input()
            match choose2:
                case '1':
                    uavs = leer(ar)
                    caminoDeterminista, costoDeterminista = gDeterminista(uavs)
                    print("Costo Determinista:",costoDeterminista) 
                    mejorCamino, mejorCosto = hill_climbing_mejor_mejora(caminoDeterminista,costoDeterminista,count_neighbors = 50)
                    print ("Mejor Costo:", mejorCosto) 
                    print('Mejor camino ', mejorCamino)
                case '2':
                    for i in range(5):
                        uavs = leer(ar)
                        caminoEstocastico, costoEstocastico = gEstocastico(uavs)
                        print("Costo Estocástico:",costoEstocastico) 
                        mejorCamino, mejorCosto = hill_climbing_mejor_mejora(caminoEstocastico,costoEstocastico,count_neighbors = 50)
                        print ("Mejor Costo:", mejorCosto) 
                        print('Mejor camino ', mejorCamino)
        case '2':
            ar = 't2_Europa.txt'
            print('1.- Aplicar Hill Climbing Mejor-Mejora con Greedy Determinista' + 
                  ' \n 2.- Aplicar Hill Climbing Mejor-Mejora con Greedy Estocástico')
            choose2 = input()
            match choose2:
                case '1':
                    uavs = leer(ar)
                    caminoDeterminista, costoDeterminista = gDeterminista(uavs)
                    print("Costo Determinista:",costoDeterminista) 
                    mejorCamino, mejorCosto = hill_climbing_mejor_mejora(caminoDeterminista,costoDeterminista,count_neighbors = 50)
                    print ("Mejor Costo:", mejorCosto) 
                    print('Mejor camino ', mejorCamino)
                case '2':
                    for i in range(5):
                        uavs = leer(ar)
                        caminoEstocastico, costoEstocastico = gEstocastico(uavs)
                        print("Costo Estocástico:",costoEstocastico) 
                        mejorCamino, mejorCosto = hill_climbing_mejor_mejora(caminoEstocastico,costoEstocastico,count_neighbors = 50)
                        print ("Mejor Costo:", mejorCosto) 
                        print('Mejor camino ', mejorCamino)
        case '3':
            ar  = 't2_Titan.txt'
            print('1.- Aplicar Hill Climbing Mejor-Mejora con Greedy Determinista' + 
                  ' \n 2.- Aplicar Hill Climbing Mejor-Mejora con Greedy Estocástico')
            choose2 = input()
            match choose2:
                case '1':
                    uavs = leer(ar)
                    caminoDeterminista, costoDeterminista = gDeterminista(uavs)
                    print("Costo Determinista:",costoDeterminista) 
                    mejorCamino, mejorCosto = hill_climbing_mejor_mejora(caminoDeterminista,costoDeterminista,count_neighbors = 50)
                    print ("Mejor Costo:", mejorCosto) 
                    print('Mejor camino ', mejorCamino)
                case '2':
                    for i in range(5):
                        uavs = leer(ar)
                        caminoEstocastico, costoEstocastico = gEstocastico(uavs)
                        print("Costo Estocástico:",costoEstocastico) 
                        mejorCamino, mejorCosto = hill_climbing_mejor_mejora(caminoEstocastico,costoEstocastico,count_neighbors = 50)
                        print ("Mejor Costo:", mejorCosto) 
                        print('Mejor camino ', mejorCamino)
    
    
    
