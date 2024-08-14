from settings import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Platformer")
        self.clock = pygame.time.Clock()
        # GROUPS.
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

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
            self.all_sprites.draw(self.screen)
            pygame.display.update()


if __name__ == "__main__":
    Game().run()
