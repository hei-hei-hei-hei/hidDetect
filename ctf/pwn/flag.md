## 题目描述

Papa brought me a packed present! let's open it.

Download : http://pwnable.kr/bin/flag

This is reversing task. all you need is binary

## 题解

bin是经过upx加壳的，直接用upx脱壳

```shell
./upx -d ../flag
```

调试得到flag

```shell
[-------------------------------------code-------------------------------------]   0x40118b <main+39>:  mov    rax,QWORD PTR [rbp-0x8]   0x40118f <main+43>:  mov    rsi,rdx   0x401192 <main+46>:  mov    rdi,rax=> 0x401195 <main+49>:  call   0x400320   0x40119a <main+54>:  mov    eax,0x0   0x40119f <main+59>:  leave     0x4011a0 <main+60>:  ret       0x4011a1:    nopGuessed arguments:arg[0]: 0x6c96b0 --> 0x0 arg[1]: 0x496628 ("UPX...? sounds like a delivery service :)")arg[2]: 0x496628 ("UPX...? sounds like a delivery service :)")[------------------------------------stack-------------------------------------]0000| 0x7fffffffe510 --> 0x401a50 (<__libc_csu_init>:   push   r14)0008| 0x7fffffffe518 --> 0x6c96b0 --> 0x0 0016| 0x7fffffffe520 --> 0x0 0024| 0x7fffffffe528 --> 0x401344 (<__libc_start_main+404>: mov    edi,eax)0032| 0x7fffffffe530 --> 0x0 0040| 0x7fffffffe538 --> 0x100000000 0048| 0x7fffffffe540 --> 0x7fffffffe618 --> 0x7fffffffe852 ("/home/user/pwn/pwnkr/4/flag")0056| 0x7fffffffe548 --> 0x401164 (<main>:  push   rbp)[------------------------------------------------------------------------------]Legend: code, data, rodata, value0x0000000000401195 in main ()gdb-peda$
```

