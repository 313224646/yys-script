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

# 用于设置各种场景的检测点
POINTS = {
  'task': {
    'x': 698,
    'y': 422,
    'color': 5597145
  },
  'start': {
    'x': 958,
    'y': 502,
    'color': 12572387
  },
  'startYuLing': {
    'x': 950,
    'y': 500,
    'color': 12769765
  },
  'startYuhunTeam': {
    'x': 1014,
    'y': 531,
    'color': 8311532
  },
  'endingMarkA': {
    'x': 68,
    'y': 52,
    'color': 2108221
  },
  'endingMarkB': {
    'x': 60,
    'y': 546,
    'color': 5735338
  },
  'endingMarkYuLing': {
    'x': 98,
    'y': 516,
    'color': 924710
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

# 用于设置各种场景点击区域
MATRIX = {
  'rejectTask': {
    'x1': 702,
    'y1': 425,
    'x2': 702,
    'y2': 425
  },
  'start': {
    'x1': 910,
    'y1': 484,
    'x2': 1014,
    'y2': 580
  },
  'ending': {
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
  },
  'startYuhunTeam': {
    'x1': 968,
    'y1': 492,
    'x2': 1050,
    'y2': 572
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
  def __init__(self, player, startPoint = POINTS['start'], startMatrix = MATRIX['start'], endingPointA = POINTS['endingMarkA'], endingPointB = POINTS['endingMarkB'], endingMatrix = MATRIX['ending']):
    self.player = player
    self.startPoint = startPoint
    self.startMatrix = startMatrix
    self.endingPointA = endingPointA
    self.endingPointB = endingPointB
    self.endingMatrix = endingMatrix
  def ready(self):
    self.player.taskInvitation()
    color = globalGetColor(self.startPoint['x'], self.startPoint['y'])
    if globalCompareColors(self.startPoint['color'], color):
      globalClick(
        random.randint(self.startMatrix['x1'], self.startMatrix['x2']),
        random.randint(self.startMatrix['y1'], self.startMatrix['y2'])
      )
    else:
      time.sleep(0.5)
      self.ready()
  def ending(self, isEnding = False):
    self.player.taskInvitation()
    self.player.teamUp()
    colorA = globalGetColor(self.endingPointA['x'], self.endingPointA['y'])
    colorB = globalGetColor(self.endingPointB['x'], self.endingPointB['y'])
    testA = globalCompareColors(self.endingPointA['color'], colorA)
    testB = globalCompareColors(self.endingPointB['color'], colorB)
    if bool(1 - isEnding):
      time.sleep(0.5)
      if testA or testB:
        self.ending(True)
      else:
        self.ending()
    if testA or testB:
      globalClick(
        random.randint(self.endingMatrix['x1'], self.endingMatrix['x2']),
        random.randint(self.endingMatrix['y1'], self.endingMatrix['y2'])
      )
      time.sleep(0.5)
      self.ending(True)
  
def getPlayer(mode):
  if mode == 1:
    return Leader()
  elif mode == 2:
    return Member()
  else:
    return Onmyoji()

def getGame(player, mode):
  if mode == 1 or mode == 2:
    return Game(
      player, 
      POINTS['startYuhunTeam'], 
      MATRIX['startYuhunTeam']
    )
  if mode == 4:
    return Game(
      player, 
      POINTS['startYuLing'], 
      MATRIX['start'],
      POINTS['endingMarkYuLing'], 
      POINTS['endingMarkYuLing']
    )
  else:
    return Game(player)
  
# 主流程
print(u"1: 御魂队长")
print(u"2: 御魂队员 or 探索自动退出")
print(u"3: 业原火")
print(u"4: 御灵")

mode = int(input("请输入序号: "))
count = 1
player = getPlayer(mode)
game = getGame(player, mode)

while True:
  print('number of runs: ', count)
  count += 1
  if mode != 2:
    game.ready()
  game.ending()
  time.sleep(0.5)
  gc.collect()
