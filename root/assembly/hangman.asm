[BITS 32]

SYS_EXIT  equ 1
SYS_READ  equ 3
SYS_WRITE equ 4
STD_IN    equ 0
STD_OUT   equ 1
SUCCESS   equ 0
KERNEL    equ 0x80
LINE_FEED equ 0xA
CARRIAGE_RETURN equ 0xD

global play_hangman
extern printf

section .data
    special_characters db 0xa, " ", "_" ; line feed, space, underscore
    start_message db "Let's play hangman!", 0xa, "Enter a character and press enter to guess.", 0xa
    start_message_length equ $ - start_message
    max_input_length equ 100
    too_long_message db "The secret string was too long. Sorry! Check the C code!", 0xa
    too_long_message_length equ $ - too_long_message
    correctly_guessed_characters times max_input_length db 0
    lives_remaining dd 10
    lives_remaining_message_plural db "You have %d lives remaining.", 0xa, 0
    lives_remaining_message_single db "You have %d life remaining! Be careful!", 0xa, 0
    you_lose_message db "Sorry, you died. :-(", 0xa
    you_lose_message_length equ $ - you_lose_message
    you_win_message db "Congratulations, you win!", 0xa
    you_win_message_length equ $ - you_win_message

section .bss
    input_length resb 1
    input resd 1
    guess resb 256 ; read extra input to consume newline characters.

section .text

play_hangman:
    push ebp
    mov ebp, esp; for correct debugging
    pushad; preserve all registers

    mov eax, start_message
    mov ebx, start_message_length
    call .print

    mov eax, [ebp + 8] ; first argument
    mov [input], eax
    call .get_string_length
    cmp ebx, max_input_length
    jg .input_too_long
    mov [input_length], bl

    call .game_loop

    popad; restore all registers
    leave
    ret

.game_loop:
    pusha
.game_loop_start:
    call .print_lives

    call .check_lose
    cmp eax, 1
    je .game_loop_end

    call .print_challenge

    call .check_win
    cmp eax, 1
    je .game_loop_end

    call .get_guess
    call .update_correct_guesses
    jmp .game_loop_start
.game_loop_end:
    popa
    ret

.check_lose:
    ; Check if the player has lost. eax will be 1 if so, and zero otherwise.
    cmp dword [lives_remaining], 0
    je .check_lose_lost
    mov eax, dword 0
    ret
.check_lose_lost:
    call .lose
    mov eax, dword 1
    ret

.check_win:
    ; Check if the player has won. eax will be 1 if so, and zero otherwise.
    xor ecx, ecx
.check_win_loop:
    cmp cl, byte [input_length]
    jge .check_win_won
    mov eax, correctly_guessed_characters
    add eax, ecx
    cmp byte [eax], 0
    je .check_win_exit
    inc ecx
    jmp .check_win_loop
.check_win_won:
    call .win
    mov eax, dword 1
    ret
.check_win_exit:
    mov eax, dword 0
    ret

.update_correct_guesses:
    pusha
    xor ecx, ecx
    xor edx, edx
.update_correct_guesses_loop:
    cmp cl, byte [input_length]
    je .update_correct_guesses_loop_exit
    mov eax, dword [input]
    add eax, ecx
    mov bl, byte [eax]
    cmp bl, [guess]
    je .update_correct_guesses_correct
    jmp .update_correct_guesses_loop_end
.update_correct_guesses_correct:
    inc edx
    mov eax, correctly_guessed_characters
    add eax, ecx
    mov byte [eax], 1
    jmp .update_correct_guesses_loop_end
.update_correct_guesses_loop_end:
    inc ecx
    jmp .update_correct_guesses_loop
.update_correct_guesses_loop_exit:
    cmp edx, 0
    jne .update_correct_guesses_exit
    sub byte [lives_remaining], 1
.update_correct_guesses_exit:
    popa
    ret

.lose:
    pusha
    mov eax, you_lose_message
    mov ebx, you_lose_message_length
    call .print
    popa
    ret

.win:
    pusha
    mov eax, you_win_message
    mov ebx, you_win_message_length
    call .print
    popa
    ret

.input_too_long:
    mov eax, too_long_message
    mov ebx, too_long_message_length
    call .print
    jmp .exit

.get_string_length:
    ; Get the length of a string, assuming it is in eax. Returns the length in ebx
    mov ebx, eax
.get_string_length_loop:
    mov dl, byte [ebx]
    cmp dl, 0
    je .get_string_length_exit
    add ebx, byte 1
    jmp .get_string_length_loop
.get_string_length_exit:
    sub ebx, eax
    ret

.get_guess:
    pusha
.get_guess_loop:
    mov eax, guess
    mov ebx, 256
    call .read
    cmp byte [guess], 0xa
    je .get_guess_loop
    cmp byte [guess], " "
    je .get_guess_loop
    cmp byte [guess], 0xd
    je .get_guess_loop
    popa
    ret

.print_lives:
    cmp dword [lives_remaining], 1
    je .print_lives_single

    push dword [lives_remaining]
    push lives_remaining_message_plural
    call printf
    add esp, 8
    ret
.print_lives_single:
    push dword [lives_remaining]
    push lives_remaining_message_single
    call printf
    add esp, 8
    ret

.print_challenge:
    xor ecx, ecx
.print_challenge_loop:
    cmp cl, byte [input_length]
    je .print_challenge_loop_exit
    mov eax, correctly_guessed_characters
    add eax, ecx
    mov bl, byte [eax]
    cmp bl, 0
    jne .print_challenge_character
    call .print_underscore
    jmp .print_challenge_loop_end
.print_challenge_character:
    mov eax, dword [input]
    add eax, ecx
    mov ebx, 1
    call .print
    jmp .print_challenge_loop_end
.print_challenge_loop_end:
    call .print_space
    inc ecx
    jmp .print_challenge_loop
.print_challenge_loop_exit:
    call .print_newline
    ret

.print_newline:
    ; Print a newline character
    pushad
    mov eax, special_characters
    mov ebx, 1
    call .print
    popad
    ret

.print_space:
    ; Print a space character
    pushad
    mov eax, special_characters + 1
    mov ebx, 1
    call .print
    popad
    ret

.print_underscore:
    ; Print an underscore character
    pushad
    mov eax, special_characters + 2
    mov ebx, 1
    call .print
    popad
    ret

.print:
    ; Print a string to the screen. The first argument in eax
    ; is the string and the second argument in ebx is the length.
    pushad
    mov  ecx, eax
    mov  edx, ebx
    mov  eax, SYS_WRITE
    mov  ebx, STD_OUT
    int  KERNEL
    popad
    ret

.read:
    ; Read a string from the user and put in the given buffer.
    ; First argument in eax should be the buffer, second in ebx is the size
    mov  ecx, eax
    mov  edx, ebx
    mov  eax, SYS_READ
    mov  ebx, STD_IN
    int  KERNEL
    ret

.exit:
    popad; restore all registers
    leave
    ret
