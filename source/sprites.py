from settings import *


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)


class Player(Sprite):
    def __init__(self, pos, groups, collision_sprites):
        surf = pygame.Surface((40, 80))
        super().__init__(pos, surf, groups)
        # MOVEMENT.
        self.direction, self.speed = pygame.Vector2(), 400
        # COLLISION.
        self.collision_sprite = collision_sprites
        # GRAVITY.
        self.gravity = 50
        self.on_floor = False

    def input(self):
        keys = pygame.key.get_pressed()
        # MOVE.
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        # JUMP.
        if self.on_floor and keys[pygame.K_SPACE]:
            self.direction.y -= 20

    def move(self, dt):
        # HORIZONTAL.
        self.rect.x += self.direction.x * self.speed * dt
        self.collide("horizontal")
        # VERTICAL.
        self.direction.y += self.gravity * dt
        self.rect.y += self.direction.y
        self.collide("vertical")

    def collide(self, direction):
        for sprite in self.collision_sprite:
            if sprite.rect.colliderect(self.rect):
                if direction == "horizontal":
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.rect.left = sprite.rect.right
                if direction == "vertical":
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom
                    self.direction.y = 0

    def check_on_floor(self):
        floor_rect = pygame.FRect((0, 0), (self.rect.width, 2))
        floor_rect = floor_rect.move_to(midtop=self.rect.midbottom)
        self.on_floor = (
            True
            if floor_rect.collidelist(
                list(map(lambda sprite: sprite.rect, self.collision_sprite))
            )
            != -1
            else False
        )

    def update(self, dt):
        self.check_on_floor()
        self.input()
        self.move(dt)
