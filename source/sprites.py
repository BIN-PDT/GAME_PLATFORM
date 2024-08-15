from settings import *


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)


class AnimatedSprite(Sprite):
    def __init__(self, pos, frames, groups):
        self.frames = frames
        self.frame_index = 0
        self.animation_speed = 10
        super().__init__(pos, self.frames[0], groups)

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.frame_index %= len(self.frames)
        self.image = self.frames[int(self.frame_index)]


class Player(AnimatedSprite):
    def __init__(self, pos, frames, groups, collision_sprites):
        super().__init__(pos, frames, groups)
        # MOVEMENT.
        self.direction, self.speed = pygame.Vector2(), 400
        self.flip = False
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

    def animate(self, dt):
        # PLAYER IS RUNNING.
        if self.direction.x:
            self.frame_index += self.animation_speed * dt
            self.frame_index %= len(self.frames)
            self.flip = self.direction.x < 0
        # PLAYER IS IDLING.
        else:
            self.frame_index = 0
        # PLAYER IS JUMPING.
        if not self.on_floor:
            self.frame_index = 1

        surf = self.frames[int(self.frame_index)]
        self.image = pygame.transform.flip(surf, self.flip, False)

    def update(self, dt):
        self.check_on_floor()
        self.input()
        self.move(dt)
        self.animate(dt)


class Bee(AnimatedSprite):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)

    def update(self, dt):
        self.animate(dt)


class Worm(AnimatedSprite):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)

    def update(self, dt):
        self.animate(dt)
