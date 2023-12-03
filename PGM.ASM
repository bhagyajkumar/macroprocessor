copy start 1000
testm macro &a,&b,&c
mov &a,&b
mov &b,&c
mend
mov AX,DX
mov CX,BX
addnum macro &a,&b,&c
mov &a,&b
alpha resw 1
beta resw 1
mend
addnum 1,2,3
gamma resw 1
