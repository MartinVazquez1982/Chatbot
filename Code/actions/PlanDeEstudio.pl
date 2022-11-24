%consult('C:/Users/s7tan/OneDrive/Desktop/Universidad/Programacion Exploratoria/Prolog/PlanDeEstudio.pl').%

%Materias es_una_materia(codigo, nombre, cuatrimestre, a�o)%

%Primer a�o - Primer Cuatrimestre%
es_una_materia(6111,'introduccion a la programacion 1',1,1).
es_una_materia(6112,'analisis matematico 1',1,1).
es_una_materia(6113,'algebra 1',1,1).
es_una_materia(6114,'quimica',1,1).

%Primero a�o - Segundo Cuatrimestre%
es_una_materia(6121,'ciencias de la computacion 1',2,1).
es_una_materia(6122,'introduccion a la programacion 2',2,1).
es_una_materia(6123,'algebra lineal',2,1).
es_una_materia(6124,'fisica general',2,1).
es_una_materia(6125,'matematica discreta',2,1).

%Segundo a�o - Primer Cuatrimestre%
es_una_materia(6211,'ciencias de la computacion 2',1,2).
es_una_materia(6212,'analisis y disenio de algoritmos 1',1,2).
es_una_materia(6213,'introduccion a la arquitectura de sistemas',1,2).
es_una_materia(6214,'analisis matematico 2',1,2).
es_una_materia(6215,'electricidad y magnetismo',1,2).

%Segundo a�o - Segundo Cuatrimestre%
es_una_materia(6221,'analisis y disenio de algoritmos 2',2,2).
es_una_materia(6222,'comunicacion de datos 1',2,2).
es_una_materia(6223,'probabilidad y estadistica',2,2).
es_una_materia(6224,'electronica digital',2,2).

%Tercer a�o - Primer Cuatrimestre%
es_una_materia(6311,'programacion orientada a objetos',1,3).
es_una_materia(6312,'estructuras de almacenamiento de datos',1,3).
es_una_materia(6313,'metodologias de desarrollo de software',1,3).
es_una_materia(6314,'arquitectura de computadoras',1,3).

%Tercer a�o - Segundo Cuatrimestre%
es_una_materia(6321,'programacion exploratoria',2,3).
es_una_materia(6322,'base de datos',2,3).
es_una_materia(6323,'lenguajes de programacion',2,3).
es_una_materia(6324,'sistemas operativos',2,3).
es_una_materia(6325,'investigacion operativa',2,3).

%Cuarto a�o - Primer Cuatrimestre%
es_una_materia(6411,'arquitectura de computadoras y tecnicas digitales',1,4).
es_una_materia(6412,'teoria de la informacion',1,4).
es_una_materia(6413,'comunicacion de datos 2',1,4).
es_una_materia(6414,'introduccion al calculo diferencial e integral',1,4).

%Cuarto a�o - Segundo Cuatrimestre%
es_una_materia(6421,'disenio de sistemas de software',2,4).
es_una_materia(6422,'disenio de compiladores',2,4).

%Quinto a�o - Primer Cuatrimestre%
es_una_materia(6511,'ingenieria de software',1,5).


%Correlativas%
%es_correlativa(materias correlativas a, esta materia)%

es_correlativa([],6111).
es_correlativa([],6112).
es_correlativa([],6113).
es_correlativa([],6114).
es_correlativa([6111],6122).
es_correlativa([6113],6123).
es_correlativa([6112],6124).
es_correlativa([6113],6125).
es_correlativa([6121,6122,6125],6211).
es_correlativa([6121,6122,6125],6212).
es_correlativa([6122],6213).
es_correlativa([6112],6214).
es_correlativa([6124],6215).
es_correlativa([6211,6212],6221).
es_correlativa([6213],6222).
es_correlativa([6214,6123,6125],6223).
es_correlativa([6215],6224).
es_correlativa([6221],6311).
es_correlativa([6221,6223],6312).
es_correlativa([6221],6313).
es_correlativa([6213,6224],6314).
es_correlativa([6221],6321).
es_correlativa([6312,6313],6322).
es_correlativa([6311],6323).
es_correlativa([6312,6314],6324).
es_correlativa([6214,6223],6325).
es_correlativa([6314],6411).
es_correlativa([6212,6222,6223],6412).
es_correlativa([6222,6324],6413).
es_correlativa([6214],6414).
es_correlativa([6311,6322,6324],6421).
es_correlativa([6323],6422).
es_correlativa([6421],6511).

%Materias Aprobadas%

aprobada(6111).
aprobada(6112).
aprobada(6113).
aprobada(6114).
aprobada(6121).
aprobada(6122).
aprobada(6123).
aprobada(6124).
aprobada(6125).
aprobada(6211).
aprobada(6212).
aprobada(6213).
aprobada(6214).
aprobada(6215).
aprobada(6221).
aprobada(6222).
aprobada(6223).
aprobada(6224).
aprobada(6311).
aprobada(6312).
aprobada(6313).
aprobada(6314).

%Materias que curso%

cursando(6321).
cursando(6322).
cursando(6323).
cursando(6324).
cursando(6325).

%Reglas%
%Ejercicio 1 - Materias de un Curso%

materias_de(X) :- write('Materias del curso:'),writeln(X),es_una_materia(_,Y,_,X),writeln(Y),nl,fail;nl.

%Ejercicio 2 - Materias de una sola correlativa%

materias_con_correlativa(L) :- es_correlativa(Y,X),length(Y,L),es_una_materia(X,N,_,_),writeln(''),write('Para hacer: '),write(N),write(' necesitas '),mostrar_correlativas(Y),writeln(" "),nl,fail;nl.

%Plan de Estudio%

plan_is :- writeln('Plan Ingenieria en Sistemas: '),es_una_materia(C,X,Y,Z),writeln(''),write('Curso: '),write(Z),write(' Cua: '),write(Y),write( ' Nombre: '),write(X),write(' Correlativas: '),es_correlativa(L,C),mostrar_correlativas(L),nl,fail;nl.

mostrar_correlativas(X) :- X=[Z|W],es_una_materia(Z,N,_,_),write(N),not(length(W,0))->write(' - '),mostrar_correlativas(W),nl,fail.

%materiasAprobadas%

materias_aprobadas(Lista) :- findall(Nom,(es_una_materia(Cod,Nom,_,_),aprobada(Cod)),Lista).

%materiasCursando%

materias_que_curso(Lista) :- findall(Nom,(es_una_materia(Cod,Nom,_,_),cursando(Cod)),Lista).

%materiasSinCursar%

materias_sin_cursar(Lista) :- findall(Nom,(es_una_materia(Cod,Nom,_,_),not(aprobada(Cod);cursando(Cod))),Lista).

%materiaAprobada%

materia_aprobada(Nom) :- es_una_materia(Cod,Nom,_,_),aprobada(Cod).

%materia cursando%

materia_en_cursada(Nom) :- es_una_materia(Cod,Nom,_,_),cursando(Cod).

%materia sin cursar%

materia_sin_cursar(Nom) :- es_una_materia(Cod,Nom,_,_),not(aprobada(Cod);cursando(Cod)).