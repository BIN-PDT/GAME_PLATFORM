from settings import *
from sprites import Sprite, Player
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

        self.setup()

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
                pos = obj.x, obj.y
                self.player = Player(pos, self.all_sprites, self.collision_sprites)

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
