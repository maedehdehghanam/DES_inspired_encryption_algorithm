# This is an algorithm that I invented inspired by DES for my cyber security course at Shahid Beheshti Universty. 

### Block Length:

64 bits

### Key Length:

32 bits

### Number of Rounds:

32 rounds

## Subkey Generation Algorithm:

To generate the subkey, we define a factor from the main key. The factor is defined as:
Factor = b32, b31, b2, b1

This factor increments by 1 in each round. The key from the previous round is divided into two halves, shifted to the left by the factor of the current round, and then XORed together. The 16-bit output is then expanded to 32 bits using an expansion function.

## Encryption Algorithm:

This algorithm is inspired by DES. The input is divided into 64-bit blocks and fed into this algorithm. The input first goes through the initial permutation function (IP) for initial permutation, and then the result is split into two parts. According to the Feistel algorithm, in each round, the next round's input is generated using the round function and the previous half. After 32 iterations, the output goes to the inverse permutation function (IP-1).

## Round Function:

This function splits the input into two parts, shifts it to the right by i, and performs modular addition. The result of the addition is XORed with the round key. The resulting 32-bit output is then divided into four 8-bit sections, which are fed into 4 SBOXes that transform 8-bit inputs into 32-bit outputs. The outputs of these functions are XORed together, and the result of this XOR undergoes a permutation.

## Example
### input:

    Computers are good at following instructions, but not at reading your mind.


### binary output:

1100000101010100110010101001000011101100100111001001100101101101000111011001000011011111001010011001000100011110011001010111010010100010110001011010101100001011011000001010110101001000111001111010010010010101110011110100111100101000000011000010111101010000001000101110100010101110011110010110101001001101100000101001101111001111001011111010100000100100001100010010001110010110101011010010000110001100011011010000010111011011111001101011110001010001100011011010011010010100111011111011100111010000101010111111000100000000100101010010010011111011000101111111001001001100001010110101110100101001111110101011110101100101100100001101100001000011

### hex output:
0xc154ca90ec9c996d1d90df29911e6574a2c5ab0b60ad48e7a495cf4f280c2f5022e8ae796a4d829bcf2fa824312396ad218c6d05dbe6bc518da694efb9d0abf1009524fb17f24c2b5d29fabd6590d843

# sboxes are taken form [this repository:]([url)](https://github.com/prophet6250/blowfish-implementation) 
