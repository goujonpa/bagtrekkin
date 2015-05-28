# -*- encoding: utf-8 -*-
import serial

baud_rate = 9600
# tag_file=open("analise/tag.txt","w")
###################### FUNCAO PARA VERIFICAR PORTAS ATIVAS ###############
def verifica_portas():

    portas_ativas = []
    for numero in range(100):

        try:
            objeto_verifica = serial.Serial(numero)
            portas_ativas.append((numero, objeto_verifica.portstr))
            objeto_verifica.close()

        except serial.SerialException:
            pass

    return portas_ativas

########################## FUNCAO PARA ABRIR A PORTA #######################
def abrirPorta(bufferPorta):

    for numero,portas_ativas in bufferPorta:
       try:
           Obj_porta = serial.Serial(portas_ativas, baud_rate)
           print "Porta %s aberta: " % portas_ativas

       except serial.SerialException:
           print"ERRO: Verifique se ha algum dispositivo conectado na porta!"

    return Obj_porta

######################### FUNCAO PARA LER A TAG DA PORTA SERIAL ############
def lerTAG(porta):
    tag = porta.readline();
    return tag

################################ MAIN ####################################
if __name__=='__main__':

    bufferTag = ''
    #bufferPorta = verifica_portas()
    #print bufferPorta
    #conexaoSerial = abrirPorta(bufferPorta)
    conexaoSerial=serial.Serial("/dev/ttyUSB0",baud_rate)
    opcao = 1
    #while(opcao == 1):
    #    print"==========================================="
    #    print"======== 1 - Ler TAG RFID ================="
    #    print"======== 2 - Sair         ================="
    #    print"==========================================="
    #    opcao = int (raw_input("Digite a Opcao: "))

    #    if opcao == 1:
    tag = lerTAG(conexaoSerial)

    if tag not in bufferTag:
        bufferTag = bufferTag + tag
        tag_file=open("tag.txt","w")
        tag_file.write(tag)
        tag_file.flush()
        tag_file.close()
        print "Cadastrada a TAG %s" % tag
    else:
        print "TAG ja cadastrada"


    conexaoSerial.close()