<h1>DuckHunter</h1>
<h3>Prevent RubberDucky (or other keystroke injection) attacks</h3>
<h3>Try Out the new setup GUI it helps you to setup the software and we have just released a new feature that allows you to run the script every time your computer starts automatically<h3>




![](https://raw.githubusercontent.com/kai9987kai/kai9987kai.github.io/master/screenshot.PNG)


**Read this program's postmortem at my [blog](http://konukoii.com/blog/2016/10/26/duckhunting-stopping-automated-keystroke-injection-attacks/)**
<h3>Intro</h3>
[Rubberduckies](https://hakshop.myshopify.com/products/usb-rubber-ducky-deluxe) are small usb devices that pretend to be usb keyboards and can type on their own at very high speeds. Because most -if not all- OS trust keyboards automatically, it is hard to protect oneself from these attacks.

**DuckHunt** is a small efficient script that acts as a daemon consistently monitoring your keyboard usage (right now, speed and selected window) that can catch and prevent a rubber ducky attack. (Technically it helps prevent any type of automated keystroke injection attack, so things like Mousejack injections are also covered.)

![](http://konukoii.com/blog/wp-content/uploads/2016/10/duckhunt-screenshot.png)

<h3>Features</h3>

**Protection Policy**
 - **Paranoid:** When an attack is detected, keyboard input is disallowed until a password is input. Attack will also be logged.
 - **Normal:** When an attack is detected, keyboard input will temporarily be disallowed. (After it is deemed that the treat is over, keyboard input will be allowed again). Attack will also be logged.
 - **Sneaky:** When an attacks is detected, a few keys will be dropped (enough to break any attack, make it look as if the attacker messed up.) Attack will also be logged.
 - **LogOnly:** When an attack is detected, simply log the attack and in no way stop it. 

**Extras**
 - Program Blacklist: If there are specific programs you neve use (cmd, powershell). Consider interactions with them as highly suspecious and take action based on the protection policy.
 - Support for AutoType software (eg. KeePass, LastPass, Breevy)
 
<h3>Setup</h3>

**Regular users**:
- Choose and download one of the two options that best suits you:
  -  Opt #1: [Normal Protection w/ Program Blacklisting for Commandline and Powershell](https://github.com/pmsosa/duckhunt/raw/master/builds/duckhunt.0.9.blacklist.exe)
  -  Opt #2: [Normal Protection (w/o any blacklisting)](https://github.com/pmsosa/duckhunt/raw/master/builds/duckhunt.0.9.exe)
- Now, copy the .exe above to the startup menu.
  -  In Windows XP,Vista,7 : This folder should be accessible from your Start Menu
  -  In Windows 10: Open a directory explorer an go to "%appdata%\Microsoft\Windows\Start Menu\Programs\Startup" (copy paste it in without the quotation marks).


**Advanced Users**
 - Keep Reading...
 - Feel Free to contact me, add issues, fork, and get involved with this project :). Together we can make a stronger tool!

<h3>Requirements</h3>
 
- [PyWin32](http://starship.python.net/~skippy/win32/Downloads.html)
- [PyHook](https://sourceforge.net/projects/pyhook/)
- [Py2Exe](http://py2exe.org/)
- [webbrowser](https://docs.python.org/2/library/webbrowser.html)




<h3>Advanced Setup</h3>

- Step 1. Customize duckhunt.conf variables to your desire
  -  You can customize the password, speed threshold, privacy, etc.
- Step 2. Turn the duckhunt-configurable**.py** to a duckhunt-configurable**.pyw** so that the console doesn't show up when you run the program
- Step 3. (opt) Use Py2Exe to create an executable.
- Step 4. Run the program. You are now protected from RubberDuckies!

<h3>TODO</h3>

- More monitoring features: 
 - Add OSX & Linux support!
 - Look for certain patterns (eg. "GUI D, GUI R, cmd, ENTER")

 
 <h1>Happy Hunting!</h1>
 
![](http://konukoii.com/blog/wp-content/uploads/2016/10/duck-hunt.jpg)





<h1>主要看bak文件，已经将注释中文化了</h1>

[Python tkinter教程-01：创建窗口_python创建一个400*500的大小主窗口-CSDN博客](https://blog.csdn.net/weixin_42725873/article/details/105622392)

[pywin32库 : Python 操作 windows 系统 API_python win32api-CSDN博客](https://blog.csdn.net/freeking101/article/details/88231952)

## 运行

需安装swig

[Python---PyHook3安装 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/505983312#:~:text=Python---PyHook3安装 1 1.首先安装wheel依赖库 2 下载好将文件解压至任意文件夹，记住swigwin.exe 所在目录，配置 环境变量 ；,14.0 (如果本机有则忽略此步骤） 4 下载好后双击VisualCppBuildTools_Full.exe 默认安装即可。 5 4. 最后安装pyhook3)



## 模拟



![image-20240126140159610](解析.assets/image-20240126140159610.png)

输入脚本

```python
import pyautogui
import time

# 延时几秒，确保将焦点切换到命令行窗口（cmd）
time.sleep(3)

# 输入文本
text = "hello world"


# 循环遍历每个字符并模拟按键输入
for char in text:
    pyautogui.typewrite(char)
    time.sleep(0.1)

# 模拟按下回车键
pyautogui.press('enter')

```







​     ![image-20240126143957004](解析.assets/image-20240126143957004.png)





点击start后：

![image-20240126144420426](解析.assets/image-20240126144420426.png)

点击关闭窗口则命令行可见键入的事件





控制效果：Paranoid模式

![image-20240126145942303](解析.assets/image-20240126145942303.png)



![image-20240126150017468](解析.assets/image-20240126150017468.png)



## 其他

### dir_path = os.path.dirname(os.path.realpath(__file__))



在Python中，`os.path.realpath(__file__)` 和 `os.path.dirname()` 是两个与文件路径处理相关的函数。

1. **os.path.realpath(\*file\*)**：
   - 这个函数接收一个参数 `_file_`，在当前上下文中，`__file__` 是一个特殊变量，它代表了当前执行的 Python 脚本或模块的绝对路径。调用 `os.path.realpath(__file__)` 的目的是获取该脚本的“真实”或解析后的绝对路径。这个函数会解决所有符号链接（symlinks）并扩展相对路径，确保返回的是一个没有引用任何别名或相对路径的完整路径。
2. **os.path.dirname(path)**：
   - 这个函数用于从给定的 `path` 中提取目录部分，即去掉最后的文件名或者最后一级目录名，只留下路径本身。所以当它作用于 `os.path.realpath(__file__)` 返回的结果时，会得到包含当前执行脚本或模块的直接父目录的路径。

因此，组合起来：

```
python

dir_path = os.path.dirname(os.path.realpath(__file__))
```

这条语句的作用是获取当前执行脚本所在的目录的实际绝对路径。这对于在脚本中需要引用同一目录下其他文件或构建相对于脚本所在位置的路径等情况非常有用。
