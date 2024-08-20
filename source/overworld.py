from random import randint

from settings import *
from timers import Timer
from groups import OverworldSprites
from sprites import Sprite, Worm, Bee


class Overwolrd:
    def __init__(self, switch_mode, worm_frames, bee_frames):
        self.screen = pygame.display.get_surface()
        # GROUPS.
        self.overworld_sprites = OverworldSprites()
        # TIMERS.
        self.bee_timer = Timer(500, self.spawn_bee, True, True)
        # CONTROL MODE.
        self.switch_mode = switch_mode
        # CONTROL BACKGROUND.
        self.bg_origin = pygame.Vector2()
        self.bg_direction, self.bg_speed = 1, 200
        # CONTROL FOREGROUND.
        self.fg_origin = 0
        self.fg_direction, self.fg_speed = 1, 150
        # LOAD DATA.
        self.worm_frames = worm_frames
        self.bee_frames = bee_frames
        self.setup()

    def input(self):
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_RETURN]:
            self.switch_mode()

    def spawn_bee(self):
        Bee(
            pos=(self.level_width + WINDOW_WIDTH, randint(0, self.level_height)),
            frames=self.bee_frames,
            groups=self.overworld_sprites,
            speed=randint(300, 500),
        )

    def setup(self):
        # BACKGROUND.
        tmx_map = load_pygame(join("data", "maps", "world.tmx"))
        self.level_width = tmx_map.width * TILE_SIZE
        self.level_height = tmx_map.height * TILE_SIZE

        self.bg_origin.y = self.level_height / 2 - 45

        for col, row, img in tmx_map.get_layer_by_name("Main").tiles():
            pos = col * TILE_SIZE, row * TILE_SIZE
            Sprite(pos, img, self.overworld_sprites)

        for col, row, img in tmx_map.get_layer_by_name("Decoration").tiles():
            pos = col * TILE_SIZE, row * TILE_SIZE
            Sprite(pos, img, self.overworld_sprites)

        for obj in tmx_map.get_layer_by_name("Entities"):
            if obj.name == "Worm":
                Worm(
                    limit_rect=pygame.FRect(obj.x, obj.y, obj.width, obj.height),
                    frames=self.worm_frames,
                    groups=self.overworld_sprites,
                )
        # FOREGROUND.
        self.font = pygame.font.Font(join("font", "dogicapixelbold.otf"), 28)
        self.fg_surf = self.font.render("PRESS ENTER TO PLAY", False, "black")
        self.fg_rect = self.fg_surf.get_frect(
            center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        )

    def update_background(self, dt):
        self.bg_origin.x += self.bg_direction * self.bg_speed * dt
        if self.bg_origin.x <= 0 or self.bg_origin.x >= self.level_width:
            self.bg_direction *= -1

    def update_foregournd(self, dt):
        self.fg_origin += self.fg_direction * self.fg_speed * dt
        self.fg_surf.set_alpha(self.fg_origin)
        if self.fg_origin < 0 or self.fg_origin > 255:
            self.fg_direction *= -1

    def run(self, dt):
        # UPDATE.
        self.input()
        self.bee_timer.update()
        self.update_background(dt)
        self.update_foregournd(dt)
        self.overworld_sprites.update(dt)
        # DRAW.
        self.overworld_sprites.draw(self.bg_origin)
        self.screen.blit(self.fg_surf, self.fg_rect)
