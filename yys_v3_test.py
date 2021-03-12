#!/usr/bin/env python
# -*- coding: utf-8 -*
from ctypes import *
import random
import time
import win32gui
import win32con
import win32api
import gc

# 全局变量
NAME = u"阴阳师-网易游戏"
HWND = win32gui.FindWindow(None, NAME)
GDI32 = windll.gdi32
USER32 = windll.user32
HDC = USER32.GetDC(HWND)  # 获取颜色值
win32gui.SetWindowPos(HWND, win32con.HWND_NOTOPMOST, 0, 0, 1076, 636, win32con.SWP_NOMOVE)  # 设置阴阳师窗口大小，需要权限比阴阳师进程高

POINTS = {
  'task': {
    'x': 698,
    'y': 422,
    'color': 5597145
  },
  'hunTuStart': {
    'x': 1014,
    'y': 531,
    'color': 8311532
  },
  'hunTuEndingA': {
    'x': 68,
    'y': 52,
    'color': 2108221
  },
  'hunTuEndingB': {
    'x': 60,
    'y': 546,
    'color': 5735338
  },
  'teamUp': {
    'x': 364,
    'y': 340,
    'color': 4663948
  },
  'beTeam': {
    'x': 114,
    'y': 216,
    'color': 6402902
  },
  'beFixedTeam': {
    'x': 202,
    'y': 227,
    'color': 6665306
  }
}

MATRIX = {
  'rejectTask': {
    'x1': 702,
    'y1': 425,
    'x2': 702,
    'y2': 425
  },
  'hunTuStart': {
    'x1': 968,
    'y1': 492,
    'x2': 1050,
    'y2': 572
  },
  'hunTuExit': {
    'x1': 768,
    'y1': 402,
    'x2': 1048,
    'y2': 586
  },
  'defaultInviteCheck': {
    'x1': 466,
    'y1': 300,
    'x2': 466,
    'y2': 300
  },
  'defaultInvite': {
    'x1': 630,
    'y1': 358,
    'x2': 630,
    'y2': 358
  }
}

# 鼠标点击
def globalClick(cx, cy): 
  long_position = win32api.MAKELONG(cx, cy) # 模拟鼠标指针 传送到指定坐标
  win32api.SendMessage(HWND, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position) # 模拟鼠标按下
  win32api.SendMessage(HWND, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position) # 模拟鼠标弹起
  
# 获取坐标点的颜色值，返回十进制
def globalGetColor(x, y):  
  pixel = GDI32.GetPixel(HDC, x, y)  # 提取RGB值
  return pixel

# 判断2个颜色是否相近，返回布尔值
def globalCompareColors(pixel1, pixel2):
  status = False
  r1 = pixel1 & 0x0000ff
  g1 = (pixel1 & 0x00ff00) >> 8
  b1 = pixel1 >> 16
  r2 = pixel2 & 0x0000ff
  g2 = (pixel2 & 0x00ff00) >> 8
  b2 = pixel2 >> 16
  return abs(r1 - r2) < 10 and abs(g1 - g2) < 10 and abs(b1 - b2) < 10

class Onmyoji:
  def __init__(self):
    pass
  def position(self):
    pass
  def teamUp(self):
    pass
  def taskInvitation(self):
    pointTask = POINTS['task']
    matrixRejectTask = MATRIX['rejectTask']
    color = globalGetColor(pointTask['x'], pointTask['y'])
    if globalCompareColors(pointTask['color'], color):
      globalClick(matrixRejectTask['x1'], matrixRejectTask['y1'])
  
class Leader(Onmyoji):
  def teamUp(self):
    point = POINTS['teamUp']
    matrixDefaultInviteCheck = MATRIX['defaultInviteCheck']
    matrixDefaultInvite = MATRIX['defaultInvite']
    color = globalGetColor(point['x'], point['y'])
    if globalCompareColors(point['color'], color):
      globalClick(matrixDefaultInviteCheck['x1'], matrixDefaultInviteCheck['y1'])
      time.sleep(0.5)
      globalClick(matrixDefaultInvite['x1'], matrixDefaultInvite['y1'])

class Member(Onmyoji):
  def teamUp(self):
    pointBeTeam = POINTS['beTeam']
    pointBeFixedTeam = POINTS['beFixedTeam']
    colorBeTeam = globalGetColor(pointBeTeam['x'], pointBeTeam['y'])
    colorBeFixedTeam = globalGetColor(pointBeFixedTeam['x'], pointBeFixedTeam['y'])
    if globalCompareColors(pointBeFixedTeam['color'], colorBeFixedTeam):
      globalClick(pointBeFixedTeam['x'], pointBeFixedTeam['y'])
    elif globalCompareColors(pointBeTeam['color'], colorBeTeam):
      globalClick(pointBeTeam['x'], pointBeTeam['y'])

class Game:
  def __init__(self, player):
    self.player = player
  def ready(self):
    pass
  def start(self):
    pass
  def ending(self):
    pass
  def teammateInvitation(self):
    pass
  
class HunTu(Game):
  def ready(self):
    self.player.taskInvitation()
    pointStart = POINTS['hunTuStart']
    matrixStart = MATRIX['hunTuStart']
    color = globalGetColor(pointStart['x'], pointStart['y'])
    if globalCompareColors(pointStart['color'], color):
      globalClick(
        random.randint(matrixStart['x1'], matrixStart['x2']),
        random.randint(matrixStart['y1'], matrixStart['y2'])
      )
    else:
      time.sleep(2)
      self.ready()
  def endingA(self):
    self.player.taskInvitation()
    self.player.teamUp()
    point = POINTS['hunTuEndingA']
    matrixExit = MATRIX['hunTuExit']
    color = globalGetColor(point['x'], point['y'])
    if globalCompareColors(point['color'], color):
      return
    else:
      time.sleep(1)
      self.endingA()
  def endingB(self):
    self.player.taskInvitation()
    self.player.teamUp()
    pointEndingA = POINTS['hunTuEndingA']
    pointEndingB = POINTS['hunTuEndingB']
    matrixExit = MATRIX['hunTuExit']
    colorA = globalGetColor(pointEndingA['x'], pointEndingA['y'])
    colorB = globalGetColor(pointEndingB['x'], pointEndingB['y'])
    if globalCompareColors(pointEndingA['color'], colorA) or globalCompareColors(pointEndingB['color'], colorB):
      globalClick(
        random.randint(matrixExit['x1'], matrixExit['x2']),
        random.randint(matrixExit['y1'], matrixExit['y2'])
      )
      time.sleep(1)
      self.endingB()
     
# 主流程
print(u"由于开发时间有限, 目前仅支持魂土")
print(u"1: 队长")
print(u"2: 队员")

mode = int(input("请输入序号: "))
count = 1
player = Leader() if mode == 1 else Member()
game = HunTu(player)

while True:
  print('number of runs: ', count)
  count += 1
  if mode == 1:
    game.ready()
  game.endingA()
  game.endingB()
  gc.collect()
  time.sleep(5)
