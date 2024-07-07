######################################################
#                   DuckHunter                       #
#                 Pedro M. Sosa                      #
# 工具，用于防止被橡胶鸭子攻击！                  #
######################################################

from ctypes import *
import pythoncom
import PyHook3
import win32clipboard
import win32ui
import os
import shutil
from time import gmtime, strftime
from sys import stdout
from tkinter import *
from tkinter import ttk
# from ttk import *
import imp
import webbrowser
import getpass


# 加载名为'duckhunt'的模块
duckhunt = imp.load_source('duckhunt', 'duckhunt.conf')
##### 备注 #####
#
# 1. 了解防护策略：
#    - Paranoid: 当检测到攻击时，锁定后续按键输入，直到正确密码输入。 (在 .conf 文件中设置密码)。攻击会被记录。
#    - Normal: 当检测到攻击时，键盘输入会被临时禁止。 (在攻击看似结束之后，键盘输入将会重新允许)。攻击会被记录。
#    - Sneaky: 当检测到攻击时，会掉几个字符（足够让攻击者出错）。攻击会被记录。
#    - LogOnly: 当检测到攻击时，仅记录攻击，不在任何方式阻止它。
#

# 2. 如何使用
#   - 修改下面可配置的用户参数。 (特别是策略和密码)
#   - 将程序转换为 .pyw 来作为无窗口脚本运行。
#   - (可选) 使用 py2exe 将其构建为 .exe
#
#################


# threshold = duckhunt.threshold  # 速度阈值
threshold = 40  # 速度阈值

size = duckhunt.size  # 历史记录数组大小
policy = duckhunt.policy.lower()  # 设定策略类型
password = duckhunt.password  # 密码（在 Paranoid 模式下使用）
allow_auto_type_software = duckhunt.allow_auto_type_software  # 允许自动输入软件（例如 KeyPass 或 LastPass）
################################################################################
pcounter = 0  # 密码计数器（如果使用密码）
speed = 0  # 当前平均按键速度
prevTime = -1  # 上一次按键的时间戳
i = 0  # 历史记录数组时间槽
intrusion = False  # 布尔标志，用于在入侵检测时被提高
history = [threshold + 1] * size  # 用于追踪平均速度的历史记录数组
randdrop = duckhunt.randdrop  # 每隔多少次掉一个字符（在 Sneaky 模式下）
prevWindow = []  # 上一个窗口名称
filename = duckhunt.filename  # 攻击记录文件名
blacklist = duckhunt.blacklist  # 程序黑名单


# 记录攻击
def log(event):
    # 定义全局变量prevWindow
    global prevWindow

    x = open(filename, "a+")  # 打开文件，文件以追加模式打开
    if prevWindow != event.WindowName:  # 如果窗口名称与上一次记录的窗口名称不同
        x.write("\n[ %s ]\n" % (event.WindowName))  # 在文件中写入窗口名称的行
        prevWindow = event.WindowName  # 更新上一次的窗口名称
    if event.Ascii > 32 and event.Ascii < 127:  # 如果字符在32到127之间（可见字符）
        x.write(chr(event.Ascii))  # 在文件中写入该字符
    else:
        x.write("[%s]" % event.Key)  # 在文件中写入按键对应的字符
        x.close()  # 关闭文件
    return  # 返回


def caught(event):
    global intrusion, policy, randdrop
    print("Quack! Quack! -- Time to go Duckhunting!")
    intrusion = True;

    # Paranoid 策略
    if (policy == "paranoid"):
        win32ui.MessageBox(
            "Someone might be trying to inject keystrokes into your computer.\nPlease check your ports or any strange programs running.\nEnter your Password to unlock keyboard.",
            "KeyInjection Detected", 4096)  # MB_SYSTEMMODAL = 4096 -- Always on top.
        return False
    # Sneaky 策略
    elif (policy == "sneaky"):
        randdrop += 1
        # 每 5 个字母掉一个
        if (randdrop == 7):
            randdrop = 0;
            return False
        else:
            return True;

    # Logging Only 策略
    elif (policy == "log"):
        log(event)
        return True;

    # Normal 策略
    log(event)
    return False


# 每次按键触发
def KeyStroke(event):
    # 定义全局变量
    global threshold, policy, password, pcounter
    global speed, prevTime, i, history, intrusion, blacklist

    # 打印事件的键
    print(event.Key)
    # 打印事件的消息
    print(event.Message)
    # 打印是否注入以及注入软件
    print("Injected", event.Injected)

    # 如果事件被注入且允许自动输入软件
    if (event.Injected != 0 and allow_auto_type_software):
        # 打印被软件注入
        print("Injected by Software")
        # 返回True
        return True

    # 如果发生了入侵并且正在使用密码保护
    # 那么锁住所有按键输入直到输入正确密码
    if (policy == "paranoid" and intrusion):
        print(event.Key)
        log(event);
        if (password[pcounter] == chr(event.Ascii)):
            pcounter += 1;
            if (pcounter == len(password)):
                win32ui.MessageBox("Correct Password!", "KeyInjection Detected",
                                   4096)  # MB_SYSTEMMODAL = 4096 -- Always on top.
                intrusion = False
                pcounter = 0
        else:
            pcounter = 0

        return False

    # 初始条件
    if (prevTime == -1):
        prevTime = event.Time;
        return True

    if (i >= len(history)): i = 0;

    # 类型Speed = NewKeyTime - OldKeyTime
    history[i] = event.Time - prevTime
    print(event.Time, "-", prevTime, "=", history[i])
    prevTime = event.Time
    speed = sum(history) / float(len(history))
    i = i + 1

    print("\rAverage Speed:", speed)

    # 黑名单
    for window in blacklist.split(","):
        if window in event.WindowName:
            return caught(event)

    # 如果速度低于阈值则认为是入侵
    if (speed < threshold):
        return caught(event)
    else:
        intrusion = False
    # 继续执行
    return True


# 创建和注册一个钩子管理器
kl = PyHook3.HookManager()
kl.KeyDown = KeyStroke

def window():
    window = Tk()  # 创建一个Tkinter窗口对象
    
    def StopScript():
        exit(0)  # 结束脚本的执行
    
    def About():
        webbrowser.open_new(r"https://github.com/pmsosa/duckhunt/blob/master/README.md")  # 在默认浏览器中打开README.md文件
    
    def WindowStarted():
        def HideWindow():
            window1.destroy()  # 关闭窗口
            def add_to_startup(file_path=dir_path):
                if file_path == "":  # 如果file_path为空，则设置为默认路径
                    file_path = os.path.dirname(os.path.realpath(__file__))  # 获取当前文件路径
                    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME  # 设置启动文件路径
                    with open(bat_path + '\\' + "duckhunt.bat", "w+") as bat_file:
                         bat_file.write(r'start "" %s''\builds\duckhunt.0.9.exe' % file_path)  # 在启动文件中写入执行脚本的命令
        
        def FullScreen():
            window1.attributes('-fullscreen', True)  # 将窗口设置为全屏模式
            window1.bind('<Escape>', lambda e: root.destroy())  # 绑定Esc按键，点击时关闭根窗口
            
        def HideTitleBar():
            window1.overrideredirect(True)  # 隐藏窗口标题栏
        
        window1 = Tk()  # 创建一个Tkinter窗口对象
        window1.title("DuckHunter")  # 设置窗口标题
        window1.iconbitmap('favicon.ico')  # 设置窗口图标
        window1.geometry('310x45')  # 设置窗口大小
        window1.resizable(False, False)  # 不允许调整窗口大小
        window1.geometry("+300+300")  # 将窗口位置设置为(300, 300)
        window1.attributes("-topmost", True)  # 窗口置顶显示
        # -----Menu----------
        menu = Menu(window1)  # 创建一个菜单对象
        new_item = Menu(menu)  # 创建一个下拉菜单对象
        new_item.add_command(label='STOP SCRIPT', command =StopScript)  # 添加"STOP SCRIPT"命令项
        new_item.add_command(label='CLOSE WINDOW', command =HideWindow)  # 添加"CLOSE WINDOW"命令项
        new_item.add_separator()  # 添加分隔线
        new_item.add_command(label='ABOUT', command =About)  # 添加"ABOUT"命令项 查看readme
        menu.add_cascade(label='Menu', menu=new_item)  # 将下拉菜单添加到菜单中
        # ----button----------
        window1.config(menu=menu)  # 设置窗口菜单
        btn = Button(window1, text="Stop Script", command=StopScript)  # 创建一个按钮对象
        btn1 = Button(window1, text="Close Window", command=HideWindow)  # 创建一个按钮对象
        btn2 = Button(window1, text="RUN SCRIPT ON STARTUP", command=add_to_startup)  # 创建一个按钮对象
        btn.grid(column=1, row=0)  # 设置按钮位置
        btn1.grid(column=2, row=0)  # 设置按钮位置
        btn2.grid(column=3, row=0)  # 设置按钮位置
        # -----Settings----------
        new_item2 = Menu(menu)  # 创建一个菜单对象
        new_item2.add_command(label='RUN SCRIPT ON STARTUP', command =add_to_startup)  # 添加"RUN SCRIPT ON STARTUP"命令项
        new_item2.add_command(label='FULLSCREEN', command =FullScreen)  # 添加"FULLSCREEN"命令项
        new_item2.add_command(label='HIDE TITLE BAR', command =HideTitleBar)  # 添加"HIDE TITLE BAR"命令项
        menu.add_cascade(label='Settings', menu=new_item2)  # 将下拉菜单添加到菜单中

        window1.mainloop()  # 进入窗口事件循环，阻塞程序执行，直到窗口被关闭
        
 
    def start():
        # 关闭窗口
        window.destroy()
        # 执行窗口启动函数
        WindowStarted()
        # 设置键盘钩子
        kl.HookKeyboard()
        # 处理消息循环
        pythoncom.PumpMessages()

    # 获取当前用户名(返回你当前系统的用户名)
    USER_NAME = getpass.getuser()
    # 获取当前文件所在目录路径
    dir_path = os.path.dirname(os.path.realpath(__file__))

    def FullScreen():
        # 将窗口设置为全屏模式
        window.attributes('-fullscreen', True)
        # 监听Escape按键，按下时关闭窗口
        window.bind('<Escape>', lambda e: root.destroy())

    def HideTitleBar():
        # 隐藏窗口标题栏
        window.overrideredirect(True)

            
    #该函数实现的功能是将某个程序配置为开机启动项，在用户登录Windows后自动执行该程序。
    def add_to_startup(file_path=dir_path):
        # 如果文件路径为空，则使用当前文件所在目录的路径
        if file_path == "":
            file_path = os.path.dirname(os.path.realpath(__file__))
        
        # 获取启动文件的路径
        bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
        
        # 打开启动文件，并写入内容
        with open(bat_path + '\\' + "duckhunt.bat", "w+") as bat_file:
            bat_file.write(r'start "" %s''\AutoRunDuckHunt.exe' % file_path)              
        




    window.title("DuckHunter")  # 设置窗口标题为"DuckHunter"
    window.iconbitmap('favicon.ico')  # 使用 favicon.ico 作为窗口图标
    window.resizable(False, False)  # 禁止调整窗口大小
    window.geometry('300x45')  # 设置窗口大小为 300x45
    window.geometry("+300+300")  # 将窗口位置设置为 +300+300
    window.attributes("-topmost", True)  # 将窗口设置为总是位于最顶层
    # -----Menu----------
    menu = Menu(window)  # 创建一个菜单对象
    new_item = Menu(menu)  # 创建一个子菜单对象
    new_item.add_command(label='START', command=start)  # 添加"START"命令，点击时调用start函数
    new_item.add_command(label='CLOSE', command=StopScript)  # 添加"CLOSE"命令，点击时调用StopScript函数
    new_item.add_separator()  # 添加一个分隔线
    new_item.add_command(label='ABOUT', command=About)  # 添加"ABOUT"命令，点击时调用About函数
    menu.add_cascade(label='Menu', menu=new_item)  # 将子菜单添加到菜单中，显示为"Menu"选项
    # ------Settings---------
    new_item2 = Menu(menu)  # 创建另一个子菜单对象
    new_item2.add_command(label='RUN SCRIPT ON STARTUP', command=add_to_startup)  # 添加"RUN SCRIPT ON STARTUP"命令，点击时调用add_to_startup函数
    new_item2.add_command(label='FULLSCREEN', command=FullScreen)  # 添加"FULLSCREEN"命令，点击时调用FullScreen函数
    new_item2.add_command(label='HIDE TITLE BAR', command=HideTitleBar)  # 添加"HIDE TITLE BAR"命令，点击时调用HideTitleBar函数
    menu.add_cascade(label='Settings', menu=new_item2)  # 将另一个子菜单添加到菜单中，显示为"Settings"选项
     # ------button---------
    window.config(menu=menu)  # 将菜单设置为窗口的配置菜单
    btn = Button(window, text="Start", command=start)  # 创建一个按钮，显示文本为"Start"，点击时调用start函数
    btn.grid(column=1, row=0)  # 将按钮放置在窗口中的(1,0)位置
    btn = Button(window, text="Close", command=StopScript)  # 创建一个按钮，显示文本为"Close"，点击时调用StopScript函数
    btn.grid(column=2, row=0)  # 将按钮放置在窗口中的(2,0)位置
    btn = Button(window, text="RUN SCRIPT ON STARTUP", command=add_to_startup)  # 创建一个按钮，显示文本为"RUN SCRIPT ON STARTUP"，点击时调用add_to_startup函数
    btn.grid(column=3, row=0)  # 将按钮放置在窗口中的(3,0)位置

    window.mainloop()

    # 注册钩子并执行永无止境的循环
window()