#!/usr/bin/env bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"/assembly
nasm -g -f elf32 $DIR/simple.asm -o $DIR/simple.o -F dwarf
gcc $DIR/simple.o -g -o $DIR/simple -m32 -fno-pie -no-pie -nodefaultlibs -nostdlib -Og
