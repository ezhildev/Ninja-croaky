from config import *
import screens


class Game:
    '''The Game class Initialize a game'''
    def __init__(self) -> None:
        pygame.display.set_caption(GAME_TITLE)
        pygame.mouse.set_visible(False)
        pygame.display.set_icon(ICON)
        self.__display = pygame.display.set_mode(DISPLAY_SIZE)
        self.__screen = screens.MainMenuScreen(self)
        self.__time = pygame.time.Clock()
        self.__BGM = pygame.mixer.Sound('./scr/audio/music.ogg')
        self.__BGM.set_volume(.84)
        self.__BGM.play(-1)
        
    def run(self) -> None:
        '''Run method is execute a gameloop for game'''
        while(True):
            delta_time = self.__time.tick_busy_loop(FPS)/1000

            # below for loop block is used to input processing
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

                self.__screen.input(event)

            # update method is used for game logic.(like physics, collision detection and etc.)
            self.__screen.update(delta_time)

            # below statements are used for render the game. (like player, obstacles and etc)
            DARK_SCREEN.fill(DARK_BLUE)
            self.__display.fill(DARK_BLUE) 
            self.__screen.draw(self.__display)
            self.__display.blit(DARK_SCREEN, (0, 0))
            pygame.display.update()

    def set_screen(self, screen) -> None:
        '''This method is used to load a new Screen for game'''
        self.__screen = screen

    def quit(self) -> None:
        '''This method used for quit a game'''
        print('\nThank you for playing.\n')
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    game = Game()
    game.run()