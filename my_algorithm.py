def string_to_binary(input_string):
    binary_string = ''.join(format(ord(char), '08b') for char in input_string)
    return binary_string

def permute(input_bits, permutation_table):
    if len(input_bits) != 64:
        raise ValueError("Input must be 64 bits long")

    output_bits = [0] * 64
    for i in range(64):
        output_bits[i] = input_bits[permutation_table[i]]

    return output_bits

def expand_16_to_32_bit(bin_str):
    if len(bin_str) != 16 or not all(c in '01' for c in bin_str):
        raise ValueError("Input must be a 16-bit binary string.")
    
    # Mapping based on the provided table
    mapping = [
        31, 0, 1, 2, 3, 4, 5, 8,
        9, 10, 11, 12, 13, 16, 17, 18,
        19, 20, 21, 24, 25, 26, 27, 28,
        29, 30, 31, 30, 29, 28, 27, 0
    ]
    
    expanded_bin_str = ''.join(bin_str[mapping[i] % 16] for i in range(32))
    
    return expanded_bin_str


def permute_32bit(input_32, permutation_table):
    output_32 = 0
    input_32 = int(input_32, 2)
    for i, position in enumerate(permutation_table):
        bit = (input_32 >> (32 - position)) & 1
        output_32 |= bit << (31 - i)

    return bin(output_32)[2:]


def inverse_permute(input_bits, permutation_table):
    if len(input_bits) != 64:
        raise ValueError("Input must be 64 bits long")

    output_bits = [0] * 64
    for i in range(64):
        output_bits[permutation_table[i]] = input_bits[i]

    return " ".join(output_bits).replace(" ", "")



def make_Sbox(filename: str, start_line: int, end_line: int) -> list[list[str]]:
    lines = []

    with open(filename, "r") as file:
        for i, line in enumerate(file, start=1):
            if i >= start_line and i <= end_line:
                lines.append(line.rstrip())
            if i > end_line:
                break

    matrix = []
    for line in lines:
        matrix.append(line.split())

    int_matrix = [[int(element, 16) for element in row] for row in matrix]
    bin_matrix = [
        [left_zero_pad(bin(integer_value)[2:], 32) for integer_value in row]
        for row in int_matrix
    ]
    return bin_matrix


def read_from_sbox(
    input_sbox: str, sbox: list[list[str]]
) -> str:  # input --> (b1,b2,b3,b4,b5,b6,b7,b8)
    column = (
        input_sbox[0] + input_sbox[1] + input_sbox[7]
    )  # fisrt, second and last bit determine the column
    row = input_sbox[2:7]  # third to 7th bit determine the row
    int_column = int(column, 2)
    int_row = int(row, 2)
    return sbox[int_row][int_column]
    return output_bits


def split_to_n_bit_chunks(
    binary_string: str, inteded_length: int, chunk_size: int
) -> list[str]:
    len_input = len(binary_string)
    n = inteded_length - len_input
    binary_string = (n * "0") + binary_string
    chunks = [
        binary_string[i : i + chunk_size]
        for i in range(0, len(binary_string), chunk_size)
    ]
    return chunks


def left_zero_pad(input_string: str, n: int) -> str:
    if len(input_string) == n:
        return input_string
    elif len(input_string) > n:
        raise ("The input string is longer than n")
    else:
        k = n - len(input_string)
        return k * "0" + input_string


def add_modulo(input_a: str, input_b: str, n: int) -> str:
    a = int(input_a, 2)
    b = int(input_b, 2)
    ans = (a + b) % (2**n)
    return bin(ans)[2:]


def rotate_right(my_string, factor, bit_size=32):
    value = int(my_string, 2)
    n = int(factor, 2)
    if not (0 <= value < (1 << bit_size)):
        raise ValueError(f"value must be a {bit_size}-bit integer.")

    n %= bit_size
    return bin(((value >> n) | (value << (bit_size - n))) & ((1 << bit_size) - 1))[2:]


def rotate_left(my_string, factor, bit_size=16):
    value = int(my_string, 2)
    n = int(factor, 2)
    if not (0 <= value < (1 << bit_size)):
        raise ValueError(f"value must be a {bit_size}-bit integer.")
    n %= bit_size
    return bin(((value << n) | (value >> (bit_size - n))) & ((1 << bit_size) - 1))[2:]


def bstr_xor(a: str, b: str) -> str:
    return bin(int(a, 2) ^ int(b, 2))[2:]


def key_gen(last_key, factor):
    key_chunks = split_to_n_bit_chunks(last_key, 32, 16)
    left_key_rotated = rotate_left(key_chunks[0], factor)
    right_key_rotated = rotate_left(key_chunks[1], factor)
    xor_two_chunks = left_zero_pad(bstr_xor(right_key_rotated, left_key_rotated),16)
    return expand_16_to_32_bit(xor_two_chunks), add_modulo(factor, "1", 32)


def round_func(input_string, key_round, i, sbox_list):

    input_chunks = split_to_n_bit_chunks(input_string, 64, 32)

    left_rotated = rotate_right(input_chunks[0], i)
    right_rotated = rotate_right(input_chunks[1], i)

    modular_addition = left_zero_pad(add_modulo(left_rotated, right_rotated, 32), 32)
    _8bit_chunks = split_to_n_bit_chunks(modular_addition, 32, 8)

    #8 bit to 32 bit transformation 
    sbox1_output = read_from_sbox(_8bit_chunks[0], sbox_list[0])
    sbox2_output = read_from_sbox(_8bit_chunks[1], sbox_list[1])
    sbox3_output = read_from_sbox(_8bit_chunks[2], sbox_list[2])
    sbox4_output = read_from_sbox(_8bit_chunks[3], sbox_list[3])

    #xor the output of each sbox
    sbox1_xor_sbox2 = left_zero_pad(bstr_xor(sbox1_output, sbox2_output), 32)
    sbox3_xor = left_zero_pad(bstr_xor(sbox1_xor_sbox2, sbox3_output), 32)
    sbox4_xor = left_zero_pad(bstr_xor(sbox3_xor, sbox4_output), 32)

    return permute_32bit(sbox4_xor, PERMUTATION_TABLE_32)


def algorithm(input_string, key, sbox_list):
    #formating inputs 
    input_string = left_zero_pad(input_string, 64)
    key = left_zero_pad(key, 32)

    initial_permutation = permute(input_string, permutation_table)

    #calculating factor as explained
    factor = key[31] + key[30] + key[1] + key[0]

    input_string_chunks = split_to_n_bit_chunks(input_string, 64, 32)
    last_L = input_string_chunks[0]
    last_R = input_string_chunks[1]

    #32 rounds 
    for i in range(32):
        key, factor = key_gen(key, factor)
        Ri = left_zero_pad(round_func(input_string, key, factor, sbox_list), 32)
        Li = last_R  # last R is the new L
        input_string = Ri + Li #making the next input ready
        last_R = Ri
    #depermute the last round 

    depermutation = inverse_permute(input_string, permutation_table)
    return depermutation

def encrypt(plain_text, key, sbox_list):
    plain_text_bin = string_to_binary(plain_text) 
    remainder = len(plain_text_bin)%64
    plain_text_bin = left_zero_pad(plain_text_bin, len(plain_text_bin)+remainder)
    input_len = len(plain_text_bin)
    plain_text_chunks = split_to_n_bit_chunks(plain_text_bin,input_len, 64)
    cipher_text =[]
    for chunk in plain_text_chunks:
        encrypted_chunk = algorithm(chunk, key, sbox_list)
        cipher_text.append(encrypted_chunk)
    return " ".join(cipher_text).replace(" ", "")


permutation_table = [
    0,
    4,
    8,
    12,
    16,
    20,
    24,
    28,
    32,
    36,
    40,
    44,
    48,
    52,
    56,
    60,
    1,
    5,
    9,
    13,
    17,
    21,
    25,
    29,
    33,
    37,
    41,
    45,
    49,
    53,
    57,
    61,
    2,
    6,
    10,
    14,
    18,
    22,
    26,
    30,
    34,
    38,
    42,
    46,
    50,
    54,
    58,
    62,
    3,
    7,
    11,
    15,
    19,
    23,
    27,
    31,
    35,
    39,
    43,
    47,
    51,
    55,
    59,
    63,
]
PERMUTATION_TABLE_32 = [
    16,
    7,
    20,
    21,
    29,
    12,
    28,
    17,
    1,
    15,
    23,
    26,
    5,
    18,
    31,
    10,
    2,
    8,
    24,
    14,
    32,
    27,
    3,
    9,
    19,
    13,
    30,
    6,
    22,
    11,
    4,
    25,
]
sbox_list = [
    make_Sbox("sbox.txt", 2, 33),
    make_Sbox("sbox.txt", 36, 67),
    make_Sbox("sbox.txt", 70, 101),
    make_Sbox("sbox.txt", 104, 135),
]
plaintext = "Computers are good at following instructions, but not at reading your mind."
key = "101010101010"

ciphertext = encrypt(plaintext, key, sbox_list)
print(f"input:\n{plaintext}")
print(f"binary output:\n{ciphertext}")
print(f"hex output:\n{hex(int(ciphertext,2))}")
