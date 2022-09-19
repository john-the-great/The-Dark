import pygame, os
from random import randint, uniform, choice

class Bee:
    def __init__(self, pos):
        image_dir = 'data/images/ai/bees/'
        self.image_id = 0
        dirs = ['right', 'left']
        self.curr_dir = choice(dirs)
        self.pre_dir = self.curr_dir
        self.ani_dirs = {
            'right':[],
            'left':[]
        }
        self.vel_dir = 1
        #load images
        for file_name in os.listdir(image_dir):
            image = pygame.image.load(image_dir + file_name)
            self.ani_dirs['right'].append(image)
            left_image = pygame.transform.flip(image, True, False)
            self.ani_dirs['left'].append(left_image)
        self.animation_len = len(self.ani_dirs['right'])-1

        self.rect = pygame.Rect(pos[0], pos[1], 8, 8)
        self.pos = pos

        self.change_cnt = 0
        self.dir_cnt = 0

    def render(self, surf, scroll, dt):
        if self.image_id >= self.animation_len-.3:
            self.image_id = 0
        self.image_id += .2 * dt
        image = self.ani_dirs[self.curr_dir][int(self.image_id)]
        surf.blit(image, (self.rect.x-scroll[0], self.rect.y-scroll[1]))

    def movement(self, dt, time, rel_fps, bee_len):
        if self.curr_dir == 'right':
            self.vel_dir = .4
        else:
            self.vel_dir = -.4
        self.pos[0] += self.vel_dir * dt
        self.rect.x = self.pos[0]
        if time >= rel_fps:
            self.change_cnt += 1
        if self.change_cnt > 4:
            change = randint(0, 1)
            if change > 0:
                self.curr_dir = 'right'
            else:
                self.curr_dir = 'left'
            if self.pre_dir == self.curr_dir:
                self.dir_cnt += 1
            else:
                self.pre_dir = self.curr_dir
                self.dir_cnt = 0
            self.change_cnt = 0
        if self.dir_cnt >= 2:
            self.change_cnt = 0
            if self.curr_dir == 'right':
                self.curr_dir = 'left'
            else:
                self.curr_dir = 'right'
            self.pre_dir = self.curr_dir
            self.dir_cnt = 0

    def run_back(self):
        self.change_cnt = 0
        if self.curr_dir == 'right':
            self.curr_dir = 'left'
        else:
            self.curr_dir = 'right'
        self.pre_dir = self.curr_dir
        self.dir_cnt = 0

def load_bees(bees, sim_dis, player_pos):
    amount = 20
    for i in range(amount):
        x = uniform((player_pos[0] - (sim_dis/2)), (player_pos[0] + (sim_dis/2)))
        y = uniform(245, (player_pos[1] + (sim_dis/1.2)))
        bees.append(Bee([x, y]))
    return bees

def run_bees(bees, sim_dis, player_pos, surf, scroll, dt, time, rel_fps):
    for bee in bees:
        if abs(player_pos[0] - bee.rect.x) < sim_dis and abs(player_pos[1] - bee.rect.y) < sim_dis:
            bee.render(surf, scroll, dt)
        bee.movement(dt, time, rel_fps, len(bees))
        if bee.rect.x <= 180 or bee.rect.x >= 620:
            bee.run_back()
        #print(bee.rect)
