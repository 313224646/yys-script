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
win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 1076, 636, win32con.SWP_NOMOVE)
# 获取颜色使用的api
gdi32 = windll.gdi32
user32 = windll.user32
hdc = user32.GetDC(hwnd)  # 获取颜色值

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
    print(int(time.time()),'-','refuse task')
    doClick(702, 425)

# 开始对战
def startGame():
  color = getColor(1014, 531)
  # 这里参数1是提前测量好的点位颜色
  if similarColors(8311532, color):
    print(int(time.time()),'-','start game')
    x = random.randint(978, 1050)
    y = random.randint(432, 590)
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
    print(int(time.time()),'-','exit game')

# def run():
#   detectTaskInvitation()
#   if detectSettlement():
#     exitGame()
#   startGame()
#   time.sleep(1)
#   gc.collect()
#   return run()
# run()

class Task:
  def run(self):
    detectTaskInvitation()
    if detectSettlement():
      exitGame()
    startGame()
    
print('running...')
while True:
  task = Task()
  task.run()
  time.sleep(1)
  del task
