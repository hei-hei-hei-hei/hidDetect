## 什么是.ino文件



.ino文件是Arduino开发平台中使用的文件扩展名。Arduino是一种开源的电子原型平台，用于制作各种交互式项目。.ino文件包含了Arduino代码，它使用基于C和C++的语法。当你在Arduino开发环境中创建一个新的项目时，它会为你生成一个以.ino为扩展名的主文件。

.ino文件包含了两个主要的函数：setup()和loop()。setup()函数在程序开始时运行一次，用于初始化设置，例如配置引脚模式和初始化变量。loop()函数会一直运行，不断重复执行，用于实现主要的程序逻辑。

在Arduino开发环境中，你可以编写和编辑.ino文件，并将其上传到Arduino开发板上运行。Arduino开发环境提供了许多库和函数，使开发者能够轻松地与各种硬件组件进行交互，例如传感器、执行器和通信模块。

总之，.ino文件是Arduino开发平台中用于编写Arduino代码的文件扩展名。





## Arduino开发平台

[【Arduino百问】\]听说用Arduino的人越来越少了？esp32和Arduino什么关系？不试试其他Arduino开发板？_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1LK4y1S7kn/?spm_id_from=333.337.search-card.all.click&vd_source=12529e4229ce118f01d5af970500b584)

[ATtiny85漏洞利用框架HID测试分析](https://www.freebuf.com/articles/system/206024.html)



Arduino开发平台是一个开源的电子原型平台，旨在使电子设备的开发变得更加简单和易于理解。它包括硬件和软件组件。

Arduino硬件是一系列基于微控制器的开发板，其中包含了处理器、输入输出引脚和其他电子组件。这些开发板可以连接到电脑上，通过Arduino开发环境进行编程和控制。

Arduino软件开发环境是一个集成开发环境（IDE），提供了编写、编译和上传代码到Arduino开发板的工具。它基于C和C++语言，并提供了一组库和函数，使开发者能够轻松地与各种硬件组件进行交互。Arduino开发环境还包括一个串行监视器，用于与开发板进行通信和调试。

使用Arduino开发平台，开发者可以快速原型化各种项目，例如智能家居系统、机器人、传感器应用和艺术装置等。它的设计理念是简单易用，使得即使对于初学者来说也能够快速入门，并且对于有经验的开发者来说也具有足够的灵活性和可扩展性。

Arduino社区非常活跃，有大量的开源项目和资源可用，开发者可以分享和获取各种代码和教程。这使得Arduino成为一个受欢迎的平台，用于学习电子和嵌入式系统开发，以及构建各种创意和实用的应用程序。



## Ducky Script

普通的U盘并不支持直接执行Ducky Script脚本，因为普通的U盘没有内置的HID模式（Human Interface Device）来模拟键盘行为。

要在普通的U盘上执行Ducky Script脚本，您需要进行一些额外的步骤：

\1. 从互联网上获取一个名为"duckencoder"的开源工具，它可以将Ducky Script脚本转换为可执行的可执行文件。

\2. 将您编写的Ducky Script脚本保存为文本文件（例如`script.txt`）。

\3. 打开命令提示符（Windows系统）或终端（Mac或Linux系统）。

\4. 使用duckencoder工具将Ducky Script脚本转换为可执行文件。运行以下命令：

\```shell
duckencoder -i script.txt -o inject.bin
\```

此命令将使用输入的Ducky Script脚本文件(`script.txt`)并生成输出文件(`inject.bin`)，该文件包含用于模拟键盘行为的二进制数据。

5. 将生成的`inject.bin`文件复制到普通的U盘中。

6. 断开U盘，并将其插入您希望执行脚本的目标计算机的USB端口。

7. 脚本将自动执行，模拟键盘行为并按照脚本文件中的命令执行操作。

请记住，在使用Ducky Script脚本执行操作时，您必须遵守适用的法律法规和道德准则，并仅在合法的和授权的测试环境中使用。







## 其他资料

##### [极客DIY：打造你的专属黑客U盘](https://www.cnblogs.com/k1two2/p/4897581.html)

[flashsploit GitHub地址](https://github.com/thewhiteh4t/flashsploit/tree/master)

[duckhunt GitHub地址](https://github.com/pmsosa/duckhunt)

[duckencoder.py GitHub地址](https://github.com/mame82/duckencoder.py) 