from random import randint

from settings import *
from supports import *
from sprites import Sprite, Player, Bee, Worm, Bullet, Fire
from groups import AllSprites
from timers import Timer


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Platformer")
        self.clock = pygame.time.Clock()
        # GROUPS.
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        # TIMERS.
        self.bee_timer = Timer(200, self.spawn_bee, True, True)
        # LOAD DATA.
        self.load_assets()
        self.setup()
        # MUSIC.
        self.sounds["music"].play(-1)

    def load_assets(self):
        # GRAPHICS.
        self.player_frames = import_images("images", "player")
        self.bullet_surf = import_image("images", "gun", "bullet")
        self.fire_surf = import_image("images", "gun", "fire")
        self.bee_frames = import_images("images", "enemies", "bee")
        self.worm_frames = import_images("images", "enemies", "worm")
        # SOUNDS.
        self.sounds = import_sounds("audio")

    def setup(self):
        tmx_map = load_pygame(join("data", "maps", "world.tmx"))
        self.level_width = tmx_map.width * TILE_SIZE
        self.level_height = tmx_map.height * TILE_SIZE

        for col, row, img in tmx_map.get_layer_by_name("Main").tiles():
            pos = col * TILE_SIZE, row * TILE_SIZE
            Sprite(pos, img, (self.all_sprites, self.collision_sprites))

        for col, row, img in tmx_map.get_layer_by_name("Decoration").tiles():
            pos = col * TILE_SIZE, row * TILE_SIZE
            Sprite(pos, img, self.all_sprites)

        for obj in tmx_map.get_layer_by_name("Entities"):
            if obj.name == "Player":
                self.player = Player(
                    pos=(obj.x, obj.y),
                    frames=self.player_frames,
                    groups=self.all_sprites,
                    collision_sprites=self.collision_sprites,
                    create_bullet=self.fire_bullet,
                )
            else:
                Worm(
                    limit_rect=pygame.FRect(obj.x, obj.y, obj.width, obj.height),
                    frames=self.worm_frames,
                    groups=(self.all_sprites, self.enemy_sprites),
                )

    def fire_bullet(self, pos, direction):
        x = pos[0] + (35 if direction == 1 else -35 - self.bullet_surf.get_width())

        Bullet(
            pos=(x, pos[1]),
            direction=direction,
            surf=self.bullet_surf,
            groups=(self.all_sprites, self.bullet_sprites),
        )
        Fire(
            pos=pos,
            surf=self.fire_surf,
            groups=self.all_sprites,
            player=self.player,
        )
        self.sounds["shoot"].play()

    def spawn_bee(self):
        Bee(
            pos=(self.level_width + WINDOW_WIDTH, randint(0, self.level_height)),
            frames=self.bee_frames,
            groups=(self.all_sprites, self.enemy_sprites),
            speed=randint(300, 500),
        )

    def check_collision(self):
        # BULLET & ENEMY.
        for bullet in self.bullet_sprites:
            collided_sprites = pygame.sprite.spritecollide(
                bullet, self.enemy_sprites, False, pygame.sprite.collide_mask
            )
            if collided_sprites:
                self.sounds["impact"].play()
                bullet.kill()
                for sprite in collided_sprites:
                    sprite.destroy()
        # ENEMY & PLAYER.
        if pygame.sprite.spritecollide(
            self.player, self.enemy_sprites, False, pygame.sprite.collide_mask
        ):
            pygame.quit()
            exit()

    def run(self):
        while True:
            dt = self.clock.tick(FRAMERATE) / 1000
            # EVENT LOOP.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            # UPDATE.
            self.check_collision()
            self.all_sprites.update(dt)
            self.bee_timer.update()
            # DRAW.
            self.screen.fill(BG_COLOR)
            self.all_sprites.draw(self.player)
            pygame.display.update()


if __name__ == "__main__":
    Game().run()
