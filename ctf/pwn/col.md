## 题目描述

Daddy told me about cool MD5 hash collision today.
I wanna do something like that too!

ssh col@pwnable.kr -p2222 (pw:guest)



## 题解

通过ssh登录服务器，查看提供的源代码col.c

```c
#include <stdio.h>
#include <string.h>
unsigned long hashcode = 0x21DD09EC;
unsigned long check_password(const char* p){
	int* ip = (int*)p;
	int i;
	int res=0;
	for(i=0; i<5; i++){
		res += ip[i];
	}
	return res;
}

int main(int argc, char* argv[]){
	if(argc<2){
		printf("usage : %s [passcode]\n", argv[0]);
		return 0;
	}
	if(strlen(argv[1]) != 20){
		printf("passcode length should be 20 bytes\n");
		return 0;
	}

	if(hashcode == check_password( argv[1] )){
		system("/bin/cat flag");
		return 0;
	}
	else
		printf("wrong passcode.\n");
	return 0;
}
```

通过代码，我们知道，要求传入一个string参数，string的长度要为20字节，并将string划分为五组，每组表示一个int，相加得到的和要为hashcode，也就是0x21DD09EC，因此考虑将string分成四组0x01010101和一组0x1DD905E8，借助python脚本实现：

```python
 from pwn import *
 payload = p32(0x1dd905e8) + p32(0x01010101) * 4
 io = process(["./col", payload])[x] Starting local process './col'[+] Starting local process './col': Done
 io.recv()[*] Process './col'
```

得到结果