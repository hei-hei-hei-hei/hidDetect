# signin

题面：

附件为一段文本：

```
WzEwNCwgOTksIDExNiwgMTAyLCAxMjMsIDY2LCA5NywgMTE1LCAxMDEsIDk1LCA3MCwgNjQsIDEwOSwgMTA1LCA0OSwgMTIxLCA5NSwgNTIsIDExNCwgMTAxLCA5NSwgODYsIDk3LCAxMTQsIDEwNSwgNDgsIDExNywgMTE1LCAxMjVd
```

题解：

base64解码后得到：

```
[104, 99, 116, 102, 123, 66, 97, 115, 101, 95, 70, 64, 109, 105, 49, 121, 95, 52, 114, 101, 95, 86, 97, 114, 105, 48, 117, 115, 125]
```

对数字进行分析，可以看出这是ASCII码，编写Python脚本：

```python
ascii_list = [104, 99, 116, 102, 123, 66, 97, 115, 101, 95, 70, 64, 109, 105, 49, 121, 95, 52, 114, 101, 95, 86, 97, 114, 105, 48, 117, 115, 125]
 
# 将ASCII码转换为字符
result = ''.join(chr(num) for num in ascii_list)
 
print(result)
```

可以得到：`hctf{Base_F@m1y_4re_Vari0us}`
