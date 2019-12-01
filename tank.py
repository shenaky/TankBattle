import random
import sys
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
        return EnemyTank(0)


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
class Map:
    def __init__(self, total):
        # 精灵组
        self.brickGroup = pygame.sprite.Group()
        self.ironGroup = pygame.sprite.Group()
        self.tanksGroup = pygame.sprite.Group()
        # 坦克精灵组
        self.myTanksGroup = pygame.sprite.Group()
        self.enemyTanksGroup = pygame.sprite.Group()
        # 子弹精灵组
        self.bulletsGroup = pygame.sprite.Group()
        self.enemyTanks_total = total
        # 场上存在的敌方坦克总数量
        self.enemyTanks_now = 0
        # 场上可以存在的敌方坦克总数量
        self.enemyTanks_now_max = 4
        # 大本营
        self.home = Home()
        self.stage()
        self.brick = None
        self.iron = None
        self.game_over = False

    # 地图初始化
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

    # 产生一定数量的敌方坦克
    def init_enemy_tank(self, factory):
        for x in range(0, 3):
            if self.enemyTanks_total > 0:
                enemy_tank = factory.factory('tank')
                if not pygame.sprite.spritecollide(enemy_tank, self.tanksGroup, False, None):
                    self.tanksGroup.add(enemy_tank)
                    self.enemyTanksGroup.add(enemy_tank)
                    self.enemyTanks_now += 1
                    self.enemyTanks_total -= 1

    # 当地图上的敌方坦克低于最大值时，新增坦克
    def create_new_enemy_tank(self, factory):
        if self.enemyTanks_total > 0:
            if self.enemyTanks_now < self.enemyTanks_now_max:
                enemy_tank = factory.factory('tank')
                if not pygame.sprite.spritecollide(enemy_tank, self.tanksGroup, False, None):
                    self.tanksGroup.add(enemy_tank)
                    self.enemyTanksGroup.add(enemy_tank)
                    self.enemyTanks_now += 1
                self.enemyTanks_total -= 1

    # 显示地图场景
    def status_display(self, screen):
        # 砖墙
        for each in self.brickGroup:
            screen.blit(each.img, each.rect)
        # 铁墙
        for each in self.ironGroup:
            screen.blit(each.img, each.rect)
        # 家
        screen.blit(self.home.img, self.home.rect)

    # 显示坦克
    def tank_bullet_display(self, screen):
        # 敌方坦克
        for each in self.enemyTanksGroup:
            screen.blit(each.img, each.rect)
            if not each.stop:
                self.tanksGroup.remove(each)
                each.move([self.tanksGroup, self.brickGroup, self.ironGroup], self.home)
                self.tanksGroup.add(each)
        # 敌方坦克发射子弹
        for each in self.enemyTanksGroup:
            if each.live:
                if not each.stop and not each.bullet.live:
                    self.bulletsGroup.remove(each.bullet)
                    each.fire()
                    self.bulletsGroup.add(each.bullet)
        # 子弹
        for tank in self.tanksGroup:
            if tank.bullet.live:
                tank.bullet.move()
                screen.blit(tank.bullet.img, tank.bullet.rect)
                # 子弹碰撞子弹
                self.bulletsGroup.remove(tank.bullet)
                for each in self.bulletsGroup:
                    if each.live:
                        if pygame.sprite.collide_rect(tank.bullet, each) and tank.bullet.flag != each.flag:
                            tank.bullet.live = False
                            each.live = False
                            self.bulletsGroup.remove(each)
                            break
                    else:
                        self.bulletsGroup.remove(each)
                # 子弹碰撞坦克
                for each in self.tanksGroup:
                    if each.live:
                        if tank.bullet.flag != each.flag and pygame.sprite.collide_rect(tank.bullet, each):
                            # 己方坦克收到伤害
                            if each.flag:
                                Music.bang_sound.play()
                                each.life -= 1
                                if each.life < 0:
                                    self.myTanksGroup.remove(each)
                                    self.tanksGroup.remove(each)
                                    if len(self.myTanksGroup) < 1:
                                        self.game_over = True
                                else:
                                    pass
                                    # each.reset()
                                tank.bullet.live = False
                                self.bulletsGroup.remove(tank.bullet)
                            # 敌方坦克收到伤害
                            else:
                                each.blood -= 1
                                # each.level -= 1
                                if each.blood < 0:
                                    Music.bang_sound.play()
                                    each.being = False
                                    self.enemyTanksGroup.remove(each)
                                    self.enemyTanks_now -= 1
                                    self.tanksGroup.remove(each)
                            tank.bullet.live = False
                            break
                    else:
                        self.tanksGroup.remove(each)
                        self.myTanksGroup.remove(each)
                        self.enemyTanksGroup.remove(each)
                # 子弹碰撞砖墙
                if pygame.sprite.spritecollide(tank.bullet, self.brickGroup, True, None):
                    tank.bullet.live = False

                # 子弹碰撞铁墙
                if pygame.sprite.spritecollide(tank.bullet, self.ironGroup, False, None):
                    tank.bullet.live = False

                # 子弹碰大本营
                if pygame.sprite.collide_rect(tank.bullet, self.home):
                    tank.bullet.live = False
                    self.game_over = True


# 开始界面显示
def show_start_interface(screen, width, height):
    t_font = pygame.font.Font('./font/simkai.ttf', width//6)
    c_font = pygame.font.Font('./font/simkai.ttf', width//20)
    title = t_font.render(u'坦克大战', True, (255, 0, 0))
    content1 = c_font.render(u'按1键进入单人游戏', True, (0, 0, 255))
    content2 = c_font.render(u'按2键进入双人人游戏', True, (0, 0, 255))
    content3 = c_font.render(u'按3键静音进入游戏', True, (0, 0, 255))
    content4 = c_font.render(u'按4键静音进入地狱模式', True, (0, 0, 255))
    t_rect = title.get_rect()
    t_rect.midtop = (width/2, height/4)
    crect1 = content1.get_rect()
    crect1.midtop = (width/2, height/1.8)
    crect2 = content2.get_rect()
    crect2.midtop = (width/2, height/1.6)
    crect3 = content3.get_rect()
    crect3.midtop = (width / 2, height / 1.45)
    crect4 = content4.get_rect()
    crect4.midtop = (width / 2, height / 1.34)
    screen.blit(title, t_rect)
    screen.blit(content1, crect1)
    screen.blit(content2, crect2)
    screen.blit(content3, crect3)
    screen.blit(content4, crect4)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 1
                if event.key == pygame.K_2:
                    return 2
                if event.key == pygame.K_3:
                    return 3
                if event.key == pygame.K_4:
                    return 4


def show_end_interface(screen, width, height, is_win):
    screen.fill((0, 0, 0))
    if is_win:
        font = pygame.font.Font('./font/simkai.ttf', width//10)
        content = font.render(u'恭喜通关！', True, (255, 0, 0))
        rect = content.get_rect()
        rect.midtop = (width/2, height/2)
        screen.blit(content, rect)
    else:
        fail_img = pygame.image.load("./images/others/gameover.png")
        rect = fail_img.get_rect()
        rect.midtop = (width/2, height/2)
        screen.blit(fail_img, rect)
        pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


# 关卡切换
def show_switch_stage(screen, width, height, stage):
    screen.fill((0, 0, 0))
    font = pygame.font.Font('./font/simkai.ttf', width//10)
    content = font.render(u'第%d关' % stage, True, (0, 255, 0))
    rect = content.get_rect()
    rect.midtop = (width/2, height/2)
    screen.blit(content, rect)
    pygame.display.update()
    delay_event = pygame.constants.USEREVENT
    pygame.time.set_timer(delay_event, 1000)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == delay_event:
                return


pygame.init()


class Music:
    # 加载音效
    bang_sound = pygame.mixer.Sound("./audios/bang.wav")
    bang_sound.set_volume(1)
    fire_sound = pygame.mixer.Sound("./audios/fire.wav")
    fire_sound.set_volume(1)
    start_sound = pygame.mixer.Sound("./audios/start.wav")
    start_sound.set_volume(1)


def main_game():
    pygame.init()
    screen = pygame.display.set_mode((630, 630))
    pygame.display.set_caption("坦克大战")
    clock = pygame.time.Clock()
    screen.fill((0, 0, 0))
    # 开始界面
    num_player = show_start_interface(screen, 630, 630)
    # 播放游戏开始的音乐
    Music.start_sound.play()
    # 关卡
    stage = 0
    num_enemyTank = 8
    num_bigTank = 4
    # 游戏主循环
    game_over = False
    while not game_over:
        # 关卡
        stage += 1
        num_bigTank += 1
        num_enemyTank += 1
        show_switch_stage(screen, 630, 630, stage)
        # 初始化地图类
        map_ = Map(num_enemyTank)
        map_.stage()
        factory = EnemyTankFactory(num_enemyTank, num_bigTank)
        # 生成己方坦克
        myTank = MyTank(24 * 8, 24 * 24, 3)
        map_.tanksGroup.add(myTank)
        map_.myTanksGroup.add(myTank)
        map_.init_enemy_tank(factory)
        # 定义生成敌方坦克事件
        genEnemyEvent = pygame.constants.USEREVENT
        pygame.time.set_timer(genEnemyEvent, 100)
        while True:
            if game_over:
                break
            if map_.enemyTanks_total < 1 and map_.enemyTanks_now < 1:
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == genEnemyEvent:
                    map_.create_new_enemy_tank(factory)

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
                            Music.fire_sound.play()

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                        myTank.stop = True

            # 背景
            screen.fill((0, 0, 0))
            map_.status_display(screen)
            # 我方坦克
            if myTank in map_.myTanksGroup:
                if not myTank.stop:
                    map_.tanksGroup.remove(myTank)
                    myTank.move([map_.tanksGroup, map_.brickGroup, map_.ironGroup], map_.home)
                    map_.tanksGroup.add(myTank)
                screen.blit(myTank.img, myTank.rect)
            map_.tank_bullet_display(screen)
            game_over = map_.game_over
            pygame.display.flip()
            clock.tick(60)
    # 结束界面
    show_end_interface(screen, 630, 630, False)


if __name__ == "__main__":
    main_game()
