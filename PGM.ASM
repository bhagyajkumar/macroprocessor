copy start 1000
testm macro &a,&b,&c
label$ mov &a,&b,&c
mov &c,&b
mov AX,DX
mov CX,BX
mend
addnum macro &a,&b,&c
mov &a,&b,&c
alpha resw 1
beta resw 1
mend
addnum 4,5,6
testm 1,2,3
testm ax,bx,cx
testm as,as,as
gamma resw 1
end
