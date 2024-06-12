Modulo para comunicação com equipamentos de medição de energia elétrica.

Modbus [![Build Status](https://travis-ci.org/Cloud-Automation/node-modbus.png)]


💾 Status
------

Versão 0.1.3 é uma versão estável funcional, em processo de aprimoramento

🖥️ Exemplo envio comando
---------------

```python 

import ComunicacaoNBR from NBR14522

''' Instancia a Classe e possui como argumentos:
 - IP str (Ip do equipamento alvo)
 - PORT int (Porta de comunicação)
'''
Smf = ComunicacaoNBR('localhost', 5006)

''' Envia o comando 26 (Receber memoria de massa atual),
    Com alvo na leitora de comunicação 123455,
'''
Smf.enviar_comando(26, 123456)

```

🎯 Objetivo
------------
Este projeto tem como intuito a interpretação e comunicação com equipamentos de medição de energia elétrica.
Utilizando da norma brasileira de intercâmbio de informações NBR14522.

🛠️ Construído com
------------------
Lista de Módulos / Frameworks utilizados na construção do projeto:

* [PymodbusTCP]
* [Pebble]
* [Socket]

✒️ Autores
-----------
Lucas Specht (https://gitlab.com/lucasspecht1)



