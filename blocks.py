import engine
import random
import Global_Variables as gv
import pygame as pg


class Tile:
    def __init__(self, x, y, previous_tile=None):
        self.rect = pg.Rect(x, y, 32, 32)
        self.previous_tile = previous_tile


class Grass(Tile):
    def __init__(self, x, y, stage=None):
        super().__init__(x, y)
        self.collision = ["monster", "player", "bullet"]
        self.buildable = True

    def __repr__(self):
        return "grass"

    def draw(self, window):
        window.blit(gv.get("grass_tile_sprite"), self.rect)

    def interact1(self, level, monsters, player):
        pass

    def interact2(self, level, monsters, player):
        pass

    def tick(self):
        pass


class Sand(Tile):
    def __init__(self, x, y, stage=None, previous_tile=None):
        super().__init__(x, y, previous_tile)
        self.collision = ["monster", "player", "bullet"]
        self.buildable = True

    def __repr__(self):
        return "sand"

    def draw(self, window):
        window.blit(gv.get("sand_tile_sprite"), self.rect)

    def interact1(self, level, monsters, player):
        pass

    def interact2(self, level, monsters, player):
        pass

    def tick(self):
        pass


class Tree(Tile):
    def __init__(self, x, y, stage=1, previous_tile=Grass):
        super().__init__(x, y, previous_tile)
        self.collision = ["monster"]
        self.stage = stage
        self.buildable = False

    def __repr__(self):
        return "tree"

    def draw(self, window):
        previous_sprite = pg.image.load(f"sprites/{self.previous_tile(0, 0)}_tile.png").convert_alpha()
        window.blit(previous_sprite, self.rect)

        if self.stage == 2:

            window.blit(gv.get("tree_tile_sprite"), self.rect)
        else:

            window.blit(gv.get("tree_tile1_sprite"), self.rect)

    def interact1(self, level, monsters, player):
        for row in level:
            for tile in row:
                if tile == self:
                    x, y, w, h = tile.rect
                    level[level.index(row)][row.index(tile)] = Grass(x, y)
                    if self.stage == 2:
                        player.inventory["wood"] += random.randint(1, 5)
                        player.inventory["apple"] += random.randint(0, 3)

    def interact2(self, level, monsters, player):
        pass

    def tick(self):
        if random.randint(1, 20) == 2:
            if self.stage < 2:
                self.stage += 0.1


class Water(Tile):
    def __init__(self, x, y, stage=None, previous_tile=None):
        super().__init__(x, y, previous_tile)
        self.collision = ["bullet"]
        self.buildable = False

    def __repr__(self):
        return "water"

    def draw(self, window):
        window.blit(gv.get("water_sprite"), self.rect)

    def interact1(self, level, monsters, player):
        pass

    def interact2(self, level, monsters, player):
        pass

    def tick(self):
        pass


class Mountain(Tile):
    def __init__(self, x, y, stage=10, previous_tile=Grass):
        super().__init__(x, y, previous_tile)
        self.collision = ["monster"]
        self.stage = stage
        self.buildable = False

    def __repr__(self):
        return "mountain"

    def draw(self, window):
        previous_sprite = pg.image.load(f"sprites/{self.previous_tile(0, 0)}_tile.png").convert_alpha()
        window.blit(previous_sprite, self.rect)

        mountain_sprite = pg.image.load(f"sprites/mountain_tile{self.stage}.png").convert_alpha()
        window.blit(mountain_sprite, self.rect)

    def interact1(self, level, monsters, player):
        if random.randint(0, 3) == 1:
            player.inventory["metal"] += random.randint(0, 4)
        if random.randint(0, 1) == 1:
            self.stage -= 1
            if self.stage == 0:
                for row in level:
                    for tile in row:
                        if tile == self:
                            x, y, w, h = tile.rect
                            try:
                                level[level.index(row)][row.index(tile)] = self.previous_tile(x, y)
                            except TypeError:
                                level[level.index(row)][row.index(tile)] = Grass(x, y)

    def interact2(self, level, monsters, player):
        pass

    def tick(self):
        if random.randint(1, 250) == 2:
            if self.stage < 10:
                self.stage += 1


class Wood(Tile):
    def __init__(self, x, y, stage=None, previous_tile=None):
        super().__init__(x, y, previous_tile)
        self.collision = []
        self.buildable = False

    def __repr__(self):
        return "wood"

    def draw(self, window):
        window.blit(gv.get("wood_sprite"), self.rect)

    def interact1(self, level, monsters, player):
        for row in level:
            for tile in row:
                if tile == self:
                    x, y, w, h = tile.rect
                    level[level.index(row)][row.index(tile)] = self.previous_tile(x, y)
                    player.inventory["wood"] += random.randint(1, 5)

    def interact2(self, level, monsters, player):
        pass

    def tick(self):
        pass


class Door(Tile):
    def __init__(self, x, y, stage=None, previous_tile=None):
        super().__init__(x, y, previous_tile)
        self.collision = ["player"]
        self.buildable = False

    def __repr__(self):
        return "door"

    def draw(self, window):
        previous_sprite = pg.image.load(f"sprites/{self.previous_tile(0, 0)}_tile.png").convert_alpha()
        window.blit(previous_sprite, self.rect)

        window.blit(gv.get("door_sprite"), self.rect)

    def interact1(self, level, monsters, player):
        for row in level:
            for tile in row:
                if tile == self:
                    x, y, w, h = tile.rect
                    level[level.index(row)][row.index(tile)] = self.previous_tile(x, y)
                    player.inventory["wood"] += random.randint(1, 5)

    def interact2(self, level, monsters, player):
        pass

    def tick(self):
        pass


class Window(Tile):
    def __init__(self, x, y, stage=None, previous_tile=None):
        super().__init__(x, y, previous_tile)
        self.collision = []
        self.buildable = False

    def __repr__(self):
        return "window"

    def draw(self, window):
        previous_sprite = pg.image.load(f"sprites/{self.previous_tile(0, 0)}_tile.png").convert_alpha()
        window.blit(previous_sprite, self.rect)

        window.blit(gv.get("window_sprite"), self.rect)

    def interact1(self, level, monsters, player):
        for row in level:
            for tile in row:
                if tile == self:
                    x, y, w, h = tile.rect
                    level[level.index(row)][row.index(tile)] = self.previous_tile(x, y)
                    player.inventory["wood"] += random.randint(1, 5)

    def interact2(self, level, monsters, player):
        pass

    def tick(self):
        pass


class Fence(Tile):
    def __init__(self, x, y, stage=None, previous_tile=None):
        super().__init__(x, y, previous_tile)
        self.collision = []
        self.buildable = False

    def __repr__(self):
        return "fence"

    def draw(self, window):
        previous_sprite = pg.image.load(f"sprites/{self.previous_tile(0, 0)}_tile.png").convert_alpha()
        window.blit(previous_sprite, self.rect)

        window.blit(gv.get("fence_sprite"), self.rect)

    def interact1(self, level, monsters, player):
        for row in level:
            for tile in row:
                if tile == self:
                    x, y, w, h = tile.rect
                    level[level.index(row)][row.index(tile)] = self.previous_tile(x, y)
                    player.inventory["metal"] += random.randint(1, 2)

    def interact2(self, level, monsters, player):
        pass

    def tick(self):
        pass


class Iron_Wall(Tile):
    def __init__(self, x, y, stage=None, previous_tile=None):
        super().__init__(x, y, previous_tile)
        self.collision = []
        self.buildable = False

    def __repr__(self):
        return "metal_wall"

    def draw(self, window):
        window.blit(gv.get("iron_wall_sprite"), self.rect)

    def interact1(self, level, monsters, player):
        for row in level:
            for tile in row:
                if tile == self:
                    x, y, w, h = tile.rect
                    level[level.index(row)][row.index(tile)] = self.previous_tile(x, y)
                    player.inventory["metal"] += random.randint(1, 2)

    def interact2(self, level, monsters, player):
        pass

    def tick(self):
        pass


class Bed(Tile):
    def __init__(self, x, y, stage=None, previous_tile=None):
        super().__init__(x, y, previous_tile)
        self.collision = []
        self.buildable = False

    def __repr__(self):
        return "bed"

    def draw(self, window):
        previous_sprite = pg.image.load(f"sprites/{self.previous_tile(0, 0)}_tile.png").convert_alpha()
        window.blit(previous_sprite, self.rect)

        window.blit(gv.get("bed_sprite"), self.rect)

    def interact1(self, level, monsters, player):
        for row in level:
            for tile in row:
                if tile == self:
                    x, y, w, h = tile.rect
                    level[level.index(row)][row.index(tile)] = self.previous_tile(x, y)
                    player.inventory["wood"] += random.randint(1, 2)
                    player.inventory["silk"] += random.randint(0, 1)

    def interact2(self, level, monsters, player):
        if player.time > player.night:
            player.time = 0
            engine.save("saves", "level.pkl", level)
            engine.save("saves", "player.pkl", player)
            engine.save("saves", "monsters.pkl", monsters)

    def tick(self):
        pass