'''
    在《外星人入侵》游戏中，玩家控制着一艘最初出现在屏幕底部中央的飞船。玩家
可以使用箭头键左右移动飞船，还可以使用空格键进行射击。游戏开始时，一群外星人出
现在天空中，他们在屏幕中向下移动。玩家的任务是射杀这些外星人。玩家将所有外星人
都消灭干净后，将出现一群新的外星人，他们的移动速度更快。只要有外星人撞到了玩家
的飞船或达到了屏幕底部，玩家就损失一艘飞船。玩家损失三艘飞船后，游戏结束。
'''

# 创建Pygame窗口以及响应用户输入
import sys
import pygame

# def run_game():
#     # 初始化游戏并创建一个屏幕对象
#     pygame.init()   # 初始化背景设置
#     screen = pygame.display.set_mode((1200,800))  # 创建显示窗口，（1200，800）指定了窗口的大小
#     pygame.display.set_caption('Alien Invasion')
#
#     # 设置背景色
#     bg_color = (230,230,230)
#
#     # 开始游戏主循环
#     while True:
#         # 监听键盘和鼠标事件
#         for event in pygame.event.get():   # 所有的键盘和鼠标事件都将促使for循环运行
#             if event.type == pygame.QUIT:
#                 sys.exit()
#
#         # 每次循环时都重新绘制屏幕
#         screen.fill(bg_color)
#
#         # 让最近绘制的屏幕可见
#         pygame.display.flip()

from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from alien import Alien

def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')

    ship = Ship(ai_settings, screen)  #创建一艘飞船
    bullets = Group()   # 子弹编组
    aliens = Group()  # 创建外星人编组
    stats = GameStats(ai_settings)  # 创建一个用于统计游戏信息的类
    # 创建外星人群
    gf.create_fleet(ai_settings, screen, aliens, ship)

    # 开始游戏主循环
    while True:
        # 监听键盘和鼠标事件
        gf.check_events(ai_settings, screen, ship, bullets)

        if stats.game_active:  # 如果游戏处于活动状态
            ship.update()
            gf.update_bullets(bullets, ai_settings, screen, aliens, ship)
            gf.update_aliens(ai_settings, screen, ship, bullets, aliens, stats)
            # 每次循环时都重新绘制屏幕

        gf.update_screen(ai_settings, screen, ship, bullets, aliens)

run_game()