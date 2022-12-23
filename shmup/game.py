import pygame
import os
from shmup.fps_stats import FPSStats

class Game:

    __screen_size = (640, 480)
    __game_title = "Shoot 'Em Up!!"
    __hero_image_filename = ["shmup", "assets", "images", "hero.png"]
    __hero_speed = 0.5
    __fps = 60
    __times_per_frame = 1000.0 / __fps 
    
    def __init__(self):

        pygame.init()
        
        self.__window = pygame.display.set_mode(Game.__screen_size, 0, 32)
        pygame.display.set_caption(Game.__game_title)
        self.__my_font = pygame.font.Font("shmup/assets/fonts/Sansation.ttf", 16)

        self.__hero = pygame.image.load(os.path.abspath(os.path.join(*Game.__hero_image_filename)))
        self.__hero_position = pygame.math.Vector2(self.__window.get_width()/2 - self.__hero.get_width()/2, self.__window.get_height()/2 - self.__hero.get_height()/2)

        self.__running = False

        self.__is_moving_up = False
        self.__is_moving_down = False
        self.__is_moving_left = False
        self.__is_moving_right = False

        self.__fps_stats = FPSStats(self.__my_font)

    def run(self):
        self.__running = True

        last_time = pygame.time.get_ticks()
        time_since_last_update = 0

        while self.__running:
            delta_time, last_time = self.__calc_delta_time(last_time)
            time_since_last_update += delta_time
            while time_since_last_update > Game.__times_per_frame:
                time_since_last_update -= Game.__times_per_frame
                
                self.__process_events()
                self.__update(Game.__times_per_frame)
            
            self.__render()

        self.__quit()

    def __process_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running = False
                if event.type == pygame.KEYDOWN:
                    self.__handle_player_input(event.key, True)
                if event.type == pygame.KEYUP:
                    self.__handle_player_input(event.key, False)

    def __calc_delta_time(self, last):
        current = pygame.time.get_ticks()
        delta = current - last
        return delta, current

    def __handle_player_input(self, key, is_pressed):
        if key == pygame.K_w:
            self.__is_moving_up = is_pressed
        if key == pygame.K_s:
            self.__is_moving_down = is_pressed
        if key == pygame.K_a:
            self.__is_moving_left = is_pressed
        if key == pygame.K_d:
            self.__is_moving_right = is_pressed

    def __update(self, delta_time):
        self.__fps_stats.update(delta_time)
        movement = pygame.math.Vector2(0.0, 0.0)

        if self.__is_moving_up:
            movement.y -= Game.__hero_speed
        if self.__is_moving_down:
            movement.y += Game.__hero_speed
        if self.__is_moving_left:
            movement.x -= Game.__hero_speed
        if self.__is_moving_right:
            movement.x += Game.__hero_speed

        self.__hero_position += movement * delta_time

    def __render(self):
        self.__fps_stats.render(self.__window)
        self.__window.fill((0,0,0))

        self.__window.blit(self.__hero, self.__hero_position.xy)

        pygame.display.update()

    def __quit(self):
        pygame.quit()