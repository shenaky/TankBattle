import random

import pygame


# 简单工厂 返回敌方坦克对象
class EnemyTankFactory:
    def __init__(self, total, big):
        # 敌方坦克总数量
        self.enemyTanks_total = total
        # 当前关卡重装坦克的数量
        self.enemyTanks_big = big
        # 坦克的等级数组
        self.list = []
        for _ in range(self.enemyTanks_big):
            self.list.append(2)
        for _ in range(self.enemyTanks_total - self.enemyTanks_big):
            self.list.append(random.randint(0, 1))
        random.shuffle(self.list)

    def factory(self, t):
        if t == 'tank':
            if len(self.list) > 0:
                return EnemyTank(self.list.pop())
        return None


# 坦克类
class Tank(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.tank = None
        self.direction = None
        self.img = None
        self.image = None
        self.rect = None
        self.live = True
        self.stop = False
        self.speed = None
        self.flag = None
        self.bullet = None

    # 坦克移动
    def move(self, group, home):
        if not self.stop:
            rect = self.rect
            if self.direction == 'U':
                self.img = self.tank.subsurface((0, 0), (48, 48))
                self.rect = self.rect.move(0, 0 - self.speed)
            elif self.direction == 'D':
                self.img = self.tank.subsurface((0, 48), (48, 48))
                self.rect = self.rect.move(0, self.speed)
            elif self.direction == 'L':
                self.img = self.tank.subsurface((0, 96), (48, 48))
                self.rect = self.rect.move(0 - self.speed, 0)
            elif self.direction == 'R':
                self.img = self.tank.subsurface((0, 144), (48, 48))
                self.rect = self.rect.move(self.speed, 0)
            # 碰撞检测
            if self.is_blocked(group, home):
                if self.flag:
                    self.rect = rect
                    self.stop = True
                else:
                    self.rect = rect
                    self.direction = random.choice(['U', 'D', 'L', 'R'])

    # 开火
    def fire(self):
        self.bullet.live = True
        self.bullet.reload(self.direction)
        if self.direction == 'U':
            self.bullet.rect.left = self.rect.left + 20
            self.bullet.rect.bottom = self.rect.top - 1
        elif self.direction == 'D':
            self.bullet.rect.left = self.rect.left + 20
            self.bullet.rect.top = self.rect.bottom + 1
        elif self.direction == 'L':
            self.bullet.rect.right = self.rect.left - 1
            self.bullet.rect.top = self.rect.top + 20
        elif self.direction == 'R':
            self.bullet.rect.left = self.rect.right + 1
            self.bullet.rect.top = self.rect.top + 20

    # 碰撞检测
    def is_blocked(self, group, home):
        if self.rect.left < 0 or self.rect.top < 0:
            return True
        elif self.rect.right > 624 or self.rect.bottom > 624:
            return True
        for each in group:
            if pygame.sprite.spritecollide(self, each, False, None):
                return True
        if pygame.sprite.collide_rect(self, home):
            return True
        return False


# 己方坦克类
class MyTank(Tank):
    def __init__(self, x, y, speed):
        super().__init__()
        self.direction = 'U'
        self.tank = pygame.image.load('images/myTank/myTank.png')
        self.img = self.tank.subsurface((0, 0), (48, 48))
        self.rect = self.img.get_rect()
        self.rect.left, self.rect.top = x, y
        self.speed = speed
        self.stop = True
        self.flag = True
        self.life = 3
        self.bullet = Bullet(6, self.flag)


# 敌方坦克类
class EnemyTank(Tank):
    def __init__(self, level, x=None, y=None):
        """
        :param x:
        :param y:
        :param level: 0-2
        """
        super().__init__()
        self.direction = 'D'
        self.tanks0 = ['./images/enemyTank/enemy_1_0.png', './images/enemyTank/enemy_1_1.png',
                       './images/enemyTank/enemy_1_2.png']
        self.tanks1 = ['./images/enemyTank/enemy_2_0.png', './images/enemyTank/enemy_2_1.png',
                       './images/enemyTank/enemy_2_2.png']
        self.tanks2 = ['./images/enemyTank/enemy_3_0.png', './images/enemyTank/enemy_3_1.png',
                       './images/enemyTank/enemy_3_2.png']
        self.tanks = [self.tanks0, self.tanks1, self.tanks2]
        self.level = level
        self.color = random.randint(0, 2)
        self.tank = pygame.image.load(self.tanks[self.level][self.color])
        self.img = self.tank.subsurface((0, 0), (48, 48))
        self.rect = self.img.get_rect()
        if x is None or y is None:
            x = random.randint(0, 2)
            self.rect.left, self.rect.top = x * 12 * 24, 3
        else:
            self.rect.left, self.rect.top = x, y
        self.speed = 3 - self.level
        self.blood = self.level + 1
        self.stop = False
        self.flag = False
        self.bullet = Bullet(6, self.flag)


# 子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, speed, flag):
        pygame.sprite.Sprite.__init__(self)

        self.bullets = {
            'U': pygame.image.load('./images/bullet/bullet_up.png'),
            'D': pygame.image.load('./images/bullet/bullet_down.png'),
            'L': pygame.image.load('./images/bullet/bullet_left.png'),
            'R': pygame.image.load('./images/bullet/bullet_right.png')
        }
        self.direction = 'U'
        self.speed = speed
        self.img = self.bullets[self.direction]
        # 在坦克类中赋实际值
        self.rect = self.img.get_rect()
        self.rect.left, self.rect.top = 0, 0
        self.live = False
        self.flag = flag

    # 子弹重载
    def reload(self, direction):
        self.direction = direction
        self.img = self.bullets[self.direction]
        self.live = True

    # 子弹移动
    def move(self):
        if self.direction == 'U':
            self.rect = self.rect.move(0, 0 - self.speed)
        elif self.direction == 'D':
            self.rect = self.rect.move(0, self.speed)
        elif self.direction == 'L':
            self.rect = self.rect.move(0 - self.speed, 0)
        elif self.direction == 'R':
            self.rect = self.rect.move(self.speed, 0)
        if (0 > self.rect.top) or (self.rect.bottom > 630) or (self.rect.left < 0) or (self.rect.right > 630):
            self.live = False


# 砖墙类
class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load('./images/scene/brick.png')
        self.rect = self.img.get_rect()
        self.rect.left, self.rect.top = x, y
        self.health = 5
        self.live = True


# 铁墙类
class Iron(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load('./images/scene/iron.png')
        self.rect = self.img.get_rect()
        self.rect.left, self.rect.top = x, y
        self.health = 10
        self.live = True


# 大本营类
class Home(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.homes = ['./images/home/home1.png', './images/home/home2.png', './images/home/home_destroyed.png']
        self.img = pygame.image.load(self.homes[0])
        self.rect = self.img.get_rect()
        self.rect.left, self.rect.top = (3 + 12 * 24, 3 + 24 * 24)
        self.alive = True


# 地图类
class Map():
    def __init__(self):
        self.brickGroup = pygame.sprite.Group()
        self.ironGroup = pygame.sprite.Group()
        self.home = Home()
        self.stage()
        self.brick = None
        self.iron = None

    def stage(self):
        for x in [2, 3, 6, 7, 18, 19, 22, 23]:
            for y in [2, 3, 4, 5, 6, 7, 8, 9, 10, 17, 18, 19, 20, 21, 22, 23]:
                self.brick = Brick(x * 24, y * 24)
                self.brickGroup.add(self.brick)
        for x in [10, 11, 14, 15]:
            for y in [2, 3, 4, 5, 6, 7, 8, 11, 12, 15, 16, 17, 18, 19, 20]:
                self.brick = Brick(x * 24, y * 24)
                self.brickGroup.add(self.brick)
        for x in [4, 5, 6, 7, 18, 19, 20, 21]:
            for y in [13, 14]:
                self.brick = Brick(x * 24, y * 24)
                self.brickGroup.add(self.brick)
        for x in [12, 13]:
            for y in [16, 17]:
                self.brick = Brick(x * 24, y * 24)
                self.brickGroup.add(self.brick)
        for x, y in [(11, 23), (12, 23), (13, 23), (14, 23), (11, 24), (14, 24), (11, 25), (14, 25)]:
            self.brick = Brick(x * 24, y * 24)
            self.brickGroup.add(self.brick)
        for x, y in [(0, 14), (1, 14), (12, 6), (13, 6), (12, 7), (13, 7), (24, 14), (25, 14)]:
            self.iron = Iron(x * 24, y * 24)
            self.ironGroup.add(self.iron)

    def display(self, screen):
        # 砖墙
        for each in self.brickGroup:
            screen.blit(each.img, each.rect)
        # 铁墙
        for each in self.ironGroup:
            screen.blit(each.img, each.rect)
        # 家
        screen.blit(self.home.img, self.home.rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((630, 630))
    screen.fill((0, 0, 0))
    clock = pygame.time.Clock()
    # 坦克精灵组
    tanksGroup = pygame.sprite.Group()
    myTanksGroup = pygame.sprite.Group()
    enemyTanksGroup = pygame.sprite.Group()
    # 子弹精灵组
    bulletsGroup = pygame.sprite.Group()
    # 敌方坦克总数量
    enemyTanks_total = 20
    # 场上存在的敌方坦克总数量
    enemyTanks_now = 0
    # 场上可以存在的敌方坦克总数量
    enemyTanks_now_max = 4
    Factory = EnemyTankFactory(enemyTanks_total, 5)
    # 定义生成敌方坦克事件
    genEnemyEvent = pygame.constants.USEREVENT
    pygame.time.set_timer(genEnemyEvent, 100)
    myTank = MyTank(24 * 8, 24 * 24, 3)
    tanksGroup.add(myTank)
    myTanksGroup.add(myTank)
    # 大本营
    home = Home()
    map_ = Map()
    for x in range(0, 3):
        if enemyTanks_total > 0:
            enemy_tank = Factory.factory('tank')
            if not pygame.sprite.spritecollide(enemy_tank, tanksGroup, False, None):
                tanksGroup.add(enemy_tank)
                enemyTanksGroup.add(enemy_tank)
                enemyTanks_now += 1
                enemyTanks_total -= 1
                pygame.display.flip()
    running = True
    # 游戏主循环
    while running:
        if enemyTanks_total < 1 and enemyTanks_now < 1:
            running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == genEnemyEvent:
                if enemyTanks_total > 0:
                    if enemyTanks_now < enemyTanks_now_max:
                        enemy_tank = Factory.factory('tank')
                        if not pygame.sprite.spritecollide(enemy_tank, tanksGroup, False, None):
                            tanksGroup.add(enemy_tank)
                            enemyTanksGroup.add(enemy_tank)
                            enemyTanks_now += 1
                            enemyTanks_total -= 1

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    myTank.direction = 'L'
                    myTank.stop = False
                elif event.key == pygame.K_RIGHT:
                    myTank.direction = 'R'
                    myTank.stop = False
                elif event.key == pygame.K_UP:
                    myTank.direction = 'U'
                    myTank.stop = False
                elif event.key == pygame.K_DOWN:
                    myTank.direction = 'D'
                    myTank.stop = False
                elif event.key == pygame.K_SPACE:
                    if not myTank.bullet.live:
                        myTank.fire()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    myTank.stop = True

        # 背景
        screen.fill((0, 0, 0))
        map_.display(screen)
        # 我方坦克
        if myTank in myTanksGroup:
            if not myTank.stop:
                tanksGroup.remove(myTank)
                myTank.move([tanksGroup, map_.brickGroup, map_.ironGroup], home)
                tanksGroup.add(myTank)
            screen.blit(myTank.img, myTank.rect)

        # 敌方坦克
        for each in enemyTanksGroup:
            screen.blit(each.img, each.rect)
            if not each.stop:
                tanksGroup.remove(each)
                each.move([tanksGroup, map_.brickGroup, map_.ironGroup], home)
                tanksGroup.add(each)

        # 敌方坦克发射子弹
        for each in enemyTanksGroup:
            if each.live:
                if not each.stop and not each.bullet.live:
                    bulletsGroup.remove(each.bullet)
                    each.fire()
                    bulletsGroup.add(each.bullet)

        # 子弹
        for tank in tanksGroup:
            if tank.bullet.live:
                tank.bullet.move()
                screen.blit(tank.bullet.img, tank.bullet.rect)

                # 子弹碰撞子弹
                bulletsGroup.remove(tank.bullet)
                for each in bulletsGroup:
                    if each.live:
                        if pygame.sprite.collide_rect(tank.bullet, each) and tank.bullet.flag != each.flag:
                            tank.bullet.live = False
                            each.live = False
                            bulletsGroup.remove(each)
                            break
                    else:
                        bulletsGroup.remove(each)

                # 子弹碰撞坦克
                for each in tanksGroup:
                    if each.live:
                        if tank.bullet.flag != each.flag and pygame.sprite.collide_rect(tank.bullet, each):
                            # 己方坦克收到伤害
                            if each.flag:
                                # bang_sound.play()
                                each.life -= 1
                                if each.life < 0:
                                    myTanksGroup.remove(each)
                                    tanksGroup.remove(each)
                                    if len(myTanksGroup) < 1:
                                        running = False
                                else:
                                    pass
                                    # each.reset()
                                tank.bullet.live = False
                                bulletsGroup.remove(tank.bullet)
                            # 敌方坦克收到伤害
                            else:
                                each.blood -= 1
                                # each.level -= 1
                                if each.blood < 0:
                                    # bang_sound.play()
                                    each.being = False
                                    enemyTanksGroup.remove(each)
                                    enemyTanks_now -= 1
                                    tanksGroup.remove(each)
                            tank.bullet.live = False
                            break
                    else:
                        tanksGroup.remove(each)
                        myTanksGroup.remove(each)
                        enemyTanksGroup.remove(each)

                # 子弹碰撞砖墙
                if pygame.sprite.spritecollide(tank.bullet, map_.brickGroup, True, None):
                    tank.bullet.live = False

                # 子弹碰撞铁墙
                if pygame.sprite.spritecollide(tank.bullet, map_.ironGroup, False, None):
                    tank.bullet.live = False

                # 子弹碰大本营
                if pygame.sprite.collide_rect(tank.bullet, home):
                    tank.bullet.live = False
                    running = False

        pygame.display.flip()
        clock.tick(60)
    # 结束界面
    screen.fill((0, 0, 0))
    img = pygame.image.load("./images/others/gameover.png")
    rect = img.get_rect()
    rect.midtop = (624 / 2, 624 / 2)
    screen.blit(img, rect)
    pygame.display.update()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


if __name__ == "__main__":
    main()
