from settings import *
from supports import *
from sprites import Sprite, Player, Bee, Worm
from groups import AllSprites


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Platformer")
        self.clock = pygame.time.Clock()
        # GROUPS.
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()

        self.load_assets()
        self.setup()

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
                )
        Bee((500, 600), self.bee_frames, self.all_sprites)
        Worm((700, 600), self.worm_frames, self.all_sprites)

    def run(self):
        while True:
            dt = self.clock.tick(FRAMERATE) / 1000
            # EVENT LOOP.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            # UPDATE.
            self.all_sprites.update(dt)
            # DRAW.
            self.screen.fill(BG_COLOR)
            self.all_sprites.draw(self.player)
            pygame.display.update()


if __name__ == "__main__":
    Game().run()
