#############################################################################################################
#                                                                                                           #
#   Este Modulo tem como função a comunicação com medidores elétricos (SMF)                                 #
#   por meio do protocolo de comunicação NBR-14522                                                          #
#                                                                                                           #
#   Autor: Lucas Specht                                                                                     #
#                                                                                                           #
#   Versão: 0.1.3                                                                                             #
#                                                                                                           #
#   Última revisão: 24/10/2023                                                                              #
#                                                                                                           #
#############################################################################################################

#----------------------->  Dicionario de termos contidos neste script  <--------------------------#                                         
''' - HEX: Hexadecimal.                                                                     
    - Word: Cadeia de caracteres que representam uma informação, podendo ser HEX ou Bits.   
    - IEEE-754: Método de conversão de Binario (bits) para float.                   
    - CRC: 'Cyclic Redundancy Check' (Verificação Cíclica de Redundância), 
        - verificação de erros e ordenação de words, contidas na Cadeia Hex.                   ''' 
#-------------------------------------------------------------------------------------------------#          
                                     
#--------------------------> Breve Explicações de funcionamento <---------------------------------#
''' - O começo de uma word de comando e resposta sempre ira conter os valores: 01, 99 
    - O comando sempre tera o tamanho de 68 'Octetos' (Bytes) - (66 Octetos mais 2: (01, 99))
    - A resposta sempre tera o tamanho de 260 'Octetos' (Bytes) - (258 Octetos mais 2: (01, 99))
        - cada Octeto é representado em HEX com dois digitos.                                  '''
#-------------------------------------------------------------------------------------------------#
import socket
from pyModbusTCP.utils import crc16
from pebble import concurrent, ProcessFuture

class ComunicacaoNBR:
    def __init__(self, ip: str, port: int) -> None:
        self.__IP = ip
        self.__PORT = port
    
    def __conexao_socket(self) -> socket.socket:
        ''' Este método conecta ao equipamento utilizando IP e porta
            e retorna um objeto Socket para comunicação '''
        try:
            Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            Socket.connect((self.__IP, self.__PORT))

            return Socket
        
        except Exception as e:
            raise ConnectionError(f'Não foi possivel efetuar a conexão com o medidor, erro: {e}')
    
    def __montar_hex_comando(self, comando: int, leitora: int, parametro = '00') -> str:
        ''' Este método Concatena uma str contendo o 
            comando junto do CRC e a retorna '''

        comando = f'0199{comando}{leitora}{parametro}'
        rep = 132 - len(comando)

        comando = f'{comando}{"0"*rep}'
        comando = self.__adcionar_crc(comando)

        return comando

    @concurrent.process(timeout=20) 
    def __envio_comando(self, hex: str) -> ProcessFuture:
        ''' Este método de uso interno envia um determinado comando baseado 
            no HEX recebido nos parametros e retorna a resposta '''
        try:
            conexao = self.__conexao_socket()
            bytes_cmd = bytes.fromhex(hex)
        
            conexao.sendall(bytes_cmd)
            resposta = conexao.recv(260).hex()

            while len(resposta) < 520:
                resposta += conexao.recv(260).hex()

            return resposta
        
        except Exception as e:
            raise ConnectionError(f'Não foi possivel se comunicar com o destino, ERRO: {e}')

    def __adcionar_crc(self, data: str) -> str:
        ''' Este método adciona o CRC ao fim do comando e 
        o retorna por completo contendo o CRC no final '''

        crc = hex(crc16(bytes.fromhex(data)))  #-> Calcula o crc do comando utilizando o método crc16 
                                               # do Pymodbus e utilizando o HEX completo
        crc = crc.split('x')[1] 
        crc = crc if len(crc) > 3 else f'0{crc}'

        crc_str = crc[2:4] + crc[0:2]  #-> Concatena a String e a tranforma em Big Endian
        data += crc_str

        return data

    def enviar_comando(self, comando: int, leitora: int, parametro: str = '00') -> str:
        ''' Monta e trata o comando completo para envio ao 
            medidor e retorna os valores de resposta '''
        try:
            comando_hex = self.__montar_hex_comando(comando, leitora, parametro)
            comando = self.__envio_comando(comando_hex)

            try:
                resposta =  comando.result()

            except TimeoutError:
                raise TimeoutError("Não foi recebida uma resposta dentro do tempo limite")
            
        except Exception as e:
            raise RuntimeError(f'Houve um erro desconhecido durante o Envio do comando!\nERRO: {e}')
        
        return resposta
    