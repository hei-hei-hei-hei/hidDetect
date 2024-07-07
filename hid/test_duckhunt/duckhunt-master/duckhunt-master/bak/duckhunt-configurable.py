######################################################
#                   DuckHunter                       #
#                 Pedro M. Sosa                      #
# 工具以防止被橡皮鸭子攻击！                           #
######################################################

from ctypes import *
import pythoncom
import pyHook 
import win32clipboard
import win32ui
import os
import shutil
from time import gmtime, strftime
from sys import stdout
import imp
duckhunt = imp.load_source('duckhunt', 'duckhunt.conf')

##### 备注 #####
#
# 1. 理解保护策略：
#    - 敏感模式：当检测到攻击时，在正确密码输入之前锁定所有按键输入。 (在.conf文件中设置密码)。还会记录攻击事件。
#    - 正常模式：当检测到攻击时，暂时禁用键盘输入。 (在认为威胁已结束之后，会再次允许键盘输入)。还会记录攻击事件。
#    - Sneaky模式：当检测到攻击时，会丢弃一些按键，以避免攻击被识破。(在Sneaky模式下，按键会被正确地丢弃，看起来像是攻击者操作失误。)。还会记录攻击事件。
#    - 只记录模式：当检测到攻击时，仅记录攻击事件而不以任何方式阻止它。
#
# 2. 如何使用
#    - 修改以下用户可配置的变量。 (特别是策略和密码)
#    - 将程序转换为.pyw文件，作为无窗口脚本运行。
#    - (可选) 使用py2exe构建.exe文件。
#
#####################



threshold  = duckhunt.threshold      # 速度阈值
size       = duckhunt.size           # 历史记录数组的大小
policy     = duckhunt.policy.lower() # 设定策略类型
password   = duckhunt.password       # 敏感模式下的密码
allow_auto_type_software = duckhunt.allow_auto_type_software # 允许自动类型软件(例如KeyPass或LastPass)
################################################################################
pcounter   = 0                       # 密码计数器(如果使用密码)
speed      = 0                       # 当前平均按键速度
prevTime   = -1                      # 上一个按键的时间戳
i          = 0                       # 历史记录数组的时间槽
intrusion  = False                   # 用于在检测到入侵时升高的布尔标志
history    = [threshold+1] * size    # 用于跟踪最近n个按键平均速度的历史记录数组
randdrop   = duckhunt.randdrop       # 多长时间内应丢弃一个字母(在Sneaky模式下)
prevWindow = []                      # 上一个窗口名称
filename   = duckhunt.filename       # 要保存攻击事件的文件名
blacklist  = duckhunt.blacklist       # 程序黑名单



# 记录攻击事件
def log(event):
    global prevWindow

    x = open(filename,"a+")
    if (prevWindow != event.WindowName):
        x.write ("\n[ %s ]\n" % (event.WindowName))
        prevWindow =event.WindowName
    if event.Ascii > 32 and event.Ascii < 127:
        x.write(chr(event.Ascii))
    else:
        x.write("[%s]" % event.Key)
        x.close()
    return


def caught(event):
    global intrusion, policy, randdrop
    print "Quack! Quack! -- Time to go Duckhunting!"
    intrusion = True;

    
    # 敏感模式
    if (policy == "paranoid"):
        win32ui.MessageBox("Someone might be trying to inject keystrokes into your computer.\nPlease check your ports or any strange programs running.\nEnter your Password to unlock keyboard.", "KeyInjection Detected",4096) # MB_SYSTEMMODAL = 4096 -- Always on top.
        return False;
    # Sneaky模式
    elif (policy == "sneaky"):
        randdrop += 1 
        # 每隔5个字母丢弃一个字母
        if (randdrop==7):
            randdrop = 0;
            return False;
        else:
            return True;

    # 只记录模式
    elif (policy == "log"):
        log(event)
        return True;


    # 正常模式
    log(event)
    return False


# 每次按键触发该函数
def KeyStroke(event):

    global threshold, policy, password, pcounter
    global speed, prevTime, i, history, intrusion,blacklist

    print event.Key;
    print event.Message;
    print "Injected",event.Injected;
    
    if (event.Injected != 0 and allow_auto_type_software):
        print "Injected by Software"
        return True;
    
    
    # 如果检测到入侵并且我们需要使用密码保护
    # 则锁定所有按键，直到输入正确密码为止
    if (policy == "paranoid" and intrusion):    
        print event.Key;
        log(event);
        if (password[pcounter] == chr(event.Ascii)):
            pcounter += 1;
            if (pcounter == len(password)):
                win32ui.MessageBox("Correct Password!", "KeyInjection Detected",4096) # MB_SYSTEMMODAL = 4096 -- Always on top.
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

    # 类型速度 = 新键时间 - 旧键时间
    history[i] = event.Time - prevTime
    print event.Time,"-",prevTime,"=",history[i]
    prevTime = event.Time
    speed = sum(history) / float(len(history))
    i=i+1

    print "\rAverage Speed:",speed
    
    # 黑名单
    for window in blacklist.split(","):
        if window in event.WindowName:
            return caught(event)

    # 检测到入侵
    if (speed < threshold):
        return caught(event)
    else:
        intrusion = False
    # 将执行权限传递给下一个已注册的钩子
    return True

# 创建并注册一个钩子管理器
kl         = pyHook.HookManager()
kl.KeyDown = KeyStroke

# 注册钩子并无限循环执行
kl.HookKeyboard()
pythoncom.PumpMessages()