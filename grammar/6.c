int a;
int b;
int c=0;
read(a);
while(a>0){
    b=a;
    c=0;
    while(b>0){
        c=10*c+b;
        b=b-1;
    }
    write(c);
    a=a-1;
}