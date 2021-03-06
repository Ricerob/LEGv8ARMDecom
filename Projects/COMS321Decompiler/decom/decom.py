import sys
import struct
from bitstring import BitArray

### Denotes done

instruction_dict = [
  ["ADD", "0b10001011000", "R"],
  ["ADDI", "0b1001000100", "I"],
  ["AND", "0b10001010000", "R"],
  ["ANDI", "0b1001001000", "I"],
  ["BL", "0b100101", "B"],
  ["BR", "0b11010110000", "R"],
  ["CBNZ", "0b10110101", "CB"],
  ["CBZ", "0b10110100", "CB"],
  ["B.cond", "0b01010100", "CB"],
  ["DUMP", "0b11111111110", "DUMP"],
  ["EOR", "0b11001010000", "R"],
  ["EORI", "0b1101001000", "I"],
  ["HALT", "0b11111111111", "HALT"],
  ["LDUR", "0b11111000010", "D"],
  ["LSL", "0b11010011011", "R"],
  ["LSR", "0b11010011010", "R"],
  ["ORR", "0b10101010000", "R"],
  ["ORRI", "0b1011001000", "I"],
  ["PRNL", "0b11111111100", "PRNL"],
  ["PRNT", "0b11111111101", "PRNT"],
  ["STUR", "0b11111000000", "D"],
  ["SUB", "0b11001011000", "R"],
  ["SUBI", "0b1101000100", "I"],
  ["SUBIS", "0b1111000100", "I"],
  ["SUBS", "0b11101011000", "R"],
  ["B", "0b000101", "B"],
  ["MUL", "0b10011011000", "R"]
]

cond_dict = [
    ["EQ", "00000"],
    ["NE", "00001"],
    ["HS", "00010"],
    ["LO", "00011"],
    ["MI", "00100"],
    ["PL", "00101"],
    ["VS", "00110"],
    ["VC", "00111"],
    ["HI", "01000"],
    ["LS", "01001"],
    ["GE", "01010"],
    ["LT", "01011"],
    ["GT", "01100"],
    ["LE", "01101"],
]

R_accepted_dict = [
    "ADD", "AND", "EOR", "ORR", "SUB", "SUBS", "MUL"
]

I_accepted_dict = [
    "ADDI", "ANDI", "ORRI", "SUBI", "EORI", "SUBIS"
]

def decodeBytes(current_byte):
    if current_byte == 0b0:
        return 0
    for instruction in instruction_dict:
        if current_byte.startswith(instruction[1]):
            return instruction
    return "ERR"

def decodeRInstruction(instruction, instruction_info):
    opcode = instruction[2:13]
    Rm = instruction[13:18]
    shamt = instruction[18:24]
    Rn = instruction[24:29]
    Rd = instruction[29:]

    if instruction_info[0] in R_accepted_dict:
        print(instruction_info[0] + " X" + str(int(Rd, 2)) + ", X" + str(int(Rn, 2)) + ", X" + str(int(Rm, 2)))
    elif instruction_info[0] == "BR":
        print(instruction_info[0] + " X" + str(int(Rn, 2)))
    elif instruction_info[0] == "LSL" or instruction_info[0] == "LSR":
        print(instruction_info[0] + " X" + str(int(Rd, 2)) + ", X" + str(int(Rn, 2)) + ", #" + str(int(shamt, 2)))
    else:
        print("Error decoding R type instruction. Instruction data: " + instruction_info[0] +
              ". Instruction binary: " + instruction)


# Played around with the BitArray stuff a bit too much here - should still work as intended. Used for getting signed
# bits from bin()s. Put bin() value in the BitArray with bin=[val], and use .int for signed, and .unit for unsigned
def decodeIInstruction(instruction, instruction_info):
    ALU_immediate = BitArray(bin=instruction[12:24])
    Rn = instruction[24:29]
    Rd = instruction[29:]

    if instruction_info[0] in I_accepted_dict:
        print(instruction_info[0] + " X" + str(int(Rd, 2)) + ", X" + str(int(Rn, 2)) + ", #" + str(ALU_immediate.int))
    else:
        print("Error decoding I type instruction. Instruction data: " + instruction_info[0] +
              ". Instruction binary: " + instruction)


def decodeDInstruction(instruction, instruction_info):
    opcode = instruction[2:13]
    DT_addreess = BitArray(bin=instruction[13:22])
    op = instruction[22:24]
    Rn = instruction[24:29]
    Rd = instruction[29:]
    
    if instruction_info[0] == "STUR" or instruction_info[0] == "LDUR":
        print(instruction_info[0] + " X" + str(int(Rd, 2)) + ", [X" + str(int(Rn, 2)) + ", #" + str(DT_addreess.int) + "]")
    else:
        print("Error decoding D type instruction. Instruction data: " + instruction_info[0] +
              ". Instruction binary: " + instruction)


def decodeBInstruction(instruction, instruction_info):
    opcode = instruction[2:8]
    BR_address = BitArray(bin=instruction[8:])

    if instruction_info[0] == "B" or instruction_info[0] == "BL":
        print(instruction_info[0] + " " + str(BR_address.int))
    else:
        print("Error decoding B type instruction. Instruction data: " + instruction_info[0] + ". Instruction binary: " +
              str(instruction))


def decodeCBInstruction(instruction, instruction_info):
    opcode = instruction[2:10]
    COND_BR_address = BitArray(bin=instruction[10:29])
    Rt = instruction[29:]

    if instruction_info[0] == "CBNZ" or instruction_info[0] == "CBZ":
        print(instruction_info[0] + " X" + str(int(Rt, 2)) + ", " +
              str(COND_BR_address.int))
    elif instruction_info[0] == "B.cond":
        for cond in cond_dict:
            if Rt == cond[1]:
                print("B." + cond[0] + " " + str(COND_BR_address.int))
    else:
        print("Error decoding CB type instruction. Instruction data: " + instruction_info[0] + ". Instruction binary: " +
              str(instruction))

def decodeDUMPInstruction(instruction, instruction_info):
    print("DUMP")


def decodeHALTInstruction(instruction, instruction_info):
    print("HALT")


def decodePRNLInstruction(instruction, instruction_info):
    print("PRNL")


# Check Rd field for register, looks like R instruction
def decodePRNTInstruction(instruction, instruction_info):
    opcode = instruction[2:13]
    Rd = instruction[29:]
    print(instruction_info[0] + " X" + str(int(Rd, 2)))


if __name__ == "__main__":
    f = open(sys.argv[1], "rb")
    while True:
        current_byte = bin(int.from_bytes(f.read(4), byteorder='big'))

        if len(current_byte) == 31: # Super super scuffed way to handle this issue.. bin() gets rid of leading zeroes so i'm adding them in manually lol
            current_byte = current_byte[:2] + "000" + current_byte[2:]
        elif len(current_byte) == 33:
            current_byte = current_byte[:2] + "0" + current_byte[2:]

        if current_byte == bin(0b0):
            break
        else:
            instruction = decodeBytes(current_byte)
            if instruction == "ERR":
                print("ERROR: Failure reading opcode. Result: " + instruction + ". Input: " + current_byte)
                exit()

        if instruction[2] == "R":
            decodeRInstruction(current_byte, instruction)
        elif instruction[2] == "I":
            decodeIInstruction(current_byte, instruction)
        elif instruction[2] == "D":
            decodeDInstruction(current_byte, instruction)
        elif instruction[2] == "B":
            decodeBInstruction(current_byte, instruction)
        elif instruction[2] == "CB":
            decodeCBInstruction(current_byte, instruction)
        elif instruction[2] == "DUMP":
            decodeDUMPInstruction(current_byte, instruction)
        elif instruction[2] == "HALT":
            decodeHALTInstruction(current_byte, instruction)
        elif instruction[2] == "PRNL":
            decodePRNLInstruction(current_byte, instruction)
        elif instruction[2] == "PRNT":
            decodePRNTInstruction(current_byte, instruction)
        else:
            print("ERROR: Failure in reading instruction class. Instruction: " + instruction[0] + ". Type: " + instruction[2])
            exit(1)
