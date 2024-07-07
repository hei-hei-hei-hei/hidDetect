## 题目描述

题目链接：https://pwnable.kr/play.php

Daddy, teach me how to use random value in programming!

ssh random@pwnable.kr -p2222 (pw:guest)

## 题解

看起来需要满足一系列要求，

```asm6502
0x0000000000400954 <+0>:     push   rbp                         
0x0000000000400955 <+1>:     mov    rbp,rsp                     
0x0000000000400958 <+4>:     sub    rsp,0x70                    
0x000000000040095c <+8>:     mov    DWORD PTR [rbp-0x54],edi    
0x000000000040095f <+11>:    mov    QWORD PTR [rbp-0x60],rsi    
0x0000000000400963 <+15>:    mov    QWORD PTR [rbp-0x68],rdx
```

汇编中的 rbp-0x54、rbp-0x60、rbp-0x68 保存了 `main` 函数的参数（`argc`, `argv[]`, 和 `envp[]`）

先尝试满足第一个条件

```asm6502
0x0000000000400994 <+64>:    cmp    DWORD PTR [rbp-0x54],0x64
0x0000000000400998 <+68>:    je     0x4009a4 <main+80>
0x000000000040099a <+70>:    mov    eax,0x0
0x000000000040099f <+75>:    jmp    0x400c9a <main+838>
0x00000000004009a4 <+80>:    mov    rax,QWORD PTR [rbp-0x60]
0x00000000004009a8 <+84>:    add    rax,0x208
0x00000000004009ae <+90>:    mov    rax,QWORD PTR [rax]
0x00000000004009b1 <+93>:    movzx  eax,BYTE PTR [rax]
0x00000000004009b4 <+96>:    test   al,al
0x00000000004009b6 <+98>:    je     0x4009c2 <main+110>
0x00000000004009b8 <+100>:   mov    eax,0x0
0x00000000004009bd <+105>:   jmp    0x400c9a <main+838>
```

先比较程序是否是输入100个参数，然后比较输入参数的即第 65 个字节（0x208(520)/8）是否为 `\x00`，问题来了，程序入参通过空格分割，然后如果输入 `\x00` 的话，会被跳过

新建个 py 文件

```python
# encoding: utf-8
import sys

for i in range(0, 100):
    if i == ord('A'):
        sys.stdout.buffer.write(b'\x00')
    else: 
        sys.stdout.buffer.write('{} '.format(i).encode())
```

调试下，先 b je 前面即可

```asm6502
pwndbg> set args $(python3 in.py)
pwndbg> b *0x00000000004009ae
pwndbg> run
pwndbg> s
pwndbg> x/gx $rbp-0x60
0x7fffffffe060: 0x00007fffffffe1b8
pwndbg> x/gx 0x00007fffffffe1b8
0x7fffffffe1b8: 0x00007fffffffe72a
pwndbg> x/gx 0x00007fffffffe72a
0x7fffffffe72a: 0x726f772f6674632f
pwndbg> x/100s 0x00007fffffffe72a ; 前面这几步可以用一句也可以 
; x/100s *((char **)(*(void **)($rbp-0x60)))
0x7fffffffe72a: "/ctf/work/input"
0x7fffffffe73a: "0"
0x7fffffffe73c: "1"
....
0x7fffffffe7ed: "63"
0x7fffffffe7f0: "64" ; 会发现这里 65不见了，就是输入被吞了
0x7fffffffe7f3: "66"
0x7fffffffe7f6: "67"
0x7fffffffe7f9: "68"
....
```

最终发现用 C 的 原始命令执行调用

```c
int execve(const char *pathname, char *const _Nullable argv[], 
char *const _Nullable envp[]);
```

比较方便，因为执行命令本质上就是调用这个，然后还有传入原始的 argv 和 envp，这样就不用担心手动输入，或者是因为输入的空格分割等问题导致输入读不进去的问题了

然后根据题目给的C代码照葫芦画瓢即可

先 ssh 连上环境，然后

```bash
mkdir /tmp/tari
cd /tmp/tari # 注意是不能直接 ls /tmp 目录，没权限
vi in.c # 把 exp 复制保存退出
gcc in.c
ln -s /home/input2/flag /tmp/tari/flag # 因为 input 程序的 flag 是相当路径
./a.out
# Welcome to pwnable.kr
# Let's see if you know how to give input to program
# Just give me correct inputs then you will get the flag :)
# Stage 1 clear!
# Stage 2 clear!
# Stage 3 clear!
# Stage 4 clear!
```

这时候目标会执行套接字的操作，此时在开一个 ssh 执行

```bash
python -c "print '\xde\xad\xbe\xef'" | nc localhost 8080
```

即可在刚刚的 ssh 拿到 flag