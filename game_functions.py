import sys
import pygame
from bullet import Bullet
from alien import Alien
import time

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
        # 按Q键关闭游戏
    elif event.key == pygame.K_q:
        sys.exit()

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

def check_events(ai_settings, screen, aliens, ship, stats, play_button, bullets, sb):
    '''响应按键和鼠标事件'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:  #按键按下时
           check_keydown_events(event, ai_settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:   # 按键松开时
            check_keyup_events(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, aliens, ship, stats, play_button, mouse_x, mouse_y, bullets, sb)

def check_play_button(ai_settings, screen, aliens, ship, stats, play_button, mouse_x, mouse_y, bullets, sb):
    # 在玩家单击Play按钮时开始新游戏
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # 重置游戏设置
        ai_settings.initialize_dynamic_settings()

        # 隐藏光标
        pygame.mouse.set_visible(False)

        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True

        # 重置计分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        bullets.empty()
        aliens.empty()

        # 新建一群外星人
        create_fleet(ai_settings, screen, aliens, ship)

        # 将飞船重新放到中间
        ship.center_ship()

def update_screen(ai_settings, screen, ship, bullets, aliens, stats, play_button, sb):
    # 游戏开始前重新绘制屏幕--飞船
    screen.fill(ai_settings.bg_color)
    ship.bltime()
    for bullet in bullets.sprites():
        bullet.draw_buller()
    aliens.draw(screen)
    # 显示得分
    sb.show_score()

    # 如果游戏处于非活动状态， 就绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()

def update_bullets(ai_settings, aliens, bullets, stats, sb):
    # 更新子弹的位置
    bullets.update()
    # 删除已消失的子弹
    for bullet in bullets.copy():  # 跟浅复制 bullets[::]一样的道理，用于遍历列表（因为列表的长度会变，浅复制能保证遍历到原来列表的各个元素）
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, aliens, bullets, stats, sb)

def check_bullet_alien_collisions(ai_settings, aliens, bullets, stats, sb):
    # 检查是否有子弹击中了外星人，如果是这样，就删除相应的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for alien in collisions.values():
            stats.score += ai_settings.alien_points * len(alien)
            # 渲染得分图像
            sb.prep_score()
        check_high_score(stats, sb)

def create_fleet(ai_settings, screen, aliens, ship):
    '''
    创建外星人群
    创建一个外星人，并计算一行课容乃多少个外星人
    外星人间距为外星人宽度
    '''
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    number_aliens_x = get_number_aliens_x(ai_settings, alien_width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # 创建一行外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
        # 创建一个外星人并将其加入当前行
            create_alien(ai_settings, screen, alien_number, aliens, row_number)

def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def create_alien(ai_settings, screen, alien_number, aliens, row_number):
    # 创建一行外星人
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height - (8 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def check_fleet_edges(ai_settings, aliens):
    # 有外星人达到边缘时外星人下移，以及改变fleet_direction的设置
    for alien in aliens.sprites():
        if alien.check_edge():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_Speed
    ai_settings.fleet_direction *= -1

def update_aliens(ai_settings, screen, ship, bullets, aliens, stats, sb):
    # 检查是否有外星人位于屏幕边缘，并更新外星人群中所有外星人的位置
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    # 检测外星人与飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, ship, bullets, aliens, stats, sb)
    # 检查是否有外星人到达屏幕底端
    check_alien_bottom(ai_settings, screen, ship, bullets, aliens, stats, sb)

    # 如果外星人全部被击落, 则提高一个等级
    if len(aliens) == 0:
        # 删除现有子弹并新建一群外星人(会把当前界面上的子弹删除）
        bullets.empty()
        ai_settings.increase_speed()

        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, aliens, ship)

def ship_hit(ai_settings, screen, ship, bullets, aliens, stats, sb):
    # 外星人和飞船碰撞时的一系列发生事项
    # 将飞船的可使用数量ship_left - 1
    if stats.ship_left > 0:
        stats.ship_left -= 1

        # 更新显示可使用的飞船数量
        sb.prep_ships()

        # 清空屏幕现有的子弹和外星人
        bullets.empty()
        aliens.empty()

        # 新建一群外星人
        create_fleet(ai_settings, screen, aliens, ship)

        # 将飞船重新放到中间
        ship.center_ship()

        # 暂停
        time.sleep(0.5)
    else:  # 当飞船都被用完的时候，游戏结束
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_alien_bottom(ai_settings, screen, ship, bullets, aliens, stats, sb):
    # 检查是否有外星人到达屏幕底端
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像外星人和飞船碰撞时一样处理
            ship_hit(ai_settings, screen, ship, bullets, aliens, stats, sb)
            break

def check_high_score(stats, sb):
    # 检查是否诞生了新的最高得分
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()