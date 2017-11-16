.data
__expr_spc: 
 .align 2 
 .space 7028
__atom: 
 .align 2 
 .space 4
__entero_auxiliar: 
 .align 2 
 .space 4
__verdadero: .asciiz "verdadero"
__falso: .asciiz "falso"
__conversion: 
 .align 2 
 .space 4
__fp1const: .float 1.0
__fp0const: .float 0.0
__nueva_linea: .word 10
__tabulacion: .word 9
__matriz_fuera_de_rango: .asciiz "Matriz fuera de rango"
__lista_fuera_de_rango: .asciiz "Lista fuera de rango"
$a:  .word 0
$b:  .word 0
$c:  .word 0
.text
.data
__str_const0: .asciiz "vete\n"
.text
la $t7, __str_const0
sw $t7, __atom
lw $t6, __atom
add $t5, $zero, $t6
add $t4, $zero, $t5
add $t3, $zero, $t4
add $t2, $zero, $t3
add $t1, $zero, $t2
add $t0, $zero, $t1
li $v0, 4
add $a0, $zero, $t0
syscall
.data
__str_const1: .asciiz "que te vayas cabron\n"
.text
la $t7, __str_const1
sw $t7, __atom
lw $t6, __atom
add $t5, $zero, $t6
add $t4, $zero, $t5
add $t3, $zero, $t4
add $t2, $zero, $t3
add $t1, $zero, $t2
add $t0, $zero, $t1
li $v0, 4
add $a0, $zero, $t0
syscall
li $v0, 10
syscall
