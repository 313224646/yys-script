#!/usr/bin/env python 
# -*- coding: utf-8 -*
from ctypes import *
import random
import time
import win32gui
import win32con
import win32api
import gc

# 当前支持的模式
print(u"选择模式：")
print(u"1: 组队魂土")
print(u"2: 单人魂土/痴/日轮/觉醒")
print(u"3: 御灵")
print(u"4: 结界突破")
print(u"5: 道馆突破")

# 全局变量
NAME = u"阴阳师-网易游戏"
HWND = win32gui.FindWindow(None, NAME)
GDI32 = windll.gdi32 
USER32 = windll.user32
HDC = USER32.GetDC(HWND)  # 获取颜色值
MODE = int(input("请输入序号: "))
DETECT_POINT = [0, 0]
DETECT_COLOR = 0
START_MATRIX = [0, 0, 0, 0]

# 相关数据初始化
win32gui.SetWindowPos(HWND, win32con.HWND_NOTOPMOST, 0, 0, 1076, 636, win32con.SWP_NOMOVE) # 设置阴阳师窗口大小，需要权限比阴阳师进程高

if MODE == 1:
  DETECT_POINT = [1014, 531]
  DETECT_COLOR = 8311532
  START_MATRIX = [978, 432, 1050, 590]
elif MODE == 2:
  DETECT_POINT = [958, 502]
  DETECT_COLOR = 12572387
  START_MATRIX = [910, 484, 1014, 580]
elif MODE == 3:
  DETECT_POINT = [1014, 531]
  DETECT_COLOR = 12703972
  START_MATRIX = [900, 480, 1000, 580]
elif MODE == 4:
  DETECT_POINT = [192, 500]
  DETECT_COLOR = 4144548
  START_MATRIX = [900, 480, 1000, 580]
elif MODE == 5:
  DETECT_POINT = [986, 463]
  DETECT_COLOR = 5279444
  START_MATRIX = [920, 426, 1020, 514]

# 工具类
def doClick(cx, cy): # 鼠标点击
  long_position = win32api.MAKELONG(cx, cy) # 模拟鼠标指针 传送到指定坐标
  win32api.SendMessage(HWND, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position) # 模拟鼠标按下
  win32api.SendMessage(HWND, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position) # 模拟鼠标弹起

def getColor(x, y): # 获取坐标点的颜色值，返回十进制
  pixel = GDI32.GetPixel(HDC, x, y)  # 提取RGB值
  return pixel

def similarColors(pixel1, pixel2): # 判断2个颜色是否相近, pixel1通常是手动测量的值
  status = False
  r1 = pixel1 & 0x0000ff
  g1 = (pixel1 & 0x00ff00) >> 8
  b1 = pixel1 >> 16
  r2 = pixel2 & 0x0000ff
  g2 = (pixel2 & 0x00ff00) >> 8
  b2 = pixel2 >> 16
  return abs(r1 - r2) < 10 and abs(g1 - g2) < 10 and abs(b1 - b2) < 10

# 检测类
def detectTask(): # 检测协作任务邀请
  color = getColor(698, 422)
  return similarColors(5597145, color)

def detectBreakthroughUI(): # 检测是否在突破界面
  color = getColor(DETECT_POINT[0], DETECT_POINT[1])
  return similarColors(DETECT_COLOR, color)

def detectSettlement(): # 检测是否进入结束阶段
  color = getColor(146, 555)
  return similarColors(2090231, color)

def detectBreakthroughRewardUI(): # 检测是否在突破奖励界面
  color = getColor(260, 196)
  return similarColors(13816530, color)

def detectBreakthrough(x, y): # 检测某格子是否可以进行突破
  color = getColor(x, y)
  return similarColors(12439002, color)

def detectStartButton(): # 检测开始按钮
  color = getColor(DETECT_POINT[0], DETECT_POINT[1])
  return similarColors(DETECT_COLOR, color)

# 行为类
def exitTask():
  print(u"拒绝协作")
  doClick(702, 425)

def exitBreakthroughRewardUI():
  print(u"退出突破结算")
  x = random.randint(738, 1057)
  y = random.randint(432, 590)
  doClick(x, y)

def startGame(): # 开始对战
  print(u"开始对战")
  x = random.randint(START_MATRIX[0], START_MATRIX[2])
  y = random.randint(START_MATRIX[1], START_MATRIX[3])
  doClick(x, y)

def exitGame(): # 退出对战
  x = random.randint(738, 1057)
  y = random.randint(432, 590)
  doClick(x, y)
  if detectSettlement():
    time.sleep(random.uniform(0.2, 0.5))
    exitGame()
  else:
    print(u"退出对战")

def startBreakthrough(): # 结界突破
  ltcx = ltcy = rbcx = rbcy = x = y = 0
  utx = 1
  uty = 0
  i = 1
  while i <= 9:
    utx = 1 if i < 4 else 4 if i < 7 else 7 # step x 
    uty = 0 if i < 4 else 1 if i < 7 else 2 # step y
    ltcx = int(122 + (i - utx) * 266 + (i - utx) * 10) # left top click x
    ltcy = int(122 + uty * 100 + uty * 10) # left top click y
    rbcx = ltcx + 266 # right bottom click x
    rbcy = ltcy + 100 # right bottom click y
    x = ltcx + 133 # task point x
    y = ltcy + 14 # task point y
    sltx = ltcx + 144 # start left top x
    slty = ltcy + 174 # start left top y
    srbx = sltx + 112 # start right bottom x
    srby = slty + 56 # start right bottom y
    i = i + 1
    if detectBreakthrough(x, y): 
      print(u"开始突破")
      doClick(random.randint(ltcx, rbcx), random.randint(ltcy, rbcy))
      time.sleep(0.5)
      doClick(random.randint(sltx, srbx), random.randint(slty, srby))
      time.sleep(1)
      break
    
# 类

class Task:
  def __init__(self, mode):
    self.mode = mode
  def run(self):
    # 协作任务相关
    if detectTask(): 
      exitTask()
    # 结算相关
    if detectSettlement(): 
      exitGame()
    # 开始相关
    if self.mode == 4: 
      if detectBreakthroughRewardUI():
        exitBreakthroughRewardUI()
      if detectBreakthroughUI():
        startBreakthrough()
    else:
      if detectStartButton():
        startGame()
        
# 主流程
while True:
  task = Task(MODE)
  task.run()
  time.sleep(1)
  # 防止内存泄漏
  del task
  gc.collect()