#!//usr/local/bin/python3


# not to be used with python below version 3.7!!!!!  This script takes advantage of python 3.7's
# ordered dictionary functionality

import os
import sys

EEPROM_SIZE = 2048
ADDR_BIT_LENGTH = 10

def main():
    HLT = 32768
    MI = 16384
    RI = 8192
    RO = 4096
    IO = 2048
    II = 1024
    AI = 512
    AO = 256
    EO = 128
    SU = 64
    BI = 32
    DI = 16
    CE = 8
    CO = 4
    J = 2
    FI = 1

    instTemplate = {
    "NOP": [MI|CO, RO|II|CE, 0,     0,     0,           0,0,0], # 0000
    "LDA": [MI|CO, RO|II|CE, IO|MI, RO|AI, 0,           0,0,0], # 0001
    "ADD": [MI|CO, RO|II|CE, IO|MI, RO|BI, AI|EO|FI,    0,0,0], # 0010
    "SUB": [MI|CO, RO|II|CE, IO|MI, RO|BI, AI|EO|SU|FI, 0,0,0], # 0011
    "STA": [MI|CO, RO|II|CE, IO|MI, AO|RI, 0,           0,0,0], # 0100
    "LDI": [MI|CO, RO|II|CE, IO|AI, 0,     0,           0,0,0], # 0101
    "JMP": [MI|CO, RO|II|CE, IO|J,  0,     0,           0,0,0], # 0110
    "JC":  [MI|CO, RO|II|CE, 0,     0,     0,           0,0,0], # 0111
    "JZ":  [MI|CO, RO|II|CE, 0,     0,     0,           0,0,0], # 1000
    "NOP2":[MI|CO, RO|II|CE, 0,     0,     0,           0,0,0], # 1001
    "NOP3":[MI|CO, RO|II|CE, 0,     0,     0,           0,0,0], # 1010
    "NOP4":[MI|CO, RO|II|CE, 0,     0,     0,           0,0,0], # 1011
    "NOP5":[MI|CO, RO|II|CE, 0,     0,     0,           0,0,0], # 1100
    "NOP6":[MI|CO, RO|II|CE, 0,     0,     0,           0,0,0], # 1101
    "DSP": [MI|CO, RO|II|CE, AO|DI, 0,     0,           0,0,0], # 1110
    "HLT": [MI|CO, RO|II|CE, HLT,   0,     0,           0,0,0]  # 1111
    }

    instFull = list()
    for i in range(EEPROM_SIZE):
        instFull.append(0)
    count = 0
    for i in range(int((2**ADDR_BIT_LENGTH)/(len(instTemplate) * len(instTemplate["NOP"])))): #it's just 8 folks, don't sweat
        for j in instTemplate:
            if (j == "JC" and i in [2,3,6,7]) or (j == "JZ" and i in [4,5,6,7]):
                ret = [MI|CO, RO|II|CE, IO|J, 0, 0, 0, 0, 0]
            else:
                ret = instTemplate[j]
            for k in ret:
                instFull[count] = k
                count += 1

    chipOne = bytearray(EEPROM_SIZE)
    chipTwo = bytearray(EEPROM_SIZE)
    address = 0
    for i in instFull:
        chipOne[address] = i >> 8
        chipTwo[address] = i - ((i >>8) <<8)
        address += 1
    with open('sapFinal1.bin', 'wb') as f:
        f.write(chipOne)
    with open('sapFinal2.bin', 'wb') as f:
        f.write(chipTwo)
    input("Insert Left Chip into Programmer and Press Enter when Ready")
    termout = os.popen('minipro -p CAT28C16A -w sapFinal1.bin').read()
    print(termout)
    input("Insert Right Chip into Progrmmer and Press Enter when Ready")
    termout = os.popen('minipro -p CAT28C16A -w sapFinal2.bin').read()
    print(termout)
    keepOutput = ''
    while keepOutput.upper() != 'Y' and keepOutput.upper() != 'N':
        keepOutput = input("programming finished, would you like to keep the binary files you created? (y/n)")
        if keepOutput.upper() == 'Y':
            print("cool, have fun with your sap1 homie!")
        elif keepOutput.upper() == 'N':
            os.system('rm sapFinal1.bin;rm sapFinal2.bin')
            print('Dilemna deleted, Britta for the win! Get your sap1 on duder')
        else:
            print("Nope, that's not an option, try again.")
if __name__ == "__main__":
	main()
