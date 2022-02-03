import random
import engine
import Global_Variables as gv
import pygame as pg


class Monster:
    def __init__(self, x, y):
        self.rect = pg.Rect(x, y, 32, 32)
        self.cooldown = 0

    def track(self, tracked):
        player = gv.get("player")
        monsters = gv.get("monsters")
        level = gv.get("level")
        bullets = gv.get("bullets")
        sidebar = gv.get("sidebar")
        window = gv.get("window")
        placables = gv.get("placables")
        current_placable = gv.get("current_placable")
        window.fill(pg.Color("BLACK"))

        x_, y_, w_, h_ = tracked.rect
        x, y, w, h = self.rect
        if player.night < player.time < player.day:
            mult = 1.5
        else:
            mult = 1

        directions = [
            [(x - round(mult * self.speed), y), (x - round(mult * self.speed) - x_) ** 2 + (y - y_) ** 2],
            [(x + round(mult * self.speed), y), (x + round(mult * self.speed) - x_) ** 2 + (y - y_) ** 2],
            [(x, y - round(mult * self.speed)), (x - x_) ** 2 + (y - round(mult * self.speed) - y_) ** 2],
            [(x, y + round(mult * self.speed)), (x - x_) ** 2 + (y + round(mult * self.speed) - y_) ** 2],
        ]
        min_path = directions[0]
        for direction in directions:
            if direction[1] <= min_path[1]:
                min_path = direction

        new_rect = (min_path[0][0], min_path[0][1], w, h)

        def check_collision(new_rect):
            for monster in monsters:
                x, y, w, h = monster.rect
                if pg.Rect(x, y, w, h).colliderect(pg.Rect(new_rect)) and monster != self:
                    return False
            else:
                return True

        if not check_collision(new_rect):
            random_choice = random.choice(directions)
            new_rect = pg.Rect(random_choice[0], random_choice[1], w, h)
            if not check_collision(new_rect):
                return
        else:
            for row in level:
                for tile in row:
                    x_, y_, w_, h_ = tile.rect
                    if pg.Rect(x_, y_, w_, h_).colliderect(pg.Rect(new_rect)) and "monster" not in tile.collision:
                        return

            self.rect = pg.Rect(new_rect)

        gv.set("player", player)
        gv.set("monsters", monsters)
        gv.set("level", level)
        gv.set("bullets", bullets)
        gv.set("sidebar", sidebar)
        gv.set("placables", placables)
        gv.set("window", window)
        gv.set("current_placable", current_placable)

    def attack(self, attacked):
        if pg.Rect(self.rect).colliderect(pg.Rect(attacked.rect)) and self.cooldown == 0:
            self.cooldown = 25
            attacked.health -= int(self.damage / attacked.defense)


class Spider(Monster):
    def __init__(self, x, y, health):
        super(Spider, self).__init__(x, y)
        self.speed = 2
        self.health = 50
        self.damage = 10

    def draw(self, window):
        sprite = pg.image.load("sprites/spider.png")
        window.blit(sprite, self.rect)

    def tick(self, level, player, monsters):
        if random.randint(1, 3) != 2:
            return
        super().track(player)
        if self.cooldown > 0:
            self.cooldown -= 1
        self.attack(player)
        for row in level:
            for tile in row:
                tile.tick()

    def interact1(self, level, monsters, player, damage=None):
        if damage is None:
            self.health -= player.damage
        else:
            self.health -= damage
        if self.health <= 0:
            monsters.remove(self)
            player.inventory["silk"] += random.randint(0, 1)

    def interact2(self, level, monsters, player):
        pass


class Elite_Spider(Monster):
    def __init__(self, x, y, health):
        super(Elite_Spider, self).__init__(x, y)
        self.speed = 3
        self.health = 120
        self.damage = 15

    def draw(self, window):
        sprite = pg.image.load("sprites/elite_spider.png")
        window.blit(sprite, self.rect)

    def tick(self, level, player, monsters):
        if random.randint(1, 3) != 2:
            return
        super().track(player)
        if self.cooldown > 0:
            self.cooldown -= 1
        self.attack(player)
        for row in level:
            for tile in row:
                tile.tick()

    def interact1(self, level, monsters, player, damage=None):
        if damage is None:
            self.health -= player.damage
        else:
            self.health -= damage
        if self.health <= 0:
            monsters.remove(self)
            player.inventory["silk"] += random.randint(2, 3)

    def interact2(self, level, monsters, player):
        pass