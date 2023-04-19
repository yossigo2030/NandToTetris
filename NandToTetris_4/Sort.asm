// This file is part of nand2tetris, as taught in The Hebrew University,
// and was written by Aviv Yaish, and is published under the Creative
// Common Attribution-NonCommercial-ShareAlike 3.0 Unported License
// https://creativecommons.org/licenses/by-nc-sa/3.0/

// An implementation of a sorting algorithm.
// An array is given in R14 and R15, where R14 contains the start address of the
// array, and R15 contains the length of the array.
// You are not allowed to change R14, R15.
// The program should sort the array in-place and in descending order -
// the largest number at the head of the array.
// You can assume that each array value x is between -16384 < x < 16384.
// You can assume that the address in R14 is at least >= 2048, and that
// R14 + R15 <= 16383.
// No other assumptions can be made about the length of the array.
// You can implement any sorting algorithm as long as its runtime complexity is
// at most C*O(N^2), like bubble-sort.

// Put your code here.
// out of array
    @index
    M=0;
    @flag
    M=0
    @locationA
    M=0
(LOOP)
    @index
    M=M+1
    D=M
    @R15
    D=D-M // if < 0 jump to end
    @ENDFIRST
    D;JEQ

    @index
    M=M-1

    @R14
    D=M // D = arr[0] // 5034
    @index
    A=D+M // A = address of arr[0] + index // 5034 + index
    D=M // D = 100 M[0]
    A=A+1 // array[i+1]
    D=D-M
    @SWAP
    D;JLT // jump if arr[0] < arr[1]

    @index
    M=M+1

    D;JLT // else jump to loop
    @LOOP
    0;JMP
(SWAP)
    @flag
    M=M+1

    // temp

    @R14
    D=M // D = arr[0] // 5034
    @index
    A=D+M // A = address of arr[0] + index // 5034 + index
    D=M // D = 100 M[0]
    @valueOfA
    M=D

    @R14
    D=M
    @index
    A=D+M
    A=A+1
    D=M
    @valueOfB
    M=D

    @R14
    D=M
    @index
    A=D+M
    A=A+1
    D=A
    @locationOfB
    M=D

    // assinment of A
    @valueOfB
    D=M
    @locationOfB
    A=M-1
    M=D

    // assinment of B

    @valueOfA
    D=M
    @locationOfB
    A=M
    M=D

    @index
    M=M+1


    @LOOP
    0;JMP



(ENDFIRST)
    @flag
    D=M
    @END
    D;JEQ
    @flag
    M=0
    @index
    M=0
    @LOOP
    0;JMP
(END)
@END
0;JMP