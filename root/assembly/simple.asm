section .data
message db "Hello world", 0xa
message_length equ $ - message

section .text
global _start
_start:
    ; Print the message
    mov eax, 4
    mov ebx, 1
    mov ecx, message
    mov edx, message_length
    int 0x80
    
    ; Choose to exit    
    mov eax, 1
    mov ebx, 0
    int 0x80
