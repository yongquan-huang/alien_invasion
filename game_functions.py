import sys
import pygame
from bullet import Bullet

def check_keydown_events(event, ai_settings, screen , ship, bullets):
    '''按键按下'''
    if event.key == pygame.K_RIGHT:
        # 向右移动飞船
        ship.move_right = True
    elif event.key == pygame.K_LEFT:
        # 向右移动飞船
        ship.move_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)

def fire_bullet(ai_settings, screen, ship, bullets):
    # 如果还没达到子弹限制，就创建一颗子弹，并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def check_keyup_events(event, ship):
    '''按键松开'''
    if event.key == pygame.K_RIGHT:
        ship.move_right = False
    elif event.key == pygame.K_LEFT:
        ship.move_left = False

def check_events(ai_settings, screen , ship, bullets):
    '''响应按键和鼠标事件'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:  #按键按下时
           check_keydown_events(event, ai_settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:   # 按键松开时
            check_keyup_events(event, ship)

def update_screen(ai_settings, screen , ship, bullets):
    # 每次循环时都重新绘制屏幕
    screen.fill(ai_settings.bg_color)
    ship.bltime()
    for bullet in bullets.sprites():
        bullet.draw_buller()

    # 让最近绘制的屏幕可见
    pygame.display.flip()

def update_bullets(bullets):
    # 更新子弹的位置
    bullets.update()
    # 删除已消失的子弹
    for bullet in bullets.copy():  # 跟浅复制 bullets[::]一样的道理，用于遍历列表（因为列表的长度会变，浅复制能保证遍历到原来列表的各个元素）
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)