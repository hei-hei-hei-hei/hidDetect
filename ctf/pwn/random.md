## 题目描述

Daddy, teach me how to use random value in programming!

ssh random@pwnable.kr -p2222 (pw:guest)

## 题解

连接服务器，获取远吗如下：

```c
#include <stdio.h>
int main(){        
  unsigned int random;        
  random = rand();        // random value!        
  unsigned int key=0;        
  scanf("%d", &key);        
  if( (key ^ random) == 0xdeadbeef ){                
    printf("Good!\n");                
    system("/bin/cat flag");                
    return 0;        
  }        
  printf("Wrong, maybe you should try 2^32 cases.\n");        
  return 0;
}
```

rand函数是固定种子生成的，不同机器种子不一样。所以这个程序在一台机器上运行每次rand的结果都为固定的一个值。通过调试看这太服务器rand的值是多少。

```shell
(gdb) disassDump of assembler code for function main:   0x00000000004005f4 <+0>: push   %rbp   0x00000000004005f5 <+1>: mov    %rsp,%rbp=> 0x00000000004005f8 <+4>: sub    $0x10,%rsp   0x00000000004005fc <+8>: mov    $0x0,%eax   0x0000000000400601 <+13>:    callq  0x400500 <rand@plt>   0x0000000000400606 <+18>:    mov    %eax,-0x4(%rbp) End of assembler dump.(gdb) b *0x0000000000400606Breakpoint 2 at 0x400606(gdb) cContinuing.Breakpoint 2, 0x0000000000400606 in main ()(gdb) print $eax$1 = 1804289383
```

所以rand固定的值为*1804289383*

```shell
random@ubuntu:~$ pythonPython 2.7.12 (default, Jul  1 2016, 15:12:24) [GCC 5.4.0 20160609] on linux2Type "help", "copyright", "credits" or "license" for more information.>>> from pwn import *>>> payload = str(1804289383 ^ 0xdeadbeef)>>> io = process("./random")[x] Starting local process './random'[+] Starting local process './random': Done>>> io.sendline(payload)>>> io.recv()[*] Process './random' stopped with exit code 0'Good!\nMommy, I thought libc random is unpredictable...\n'>>>
```