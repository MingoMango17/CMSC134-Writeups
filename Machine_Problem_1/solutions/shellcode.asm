section .text
global main

main:
    xor eax, eax   ; Clear EAX register
    inc eax        ; Increment EAX to 1
    mov ebx, eax   ; Move the value of EAX into EBX (not %eab)
    int 0x80       ; Invoke system call
