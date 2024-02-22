import time
import random
from os import system
from colorama import Fore,Style,Back,init, Cursor
from pynput import keyboard


init(autoreset=True)  # Inicializar colorama
a = 'x'

class Process:
    def __init__(self, id, n1, n2, opcion, finalizacion, tiempo,  tiempo_transcurrido, tiempo_bloqueado, tiempo_llegada, tiempo_finalizacion, tiempo_respuesta,tiempo_respuesta_bandera):
        self.id = id          # ID del proceso
        self.n1 = n1          # Primer número
        self.n2 = n2          # Segundo número
        self.opcion = opcion  # Opción de procesamiento
        self.finalizacion = finalizacion  #Estado en el que termino el tiempo, 0 por tiempo, 1 por error
        self.tiempo = tiempo  # Tiempo maximo estimado de ejecución
        self.tiempo_transcurrido = tiempo_transcurrido #Tiempo transcurrido, va a inicializarse en 0 tiempo en servicio
        self.tiempo_bloqueado = tiempo_bloqueado
        self.tiempo_llegada = tiempo_llegada
        self.tiempo_finalizacion = tiempo_finalizacion
        self.tiempo_respuesta = tiempo_respuesta
        self.tiempo_respuesta_bandera = tiempo_respuesta_bandera


def on_press(key):
    global a
    if (key.char == 'e'):
        a = 'e'
    elif (key.char == 'i'):
        a = 'i'
    elif (key.char == 'p'):
        a = 'p'
    elif (key.char == 'c'):
        a = 'c'
    elif (key.char == 'n'):
        a = 'n'
    elif (key.char == 'b'):
        a = 'b'
    elif (key.char == 't'):
        a = 't'

def ordenar_procesos(lote):#Funcion para la interrupcion, cambia el indice de los procesos en la lista lotes
  borrado_Segpantalla()
  b = lote[0]
  for i in range(len(lote)-1):
    lote[i] = lote [i+1]
  lote[len(lote)-1] = b
  return lote

def animacion():
   print(Cursor.POS(2, 2) +"Procesos Nuevos: ")
   print(Cursor.POS(2, 20) +"Contador: ")
   #Primer ventana
   print(Cursor.POS(2, 7) + Fore.CYAN + Style.BRIGHT + "Lote trabajando" + Style.RESET_ALL)
   print(Cursor.POS(2, 9) + Back.CYAN + Style.BRIGHT + "  ID      "+Cursor.POS(12, 9) +"TME     "+Cursor.POS(20, 9) +"TT  ")
   #Segunda ventana
   print(Cursor.POS(40, 7) + Fore.CYAN + Style.BRIGHT + "Proceso en ejecucion" + Style.RESET_ALL)
   print(Cursor.POS(40, 9) + Style.BRIGHT +"ID:")
   print(Cursor.POS(40, 10) + Style.BRIGHT +"Ope:")          
   print(Cursor.POS(40, 11) + Style.BRIGHT +"TME:")
   print(Cursor.POS(40, 12) + Style.BRIGHT +"TT:")
   print(Cursor.POS(40, 13) + Style.BRIGHT +"TR:")
   #Segunda ventana bajo
   print(Cursor.POS(40, 16) + Fore.CYAN + Style.BRIGHT + "Procesos bloqueados" + Style.RESET_ALL)
   print(Cursor.POS(40, 18) + Back.CYAN + Style.BRIGHT + "  ID      "+Cursor.POS(50, 18) +"TTB     "+Cursor.POS(20, 9))
   #Tercera ventana
   print(Cursor.POS(80, 7) + Fore.CYAN + Style.BRIGHT +"Terminados" + Style.RESET_ALL)
   print(Cursor.POS(80, 9) + Back.CYAN + Style.BRIGHT +"ID          "+Cursor.POS(86, 9) +"Ope         "+Cursor.POS(97, 9) +"Res        "+Style.RESET_ALL)

def borrado_Pripantalla(j):
  for x in range(5-j):
    print(Cursor.POS(4, 10+x)+"                      ")

def borrado_Segpantalla():
  #Borrar los datos para siguiente proceso
  for i in range(6):
    print(Cursor.POS(48, 9+i)+"               ")
  
def borrado_bloqueados():
  #Borrar los datos para siguiente proceso
  for i in range(6):
    print(Cursor.POS(40, 19+i)+"                ")

def redondeo(valor):
  valor = round(valor,1)
  return valor

def proceso_ejecucion(list_process,contador,bloqueados):
  global a
  a = ''
  borrado_Segpantalla()
  #Impresion de datos para el proceso en ejecucion estado NULL
  if list_process.id == "N/A":
    print(Cursor.POS(48, 9), "N/A")
    print(Cursor.POS(48, 10),"N/A","+","N/A")
    print(Cursor.POS(48, 11),"N/A")#Tiempo maximo
    print(Cursor.POS(48, 12)+ " 0")#Tiempo transcurrido
    print(Cursor.POS(48, 13),"N/A")#Tiempo restante
    while True:
      if a == 'n':
        break
      elif a == 'b':
        break
      print(Cursor.POS(48, 12)+"               ")
      print(Cursor.POS(48, 12) + f" {list_process.tiempo_transcurrido:.1f}")#Tiempo transcurrido
      list_process.tiempo_transcurrido += .1
      print(Cursor.POS(2, 20) +"Contador:                        ")
      print(Cursor.POS(2, 20) +f"Contador: {contador:.1f}")
      contador = contador + .1
      borrado_bloqueados()
      pos = 0
      for bloqueado in bloqueados:
        print(Cursor.POS(40, 19+pos),bloqueado.id)
        print(Cursor.POS(50, 19+pos),bloqueado.tiempo_bloqueado)
        bloqueado.tiempo_bloqueado = bloqueado.tiempo_bloqueado + .1
        bloqueado.tiempo_bloqueado = redondeo(bloqueado.tiempo_bloqueado)
        pos += 1
      for bloqueado in bloqueados:
        if bloqueado.tiempo_bloqueado == 8:
          return contador,a,bloqueados
      time.sleep(.1)
  else:
    print(Cursor.POS(48, 9),list_process.id)
    if list_process.opcion == 1:
      print(Cursor.POS(48, 10),list_process.n1,"+",list_process.n2)
    elif list_process.opcion == 2:
      print(Cursor.POS(48, 10),list_process.n1,"-",list_process.n2)
    elif list_process.opcion == 3:
      print(Cursor.POS(48, 10),list_process.n1,"*",list_process.n2)
    elif list_process.opcion == 4:
      print(Cursor.POS(48, 10),list_process.n1,"/",list_process.n2)
    elif list_process.opcion == 5:
      print(Cursor.POS(48, 10),list_process.n1,"MR",list_process.n2)
    else:
      print(Cursor.POS(48, 10),list_process.n1,"%",list_process.n2)
    print(Cursor.POS(48, 11),list_process.tiempo)#Tiempo maximo
    print(Cursor.POS(48, 12)+ " 0")#Tiempo transcurrido
    print(Cursor.POS(48, 13),list_process.tiempo)#Tiempo restante
    redondeado = round(list_process.tiempo-list_process.tiempo_transcurrido,1)*10
    redondeado = int(redondeado)
    for i in range(redondeado):
      #print(a)
      if a == 'i':
        break
      elif a == 'e':
        break
      elif a == 'p':
        print(Cursor.POS(2, 20) +f"Contador: {contador:.1f}")
        print(Cursor.POS(48, 12) + f" {list_process.tiempo_transcurrido:.1f}")#Tiempo transcurrido
        print(Cursor.POS(48, 13) + f" {list_process.tiempo-list_process.tiempo_transcurrido:.1f}")#Tiempo restante
        while True:
            if (a == "c"):
              break
      elif a == 'n':
        break
      elif a == 'b':
        break
      print(Cursor.POS(48, 12)+"               ")
      print(Cursor.POS(48, 13)+"               ")
      print(Cursor.POS(48, 12) + f" {list_process.tiempo_transcurrido:.1f}")#Tiempo transcurrido
      print(Cursor.POS(48, 13) + f" {list_process.tiempo-list_process.tiempo_transcurrido:.1f}")#Tiempo restante
      list_process.tiempo_transcurrido = list_process.tiempo_transcurrido + .1
      print(Cursor.POS(2, 20) +"Contador:             ")
      print(Cursor.POS(2, 20) +f"Contador: {contador:.1f}")
      contador = contador + .1
      borrado_bloqueados()
      pos = 0
      for bloqueado in bloqueados:
        print(Cursor.POS(40, 19+pos),bloqueado.id)
        print(Cursor.POS(50, 19+pos),bloqueado.tiempo_bloqueado)
        bloqueado.tiempo_bloqueado = bloqueado.tiempo_bloqueado + .1
        bloqueado.tiempo_bloqueado = redondeo(bloqueado.tiempo_bloqueado)
        pos += 1
        if bloqueado.tiempo_bloqueado == 8:
          return contador,a,bloqueados
      time.sleep(.1)
  return contador,a,bloqueados

def proceso_terminado(list_process,posTerm,estado):
  resultado=0
  posTerm=posTerm+1
  print(Cursor.POS(79, 9+posTerm),list_process.id)
  if list_process.opcion == 1:#Operacion
    print(Cursor.POS(85, 9+posTerm),list_process.n1,"+",list_process.n2)
    resultado = list_process.n1 + list_process.n2
  elif list_process.opcion  == 2:
    print(Cursor.POS(85, 9+posTerm),list_process.n1,"-",list_process.n2)
    resultado = list_process.n1 - list_process.n2
  elif list_process.opcion  == 3:
    print(Cursor.POS(85, 9+posTerm),list_process.n1,"*",list_process.n2)
    resultado = list_process.n1 * list_process.n2
  elif list_process.opcion  == 4:
    print(Cursor.POS(85, 9+posTerm),list_process.n1,"/",list_process.n2)
    resultado = list_process.n1 / list_process.n2
  elif list_process.opcion  == 5:
    print(Cursor.POS(85, 9+posTerm),list_process.n1,"MR",list_process.n2)
    resultado = list_process.n1 % list_process.n2
  else:
    print(Cursor.POS(85, 9+posTerm),list_process.n1,"%",list_process.n2)
    resultado = list_process.n1 * (list_process.n2 / 100)
  if(estado == 'e' or estado == 1):
    print(Cursor.POS(97, 9+posTerm) + "Error")#Resultado
  else:
    print(Cursor.POS(97, 9+posTerm)+"{:.2f}".format(resultado))#Resultado
    list_process.tiempo_transcurrido = round(list_process.tiempo_transcurrido,1)
  print(Cursor.POS(112, 9+posTerm),list_process.tiempo_transcurrido)
  return posTerm

def operando(process,pos):
  process.tiempo_transcurrido = round(process.tiempo_transcurrido,1)
  process.tiempo_llegada = round(process.tiempo_llegada,1)
  process.tiempo_respuesta = round(process.tiempo_respuesta,1)
  process.tiempo_finalizacion = round(process.tiempo_finalizacion,1)
  print(Cursor.POS(4, 6+pos),process.id)
  if process.opcion == 1:#Operacion
    print(Cursor.POS(9, 6+pos),process.n1,"+",process.n2)
    resultado = process.n1 + process.n2
  elif process.opcion  == 2:
    print(Cursor.POS(9, 6+pos),process.n1,"-",process.n2)
    resultado = process.n1 - process.n2
  elif process.opcion  == 3:
    print(Cursor.POS(9, 6+pos),process.n1,"*",process.n2)
    resultado = process.n1 * process.n2
  elif process.opcion  == 4:
    print(Cursor.POS(9, 6+pos),process.n1,"/",process.n2)
    resultado = process.n1 / process.n2
  elif process.opcion  == 5:
    print(Cursor.POS(9, 6+pos),process.n1,"MR",process.n2)
    resultado = process.n1 % process.n2
  else:
    print(Cursor.POS(9, 6+pos),process.n1,"%",process.n2)
    resultado = process.n1 * (process.n2 / 100)
  return process,resultado

def BCP(all_process_finish,memoria,bloqueados,all_process,null_process,contador,mostrar,iteraciones):#El estado determina si se mostrara la tabla en ejecucion o al finalizar
  var = 15
  pos = 0
  print(Cursor.POS(5, 5) + Fore.CYAN + Style.BRIGHT + "ID        " + Style.RESET_ALL)
  print(Cursor.POS(10, 5) + Fore.CYAN + Style.BRIGHT + "Ope        " + Style.RESET_ALL)
  print(Cursor.POS(23, 5) + Fore.CYAN + Style.BRIGHT + "Res       " + Style.RESET_ALL)
  print(Cursor.POS(var + 18, 5) + Fore.CYAN + Style.BRIGHT + "T. Servicio    " + Style.RESET_ALL)
  print(Cursor.POS(var + 33, 5) + Fore.CYAN + Style.BRIGHT + "T. Llegada     " + Style.RESET_ALL)
  print(Cursor.POS(var + 48, 5) + Fore.CYAN + Style.BRIGHT + "T. Finalizacion   " + Style.RESET_ALL)
  print(Cursor.POS(var + 66, 5) + Fore.CYAN + Style.BRIGHT + "T. Retorno       " + Style.RESET_ALL)
  print(Cursor.POS(var + 81, 5) + Fore.CYAN + Style.BRIGHT + "T. Respuesta        " + Style.RESET_ALL)
  print(Cursor.POS(var + 96, 5) + Fore.CYAN + Style.BRIGHT + "T. Espera        " + Style.RESET_ALL)
  if mostrar == "fin":
    for process in all_process_finish:
      process,resultado = operando(process,pos)
      tiempo_retorno = round(process.tiempo_finalizacion - process.tiempo_llegada,1)
      tiempo_espera = round(tiempo_retorno - process.tiempo_transcurrido,1)
      print(Cursor.POS(var +17, 6+pos),process.tiempo_transcurrido)
      print(Cursor.POS(var +32, 6+pos),process.tiempo_llegada)
      print(Cursor.POS(var +47, 6+pos),process.tiempo_finalizacion)
      print(Cursor.POS(var +66, 6+pos),tiempo_retorno)
      print(Cursor.POS(var +81, 6+pos),process.tiempo_respuesta)
      print(Cursor.POS(var +95, 6+pos),tiempo_espera)
      if(process.finalizacion == 1):
        print(Cursor.POS(24, 6+pos) + "Error")#Resultado
      else:
        print(Cursor.POS(24, 6+pos)+"{:.2f}".format(resultado))#Resultado
      pos += 1
    print(Cursor.POS(5, 7+pos) + Fore.CYAN + Style.BRIGHT + "Tiempo proceso NULL:" + Style.RESET_ALL)
    print(Cursor.POS(25, 7+pos),null_process.tiempo_transcurrido)  
    print(Cursor.POS(5, 8+pos) + Fore.CYAN + Style.BRIGHT + "Tiempo de ejecucion:" + Style.RESET_ALL)
    print(Cursor.POS(25, 8+pos),contador)
    # print(Cursor.POS(1,10+pos) + "Escobedo Alvarado Jose Alejandro")
    # print(Cursor.POS(1,11+pos) + "Fernandez Roman Bryan Daniel")
  elif mostrar == "ejecucion":
      print(Cursor.POS(var + 108, 5) + Fore.CYAN + Style.BRIGHT + "T. Restante  " + Style.RESET_ALL)
      print(Cursor.POS(var + 121, 5) + Fore.CYAN + Style.BRIGHT + "T. Bloqueado        " + Style.RESET_ALL)
      print(Cursor.POS(var + 136, 5) + Fore.CYAN + Style.BRIGHT + "Estado        " + Style.RESET_ALL)
      for process in all_process_finish:#Mostrar procesos terminados
            process,resultado = operando(process,pos)
            tiempo_retorno = round(process.tiempo_finalizacion - process.tiempo_llegada,1)
            tiempo_espera = round(tiempo_retorno - process.tiempo_transcurrido,1)
            print(Cursor.POS(var +17, 6+pos),process.tiempo_transcurrido)
            print(Cursor.POS(var +32, 6+pos),process.tiempo_llegada)
            print(Cursor.POS(var +47, 6+pos),process.tiempo_finalizacion)
            print(Cursor.POS(var +65, 6+pos),tiempo_retorno)
            print(Cursor.POS(var +81, 6+pos)+"{:.1f}".format(process.tiempo_respuesta))
            print(Cursor.POS(var +95, 6+pos),tiempo_espera)
            if(process.finalizacion == 1):
              print(Cursor.POS(23, 6+pos) + "Error")#Resultado
            else:
              print(Cursor.POS(23, 6+pos)+"{:.2f}".format(resultado))#Resultado
            print(Cursor.POS(var + 108, 6+pos) + Style.BRIGHT + "N/A" + Style.RESET_ALL) #Res Cpu
            print(Cursor.POS(var + 121, 6+pos) + Style.BRIGHT + "N/A" + Style.RESET_ALL) #Bloqueado
            print(Cursor.POS(var + 136, 6+pos) + Fore.GREEN  + Style.BRIGHT + "Finalizado" + Style.RESET_ALL) #Estado  
            pos += 1
      for num, process in enumerate(memoria):#Mostrar procesos en listos y ejecucion
            process,resultado = operando(process,pos)
            tiempo_auxiliar_retorno = round(contador - process.tiempo_llegada,1)
            tiempo_espera_momento = round(tiempo_auxiliar_retorno - process.tiempo_transcurrido,1)
            tiempo_restante_cpu = round(process.tiempo - process.tiempo_transcurrido,1)
            print(Cursor.POS(23, 6+pos)  + Style.BRIGHT + "N/A" + Style.RESET_ALL)
            print(Cursor.POS(var +17, 6+pos),process.tiempo_transcurrido)
            print(Cursor.POS(var +32, 6+pos),process.tiempo_llegada)
            print(Cursor.POS(var +48, 6+pos)+ Style.BRIGHT + "N/A" + Style.RESET_ALL)#Finalizacion
            print(Cursor.POS(var +66, 6+pos)+ Style.BRIGHT + "N/A" + Style.RESET_ALL)#Retorno
            if (process.tiempo_respuesta_bandera is False):
              print(Cursor.POS(var +81, 6+pos) + Style.BRIGHT + "N/A" + Style.RESET_ALL)
            else:
              print(Cursor.POS(var +80, 6+pos),process.tiempo_respuesta)
            print(Cursor.POS(var +95, 6+pos),tiempo_espera_momento)
            print(Cursor.POS(var + 107, 6+pos),tiempo_restante_cpu) #Restante en CPU
            print(Cursor.POS(var + 121, 6+pos)  + Style.BRIGHT + "N/A" + Style.RESET_ALL) #Bloqueado
            if num == 0:
              print(Cursor.POS(var + 136, 6+pos) + Fore.YELLOW + Style.BRIGHT + "Ejecucion" + Style.RESET_ALL) #Estado
            else:
              print(Cursor.POS(var + 136, 6+pos) + Style.BRIGHT + "Listo" + Style.RESET_ALL) #Estado   
            pos += 1
      for process in bloqueados: #Mostrar procesos bloqueados
            process,resultado = operando(process,pos)
            tiempo_auxiliar_retorno = round(contador - process.tiempo_llegada,1)
            tiempo_espera_momento = round(tiempo_auxiliar_retorno - process.tiempo_transcurrido,1)
            tiempo_restante_cpu = round(process.tiempo - process.tiempo_transcurrido,1)
            tiempo_restante_bloqueado = round(8 - process.tiempo_bloqueado,1)
            print(Cursor.POS(23, 6+pos) + Style.BRIGHT + "N/A" + Style.RESET_ALL)
            print(Cursor.POS(var +17, 6+pos),process.tiempo_transcurrido)
            print(Cursor.POS(var +32, 6+pos),process.tiempo_llegada)
            print(Cursor.POS(var +48, 6+pos) + Style.BRIGHT  + "N/A" + Style.RESET_ALL)#Finalizacion
            print(Cursor.POS(var +66, 6+pos) + Style.BRIGHT  + "N/A" + Style.RESET_ALL)#Retorno
            print(Cursor.POS(var +80, 6+pos),process.tiempo_respuesta)
            print(Cursor.POS(var +95, 6+pos),tiempo_espera_momento)
            print(Cursor.POS(var + 107, 6+pos),tiempo_restante_cpu) #Restante en CPU
            print(Cursor.POS(var + 120, 6+pos),tiempo_restante_bloqueado) #Bloqueado
            print(Cursor.POS(var + 136, 6+pos) + Fore.RED + Style.BRIGHT + "Bloqueado" + Style.RESET_ALL) #Estado  
            pos += 1
      for num, process in enumerate(all_process): #Mostrar procesos nuevos
            if num>=iteraciones:
              process,resultado = operando(process,pos)
              print(Cursor.POS(23, 6+pos)  + Style.BRIGHT + "N/A" + Style.RESET_ALL)#Resultado
              print(Cursor.POS(var + 18, 6+pos)  + Style.BRIGHT + "N/A" + Style.RESET_ALL) #Servicio
              print(Cursor.POS(var + 33, 6+pos)  + Style.BRIGHT + "N/A" + Style.RESET_ALL) #LLegada
              print(Cursor.POS(var + 48, 6+pos)  + Style.BRIGHT + "N/A" + Style.RESET_ALL) #Finalizacion
              print(Cursor.POS(var + 66, 6+pos)  + Style.BRIGHT + "N/A" + Style.RESET_ALL) #Retorno
              print(Cursor.POS(var + 81, 6+pos)  + Style.BRIGHT + "N/A" + Style.RESET_ALL) #Respuesta
              print(Cursor.POS(var + 96, 6+pos)  + Style.BRIGHT + "N/A" + Style.RESET_ALL) #Espera
              print(Cursor.POS(var + 108, 6+pos)  + Style.BRIGHT + "N/A" + Style.RESET_ALL) #Restante en CPU
              print(Cursor.POS(var + 121, 6+pos)  + Style.BRIGHT + "N/A" + Style.RESET_ALL) #Bloqueado
              print(Cursor.POS(var + 136, 6+pos)  + Style.BRIGHT + "NUEVO" + Style.RESET_ALL) #Estado
              pos += 1
      while True:
        if a == "c":
          system("cls")
          break
          
        




def crear_proceso(id):
    id = id+1
    opcion = random.randrange(1,7)#Elige una opcion de las 6 posibles operaciones
    n1 = random.randrange(100)
    if (opcion == 4 or opcion == 5):#Validacion para que en caso de ser division o modulo residuo, el denominador no pueda ser 0
      n2 = random.randrange(1,100)
    else:
      n2 = random.randrange(100)
    finalizacion = 0
    tiempo = random.randrange(6,12)#Random tiempo de 6 hasta 18 segundos
    tiempo_transcurrido = 0
    tiempo_bloqueado = 0
    tiempo_llegada = 0
    tiempo_finalizacion = 0
    tiempo_respuesta = 0
    tiempo_respuesta_bandera = False
    proceso = Process(id,n1,n2,opcion,finalizacion,tiempo,tiempo_transcurrido,tiempo_bloqueado,tiempo_llegada,tiempo_finalizacion,tiempo_respuesta,tiempo_respuesta_bandera)
    return id, proceso

def main():
  global a
  #Ingreso de cantidad de procesos
  bandera = True
  while bandera:
    validacion = input("Ingrese la cantidad de procesos: ")
    if validacion.isdigit():
      proceso = int(validacion)
      bandera = False
    else:
      print("Ingrese un numero valido")
  listener = keyboard.Listener(on_press=on_press,suppress=True)
  listener.start()  # start to listen on a separate thread
  all_process = []#Todos los procesos al comienzo
  all_process_finish = []#Todos los procesos terminados
  memoria = []#Sustitucion de lotes por memoria
  bloqueados = []
  null_process = Process("N/A","N/A","N/A","N/A",0,0,0,0,0,0,0,0)
  id = 0
  for i in range(id,proceso):
    id, proceso = crear_proceso(id)
    all_process.append(proceso)#Se agrega data_process en forma de copia para posteriormente poder borrar la lista y que no se modifique el resultado
  system("cls")
  #Inicio del proceso de ejecucion y muestra de resultados
  animacion()
  if len(all_process) > 5:
    print(Cursor.POS(2, 2) +"Procesos nuevos:",len(all_process)-5)#Primera impresion de procesos, se toman los totales y se le restan 5 para la primera impresion
  else:
    print(Cursor.POS(2, 2) +"Procesos nuevos:",len(all_process)-len(all_process))#Primera impresion de procesos, se toman los totales y se le restan 5 para la primera impresion
  aux=len(all_process)#Auxiliar para longitud de all_process y conocer cuantos procesos hay nuevos, se le restan 5 por los primeros
  posTerm = 0#Posicion que se asigna a la funcion proceso_terminado para conocer la posicion que se quedo e imprimir los lotes terminados en orden
  contador=0
  iteraciones=0#Numero de procesos pasados
  estado = ""
  if aux>5:#Si Hay mas de 5 procesos al comienzo de la ejecucion
    if aux == len(all_process):
      for i in range(5):#Ciclo para agregar los elementos de all_process en la lista memoria
          memoria.append(all_process[i])
      aux -= 5
      iteraciones = 5
  if aux<=5:#Si Hay mas de 5 procesos al comienzo de la ejecucion
    if aux == len(all_process):
      for i in range(aux):#Ciclo para agregar los elementos de all_process en la lista memoria
          memoria.append(all_process[i])
      aux = 0
      iteraciones = len(all_process)
  while len(memoria) + len(bloqueados) > 0:
    borrado_Pripantalla(0)
    if len(memoria) == 0:#Este condicional se utiliza cuando hay n-1 procesos en bloqueados y un proceso en ejecucion, al presionar la letra de error, cae en esta condicion
      while len(memoria)==0:
        contador,estado,bloqueados = proceso_ejecucion(null_process,contador,bloqueados)
        if estado == 'n':#Si el estado regresado durante el proceso nulo es n, se crea el proceso y se sigue la ejecucion
          id, proceso = crear_proceso(id)
          all_process.append(proceso)
          if len(bloqueados) < 5:#No hay procesos en listos pero si puede haber, la longitud de bloqueados no puede ser 5
            memoria.append(proceso)
            memoria[0].tiempo_llegada = contador
            memoria[0].tiempo_respuesta = 0
            memoria[0].tiempo_respuesta_bandera = True
            iteraciones += 1
          else: 
            aux+=1
          a = ''
          break
        elif estado == 'b':#Si el estado regresado durante el proceso nulo es n, se crea el proceso y se sigue la ejecucion
          mostrar = "ejecucion"
          system("cls")
          BCP(all_process_finish,memoria,bloqueados,all_process,null_process,contador,mostrar,iteraciones)
          a = ''
          animacion()
          posTerm = 0
          for process in all_process_finish:
            posTerm = proceso_terminado(process,posTerm,process.finalizacion)
          break
        else:#En caso de que regrese un resultado diferente de n, o sea que no se creo un nuevo proceso, se asigna el tiempo del primer bloqueado que ya cumplio su tiempo en 0, y se asigna a listos, continuando la simulacion
          bloqueados[0].tiempo_bloqueado = 0
          memoria.append(bloqueados.pop(0))
          break
    for i in range(len(memoria)):#Mostrar en la primera pantalla o primera parte
      print(Cursor.POS(4, 10+i),memoria[i].id)
      print(Cursor.POS(12, 10+i),memoria[i].tiempo)
      print(Cursor.POS(20, 10+i) + f"{memoria[i].tiempo_transcurrido:.1f}" )
    #time.sleep(.2)#Retraso para poder visualizar los lotes
    for i in range(len(memoria)):#Mostrar en la segunda parte y tercera parte, ademas reimprime los procesos de la primera parte
      pos = 1#Variable auxiliar para aumentar en la posicion del cursor y asi recorrer los procesos hacia arriba
      borrado_Pripantalla(i)
      for j in range(i+1,len(memoria)):
        print(Cursor.POS(4, 9+pos),memoria[j].id)
        print(Cursor.POS(12, 9+pos),memoria[j].tiempo)
        print(Cursor.POS(20, 9+pos)+ f"{memoria[j].tiempo_transcurrido:.1f}")
        pos = pos + 1
      if memoria[i].tiempo_respuesta_bandera == False:#Asignar tiempo de respuesta
        memoria[i].tiempo_respuesta = contador - memoria[i].tiempo_llegada
        memoria[i].tiempo_respuesta_bandera = True
      contador,estado,bloqueados = proceso_ejecucion(memoria[i],contador,bloqueados)#Ejecuta el proceso
      borrado_Segpantalla()
      if estado == 'i':
        a = ''
        bloqueados.append(memoria.pop(0))
        if len(memoria) == 0:#Si se queda vacia la zona de memoria o de listos, pasara el proceso nulo, si este concluye sin interrupcion de un nuevo proceso pasara el primer proceso en completar su bloqueo de 8 segundos a la memorio o listos
          contador,estado,bloqueados = proceso_ejecucion(null_process,contador,bloqueados)
          if estado == 'n':
            id, proceso = crear_proceso(id)
            all_process.append(proceso)
            if len(bloqueados) < 5:#No hay procesos en listos pero si puede haber 
              memoria.append(proceso)
              memoria[0].tiempo_llegada = contador
              memoria[0].tiempo_respuesta = 0
              memoria[0].tiempo_respuesta_bandera = True
              iteraciones += 1
            else: 
              aux+=1
            a = ''
            break
          elif estado == 'b':
            mostrar = "ejecucion"
            system("cls")
            BCP(all_process_finish,memoria,bloqueados,all_process,null_process,contador,mostrar,iteraciones)
            a = ''
            animacion()
            posTerm = 0
            for process in all_process_finish:
              posTerm = proceso_terminado(process,posTerm,process.finalizacion)
            break
          else:#Entra aqui unicamente si el estado retornado por la linea de arriba es diferente de n, en caso de que sea n, seguira a los siguientes condicionales de abajo e,n,etc
            bloqueados[0].tiempo_bloqueado = 0
            memoria.append(bloqueados.pop(0))
            break
        else:#En caso de que la zona de listos No se quede vacia unicamente ocurre un break
          break#Se rompe el ciclo y regresa al ciclo while permitiendo continuar la simulacion
      if estado == 'e':#Finalizacion por error
        memoria[i].finalizacion = 1
        memoria[i].tiempo_finalizacion = contador
        memoria[i].tiempo_transcurrido = round(memoria[i].tiempo_transcurrido,1)
        posTerm = proceso_terminado(memoria[i],posTerm,estado)
        all_process_finish.append(memoria.pop(0))
        a = ''
        if aux > 0:
          memoria.append(all_process[iteraciones])
          memoria[-1].tiempo_llegada = contador
          iteraciones += 1
          aux -= 1
        break
      if estado == 'n':
        id, proceso = crear_proceso(id)
        all_process.append(proceso)
        if len(memoria) + len(bloqueados)<5:
          memoria.append(proceso)
          memoria[-1].tiempo_llegada = contador
          iteraciones += 1
        else:
          aux+=1
        a = ''
        break
      if estado == 'b':
        mostrar = "ejecucion"
        system("cls")
        BCP(all_process_finish,memoria,bloqueados,all_process,null_process,contador,mostrar,iteraciones)
        a = ''
        animacion()
        posTerm = 0
        for process in all_process_finish:
          posTerm = proceso_terminado(process,posTerm,process.finalizacion)
        break
      if len(bloqueados) > 0 and bloqueados[0].tiempo_bloqueado == 8:#Cuando un proceso bloqueado cumple con su tiempo en bloqueado y viene del retorno de un proceso no nulo
          bloqueados[0].tiempo_bloqueado = 0
          memoria.append(bloqueados.pop(0))
          break#Se rompe el ciclo y regresa al ciclo while permitiendo continuar la simulacion
      else:#Termino exitosamente el proceso por tiempo maximo
        memoria[i].tiempo_finalizacion = contador
        if aux == 0:
          posTerm = proceso_terminado(memoria[i],posTerm,estado)
          all_process_finish.append(memoria.pop(0))
        else:
          posTerm = proceso_terminado(memoria[i],posTerm,estado)
          all_process_finish.append(memoria.pop(0))
          memoria.append(all_process[iteraciones])
          memoria[-1].tiempo_llegada = contador
          iteraciones += 1
          aux -= 1
        break
    print(Cursor.POS(2, 2) +"Procesos nuevos:",aux)
    borrado_Segpantalla() 
  contador = round(contador,1)
  print(Cursor.POS(2, 20) +"Contador: ",contador)#Impresion final del cursor
  null_process.tiempo_transcurrido = round(null_process.tiempo_transcurrido,1)
  print(Cursor.POS(2, 22) +"NULL: ",null_process.tiempo_transcurrido)#Impresion final del cursor
  mostrar = "fin"
  print("Presiona la tecla 't' para ver la tabla de procesos")
  print(len(all_process))
  print(len(all_process_finish))
  while True:
    if a == 't':
      system("cls")
      break
    
  BCP(all_process_finish,memoria,bloqueados,all_process,null_process,contador,mostrar,0)

main()