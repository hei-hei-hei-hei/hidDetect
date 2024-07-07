# rememberornot

观察main函数，发现只要计算100道题的答案即可获得flag

```python
from pwn import *
p = remote("10.102.32.142",38108)
p.recvuntil(b':')
for i in range(100):
    p.recvuntil(b':')
    expression = p.recvline()
    Expression = expression[:-3]
    print(Expression)
    ans = eval(Expression)
    Ans = str(ans)
    print(ans)
    p.sendline(Ans)
p.interactive()
```

利用python内置的eval函数即可进行表达式的运算

flag: `HCTF{Y0U_RE@l1Y_REMEMbER_Y0uR_mA7H968ce06ba4d9}`
