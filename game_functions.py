import sys
import pygame

def check_events():
    '''响应按键和鼠标事件'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

def update_screen(ai_setting, screen, ship):
    # 每次循环时都重新绘制屏幕
    screen.fill(ai_setting.bg_color)
    ship.bltime()

    # 让最近绘制的屏幕可见
    pygame.display.flip()