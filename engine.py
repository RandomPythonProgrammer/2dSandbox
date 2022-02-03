import random
import pygame as pg
import pickle
import Global_Variables as gv
import mobs


class BreakLoop(Exception):
    pass


class Player:
    def __init__(self, x, y):
        self.rect = pg.Rect(x, y, 32, 32)
        self.direction = "up"
        self.cooldown = 0
        self.health = 100
        self.switch_delay = 2
        self.inventory = {"wood": 0, "apple": 0, "metal": 0, "silk": 0}
        self.time = 0
        self.night = 2000
        self.day = 4000
        self.next_day = 6000
        self.damage = 20
        self.defense = 2
        self.speed = 4
        self.walking = False
        self.walkcount = 0
        self.down = [pg.image.load("sprites/player_D1.png").convert_alpha(),
                     pg.image.load("sprites/player_D2.png").convert_alpha(),
                     pg.image.load("sprites/player_D3.png").convert_alpha(),
                     pg.image.load("sprites/player_D4.png").convert_alpha()]

        self.up = [pg.image.load("sprites/player_U1.png").convert_alpha(),
                   pg.image.load("sprites/player_U2.png").convert_alpha(),
                   pg.image.load("sprites/player_U3.png").convert_alpha(),
                   pg.image.load("sprites/player_U4.png").convert_alpha()]

        self.right = [pg.image.load("sprites/player_R1.png").convert_alpha(),
                     pg.image.load("sprites/player_R2.png").convert_alpha(),
                     pg.image.load("sprites/player_R3.png").convert_alpha(),
                     pg.image.load("sprites/player_R4.png").convert_alpha()]

        self.left = [pg.image.load("sprites/player_L1.png").convert_alpha(),
                   pg.image.load("sprites/player_L2.png").convert_alpha(),
                   pg.image.load("sprites/player_L3.png").convert_alpha(),
                   pg.image.load("sprites/player_L4.png").convert_alpha()]

    def __repr__(self):
        x, y, w, h = self.rect
        return f"x:{x}, y{y}, w:{w}, h:{h}"

    def draw(self, window):
        if self.walkcount + 1 >= 12:
            self.walkcount = 0

        if self.direction == "up":
            if self.walking:
                window.blit(self.up[self.walkcount // 3], self.rect)
                self.walkcount += 1
            else:
                window.blit(gv.get("player_up_sprite"), self.rect)
                self.walkcount = 0
        if self.direction == "right":
            if self.walking:
                window.blit(self.right[self.walkcount // 3], self.rect)
                self.walkcount += 1
            else:
                window.blit(gv.get("player_right_sprite"), self.rect)
                self.walkcount = 0
        if self.direction == "down":
            if self.walking:
                window.blit(self.down[self.walkcount // 3], self.rect)
                self.walkcount += 1
            else:
                window.blit(gv.get("player_down_sprite"), self.rect)
                self.walkcount = 0
        if self.direction == "left":
            if self.walking:
                window.blit(self.left[self.walkcount // 3], self.rect)
                self.walkcount += 1
            else:
                window.blit(gv.get("player_left_sprite"), self.rect)
                self.walkcount = 0


class Bullet:
    def __init__(self, x, y, direction):
        self.rect = pg.Rect(x, y, 32, 32)
        self.direction = direction
        self.speed = 12
        self.damage = 40

    def __repr__(self):
        x, y, w, h = self.rect
        return f"x:{x}, y:{y}, w:{w}, h:{h}"

    def tick(self, monsters, level, player, bullets):
        if self.direction == "up":
            x, y, w, h = self.rect
            self.rect = pg.Rect(x, y - self.speed, w, h)
        if self.direction == "right":
            x, y, w, h = self.rect
            self.rect = pg.Rect(x + self.speed, y, w, h)
        if self.direction == "down":
            x, y, w, h = self.rect
            self.rect = pg.Rect(x, y + self.speed, w, h)
        if self.direction == "left":
            x, y, w, h = self.rect
            self.rect = pg.Rect(x - self.speed, y, w, h)
        x, y, w, h = self.rect
        collision = pg.Rect(x - 4, y - 4, w / 2, h / 2)
        break_ = False
        for monster in monsters:
            if collision.colliderect(monster.rect):
                monster.interact1(level, monsters, player, damage=self.damage)
                try:
                    bullets.remove(self)
                except ValueError:
                    pass
        for row in level:
            if break_:
                break
            for tile in row:
                if "bullet" not in tile.collision:
                    if pg.Rect(tile.rect).colliderect(self.rect):
                        try:
                            bullets.remove(self)
                        except ValueError:
                            pass
                        tile.interact1(level, monsters, player)
                        break_ = True
                        break

    def draw(self, window):
        window.blit(gv.get("bullet_sprite"), self.rect)


class Sidebar:
    def __init__(self):
        self.rect = pg.Rect(288, 0, 128, 288)
        self.sapling = pg.image.load("sprites/tree_tile1.png").convert_alpha()
        self.wood = pg.image.load("sprites/wood_tile.png").convert_alpha()
        self.door = pg.image.load("sprites/door_item.png").convert_alpha()
        self.window = pg.image.load("sprites/window_item.png").convert_alpha()
        self.fence = pg.image.load("sprites/fence_item.png").convert_alpha()
        self.iron_wall = pg.image.load("sprites/iron_wall_item.png").convert_alpha()
        self.bed = pg.image.load("sprites/bed_item.png").convert_alpha()

        self.apple_sprite = pg.image.load("sprites/apple_item.png").convert_alpha()
        self.wood_sprite = pg.image.load("sprites/wood_item.png").convert_alpha()
        self.metal_sprite = pg.image.load("sprites/metal_item.png").convert_alpha()
        self.silk_sprite = pg.image.load("sprites/silk_item.png").convert_alpha()

        self.frame = pg.image.load("sprites/item_frame.png").convert_alpha()
        self.inventory = pg.image.load("sprites/inventory.png").convert()

    def draw(self, window, player, current_placable, placables):
        pg.draw.rect(window, pg.Color(195, 110, 50), self.rect)
        font = pg.font.Font('sprites/arial.ttf', 32)
        text = font.render(str(player.health), True, pg.Color("RED"))
        window.blit(text, (336, 0))
        heart_sprite = pg.image.load("sprites/health.png").convert_alpha()
        window.blit(heart_sprite, (300, 2))
        font = pg.font.Font('sprites/arial.ttf', 16)

        window.blit(self.inventory, (304, 64))


class CollisionBox:
    def __init__(self, x, y):
        self.rect = pg.Rect(x, y, 8, 8)


def draw_scene():
    player = gv.get("player")
    monsters = gv.get("monsters")
    level = gv.get("level")
    bullets = gv.get("bullets")
    sidebar = gv.get("sidebar")
    window = gv.get("window")
    placables = gv.get("placables")
    current_placable = gv.get("current_placable")
    window.fill(pg.Color("BLACK"))

    for row in level:
        for tile in row:
            tile_x, tile_y, tile_w, tile_h = tile.rect
            player_x, player_y, player_w, tile_h = player.rect
            if abs(player_y - tile_y) < 224 and abs(player_x - tile_x) < 224:
                tile.draw(window)
    player.draw(window)
    for monster in monsters:
        monster.draw(window)
    for bullet in bullets:
        bullet_x, bullet_y, bullet_w, bullet_h = bullet.rect
        if abs(player_y - bullet_y) < 224 and abs(player_x - bullet_x) < 224:
            bullet.draw(window)
    sidebar.draw(window, player, current_placable, placables)
    night_image = pg.Surface((288, 288), pg.SRCALPHA)
    if player.time < player.day:
        if player.time / 15 < 200:
            pg.draw.rect(night_image, (0, 0, 0, player.time / 15), pg.Rect(0, 0, 288, 288))
        else:
            pg.draw.rect(night_image, (0, 0, 0, 200), pg.Rect(0, 0, 288, 288))
    if player.time > player.day:
        if (6000 - player.time) / 15 < 200:
            pg.draw.rect(night_image, (0, 0, 0, (6000 - player.time) / 15), pg.Rect(0, 0, 288, 288))
        else:
            pg.draw.rect(night_image, (0, 0, 0, 200, pg.Rect(0, 0, 288, 288)))

    window.blit(night_image, (0, 0))
    pg.display.update()

    gv.set("player", player)
    gv.set("monsters", monsters)
    gv.set("level", level)
    gv.set("bullets", bullets)
    gv.set("sidebar", sidebar)
    gv.set("placables", placables)
    gv.set("window", window)
    gv.set("current_placable", current_placable)


def spawn_spiders(level, monsters, player, num1, num2):
    if random.randint(1, 3) != 2:
        return monsters
    if len(monsters) > 10:
        return
    for i in range(num1, num2):
        seed_y = random.randint(0, 100)
        seed_x = random.randint(0, 100)
        player_x, player_y, w, h = player.rect
        tile = level[seed_y][seed_x]
        if "monster" in tile.collision:
            tile_x, tile_y, w, h = tile.rect
            if abs(player_y - tile_y) < 224 and abs(player_x - tile_x) < 224:
                if abs(player_y - tile_y) > 64 and abs(player_x - tile_x) > 64:
                    monsters.append(mobs.Spider(tile_x, tile_y, 100))
    return monsters


def spawn_elite_spiders(level, monsters, player, num1, num2):
    if random.randint(1, 4) != 2:
        return monsters
    if len(monsters) > 10:
        return
    for i in range(num1, num2):
        seed_y = random.randint(0, 100)
        seed_x = random.randint(0, 100)
        player_x, player_y, w, h = player.rect
        tile = level[seed_y][seed_x]
        if "monster" in tile.collision:
            tile_x, tile_y, w, h = tile.rect
            if abs(player_y - tile_y) < 224 and abs(player_x - tile_x) < 224:
                if abs(player_y - tile_y) > 64 and abs(player_x - tile_x) > 64:
                    monsters.append(mobs.Elite_Spider(tile_x, tile_y, 100))
    return monsters


def tick(*args):
    player = gv.get("player")
    monsters = gv.get("monsters")
    level = gv.get("level")
    bullets = gv.get("bullets")
    sidebar = gv.get("sidebar")
    window = gv.get("window")
    placables = gv.get("placables")
    current_placable = gv.get("current_placable")

    for monster in monsters:
        monster.tick(level, player, monsters)
    if player.time < player.night:
        if random.randint(1, 120) == 10:
            spawn_spiders(level, monsters, player, 70, 90)
    elif player.time > player.night:
        if random.randint(1, 20) == 10:
            spawn_spiders(level, monsters, player, 70, 90)
        if random.randint(1, 25) == 10:
            spawn_elite_spiders(level, monsters, player, 65, 85)

    if player.cooldown > 0:
        player.cooldown -= 1
    if random.randint(1, 250) == 1:
        if player.health < 100:
            player.health += 1
    if player.switch_delay > 0:
        player.switch_delay -= 1
    player.time += 1
    if player.time > player.next_day:
        player.time = 0

    for bullet in bullets:
        bullet.tick(monsters, level, player, bullets)

    player_x, player_y, w, h = player.rect

    for bullet in bullets:
        bullet_x, bullet_y, bullet_w, bullet_h = bullet.rect
        if abs(player_y - bullet_y) > 800 or abs(player_x - bullet_x) > 800:
            bullets.remove(bullet)

    for monster in monsters:
        _x, _y, _w, _h = monster.rect
        if abs(player_y - _y) > 800 or abs(player_x - _x) > 800:
            monsters.remove(monster)

    gv.set("player", player)
    gv.set("monsters", monsters)
    gv.set("level", level)
    gv.set("bullets", bullets)
    gv.set("sidebar", sidebar)
    gv.set("placables", placables)
    gv.set("window", window)
    gv.set("current_placable", current_placable)


def generate_element(level, num1, num2, num3, num4, stage, replaced, replacement):
    for i in range(num1, num2):
        seed_y = random.randint(0, 100)
        seed_x = random.randint(0, 100)
        if type(level[seed_y][seed_x]) == replaced:
            level[seed_y][seed_x] = replacement(seed_x * 32, seed_y * 32, stage)

    for i in range(num3, num4):
        for row in level:
            for tile in row:
                if type(tile) == replacement:
                    x, y, w, h = tile.rect
                    tile_x = int(x / 32)
                    tile_y = int(y / 32)
                    position = random.choice([1, 2, 3, 4])

                    try:

                        if position == 1:
                            if type(level[tile_y - 1][tile_x]) == replaced:
                                if 3232 > x > 0 and 3232 > y - 32 > 0:
                                    level[tile_y - 1][tile_x] = replacement(x, y - 32, stage, previous_tile=replaced)

                        if position == 2:
                            if type(level[tile_y + 1][tile_x]) == replaced:
                                if 3232 > x > 0 and 3232 > y + 32 > 0:
                                    level[tile_y + 1][tile_x] = replacement(x, y + 32, stage, previous_tile=replaced)

                        if position == 3:
                            if type(level[tile_y][tile_x - 1]) == replaced:
                                if 3232 > x - 32 > 0 and 3232 > y > 0:
                                    level[tile_y][tile_x - 1] = replacement(x - 32, y, stage, previous_tile=replaced)

                        if position == 4:
                            if type(level[tile_y][tile_x - 1]) == replaced:
                                if 3232 > x + 32 > 0 and 3232 > y > 0:
                                    level[tile_y][tile_x + 1] = replacement(x + 32, y, stage, previous_tile=replaced)

                    except IndexError:
                        continue

    return level


def save(filepath, filename, info):
    with open(f"{filepath}/{filename}", "wb") as file:
        pickle.dump(info, file)


def load(filepath, filename):
    with open(f"{filepath}/{filename}", "rb") as file:
        return pickle.load(file)


def move_world(x_change, y_change, direction):
    player = gv.get("player")
    level = gv.get("level")
    monsters = gv.get("monsters")
    bullets = gv.get("bullets")
    player.walking = True
    player_x, player_y, player_w, player_h = player.rect
    new_rect = pg.Rect(player_x - x_change, player_y - y_change, player_w, player_h)
    if not pg.key.get_mods() & pg.KMOD_SHIFT:
        player.direction = direction
    for row in level:
        for tile in row:
            if pg.Rect(tile.rect).colliderect(new_rect) and "player" not in tile.collision:
                return
    for row in level:
        for tile in row:
            x, y, w, h, = tile.rect
            tile.rect = pg.Rect(x + x_change, y + y_change, w, h)
    for monster in monsters:
        x_, y_, w_, h_, = monster.rect
        monster.rect = pg.Rect(x_ + x_change, y_ + y_change, w_, h_)
    for bullet in bullets:
        x_, y_, w_, h_, = bullet.rect
        bullet.rect = pg.Rect(x_ + x_change, y_ + y_change, w_, h_)
    gv.set("player", player)
    gv.set("monsters", monsters)
    gv.set("level", level)
