import sys
import pygame

def check_keydown_events(event, ship):
    '''按键按下'''
    if event.key == pygame.K_RIGHT:
        # 向右移动飞船
        ship.move_right = True
    elif event.key == pygame.K_LEFT:
        # 向右移动飞船
        ship.move_left = True

def check_keyup_events(event, ship):
    '''按键松开'''
    if event.key == pygame.K_RIGHT:
        ship.move_right = False
    elif event.key == pygame.K_LEFT:
        ship.move_left = False

def check_events(ship):
    '''响应按键和鼠标事件'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:  #按键按下时
           check_keydown_events(event, ship)

        elif event.type == pygame.KEYUP:   # 按键松开时
            check_keyup_events(event,ship)

def update_screen(ai_setting, screen, ship):
    # 每次循环时都重新绘制屏幕
    screen.fill(ai_setting.bg_color)
    ship.bltime()

    # 让最近绘制的屏幕可见
    pygame.display.flip()