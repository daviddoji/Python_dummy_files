# -*- coding: utf-8 -*-
#"""
#Created on Sat May  3 20:08:45 2014
#
#@author: david
#"""

import sys

def Hello(name):
    name = name + '!!!!!'
    print('Hello', name)

#Define una función main() que imprime un saludo
def main():
    Hello(sys.argv[1])


#Este es el texto estandar para llamar a la función main()
if __name__ == '__main__':
    main()
#Ejecutar así
#python test.py David
#Hello David!!!!!