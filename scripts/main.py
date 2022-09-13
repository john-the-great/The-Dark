import pygame, sys
from pygame.locals import *
from map import MapC
from player import Player

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
    #############

    map = MapC('data/map/physical_map_data', 'data/images/map', [30, 150, 150])
    map.convert_tile_size(8)
    map.slice_chunks()

    player = Player()

    while 1:
        dt = clock.tick(fps_cap) * .001 * rel_fps

        size_diffx = (WINDOW_SIZE[0]/RES[0]*2)+1
        size_diffy = (WINDOW_SIZE[1]/RES[1]*2)+1
        tscroll[0] += (((player.rect.x-player.size/2 - tscroll[0]) - (WINDOW_SIZE[0]/size_diffx)))/20 * dt
        tscroll[1] += (((player.rect.y-player.size/2 - tscroll[1]) - (WINDOW_SIZE[1]/size_diffy)))/20 * dt
        scroll = tscroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])

        #NEW FRAME#
        game_surf.fill((0, 0, 0))
        player_pos = [player.rect.x, player.rect.y]
        tiles = map.show_map(game_surf, player_pos, scroll)
        #NEW FRAME#

        #MECHANICS#
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        player.movement(dt)
        collis = player.physics(tiles)
        if collis['bottom']:
            player.movement_data['jump_timer'] = 0
        #MECHANICS#

        #RENDER#
        player.render(game_surf, scroll)
        #RENDER#

        #DISPLAY#
        scaled_surf = pygame.transform.scale(game_surf, WINDOW_SIZE)
        window.blit(scaled_surf, (0, 0))
        #DISPLAY#

        pygame.display.update()

if __name__ == '__main__': main()
