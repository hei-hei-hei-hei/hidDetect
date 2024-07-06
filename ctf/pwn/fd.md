## 题目描述

Mommy! what is a file descriptor in Linux?

* try to play the wargame your self but if you are ABSOLUTE beginner, follow this tutorial link:
https://youtu.be/971eZhMHQQw

ssh fd@pwnable.kr -p2222 (pw:guest)

## 题解

根据描述，使用ssh登录，密码为guest

<img src="/Users/stephend/Library/Application Support/typora-user-images/image-20240706102207307.png" alt="image-20240706102207307" style="zoom:50%;" />

查看fd.c源代码

<img src="/Users/stephend/Library/Application Support/typora-user-images/image-20240706102302188.png" alt="image-20240706102302188" style="zoom:50%;" />

因此只要atoi(argv[1]) == 0x1234即可，于是执行 ./fd 4660，再输入LETMEWIN即可

<img src="/Users/stephend/Library/Application Support/typora-user-images/image-20240706102502853.png" alt="image-20240706102502853" style="zoom:50%;" />