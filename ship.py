import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        super(Ship, self).__init__()
        # 初始化飞船并设置其初始位置
        self.screen = screen
        self.ai_settings = ai_settings
        # 加载飞船图像并获取器外接矩形
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # 将每艘新飞创放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # 在飞船的属性center中存储小数值
        self.center = float(self.rect.centerx)

        # 移动标志
        self.move_right = False
        self.move_left = False

    def update(self):
        # 移动飞船，更新飞船的center值
        if self.move_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.move_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # 更新rect对象
        self.rect.centerx = self.center

    def bltime(self):
        '''在指定位置绘制飞船'''
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        # 让飞船放在屏幕中间
        self.center = self.screen_rect.centerx
