import os

CONSTS = {
    "G": ("1", "GPS"),
    "S": ("2", "SBAS"),
    "R": ("3", "GLONASS"),
    "J": ("4", "QZSS"),
    "C": ("5", "BeiDou"),
    "E": ("6", "Galileo"),
    "I": ("7", "IRNSS")
}
VALID_CONST_CHARS = list(CONSTS.keys())


const_present = []

print("|- Enter the absolute path of the raw (.txt) log file to be cleaned:")
input_filepath = input("|-> ")

while True:
    input_filepath = input_filepath.strip().strip('"')

    if os.path.exists(input_filepath):
        if not os.path.isfile(input_filepath) or not input_filepath.endswith(".txt"):
            print("\n|-! \033[31mERROR: The selected file is not a '.txt' file.\033[0m")
        else:
            break
    else:
        print("\n|-! \033[31mERROR: The file path entered does not exist.\033[0m")


    print("\n|- Enter a valid absolute file path of a '.txt' file:")
    input_filepath = input("|-> ")

output_filepath = os.path.join(os.path.dirname(input_filepath), "cleaned_" + os.path.basename(input_filepath))

print("\n|- To remove the data from the particular constellation,")
print("|- Enter the constellation characters, in comma separated or space separated manner")
print("    \033[34m(GPS: G, SBAS: S, GLONASS: R, QZSS: J, BeiDou: C, Galileo: E, IRNSS: I)\033[0m")

rm_consts = input("|-> ").upper()

invalid_consts_provided = []
while True:
    rm_consts_list = [c for c in rm_consts.replace(",", "").strip()]
    for const_char in rm_consts_list:
        const_char = const_char.strip()
        if not const_char or const_char in VALID_CONST_CHARS:
            continue
        invalid_consts_provided.append(const_char)
    if not len(invalid_consts_provided):
        break
    print(f"\n|-! \033[31mERROR: The Constellation Characters provided are not valid; Invalid characters:\033[0m {invalid_consts_provided}")
    print("\n|- Enter the Correct Constellation Character for the Constellation to be removed: ")
    
    invalid_consts_provided = []
    rm_consts = input("|-> ")

print("\n|- Enter the C/N0 threshold for the removal of the satellite data")
print("   \033[34m(Default value of the threshold is 20, Press \033[35mEnter\033[34m for default)\033[0m")
cn0_threshold = input("|-> ").upper()

while True:
    try:
        if cn0_threshold == "":
            print("\033[A\033[4C20\n", end="")
            cn0_threshold = 20
            break
        cn0_threshold = float(cn0_threshold)
        if cn0_threshold < 0:
            raise ValueError("The value of the C/N0 threshold can't be less than zero.")
        if cn0_threshold <= 10:
            print("\n|-? \033[33mWARNING: The C/N0 threshold less than '10' is not recommended, as corrupted data may creep in.\033[0m")
        if cn0_threshold > 40:
            print("\n|-? \033[33mWARNING: The C/N0 threshold greater than '40' is not recommended, as no satellite may have C/N0 greater than 40.\033[0m")
        break
    except ValueError as e:
        print(f"\n|-! \033[31mERROR: {e}\033[0m")
        print("\n|- Please enter a valid C/N0 threshold")
        cn0_threshold = input("|-> ")

# print(rm_consts_list)
# print("\n", input_filepath, "\n", output_filepath)

def is_valid_raw(parts):
    try:
        cn0 = float(parts[16])
        const_num = parts[28]


        if int(const_num) <= 0 or int(const_num) > 7:
            return False

        const = ""
        for c in VALID_CONST_CHARS:
            if const_num == CONSTS[c][0]:
                const = c
                break
        
        if const == "" or const in rm_consts_list:
            return False


        if cn0 < cn0_threshold:
            return False
        
        if const not in const_present:
            const_present.append(const)
        return True
    except (ValueError, IndexError):
        return False


print("\n     [Processing...]")

with open(input_filepath, 'r') as f_in, open(output_filepath, 'w') as f_out:
    for line in f_in:
        if line.startswith("Raw"):
            parts = line.split(',')
            if is_valid_raw(parts):
                f_out.write(line)
        else:
            f_out.write(line)

print(f"\033[A\033[19C{"\b" * 3} Completed.]")        

print("\n|->> \033[32mCleaned file saved:\033[0m ", output_filepath)
print("|->> \033[32mConstellations present in the cleaned raw file: \033[0m", const_present)

print("\n\n[Press \033[34mEnter\033[0m to close]")
while input():
    break