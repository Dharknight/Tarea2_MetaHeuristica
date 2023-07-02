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

#FUNCIÓN QUE GENERA VECINOS EN UNA CANTIDAD DE NxN SIENDO N EL TAMAÑO DE LA LISTA DE UAVS.
def generate_neighbour(current_solution,premium):
    if premium == 0:
        while True:
            p = random.randint(0,len(current_solution)-1)
            k = random.randint(0,len(current_solution)-1)
            if p != k:
                current_solution[p] , current_solution[k] = current_solution[k], current_solution[p]
                break
    else:
        while True:
            p = random.randint(1,14)
            k = random.randint(1,14)
            if p != k:
                current_solution[p] , current_solution[k] = current_solution[k], current_solution[p]
                break
    return current_solution

#FUNCIÓN QUE CALCULA EL COSTO DE LA SECUENCIA DE ATERRIZAJE DE LOS UAVS.
def evaluate_solution(neighbour):
    cost = 0
    uav_ant = None
    for index, uav in enumerate(neighbour):    #SE RECORRE LA LISTA DE UAVS A ATERRIZAR EN ORDEN.
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
    return cost, neighbour

#FUNCIÓN QUE EJECUTA EL ALGORITMO HILL CLIMBING ALGUNA-MEJORA.
def hill_climbing_alguna_mejora(initial_solution, current_solution_score, max_sol,count_neighbors):
    best_current_score = current_solution_score
    tmp_bestNeighbor = initial_solution
    a = 0
    b = 0
    while a < max_sol:
        for nei in tmp_bestNeighbor: #SE LIMPIA AL IGUAL QUE EN LOS DEMÁS ALGORITMOS LA LISTA DE UAVS A ATERRIZAR PARA PODER REALIZAR EL CALCULO DE ATERRIZAJE Y COSTO DE FORMA CORRECTA
            if 'tiempo_aterrizaje' in nei:
                del nei['tiempo_aterrizaje']
        while b < count_neighbors:
            if tmp_bestNeighbor[0]['botTime'] == 0 and tmp_bestNeighbor[0]['midTime'] == 0 and tmp_bestNeighbor[0]['topTime'] == 0:
                neighbour = generate_neighbour(tmp_bestNeighbor,0)
            else:
                neighbour = generate_neighbour(tmp_bestNeighbor,1)
            neighbour_score, neighbour_evaluado = evaluate_solution(neighbour)
            if neighbour_score < best_current_score:
                print('Estoy ', neighbour_score)
                tmp_bestNeighbor = neighbour_evaluado
                bestNeighbor = copy.deepcopy(neighbour_evaluado)
                best_current_score = neighbour_score
                b = 0
                break
            else:
                b = b + 1
        a = a + 1
        if b == count_neighbors and tmp_bestNeighbor == initial_solution:
            return tmp_bestNeighbor, best_current_score
        elif b == count_neighbors and tmp_bestNeighbor != initial_solution:
            return bestNeighbor, best_current_score
    
#MAIN DEL PROGRAMA.
if __name__ == '__main__':
    ar  = 't2_Deimos.txt'
    uavs = leer(ar)
    caminoDeterminista, costoDeterminista = gDeterminista(uavs)
    print("Costo Determinista:",costoDeterminista)
    try:
        mejorCamino, mejorCosto = hill_climbing_alguna_mejora(caminoDeterminista, costoDeterminista, max_sol = 10, count_neighbors= 10000)
    except TypeError:
        mejorCamino, mejorCosto = hill_climbing_alguna_mejora(caminoDeterminista, costoDeterminista, max_sol = 10, count_neighbors= 10000)
    print ("Mejor Costo:", mejorCosto) 
    print('Mejor camino ', mejorCamino)