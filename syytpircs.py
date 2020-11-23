#!/usr/bin/env python 
# -*- coding: utf-8 -*
from ctypes import *
import random
import time
import win32gui
import win32con
import win32api
import gc

# 获取句柄
name = u"阴阳师-网易游戏"
hwnd = win32gui.FindWindow(None, name)
# 设置阴阳师窗口大小，需要权限比阴阳师进程高
# win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 1076, 636, win32con.SWP_NOMOVE)

# 获取颜色使用的api
gdi32 = windll.gdi32
user32 = windll.user32
hdc = user32.GetDC(hwnd)  # 获取颜色值

# 待开发
print(u"选择模式：")
print(u"1: 组队魂土")
print(u"2: 单人魂土/痴/日轮/觉醒")
print(u"3: 御灵")
print(u"4: 结界突破")
print(u"5: 道馆突破")
mode = int(input('请输入序号: '))
taskPosition = [0, 0]
taskColor = 0
clickPosition = [0, 0, 0, 0] # x1, y1, x2, y2
if mode == 1:
  taskPosition = [1014, 531]
  taskColor = 8311532
  clickPosition = [978, 432, 1050, 590]
if mode == 2:
  taskPosition = [958, 502]
  taskColor = 12572387
  clickPosition = [910, 484, 1014, 580]
elif mode == 3:
  taskPosition = [1014, 531]
  taskColor = 12703972
  clickPosition = [900, 480, 1000, 580]
elif mode == 5:
  taskPosition = [986, 463]
  taskColor = 5279444
  clickPosition = [920, 426, 1020, 514]

# 鼠标点击
def doClick(cx, cy):
  long_position = win32api.MAKELONG(cx, cy)#模拟鼠标指针 传送到指定坐标
  win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)#模拟鼠标按下
  win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)#模拟鼠标弹起

# 获取坐标点的颜色值，返回十进制
def getColor(x, y):
  pixel = gdi32.GetPixel(hdc, x, y)  # 提取RGB值
  return pixel

# 获取坐标点的颜色值，返回RGB
def getColorRGB(x, y):
  pixel = gdi32.GetPixel(hdc, x, y)  # 提取RGB值
  r = pixel & 0x0000ff
  g = (pixel & 0x00ff00) >> 8
  b = pixel >> 16
  return [r, g, b]

# 判断2个颜色是否相近
def similarColors(pixel1, pixel2):
  status = False
  r1 = pixel1 & 0x0000ff
  g1 = (pixel1 & 0x00ff00) >> 8
  b1 = pixel1 >> 16
  r2 = pixel2 & 0x0000ff
  g2 = (pixel2 & 0x00ff00) >> 8
  b2 = pixel2 >> 16
  return abs(r1 - r2) < 10 and abs(g1 - g2) < 10 and abs(b1 - b2) < 10

# 检测协作邀请并拒绝
def detectTaskInvitation():
  color = getColor(698, 422)
  # 这里参数1是提前测量好的点位颜色
  if similarColors(5597145, color):
    print('refuse task(',int(time.time()),')')
    doClick(702, 425)

# 开始对战
def startGame():
  color = getColor(taskPosition[0], taskPosition[1])
  # 这里参数1是提前测量好的点位颜色
  if similarColors(taskColor, color):
    print('start game(',int(time.time()),')')
    x = random.randint(clickPosition[0], clickPosition[2])
    y = random.randint(clickPosition[1], clickPosition[3])
    doClick(x, y)
  
# 检测是否进入结束阶段
def detectSettlement():
  color = getColor(146, 555)
  # 这里参数1是提前测量好的点位
  return similarColors(2090231, color)

# 退出对战
def exitGame():
  x = random.randint(738, 1057)
  y = random.randint(432, 590)
  doClick(x, y)
  if detectSettlement():
    time.sleep(random.uniform(0.2, 0.5))
    exitGame()
  else:
    print('exit game(',int(time.time()),')')

# 结界突破 - 测试版
def tuPo():
  i = 1
  ltcx = ltcy = rbcx = rbcy = x = y = 0
  utx = 1
  uty = 0
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
    color = getColor(x, y)
    i = i + 1
    print(color)
    if similarColors(12439002, color): 
      print('start game(',int(time.time()),')')
      doClick(random.randint(ltcx, rbcx), random.randint(ltcy, rbcy))
      time.sleep(0.25)
      doClick(random.randint(sltx, srbx), random.randint(slty, srby))
      break
  if i == 10: # 9次已全部打完，需要刷新
    print('refresh game(',int(time.time()),')')
    doClick(870, 500)
    time.sleep(0.25)
    doClick(630, 358)
  

class Task:
  def __init__(self, mode):
    self.mode = mode
  def run(self):
    detectTaskInvitation()
    if detectSettlement():
      exitGame()
    if self.mode == 4:
      tuPo()
    else:
      startGame()

print('running...')
while True:
  task = Task(mode)
  task.run()
  time.sleep(1)
  # 防止内存泄漏
  del task
  gc.collect()
