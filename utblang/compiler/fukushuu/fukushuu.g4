grammar fukushuu;

operaciones: a=opAnd (operacion=OLOGICO b=opAnd)*;

opAnd: a=igualdad (operacion=YLOGICO b=igualdad)*;

igualdad:	a=desigualdad ( operacion=(IGUAL_QUE|DESIGUALDAD) b=desigualdad)*;

desigualdad:	a=sumr ( operacion=(MENOR_QUE|MENOR_IGUAL_QUE|MAYOR_QUE|MAYOR_IGUAL_QUE) b=sumr)*;

sumr:	a=op_div (operacion=(SUM|RES) b=op_div)*;

op_div:
		a=conversion
		(operacion=(MUL|DIV|MODULO) b=conversion)*
		;

conversion: op=(NEGACION|CONVERSION)? a=atom ('a' m=(TENTERO|TREAL|TBOOLEANO|TCADENA))?;

obtenerValor:
			(
			id3=ID
			|id1=ID EN_LA_POSICION indice=operaciones
			|id2=ID EN_LA_COORDENADA '(' fila=operaciones ',' columna=operaciones ')'
			 );

atom:	(
		(SUM|r=RES)?i=INT
		|(SUM|r=RES)? f=FLOAT
		|(SUM|r=RES)? var=obtenerValor
		|s=STRING
		| (SUM|r=RES)? '(' op=operaciones ')'
		| b=BOOL
		);

mostrar	:	most=MOSTRAR op=operaciones;

asignacionLista
	:	CAMBIAR_VALOR_A lista=ID EN_LA_POSICION indice=operaciones err=POR op=operaciones;

asignacionMatriz
	:	CAMBIAR_VALOR_A matriz=ID EN_LA_COORDENADA '(' fila=operaciones ',' columna=operaciones ')' err=POR op=operaciones;

asignacionID
	:	CAMBIAR_VALOR_A nombre=ID err=POR op=operaciones;

asignacion
	:	asignacionLista|asignacionMatriz|asignacionID;

para_cada_elemento:	PARA temp=ID ('en' nombre=ID
		|'en_rango_de' a=operaciones 'hasta' b=operaciones) DPUNTOS com=dummy_comandos FINPARA;

agregar_elemento_lista: AGREGAR_A nombre=ID AGREGAR_LISTA_OP op=operaciones;

leer: LEER nombre=ID ((EN_LA_COORDENADA '(' fila=operaciones ',' columna=operaciones ')')|(EN_LA_POSICION indice=operaciones))?;

comandos:	leer|mostrar|mientras|si|para_cada_elemento|asignacion|agregar_elemento_lista;

sinotonces
	:	SINO ENTONCES comandos+;

dummy_comandos: comandos+;

si	:	err=SI op=operaciones ENTONCES com=dummy_comandos el=sinotonces? FINSI;

mientras:	err=MIENTRAS op=operaciones DPUNTOS com=dummy_comandos FINMIENTRAS;

flujo	:	INICIO_FLUJO comandos+ FIN_FLUJO;

declaracion
	:	TIPO
	(tipo=TENTERO
	|tipo=TREAL
	|tipo=TBOOLEANO
	|tipo=TCADENA
	|tipo=LISTA_ENTERO NOMBRE
	|tipo=LISTA_REAL NOMBRE
	|tipo=LISTA_BOOL NOMBRE
	|tipo=LISTA_CADENA NOMBRE
	|tipo=MATRIZ_ENTERO NOMBRE
	|tipo=MATRIZ_REAL NOMBRE
	|tipo=MATRIZ_BOOL NOMBRE
	|tipo=MATRIZ_CADENA NOMBRE) nombre=ID
	(filas=INT 'x' columnas=INT)?;

variables
	:	INICIO_VARIABLES declaracion+ FIN_VARIABLES;

nombrePrograma
	:	NOMBRE_PROGRAMA nombre=ID_PROGRAMA;

inicio	:	nombrePrograma variables flujo;

start_rule: inicio;

TBOOLEANO: 'booleano';

TCADENA: 'cadena';

LEER: 'leer';

COMENTARIOS: ('nota:' ('a'..'z'|'A'..'Z')* '\n') -> skip;

AGREGAR_LISTA_OP: '<-';

AGREGAR_A: 'agregar_a';

MODULO	:	'%';

IGUAL_QUE:	'es_igual_que';

MAYOR_QUE
	:	'es_mayor_que';
	
MENOR_QUE
	:	'es_menor_que';
	
MAYOR_IGUAL_QUE
	:	'es_mayor_o_igual_que';

MENOR_IGUAL_QUE
	:	'es_menor_o_igual_que';

DESIGUALDAD
	:	'no_es_igual_a';

YLOGICO	:	'y';

OLOGICO	:	'o';

NEGACION:	'no';

CONVERSION
	:	'convertir_a';
 
PARA	:	'para_cada';

FINPARA	:	'fin_para';
 
DPUNTOS:	':';
 
MIENTRAS:	'mientras';
  
FINMIENTRAS:	'fin_mientras';
 
SI	:	'si';

ENTONCES:	'entonces';

FINSI	:	'fin_si'; 
 
SINO	:	'sino';

TAMANO	:	'de_tamano';

NOMBRE	:	'nombre';

LISTA_ENTERO
	:	'lista_de_entero';
	
LISTA_REAL	:	'lista_de_real';

LISTA_BOOL
	:	'lista_de_booleano';
	
LISTA_CADENA
	:	'lista_de_cadena';
	
MATRIZ_ENTERO
	:	'matriz_de_entero';
	
MATRIZ_REAL
	:	'matriz_de_real';
	
MATRIZ_CADENA	: 'matriz_de_cadena';

MATRIZ_BOOL
	:	'matriz_de_booleano';

BOOL	:	'verdadero'|'falso';

EN_LA_POSICION
	:	'en_la_posicion';
	
EN_LA_COORDENADA
	:	'en_la_coordenada';

POR	:	'por';

CAMBIAR_VALOR_A
	:	'cambiar_valor_a';

NOMBRE_PROGRAMA
	:	'nombre_programa';

SUM	:	'+';

RES	:	'-';

MUL	:	'*';

DIV	:	'/';

IGUAL	:	'=';

TREAL	:	'real';

TENTERO	:	'entero';

TIPO	:	'tipo';

MOSTRAR	:	'mostrar_en_pantalla';

INICIO_VARIABLES
	:	'variables';
	
FIN_VARIABLES
	:	'fin_variables';

INICIO_FLUJO
	:	'flujo';
	
FIN_FLUJO
	:	'fin_flujo';

INT :	'0'..'9'+
    ;

ID_PROGRAMA
	:	('a'..'z'|'A'..'Z'|'0'..'9'|'_')+;

ID  :	'$' ('a'..'z'|'A'..'Z'|'_') ('a'..'z'|'A'..'Z'|'0'..'9'|'_')*
    ;

FLOAT
    :   ('0'..'9')+ '.' ('0'..'9')*;

WS  :   ( ' '
        | '\t'
        | '\r'
        | '\n'
        ) -> skip
    ;

STRING
    :  '"' ('a'..'z'|'A'..'Z'|'0'..'9'|'_'|' '|','|'.'|'\n'|'\t'|'\\' [btnfr"'\\]|'['|']'|';'|':'|'$')* '"'
    ;
