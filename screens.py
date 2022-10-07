from config import *
import entities
import level

class Screen:
    '''Screen class provide template for screens'''
    def __init__(self, game) -> None:
        self.game = game

    def input(self, input) -> None:
        '''this method used for input handaling'''
        pass

    def update(self, dt) -> None:
        '''this method used to process game logics'''
        pass

    def draw(self, display) -> None:
        '''this method used for rendering game entities'''
        pass


class MainMenuScreen(Screen):
    def __init__(self, game) -> None:
        super().__init__(game)
        # create a title
        title = entities.Text(GAME_TITLE, LARGE_FONT, GHOST_WHITE)
        title.rect.center = (DISPLAY_CENTER[0], GRID_SIZE * 6)

        # create buttons
        self.play_button = entities.Button((DISPLAY_CENTER[0], GRID_SIZE * 12), 'PLAY', MED_FONT, GHOST_WHITE, focus=True)
        self.exit_button = entities.Button((DISPLAY_CENTER[0], GRID_SIZE * 15), 'EXIT', MED_FONT, GHOST_WHITE)
        
        # add buttons and title in Group (Group is like python's list but it will do much more than list)
        self.ui = pygame.sprite.Group()
        self.ui.add(title, self.play_button, self.exit_button)
        self.play_button_pressed = False

        # create sfx 
        self.sfx_click_btn = pygame.mixer.Sound('./scr/audio/SFX/btn_click.ogg')
        self.sfx_change_btn = pygame.mixer.Sound('./scr/audio/SFX/btn_change.ogg')

    def input(self, event) -> None:
        if event.type == KEYUP:
            # below code block is switch button focus
            if event.key == K_UP or event.key == K_DOWN:
                self.play_button.set_focus(not self.play_button.get_focus())
                self.exit_button.set_focus(not self.exit_button.get_focus())
                self.sfx_change_btn.play()

            # select the button based on their focus state
            if event.key == K_SPACE or event.key == K_RETURN:
                self.sfx_click_btn.play()
                if self.play_button.get_focus() and not self.play_button_pressed:
                    self.play_button_pressed = True

                if self.exit_button.get_focus():
                    self.game.quit()
            
    def update(self, dt) -> None:
        if self.play_button_pressed:
            fade_in(DARK_SCREEN, 10)
            if DARK_SCREEN.get_alpha() >= 255:
                self.game.set_screen(GameScreen(self.game))
        
        else: fade_out(DARK_SCREEN, 10)
        self.ui.update()

    def draw(self, display) -> None:
        self.ui.draw(display)


class GameScreen(Screen):
    def __init__(self, game) -> None:
        super().__init__(game)
        # Initialise pause ui's components
        title = entities.Text('PAUSE', LARGE_FONT, position=(DISPLAY_CENTER[0], DISPLAY_CENTER[1] - (GRID_SIZE * 3)))
        self.resume_button = entities.Button((DISPLAY_CENTER[0], DISPLAY_CENTER[1] + (GRID_SIZE * 1)), 'RESUME', MED_FONT)
        self.restart_button = entities.Button((DISPLAY_CENTER[0], DISPLAY_CENTER[1] + (GRID_SIZE * 4)), 'RESTART', MED_FONT)
        self.back_button = entities.Button((DISPLAY_CENTER[0], DISPLAY_CENTER[1] + (GRID_SIZE * 7)), 'BACK', MED_FONT)

        self.pause_ui = pygame.sprite.Group()
        self.pause_ui.add(title, self.resume_button, self.restart_button, self.back_button)
        self.current_button_index = 1
        
        self.is_paused = False
        self.is_back = False
        self.is_reload = False
        self.current_level = 0

        # Initialise level's components
        self.player = entities.Player()
        self.levels = []

        # load all 12 levels
        for lvl_num in range(1 , 13):
            self.levels.append(level.Level('./scr/maps/level_' + str(lvl_num) + '.tmx', self.player))
        self.levels[self.current_level].load_map()

    def input(self, event) -> None:
        if event.type == KEYUP:
            # when esc button pressed pause ui either hide or visiable
            if event.key == K_ESCAPE:
                self.is_paused = not self.is_paused
                self.resume_button.set_focus(True)
                self.restart_button.set_focus(False)
                self.back_button.set_focus(False)
                self.current_button_index = 0

            # below code block is switch the button focus state
            if event.key == K_UP or event.key == K_DOWN:
                self.current_button_index += -1 if event.key == K_UP else 1
                if self.current_button_index < 0:
                    self.current_button_index = 2
                elif self.current_button_index > 2:
                    self.current_button_index = 0

                for button in self.pause_ui.sprites()[1:]:
                    button.set_focus(False)
                self.pause_ui.sprites()[self.current_button_index+1].set_focus(True)

            # select the button based on their focus state
            if event.key == K_SPACE or event.key == K_RETURN:
                if self.resume_button.get_focus():
                    self.is_paused = False

                if self.restart_button.get_focus():
                    self.is_reload = True

                if self.back_button.get_focus():
                    self.is_back = True

            if event.key == K_r:
                self.is_reload = True

        # call the level's input method
        self.levels[self.current_level].input(event)

    def update(self, dt) -> None:
        # below code block is initialise the menu screen or reload the level
        if self.is_back or self.is_reload:
            fade_in(DARK_SCREEN, 10)
            if DARK_SCREEN.get_alpha() >= 255:
                if self.is_reload:
                    self.levels[self.current_level].reload()
                    self.is_reload = False
                    self.is_paused = False
                else:
                    self.game.set_screen(MainMenuScreen(self.game))

        # below code block is used to change level and initialise credit screen
        elif not self.is_paused:
            self.levels[self.current_level].update(dt)
            if self.levels[self.current_level].is_completed():
                if len(self.levels) > self.current_level+1:
                    self.levels[self.current_level].exit()
                    self.current_level += 1
                    self.levels[self.current_level].load_map()
                else:
                    self.game.set_screen(CreditScreen(self.game))

        # this will controll pause ui's visiablity
        else:
            if DARK_SCREEN.get_alpha() < 126:
                fade_in(DARK_SCREEN, 10)

    def draw(self, display) -> None:
        if self.is_paused:
            self.pause_ui.draw(DARK_SCREEN)

        self.levels[self.current_level].draw(display)
        # pygame.draw.rect(display, 'red', self.player.rect, 1)
        # pygame.draw.rect(display, 'yellow', self.player.body_rect, 1)
        

class CreditScreen(Screen):
    '''Credit screen is display the details'''
    def __init__(self, game) -> None:
        super().__init__(game)
        content1 = 'Code and Level Design : Ezhil' 
        content2 = 'Pixel Art : PixelForg, Essssam (itch.io)'
        content3 = 'SFX and Music : Pixabay music'
        content4 = 'Fonts : TinyWorlds (itch.io)'
        content5 = 'Thank you for Playing!'

        self.credits_txt  = entities.Text('CREDITS', LARGE_FONT, position=(DISPLAY_CENTER[0], GRID_SIZE * 3))
        self.content1_txt = entities.Text(content1, position=(DISPLAY_CENTER[0], GRID_SIZE * 9))
        self.content2_txt = entities.Text(content2, position=(DISPLAY_CENTER[0], GRID_SIZE * 12))
        self.content3_txt = entities.Text(content3, position=(DISPLAY_CENTER[0], GRID_SIZE * 15))
        self.content4_txt = entities.Text(content4, position=(DISPLAY_CENTER[0], GRID_SIZE * 18))
        self.content5_txt = entities.Text(content5, position=(DISPLAY_CENTER[0], GRID_SIZE * 21))
        self.info = entities.Text('[ Press Esc for back to Menu ]', SMALL_FONT, position=(DISPLAY_CENTER[0], GRID_SIZE * 24))
        
        self.txts = pygame.sprite.Group(self.credits_txt, self.content1_txt, self.content2_txt, self.content3_txt, self.content4_txt, self.content5_txt,self.info)
        self.is_back_to_menu = False

    def input(self, event) -> None:
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                self.is_back_to_menu = True

    def update(self, dt) -> None:
        if self.is_back_to_menu:
            fade_in(DARK_SCREEN, 5)
            if DARK_SCREEN.get_alpha() >= 255:
                self.game.set_screen(MainMenuScreen(self.game))
        else:
            fade_out(DARK_SCREEN, 5)

    def draw(self, display) -> None:
        self.txts.draw(display)


