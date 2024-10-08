from settings import *


class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.offset = pygame.Vector2()

    def draw(self, player):
        self.offset.x = -(player.rect.centerx - WINDOW_WIDTH / 2)
        self.offset.y = -(player.rect.centery - WINDOW_HEIGHT / 2)

        for sprite in self:
            self.screen.blit(sprite.image, sprite.rect.topleft + self.offset)


class OverworldSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.offset = pygame.Vector2()

    def draw(self, origin):
        self.offset.x = -(origin.x - WINDOW_WIDTH / 4)
        self.offset.y = -(origin.y - WINDOW_HEIGHT / 4)

        for sprite in self:
            self.screen.blit(sprite.image, sprite.rect.topleft + self.offset)
