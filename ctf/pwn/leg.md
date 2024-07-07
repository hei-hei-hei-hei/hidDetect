## 题目描述

Daddy told me I should study arm. But I prefer to study my leg!

Download : http://pwnable.kr/bin/leg.c Download : http://pwnable.kr/bin/leg.asm

ssh leg@pwnable.kr -p2222 (pw:guest)

## 题解

观察代码

```python
#include <stdio.h>
#include <fcntl.h>
int key1(){
	asm("mov r3, pc\n");
}
int key2(){
	asm(
	"push	{r6}\n"
	"add	r6, pc, $1\n"
	"bx	r6\n"
	".code   16\n"
	"mov	r3, pc\n"
	"add	r3, $0x4\n"
	"push	{r3}\n"
	"pop	{pc}\n"
	".code	32\n"
	"pop	{r6}\n"
	);
}
int key3(){
	asm("mov r3, lr\n");
}
int main(){
	int key=0;
	printf("Daddy has very strong arm! : ");
	scanf("%d", &key);
	if( (key1()+key2()+key3()) == key ){
		printf("Congratz!\n");
		int fd = open("flag", O_RDONLY);
		char buf[100];
		int r = read(fd, buf, 100);
		write(0, buf, r);
	}
	else{
		printf("I have strong leg :P\n");
	}
	return 0;
}
```

通过获取 key1() key2() key3() 返回值相加结果即可获取 flag

### main 汇编

这是一段 ARM 架构下的汇编代码，用于定义一个 `main` 函数的流程。下面是对这些指令的解释：

* `push {r4, r11, lr}`：

  将寄存器 `r4`、`r11`（帧指针）和链接寄存器 `lr`（返回地址）压入栈中。这在函数开始时保存了重要的寄存器。

* `add r11, sp, #8`：

  设置帧指针 `r11`（fp）为当前栈指针 `sp` 加 8。这是新的帧基址。

* `sub sp, sp, #12`：

  将栈指针 `sp` 减去 12，为局部变量分配空间。

* `mov r3, #0`：

  将立即数 0 移动到寄存器 `r3`。

* `str r3, [r11, #-16]`：

  将 `r3`（即 0）存储到帧指针 `r11` 偏移 -16 的位置，可能用于初始化一个局部变量。

* `ldr r0, [pc, #104]; 0x8dc0 <main+132>`：

  从程序计数器 `pc` 偏移 104 的地方加载数据到 `r0`，这可能是一个字符串或其他数据。

* `bl 0xfb6c <printf>`：

  调用 `printf` 函数，参数是 `r0` 寄存器的内容。

* `sub r3, r11, #16`：

  计算 `r11` 减 16 的结果，并将其存储到 `r3`。

* `ldr r0, [pc, #96]; 0x8dc4 <main+136>`：

  从程序计数器 `pc` 偏移 96 的地方加载数据到 `r0`。

* `mov r1, r3`：

  将 `r3` 的值移动到 `r1`。

* `bl 0xfbd8 <__isoc99_scanf>`：

  调用 `__isoc99_scanf` 函数，参数是 `r0` 和 `r1`。

可以发现，key1() key2() key3() 函数调用的返回值通过 `r0` 寄存器存储，`r0` 的值都和 pc（程序计数器）相关，然后在 arm 中有个特性：当一个指令正在执行时，`**pc**` 实际上已经预先读取了之后的两条指令，即当前指令地址加上 8 字节，也就是说

1. key1: `0x00008cdc + 8 = 0x00008ce4`

```asm6502
0x00008cdc <+8>:	mov	r3, pc
```

2. key2: `0x00008d04 + 8 + 4 = 0x00008d0c`

```asm6502
0x00008d04 <+20>:	mov	r3, pc
0x00008d06 <+22>:	adds	r3, #4
```

3. key3: `lr` 为函数返回地址 `0x00008d80`

```asm6502
0x00008d7c <+64>:	bl	0x8d20 <key3>
0x00008d80 <+68>:	mov	r3, r0
```

加起来十进制就是 `108400`

```asm6502
/ $ ./leg
Daddy has very strong arm! : 108400
Congratz!
My daddy has a lot of ARMv5te muscle!
```