#!/usr/bin/python

# tratar comentarios na primeira linha da .MMSG file com a palavra chave extends.
# gerar MSG file sem comentarios e sem espaco entre as linhas
# comentar contribuicao da heranca
# fatorar codigo em funcoes

import sys
from message_generator import MessageGenerator

if __name__ == "__main__":
	app = MessageGenerator()
	if len(sys.argv) == 2:
		app.generate_for_package(sys.argv[1])
	elif len(sys.argv) >= 3:
		for i in range(2, len(sys.argv)):
			app.generate_for_metamessage(sys.argv[1], sys.argv[i])
