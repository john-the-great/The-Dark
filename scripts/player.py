import pygame

class Player:
    def __init__(self):
        self.size = 8
        self.rect = pygame.Rect(300, -10, self.size, self.size)
        self.rounded_pos = [
        self.rect.x, self.rect.y]
        self.direc = [0, 0]
        self.falling = 0
        self.movement_data = {
        'jump_timer':0}
        self.dirs = {
        'right':False, 'left':False, 'jump':False}

    def render(self, surf, scroll):
        pygame.draw.rect(surf, (
        255, 255, 255), (
        self.rect.x-scroll[0], self.rect.y-scroll[1],
        self.rect.width, self.rect.height))

    def update_rpos(self, dt):
        self.rounded_pos[0] += self.direc[0] * dt
        self.rounded_pos[1] += self.direc[1] * dt

    def movement(self, dt):
        keys = pygame.key.get_pressed()
        self.direc = [0, 0]
        self.movement_data['jump_timer'] += 1
        self.dirs = {
        'right':False, 'left':False, 'jump':False}

        if keys[pygame.K_d]:
            self.direc[0] += 2
            self.dirs['right'] = True
        elif keys[pygame.K_a]:
            self.direc[0] -= 2
            self.dirs['left'] = True
        if keys[pygame.K_SPACE]:
            if self.movement_data['jump_timer'] < 6:
                self.falling = -4
                self.dirs['jump'] = True

        self.falling += .2 * dt
        self.direc[1] += self.falling
        if self.falling >= 4:
            self.falling = 4

        self.update_rpos(dt)

    def physics(self, tiles):
        tolerance = 1
        collis = {
        'right':False, 'left':False,
        'top':False, 'bottom':False
        }
        self.rect.x = self.rounded_pos[0]
        self.rect.y = self.rounded_pos[1]
        for tile in tiles:
            if self.rect.top < tile.bottom and self.rect.bottom > tile.top:
                if abs(self.rect.right - tile.left) < tolerance:
                    self.rect.right = tile.left
                    self.rounded_pos[0] = self.rect.x
                    collis['right'] = True
                elif abs(self.rect.left - tile.right) < tolerance:
                    self.rounded_pos[0] = tile.right
                    self.rect.x = self.rounded_pos[0]
                    collis['left'] = True
            elif self.rect.left < tile.right and self.rect.right > tile.left:
                if abs(self.rect.top - tile.bottom) < tolerance:
                    self.falling = 1
                    collis['top'] = True
                elif abs(self.rect.bottom - tile.top) < tolerance:
                    self.rect.bottom = tile.top
                    self.rounded_pos[1] = self.rect.y
                    self.falling = 0
                    collis['bottom'] = True

        return collis
