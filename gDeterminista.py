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

#FUNCIÓN QUE EJECUTA EL GREEDY DETERMINISTA.
def gDeterminista(uavs):
    cost = 0
    uav_ant_id = 0
    uavs_orden = sorted(uavs, key=lambda uavs: uavs['midTime'], reverse=False) #UAVS ORDENADOS DE MENOR A MAYOR POR MEDIO DEL TIEMPO PREFERENTE.
    
    for index, uav in enumerate(uavs_orden): #SE RECORREN LOS UAVS PREVIAMENTE ORDENADOS.
        if index == 0: #PRIMER UAVS EN ATERRIZAR LO DESIGNAMOS EN QUE SU TIEMPO DE ATERRIZAJE ES IGUAL A SU TIEMPO PREFERENTE.
            uav['tiempo_aterrizaje'] = uav['midTime']
            cost = cost + 0 #GENERAMOS COSTO CERO POR ESTABLECER EL ATERRIZAJE DEL PRIMER UAV EN SU TIEMPO PREFERENTE.
            uav_ant_id = uav['id_uav']
            show_uavs_determinista(uav,cost)
        else:
            tiempo_aterrizaje = uavs[uav_ant_id-1]['tiempo_aterrizaje'] + uav['times'][uav_ant_id-1] #CALCULO PARA EL TIEMPO DE ATERRIZAJE DE LOS DEMÁS UAVS.
            if tiempo_aterrizaje <= uav['topTime'] and tiempo_aterrizaje >= uav['botTime']: #VERIRIFICACIÓN DE QUE LOS UAVS NO PUEDEN ATERRIZAR FUERA DEL RANGO ESTABLECIDO POR EL TIEMPO MENOR Y TIEMPO MAYOR.
                uav['tiempo_aterrizaje'] = tiempo_aterrizaje
                cost = cost + abs(tiempo_aterrizaje - uav['midTime']) #SE REALIZA EL CÁLCULO DEL COSTO.
                uav_ant_id = uav['id_uav']
            else:
                print('Se extiende su tiempo de aterrizaje para que pueda aterrizar.')
                tiempo_aterrizaje =  abs(uavs[uav_ant_id-1]['tiempo_aterrizaje'] + uav['times'][uav_ant_id-1] - uav['midTime']) #EL MISMO CÁLCULO QUE EN EL IF ANTERIOR.
                uav['tiempo_aterrizaje'] = uav['botTime'] #COMO EL UAV EN ESTE CASO ATERRIZARÍÁ FUERA DEL RANGO PERMITIDO, ENTONCES SE LE OBLIGA A QUE ESTE CAIGO LO ANTES POSIBLE DENTRO DE SU RANGO. EN EL TIEMPO MENOR.
                cost = cost + tiempo_aterrizaje #MISMO CÁLCULO DEL COSTO.
            show_uavs_determinista(uav,cost)
    print('Costo Total: ',cost)
 
#FUNCIÓN PARA MOSTRAR A LOS UAVS EN EL PROCESAMIENTO DEL GREEDY DETERMINISTA.
def show_uavs_determinista(uav,cost): 
    print(' ID :',uav.get('id_uav')," | Tiempo de aterrizaje: ", uav.get('tiempo_aterrizaje'), ' | Costo actual: ', cost)

#MAIN DEL PROGRAMA
if __name__ == '__main__':
    print('Archivo a leer para aplicar Greedy Determinista \n 1.- t2_Deimos.txt \n 2.- t2_Europa.txt \n 3.- t2_Titan.txt')
    choose = input()
    match choose:
        case '1':
            archivo = 't2_Deimos.txt'
            uavs = leer(archivo) 
            gDeterminista(uavs)
        case '2':
            archivo = 't2_Europa.txt'
            uavs = leer(archivo) 
            gDeterminista(uavs)
        case '3':
            archivo = 't2_Titan.txt'
            uavs = leer(archivo) 
            gDeterminista(uavs)
            #show_uavs(uavs)