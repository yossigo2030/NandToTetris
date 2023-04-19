// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed.
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
//

(LOOP)


    @SCREEN
    D=A
    @i // m = address of screen
    M=D

    @KBD
    D=M

    @BLACK // if not 0 jump
    D;JNE
    // white

(WHITELOOP)

    @i
    A=M // run on the screen adress
    M=0 // make white

    @i
    M=M+1 // run on the screen adress

    @24576
    D=A
    @i
    D=D-M // get back to whiteloop if the screen is not full
    @WHITELOOP
    D;JGT // if D > 0 jump
    @LOOP
    0;JMP
(BLACK)
    @i
    A=M // run on the screen adress
    M=-1 // make black

    @i
    M=M+1 // run on the screen adress


    @24576
    D=A

    @i
    D=D-M // get back to blackloop if the screen is not full
    @BLACK
    D;JGT // if D > 0 jump
    @LOOP
    0;JMP