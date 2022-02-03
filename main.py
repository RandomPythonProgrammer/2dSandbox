import pygame as pg
import engine
import Global_Variables as gv
import blocks
import os
import mobs
import _thread
from engine import BreakLoop


def main():
    threading = False
    pg.init()
    screen = (416, 288)
    gv.set("window", pg.display.set_mode(screen))
    pg.display.set_caption("Game")
    clock = pg.time.Clock()

    gameIcon = pg.image.load('sprites/mountain_tile10.png').convert_alpha()

    for sprite in os.listdir("sprites"):
        try:
            filename, extension = os.path.splitext(sprite)
            gv.set(filename + "_sprite", pg.image.load(f"sprites/{sprite}.").convert_alpha())
        except:
            pass

    pg.display.set_icon(gameIcon)

    gv.set("game_over", False)

    level = []

    gv.set("bullets", [])

    gv.set("game_over", False)

    while len(level) < 181:
        row = []
        while len(row) < 181:
            tile_x = 32 * len(row)
            tile_y = 32 * len(level)
            row.append(blocks.Grass(tile_x, tile_y))
        level.append(row)

    player = engine.Player(128, 128)
    gv.set("sidebar", engine.Sidebar())
    level = engine.generate_element(level, 20, 30, 20, 30, 2, blocks.Grass, blocks.Water)
    level = engine.generate_element(level, 15, 20, 20, 30, 2, blocks.Grass, blocks.Sand)
    level = engine.generate_element(level, 15, 25, 20, 30, 10, blocks.Grass, blocks.Mountain)
    level = engine.generate_element(level, 15, 25, 20, 30, 10, blocks.Sand, blocks.Mountain)
    level = engine.generate_element(level, 20, 40, 100, 120, 2, blocks.Grass, blocks.Tree)

    gv.set("monsters", [])

    gv.set("placables", {"sapling": (0, 1, 0, 0, blocks.Tree), "wood": (5, 0, 0, 0, blocks.Wood),
                 "door": (8, 0, 0, 0, blocks.Door), "window": (4, 0, 0, 0, blocks.Window),
                 "fence": (0, 0, 3, 0, blocks.Fence), "iron_wall": (0, 0, 5, 0, blocks.Iron_Wall),
                 "bed": (5, 0, 0, 5, blocks.Bed)})

    gv.set("current_placable", "sapling")

    for row in level:
        for tile in row:
            x, y, w, h = tile.rect
            tile.rect = pg.Rect(x - 1600, y - 1600, w, h)

    for row in level:
        for tile in row:
            if tile.rect.colliderect(player.rect):
                x, y, w, h = tile.rect
                level[level.index(row)][row.index(tile)] = blocks.Grass(x, y)

    gv.set("level", level)
    gv.set("player", player)

    while not gv.get("game_over"):
        clock.tick(120)

        if gv.get("player").health <= 0:
            try:
                gv.set("level", engine.load("saves", "level.pkl"))
                gv.set("player", engine.load("saves", "player.pkl"))
                gv.set("monsters", engine.load("saves", "monsters.pkl"))
            except:
                gv.set("game_over", True)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                gv.set("game_over", True)

        pressed_keys = pg.key.get_pressed()
        mods = pg.key.get_mods()

        if pressed_keys[pg.K_e]:
            if threading:
                _thread.start_new_thread(engine.move_world, (0, player.speed, "up"))
            else:
                engine.move_world(0, player.speed, "up")

        elif pressed_keys[pg.K_s]:
            if threading:
                _thread.start_new_thread(engine.move_world, (player.speed, 0, "left"))
            else:
                engine.move_world(player.speed, 0, "left")

        elif pressed_keys[pg.K_d]:
            if threading:
                _thread.start_new_thread(engine.move_world, (0, -player.speed, "down"))
            else:
                engine.move_world(0, -player.speed, "down")

        elif pressed_keys[pg.K_f]:
            if threading:
                _thread.start_new_thread(engine.move_world, (-player.speed, 0, "right"))
            else:
                engine.move_world(-player.speed, 0, "right")

        player = gv.get("player")
        monsters = gv.get("monsters")
        level = gv.get("level")
        bullets = gv.get("bullets")
        if pressed_keys[pg.K_j] and player.cooldown == 0:
            try:
                player.cooldown = 20
                if player.direction == "up":
                    x, y, w, h = player.rect
                    collision_box = engine.CollisionBox(x, y - 32)
                    for row in level:
                        for tile in row:
                            if pg.Rect(tile.rect).colliderect(collision_box.rect):
                                tile.interact1(level, monsters, player)
                                raise BreakLoop
                    for monster in monsters:
                        if pg.Rect(monster.rect).colliderect(collision_box.rect):
                            monster.interact1(level, monsters, player)
                            raise BreakLoop

                elif player.direction == "right":
                    x, y, w, h = player.rect
                    collision_box = engine.CollisionBox(x + 32, y)
                    for row in level:
                        for tile in row:
                            if pg.Rect(tile.rect).colliderect(collision_box.rect):
                                tile.interact1(level, monsters, player)
                                raise BreakLoop
                    for monster in monsters:
                        if pg.Rect(monster.rect).colliderect(collision_box.rect):
                            monster.interact1(level, monsters, player)
                            raise BreakLoop

                elif player.direction == "down":
                    x, y, w, h = player.rect
                    collision_box = engine.CollisionBox(x, y + 32)
                    for row in level:
                        for tile in row:
                            if pg.Rect(tile.rect).colliderect(collision_box.rect):
                                tile.interact1(level, monsters, player)
                                raise BreakLoop
                    for monster in monsters:
                        if pg.Rect(monster.rect).colliderect(collision_box.rect):
                            monster.interact1(level, monsters, player)
                            raise BreakLoop

                elif player.direction == "left":
                    x, y, w, h = player.rect
                    collision_box = engine.CollisionBox(x - 32, y)
                    for row in level:
                        for tile in row:
                            if pg.Rect(tile.rect).colliderect(collision_box.rect):
                                tile.interact1(level, monsters, player)
                                raise BreakLoop
                    for monster in monsters:
                        if pg.Rect(monster.rect).colliderect(collision_box.rect):
                            monster.interact1(level, monsters, player)
                            raise BreakLoop

            except BreakLoop:
                pass

            gv.set("player", player)
            gv.set("monsters", monsters)
            gv.set("level", level)
            gv.set("bullets", bullets)

        player = gv.get("player")
        monsters = gv.get("monsters")
        level = gv.get("level")
        current_placable = gv.get("current_placable")
        if pressed_keys[pg.K_k] and player.cooldown == 0:
            player.cooldown = 20
            if player.direction == "up":
                x, y, w, h = player.rect
                collision_box = engine.CollisionBox(x, y - 32)
                for row in level:
                    for tile in row:
                        if pg.Rect(tile.rect).colliderect(collision_box.rect):
                            tile.interact2(level, monsters, player)
                for monster in monsters:
                    if pg.Rect(monster.rect).colliderect(collision_box.rect):
                        monster.interact2(level, monsters, player)

            elif player.direction == "right":
                x, y, w, h = player.rect
                collision_box = engine.CollisionBox(x + 32, y)
                for row in level:
                    for tile in row:
                        if pg.Rect(tile.rect).colliderect(collision_box.rect):
                            tile.interact2(level, monsters, player)
                for monster in monsters:
                    if pg.Rect(monster.rect).colliderect(collision_box.rect):
                        monster.interact2(level, monsters, player)

            elif player.direction == "down":
                x, y, w, h = player.rect
                collision_box = engine.CollisionBox(x, y + 32)
                for row in level:
                    for tile in row:
                        if pg.Rect(tile.rect).colliderect(collision_box.rect):
                            tile.interact2(level, monsters, player)
                for monster in monsters:
                    if pg.Rect(monster.rect).colliderect(collision_box.rect):
                        monster.interact2(level, monsters, player)

            elif player.direction == "left":
                x, y, w, h = player.rect
                collision_box = engine.CollisionBox(x - 32, y)
                for row in level:
                    for tile in row:
                        if pg.Rect(tile.rect).colliderect(collision_box.rect):
                            tile.interact2(level, monsters, player)
                for monster in monsters:
                    if pg.Rect(monster.rect).colliderect(collision_box.rect):
                        monster.interact2(level, monsters, player)
            gv.set("player", player)
            gv.set("monsters", monsters)
            gv.set("level", level)
            gv.set("current_placable", current_placable)

        if pressed_keys[pg.K_o]:
            player = gv.get("player")
            monsters = gv.get("monsters")
            level = gv.get("level")
            if player.direction == "up":
                x, y, w, h = player.rect
                collision_box = engine.CollisionBox(x, y - 16)
                for row in level:
                    for tile in row:
                        x, y, w, h = tile.rect
                        if pg.Rect(tile.rect).colliderect(collision_box.rect) and tile.buildable and not pg.Rect(
                                tile.rect).colliderect(player.rect):
                            wood, apple, metal, silk, block = gv.get("placables")[current_placable]
                            tile_index = row.index(tile)
                            row_index = level.index(row)
                            if player.inventory["wood"] - wood >= 0:
                                if player.inventory["apple"] - apple >= 0:
                                    if player.inventory["metal"] - metal >= 0:
                                        if player.inventory["silk"] - silk >= 0:
                                            player.inventory["metal"] -= metal
                                            player.inventory["apple"] -= apple
                                            player.inventory["wood"] -= wood
                                            player.inventory["silk"] -= silk
                                            level[row_index][tile_index] = block(x, y, 1, type(tile))

            elif player.direction == "right":
                x, y, w, h = player.rect
                collision_box = engine.CollisionBox(x + 32, y)
                for row in level:
                    for tile in row:
                        x, y, w, h = tile.rect
                        if pg.Rect(tile.rect).colliderect(collision_box.rect) and tile.buildable and not pg.Rect(
                                tile.rect).colliderect(player.rect):
                            wood, apple, metal, silk, block = gv.get("placables")[current_placable]
                            tile_index = row.index(tile)
                            row_index = level.index(row)
                            if player.inventory["wood"] - wood >= 0:
                                if player.inventory["apple"] - apple >= 0:
                                    if player.inventory["metal"] - metal >= 0:
                                        if player.inventory["silk"] - silk >= 0:
                                            player.inventory["metal"] -= metal
                                            player.inventory["apple"] -= apple
                                            player.inventory["wood"] -= wood
                                            player.inventory["silk"] -= silk
                                            level[row_index][tile_index] = block(x, y, 1, type(tile))

            elif player.direction == "down":
                x, y, w, h = player.rect
                collision_box = engine.CollisionBox(x, y + 32)
                for row in level:
                    for tile in row:
                        x, y, w, h = tile.rect
                        if pg.Rect(tile.rect).colliderect(collision_box.rect) and tile.buildable and not pg.Rect(
                                tile.rect).colliderect(player.rect):
                            wood, apple, metal, silk, block = gv.get("placables")[current_placable]
                            tile_index = row.index(tile)
                            row_index = level.index(row)
                            if player.inventory["wood"] - wood >= 0:
                                if player.inventory["apple"] - apple >= 0:
                                    if player.inventory["metal"] - metal >= 0:
                                        if player.inventory["silk"] - silk >= 0:
                                            player.inventory["metal"] -= metal
                                            player.inventory["apple"] -= apple
                                            player.inventory["wood"] -= wood
                                            player.inventory["silk"] -= silk
                                            level[row_index][tile_index] = block(x, y, 1, type(tile))

            elif player.direction == "left":
                x, y, w, h = player.rect
                collision_box = engine.CollisionBox(x - 16, y)
                for row in level:
                    for tile in row:
                        x, y, w, h = tile.rect
                        if pg.Rect(tile.rect).colliderect(collision_box.rect) and tile.buildable and not pg.Rect(
                                tile.rect).colliderect(player.rect):
                            wood, apple, metal, silk, block = gv.get("placables")[current_placable]
                            tile_index = row.index(tile)
                            row_index = level.index(row)
                            if player.inventory["wood"] - wood >= 0:
                                if player.inventory["apple"] - apple >= 0:
                                    if player.inventory["metal"] - metal >= 0:
                                        if player.inventory["silk"] - silk >= 0:
                                            player.inventory["metal"] -= metal
                                            player.inventory["apple"] -= apple
                                            player.inventory["wood"] -= wood
                                            player.inventory["silk"] -= silk
                                            level[row_index][tile_index] = block(x, y, 1, type(tile))
            gv.set("player", player)
            gv.set("monsters", monsters)
            gv.set("level", level)

        if pressed_keys[pg.K_u]:
            player = gv.get("player")
            monsters = gv.get("monsters")
            level = gv.get("level")
            current_placable = gv.get("current_placable")
            if player.switch_delay == 0:
                player.switch_delay = 3
                list_ = []
                for key in gv.get("placables").keys():
                    list_.append(key)
                try:
                    current_placable = list_[list_.index(current_placable) - 1]
                except IndexError:
                    pass
            gv.set("player", player)
            gv.set("monsters", monsters)
            gv.set("level", level)
            gv.set("current_placable", current_placable)

        if pressed_keys[pg.K_i]:
            player = gv.get("player")
            monsters = gv.get("monsters")
            level = gv.get("level")
            if player.inventory["apple"] > 0:
                if player.health < 100:
                    player.inventory["apple"] -= 1
                    player.health += 1
                if player.health > 100:
                    player.health = 100
            gv.set("player", player)
            gv.set("monsters", monsters)
            gv.set("level", level)

        if pressed_keys[pg.K_z]:
            player = gv.get("player")
            monsters = gv.get("monsters")
            level = gv.get("level")
            content = input("\ncommand:\n")
            command, arg1, arg2 = tuple(content.split(" "))
            if command == "give":
                player.inventory[arg1] += int(arg2)
            if command == "health":
                if arg1 == "set":
                    player.health = int(arg2)
                if arg1 == "give":
                    player.health += int(arg2)
            if command == "time":
                if arg1 == "set":
                    player.time = int(arg2)
                if arg1 == "add":
                    player.time += int(arg2)
            if command == "spawn":
                if arg1 == "spider":
                    for i in range(0, int(arg2)):
                        x, y, w, h = player.rect
                        monsters = gv.get("monsters")
                        monsters.append(mobs.Spider(x, y, 100))
                        gv.set("monsters", monsters)
                if arg1 == "elite_spider":
                    for i in range(1, int(arg2)):
                        engine.spawn_elite_spiders(level, monsters, player, 70, 90)
            gv.set("player", player)
            gv.set("monsters", monsters)
            gv.set("level", level)

        if pressed_keys[pg.K_r]:
            player = gv.get("player")
            monsters = gv.get("monsters")
            level = gv.get("level")
            engine.save("saves", "level.pkl", level)
            engine.save("saves", "player.pkl", player)
            engine.save("saves", "monsters.pkl", monsters)
            engine.save("saves", "bullets.pkl", bullets)
            gv.set("player", player)
            gv.set("monsters", monsters)
            gv.set("level", level)

        if pressed_keys[pg.K_t]:
            player = gv.get("player")
            monsters = gv.get("monsters")
            level = gv.get("level")
            level = engine.load("saves", "level.pkl")
            player = engine.load("saves", "player.pkl")
            monsters = engine.load("saves", "monsters.pkl")
            bullets = engine.load("saves", "bullets.pkl")
            gv.set("player", player)
            gv.set("monsters", monsters)
            gv.set("level", level)

        if pressed_keys[pg.K_p]:
            player = gv.get("player")
            monsters = gv.get("monsters")
            level = gv.get("level")
            if player.inventory["metal"] - 1 >= 0:
                if player.cooldown == 0:
                    player.inventory["metal"] -= 1
                    player.cooldown = 5
                    x, y, w, h = player.rect
                    bullets.append(engine.Bullet(x, y, player.direction))
            gv.set("player", player)
            gv.set("monsters", monsters)
            gv.set("level", level)

        if pressed_keys[pg.K_q]:
            if threading:
                threading = False
                print("threading off")
            else:
                threading = True
                print("threading on")

        player = gv.get("player")

        _thread.start_new_thread(engine.tick, (None, None))

        engine.draw_scene()

        player.walking = False

        gv.set("player", player)


if __name__ == '__main__':
    main()
