import os

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

    instFull = [
    MI|CO, RO|II|CE, 0,     0,     0,        0,0,0, # NOP   0000 0000
    MI|CO, RO|II|CE, IO|MI, RO|AI, 0,        0,0,0, # LDA   0001 0000
    MI|CO, RO|II|CE, IO|MI, RO|BI, AI|EO,    0,0,0, # ADD   0010 0000
    MI|CO, RO|II|CE, IO|MI, RO|BI, AI|EO|SU, 0,0,0, # SUB   0011 0000
    MI|CO, RO|II|CE, IO|MI, AO|RI, 0,        0,0,0, # STA   0100 0000
    MI|CO, RO|II|CE, IO|AI, 0,     0,        0,0,0, # LDI   0101 0000
    MI|CO, RO|II|CE, IO|J,  0,     0,        0,0,0, # JMP   0110 0000
    MI|CO, RO|II|CE, 0,     0,     0,        0,0,0, # NOP   0111 0000
    MI|CO, RO|II|CE, 0,     0,     0,        0,0,0, # NOP   1000 0000
    MI|CO, RO|II|CE, 0,     0,     0,        0,0,0, # NOP   1001 0000
    MI|CO, RO|II|CE, 0,     0,     0,        0,0,0, # NOP   1010 0000
    MI|CO, RO|II|CE, 0,     0,     0,        0,0,0, # NOP   1011 0000
    MI|CO, RO|II|CE, 0,     0,     0,        0,0,0, # NOP   1100 0000
    MI|CO, RO|II|CE, 0,     0,     0,        0,0,0, # NOP   1101 0000
    MI|CO, RO|II|CE, AO|DI, 0,     0,        0,0,0, # DSP   1110 0000
    MI|CO, RO|II|CE, HLT,   0,     0,        0,0,0  # HLT   1111 0000
    ]

    chipOne = bytearray(2048)
    chipTwo = bytearray(2048)
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
        if keepOut.upper() == 'Y':
            print("cool, have fun with your sap1 homie!")
        elif keepOut.upper() == 'N':
            os.system('rm sapFinal1.bin;rm sapFinal2.bin')
            print('Dilemna deleted, Britta for the win! Get your sap1 on duder')
        else:
            "Nope, that's not an option, try again."
if __name__ == "__main__":
	main()
