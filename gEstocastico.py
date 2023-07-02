import random

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
            show_uavs_info(this_uav,cost)
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
            show_uavs_info(this_uav,cost)
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
                show_uavs_info(this_uav,cost)
                probUavs = [] # Reinicio la probabilidad de los uavs.
                for uav in uavs:
                    probUavs.append(uav['midTime']/midTimeTotal)
            else:
                tmpAterrizaje =  abs(uav_ant['tiempo_aterrizaje']-this_uav['midTime'])
                this_uav['tiempo_aterrizaje'] = this_uav['botTime']
                cost = cost + tmpAterrizaje
                uav_ant = this_uav
                uavs.remove(this_uav)
                show_uavs_info(this_uav,cost)
                probUavs = [] # Reinicio la probabilidad de los uavs.
                for uav in uavs:
                    probUavs.append(uav['midTime']/midTimeTotal)
        i = i + 1
    print("Se leyeron ",i, " uavs")

def show_uavs_info(uav,cost): 
    print(' ID :',uav.get('id_uav')," | Tiempo de aterrizaje: ", uav.get('tiempo_aterrizaje'), ' | Costo actual: ', cost)

def printRdys(rdys):
    print('Rdys :')
    for rdy in rdys:
        print(rdy)

def show_uavs(uavs):
    b = True
    large = len(uavs) 
    for uav in uavs: 
        if b :
            print("UAVs :", large  ) 
            print(' ID :',uav.get('id_uav')," | ", 'Range :', uav.get('botTime')," | ", uav.get('midTime')," | ",uav.get('topTime'),'|', uav.get('times'))
            b = False
        else:
            print(' ID :',uav.get('id_uav')," | ", 'Range :', uav.get('botTime')," | ", uav.get('midTime')," | ",uav.get('topTime'),'|', uav.get('times')) 

def printUAVs(uavs):
    for uav in uavs:
        print(uav)
        print("")

if __name__ == '__main__':
    print('Archivo a leer para aplicar Greedy Estocástico \n 1.- t2_Deimos.txt \n 2.- t2_Europa.txt \n 3.- t2_Titan.txt')
    choose = input()
    match choose:
        case '1':
            archivo = 't2_Deimos.txt'
            for i in range(5):
                uavs = leer(archivo)
                gEstocastico(uavs)
        case '2':
            archivo = 't2_Europa.txt'
            for i in range(5):
                uavs = leer(archivo)
                gEstocastico(uavs)
        case '3':
            archivo = 't2_Titan.txt'
            for i in range(5):
                uavs = leer(archivo)
                gEstocastico(uavs)