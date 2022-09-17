import pygame, sys
from pygame.locals import *
from random import uniform, randint
from map import MapC
from player import Player
from background.square_objects import S_Objects as square_bg_object

def run_bg_objects(surf, scroll, dt, bgobj_list):
    for id, obj in enumerate(bgobj_list):
        #delete obj if its above the screen
        if obj.pos[1] <= 0:
            del bgobj_list[id]
        obj.move(dt)
        obj.render(surf, scroll)
    return bgobj_list

def main():
    #PYGAME INIT#
    pygame.init()
    WINDOW_SIZE = (600, 300)
    window = pygame.display.set_mode(WINDOW_SIZE)
    RES = (int(WINDOW_SIZE[0]/3), int(WINDOW_SIZE[1]/3))
    game_surf = pygame.Surface(RES)

    clock = pygame.time.Clock()
    fps_cap, rel_fps = 10_000, 60

    tscroll = [0, 0]
    para_tscroll = [0, 0]

    time = 0
    ticks = 0
    #############

    map = MapC('data/map/physical_map_data', 'data/images/map', [30, 150, 150])
    map.convert_tile_size(8)
    map.slice_chunks()

    player = Player()

    #BACKGROUND#
    #bgobj_list = []
    bg_objs = {
    'green_obj': {
        'y':400
        }
    }
    #BACKGROUND#

    while 1:
        fps = clock.tick(fps_cap)
        dt = fps * .001 * rel_fps

        size_diffx = (WINDOW_SIZE[0]/RES[0]*1.65)+1
        size_diffy = (WINDOW_SIZE[1]/RES[1]*1.65)+1
        tscroll[0] += (((player.rect.centerx - tscroll[0]) - (WINDOW_SIZE[0]/size_diffx)))/20 * dt
        tscroll[1] += (((player.rect.centery - tscroll[1]) - (WINDOW_SIZE[1]/size_diffy)))/20 * dt
        scroll = tscroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])

        para_tscroll[0] += (player.rect.centerx - para_tscroll[0])/20 * dt
        para_tscroll[1] += (player.rect.centery - para_tscroll[1])/20 * dt
        para_scroll = para_tscroll.copy()
        para_scroll[0] = int(para_scroll[0])
        para_scroll[1] = int(para_scroll[1])

        time += 1 * dt
        ticks += 1
        if time >= rel_fps:
            print(f'fps: {ticks}')
            time = 0
            ticks = 0
            # colour, r_propeties, vels, player_y
            #colour = (randint(0, 255), randint(0, 255), randint(0, 255))
            #r_propeties = (randint(int(player.rect.x-90), int(player.rect.x+90)), randint(15, 25), randint(15, 25))
            #vels = [uniform(-1, 1), uniform(-.2, -.6), randint(5, 5)]
            #bgobj_list.append(
            #    square_bg_object(colour, r_propeties, vels, player.rect.y))

        #NEW FRAME#
        game_surf.fill((0, 125, 225))
        pygame.draw.rect(game_surf, (0, 185, 0),
            (bg_objs['green_obj']['x'], bg_objs['green_obj']['y']-para_scroll[1],
            WINDOW_SIZE[0], 125))
        #bgobj_list = run_bg_objects(game_surf, scroll, dt, bgobj_list)
        player_pos = [player.rect.x, player.rect.y]
        tiles = map.show_map(game_surf, player_pos, scroll)
        #NEW FRAME#

        #MECHANICS#
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        collis = player.physics(tiles)
        player.movement(dt, collis)
        if player.falling > .5:
            player.ground_touches = 0
            player.hit_ground = False
        if collis['bottom']:
            player.movement_data['jump_timer'] = 0
            if player.ground_touches < 3:
                player.hit_ground = True
            else:
                player.hit_ground = False
                player.ground_touches -= .2 * dt
            player.ground_touches += .2 * dt
            player.falling = 0
        #MECHANICS#

        #RENDER#
        player.render(game_surf, scroll, dt)
        #RENDER#

        #DISPLAY#
        scaled_surf = pygame.transform.scale(game_surf, WINDOW_SIZE)
        window.blit(scaled_surf, (0, 0))
        #DISPLAY#

        pygame.display.update()

if __name__ == '__main__': main()
