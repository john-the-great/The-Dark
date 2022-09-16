import pygame, os

class Player:
    def __init__(self):
        self.size = 8
        self.rect = pygame.Rect(300, -10, self.size, self.size)
        self.rounded_pos = [
        self.rect.x, self.rect.y]
        self.direc = [0, 0]
        self.MAX = 1.4
        self.ACCEL = .2
        self.FRICTION = .15
        self.falling = 0
        self.movement_data = {
        'jump_timer':0}
        self.curr_mov = 'run_right'
        self.pre_direction = 'right'
        self.was_dirs = {'right':True, 'left':False}
        self.ground_touches = 0
        self.hit_ground = False

        self.image_dir = 'data/images/player/'
        self.image_id = 0
        self.animations = {
            'run_right':[], 'run_left':[],
            'idle_right':[], 'idle_left':[],
            'jump_right':[], 'jump_left':[],
            'hitground_right':[], 'hitground_left':[]
        }
        #load images
        for file_name in os.listdir(self.image_dir):
            rel_name = ''
            for char in file_name:
                if char.isdigit():
                    break
                rel_name += char
            for key in self.animations:
                if rel_name in key:
                    image = pygame.image.load((self.image_dir + file_name))
                    self.animations[key].append(image)
                    #for moving left
                    left_image = pygame.transform.flip(image, True, False)
                    self.animations[f'{rel_name}_left'].append(left_image)
                    break

    def render(self, surf, scroll, dt):
        #pygame.draw.rect(surf, (
        #255, 255, 255), (
        #self.rect.x-scroll[0], self.rect.y-scroll[1],
        #self.rect.width, self.rect.height), 1)
        try:
            if self.image_id >= (len(self.animations[self.curr_mov])-1)+.3:
                self.image_id = 0
            self.image_id += 0.1 * dt
            image = self.animations[self.curr_mov][int(self.image_id)]
        except:
            if self.image_id >= (len(self.animations['idle_' + self.curr_mov])-1)+.3:
                self.image_id = 0
            self.image_id += 0.1 * dt
            image = self.animations['idle_' + self.curr_mov][int(self.image_id)]

        surf.blit(image, (self.rect.x-scroll[0], self.rect.y-scroll[1]))

    def update_rpos(self, dt):
        self.rounded_pos[0] += self.direc[0] * dt
        self.rounded_pos[1] += self.direc[1] * dt

    def movement(self, dt, collis):
        keys = pygame.key.get_pressed()
        self.direc[1] = 0
        self.movement_data['jump_timer'] += 1
        set_to_jump = False
        set_to_hitground = False
        #hitground override set_to_jump
        if self.hit_ground:
            set_to_hitground = True
        if 'jump' in self.curr_mov and not collis['bottom'] and not set_to_hitground:
            set_to_jump = True
        self.curr_mov = self.pre_direction
        if collis['left'] or collis['right']:
            self.direc[0] = 0

        if keys[pygame.K_d]:
            if not collis['right']:
                if self.direc[0] < self.MAX:
                    self.direc[0] += self.ACCEL * dt
            self.curr_mov = 'run_right'
            self.pre_direction = 'right'
            self.was_dirs['right'] = True
            self.was_dirs['left'] = False
        elif keys[pygame.K_a]:
            if not collis['left']:
                if self.direc[0] > -self.MAX:
                    self.direc[0] -= self.ACCEL * dt
            self.curr_mov = 'run_left'
            self.pre_direction = 'left'
            self.was_dirs['right'] = False
            self.was_dirs['left'] = True
        else:
            if self.direc[0] > 0:
                self.direc[0] -= self.FRICTION * dt
                if abs(self.direc[0] - 0.05) < 0.06:
                    self.direc[0] = 0
            elif self.direc[0] < 0:
                self.direc[0] += self.FRICTION * dt
                if (self.direc[0] + 0.05) > -0.06:
                    self.direc[0] = 0

        if keys[pygame.K_SPACE]:
            if self.movement_data['jump_timer'] < 6:
                self.falling = -4
                if self.was_dirs['right']:
                    self.curr_mov = 'jump_right'
                else:
                    self.curr_mov = 'jump_left'

        if set_to_jump:
            if self.was_dirs['right']:
                self.curr_mov = 'jump_right'
            else:
                self.curr_mov = 'jump_left'
        elif set_to_hitground:
            if self.was_dirs['right']:
                self.curr_mov = 'hitground_right'
            else:
                self.curr_mov = 'hitground_left'

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
                    collis['right'] = True
                elif abs(self.rect.left - tile.right) < tolerance:
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
