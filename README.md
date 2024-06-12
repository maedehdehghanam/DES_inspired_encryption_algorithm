## This is an algorithm that I invented inspired by DES for my cyber security course at Shahid Beheshti Universty. 

Block Length
64 bits

Key Length
32 bits

Number of Rounds
32 rounds

Subkey Generation Algorithm
To generate the subkey, we define a factor from the main key. The factor is defined as:
Factor = b32, b31, b2, b1

This factor increments by 1 in each round. The key from the previous round is divided into two halves, shifted to the left by the factor of the current round, and then XORed together. The 16-bit output is then expanded to 32 bits using an expansion function.

Encryption Algorithm
This algorithm is inspired by DES. The input is divided into 64-bit blocks and fed into this algorithm. The input first goes through the initial permutation function (IP) for initial permutation, and then the result is split into two parts. According to the Feistel algorithm, in each round, the next round's input is generated using the round function and the previous half. After 32 iterations, the output goes to the inverse permutation function (IP-1).

Round Function
This function splits the input into two parts, shifts it to the right by i, and performs modular addition. The result of the addition is XORed with the round key. The resulting 32-bit output is then divided into four 8-bit sections, which are fed into 4 SBOXes that transform 8-bit inputs into 32-bit outputs. The outputs of these functions are XORed together, and the result of this XOR undergoes a permutation.
