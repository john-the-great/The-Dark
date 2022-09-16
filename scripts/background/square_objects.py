import pygame

class S_Objects:
    def __init__(self, colour, r_propeties, vels, player_y):
        self.pos = [r_propeties[0], player_y+20]
        self.r_width = r_propeties[1]
        self.r_height = r_propeties[2]
        self.colour = colour
        self.vels = [vels[0], vels[1]]
        self.angle = 0
        self.rot_speed = vels[2]
        self.image = pygame.Surface((self.r_width, self.r_height))
        pygame.draw.rect(self.image, self.colour, (0, 0,
        self.r_width, self.r_height))

    def render(self, surf, scroll):
        rot_image = pygame.transform.rotate(self.image, self.angle)
        surf.blit(rot_image, (self.pos[0]-scroll[0], self.pos[1]-scroll[1]))

    def move(self, dt):
        self.pos[0] += self.vels[0] * dt
        self.pos[1] += self.vels[1] * dt
        self.angle += self.rot_speed * dt
        self.angle %= 360
