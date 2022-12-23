class FPSStats:

    def __init__(self, font):
        self.__font = font
        self.__update_time = 0
        self.__render_frames = 0
        self.__logic_frames = 0
        self.__set_fps_surface()

    def update(self, delta):
        self.__update_time += delta
        self.__logic_frames += 1

        if self.__update_time >= 1000:
            self.__set_fps_surface()

            self.__update_time -= 1000
            self.__render_frames = 0
            self.__logic_frames = 0

    def render(self, surface):
        self.__render_frames += 1
        surface.blit(self.__fps, (0,0))

    def __set_fps_surface(self):
        self.__fps = self.__font.render(f"Logic {self.__logic_frames} fps - Render {self.__render_frames}", True, (255,255,255), (0,0,0) )