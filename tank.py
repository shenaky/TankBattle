import pygame
import random

# 砖墙类
class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load('images/scene/brick.png')
        self.rect = self.img.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.health = 5
        self.live = True

# 坦克类
class Tank(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.direction =None
        self.img = None
        self.image = None
        self.speed = 0
        self.rect = None
        self.live = True
        self.stop = False
    def move(self):
        if not self.stop:
            rect = self.rect
            if self.direction == 'U':
                self.img = self.tank.subsurface((0, 0), (48, 48))
                self.rect = self.rect.move(0, 0-self.speed)
            elif self.direction == 'D':
                self.img = self.tank.subsurface((0, 48), (48, 48))
                self.rect = self.rect.move(0, self.speed)
            elif self.direction == 'L':
                self.img = self.tank.subsurface((0, 96), (48, 48))
                self.rect = self.rect.move(0-self.speed, 0)
            elif self.direction == 'R':
                self.img = self.tank.subsurface((0, 144), (48, 48))
                self.rect = self.rect.move(self.speed, 0)
            if self.isblocked():
                self.rect = rect
                self.stop = True
    def fire(self):
        pass
    def isblocked(self):
        if self.rect.left < 0 or self.rect.top < 0:
            return True
        elif self.rect.right > 624 or self.rect.bottom > 624:
            return True
        return False

class myTank(Tank):
    def __init__(self, x, y, speed):
        super().__init__()
        self.direction ='U'
        self.tank = pygame.image.load('images/myTank/myTank.png')
        self.img = self.tank.subsurface((0, 0), (48, 48))
        self.rect = self.img.get_rect()
        self.rect.left, self.rect.top = x, y
        self.speed = speed
        self.stop = True


class enemyTank(Tank):
    def __init__(self, x, y, speed):
        super().__init__()
        self.direction ='D'
        self.tank = pygame.image.load('images/enemyTank/enemyTank.png')
        self.img = self.tank.subsurface((0, 0), (48, 48))
        self.rect = self.img.get_rect()
        self.rect.left, self.rect.top = x, y
        self.speed = speed
        self.stop = False

    def move(self):
        if not self.stop:
            rect = self.rect
            if self.direction == 'U':
                self.img = self.tank.subsurface((0, 0), (48, 48))
                self.rect = self.rect.move(0, 0-self.speed)
            elif self.direction == 'D':
                self.img = self.tank.subsurface((0, 48), (48, 48))
                self.rect = self.rect.move(0, self.speed)
            elif self.direction == 'L':
                self.img = self.tank.subsurface((0, 96), (48, 48))
                self.rect = self.rect.move(0-self.speed, 0)
            elif self.direction == 'R':
                self.img = self.tank.subsurface((0, 144), (48, 48))
                self.rect = self.rect.move(self.speed, 0)
            if self.isblocked():
                self.rect = rect
                self.direction = random.choice(['U', 'D', 'L', 'R'])
                print(self.direction)

class Map():
	def __init__(self):
		self.brickGroup = pygame.sprite.Group()
		self.stage()

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



def main():
    pygame.init()
    screen = pygame.display.set_mode((630, 630))
    screen.fill((0, 0, 0))
    clock = pygame.time.Clock()
    # 精灵组
    tanksGroup = pygame.sprite.Group()
    mytanksGroup = pygame.sprite.Group()
    enemytanksGroup = pygame.sprite.Group()
    # 敌方坦克总数量
    enemytanks_total = 60     
	# 场上存在的敌方坦克总数量
    enemytanks_now = 0
    # 场上可以存在的敌方坦克总数量
    enemytanks_now_max = 6
    # 定义生成敌方坦克事件
    genEnemyEvent = pygame.constants.USEREVENT
    pygame.time.set_timer(genEnemyEvent, 100)
    mytank = myTank(24 * 8, 24 * 24, 3)
    tanksGroup.add(mytank)
    mytanksGroup.add(mytank)
    map = Map()
    for x in range(0, 3):
        if enemytanks_total > 0:
            enemytank = enemyTank(x * 12 * 24, 3, 3)
            tanksGroup.add(enemytank)
            enemytanksGroup.add(enemytank)
            enemytanks_now += 1
            enemytanks_total -= 1
            pygame.display.flip()
    running = True
    # 游戏主循环
    while running:
        if enemytanks_total < 1 and enemytanks_now < 1:
            running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == genEnemyEvent:
                if enemytanks_total > 0:
                    if enemytanks_now < enemytanks_now_max:
                        x = random.randint(0, 2)
                        enemytank = enemyTank(x * 12 * 24, 3, 3)
                        if not pygame.sprite.spritecollide(enemytank, tanksGroup, False, None):
                            tanksGroup.add(enemytank)
                            enemytanksGroup.add(enemytank)
                            enemytanks_now += 1
                            enemytanks_total -= 1
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    print('K_left')
                    mytank.direction = 'L'
                    mytank.stop = False
                elif event.key == pygame.K_RIGHT:
                    mytank.direction = 'R'
                    mytank.stop = False
                elif event.key == pygame.K_UP:
                    mytank.direction = 'U'
                    mytank.stop = False
                elif event.key == pygame.K_DOWN:
                    mytank.direction = 'D'
                    mytank.stop = False

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    mytank.stop = True
        # 背景
        screen.fill((0, 0, 0))
        # 砖墙
        for each in map.brickGroup:
            screen.blit(each.img, each.rect)
        # 我方坦克
        if mytank in mytanksGroup:
            if not mytank.stop:
                tanksGroup.remove(mytank)
                # mytank.move(tanksGroup, map.brickGroup)
                mytank.move()
                tanksGroup.add(mytank)
            screen.blit(mytank.img, mytank.rect)
        #敌方坦克 
        for each in enemytanksGroup:
            screen.blit(each.img, each.rect)
            if not each.stop:
                tanksGroup.remove(each)
                each.move()
                tanksGroup.add(each)

        pygame.display.flip()
        clock.tick(30)
        print('%d %d' % (mytank.rect.right, mytank.rect.top))
    # 结束界面
    screen.fill((0, 0, 0))
    img = pygame.image.load("./images/others/gameover.png")
    rect = img.get_rect()
    rect.midtop = (624/2, 624/2)
    screen.blit(img, rect)
    pygame.display.update() 
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

if __name__ == "__main__":
    main()