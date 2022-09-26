from config import *

class Text(pygame.sprite.Sprite):
    '''Text class used to make a Text object'''
    def __init__(self, text, font = MED_FONT,color = 'white', position = (0, 0)) -> None:
        super().__init__() 
        self.image = font.render(text, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = position


class Button(pygame.sprite.Sprite):
    '''Button class used to make a Button and render Button'''
    def __init__(self, position, text, font, text_color = 'white', btn_color = 'gray', focus = False) -> None:
        super().__init__() 
        self.__text = Text(text, font, text_color, position)
        self.image = pygame.surface.Surface((self.__text.rect.width + 18, self.__text.rect.height + 6), pygame.SRCALPHA)
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.__focus = focus

        self.rect.width = self.image.get_rect().width
        self.rect.height = self.image.get_rect().height
        self.rect.center = position
        self.btn_color = pygame.Color(btn_color)
        self.set_focus(self.__focus)

    def set_focus(self, value) -> None:
        '''this method used to set the focus on button'''
        self.__focus = value
        self.image = pygame.surface.Surface((self.__text.rect.width + 18, self.__text.rect.height + 6), pygame.SRCALPHA)
        self.image.blit(self.__text.image, [9, 3, self.__text.rect.w, self.__text.rect.h])
        if value:
            pygame.draw.rect(self.image, self.btn_color, [0, 0, self.rect.w, self.rect.h], 3)

    def get_focus(self) -> bool:
        '''this will return focus state of the button'''
        return self.__focus


class Background(pygame.sprite.Sprite):
    '''Background class is create backgraound image and render'''
    BG_IMGS = ['Blue.png', 'Brown.png', 'Gray.png', 'Green.png', 'Pink.png', 'Purple.png', 'Yellow.png']
    def __init__(self, pos, img) -> None:
        super().__init__()
        self.image = pygame.image.load('./scr/image/Background/' + img)
        self.image = pygame.transform.scale(self.image, (64 * SCALE_RATIO, 64 * SCALE_RATIO))
        self.rect = pygame.rect.Rect((0, 0, 0, 0))
        self.rect.topleft = pos


class AnimatedSprite(pygame.sprite.Sprite):
    '''AnimatedSprite class used for sprite animation.'''
    def __init__(self) -> None:
        super().__init__()
        self.__animations = {}
        self.__current_animation = None
        self.__index = 0
        self.__horizontal_flip = False
        self.__vertical_flip = False

    def load_frames(self, anim_name, file_path, anim_time, scale = 1, repeat = True) -> None:
        '''This method used to load all sprite images in given file path.'''
        frames = []
        for frame in os.listdir(file_path):
            image = pygame.image.load(file_path + frame)
            size = image.get_rect().size
            image = pygame.transform.scale(image, (size[0] * scale, size[1] * scale))
            frames.append(image)
        self.__animations[anim_name] = {'frames': frames, 'time': anim_time, 'repeat': repeat}

    def load_spritesheet(self, anim_name, file, size, anim_time = 0.0, scale = 1.0, repeat = True) -> None:
        '''This method used to load spritesheet. All sprite images are extracted from spritesheet and saved in list.'''
        sheet = pygame.image.load(file)
        frames = []
        rows, columns = sheet.get_rect().height // size[1], sheet.get_rect().width // size[0]
        for y in range(rows):
            for x in range(columns):
                image = image_at(sheet, (x * size[0], y * size[1], size[0], size[1]))
                image = pygame.transform.scale(image, (size[0] * scale, size[1] * scale))
                frames.append(image)
        self.__animations[anim_name] = {'frames': frames, 'time': anim_time, 'repeat': repeat}

    def set_anim(self, anim_name) -> None:
        '''This used to set current animation state.'''
        if self.__current_animation != anim_name:
            self.__current_animation = anim_name
            self.play_anim()
            self.__index = 0

    def set_anim_index(self, index = 0):
        '''This method set the current index of animation.'''
        self.__index = index

    def add_frame(self, anim_name, frame) -> None:
        '''This method added the frame based on given animation name'''
        frame = pygame.transform.scale(frame, self.__animations[anim_name]['frames'][0].get_rect().size)
        self.__animations[anim_name]['frames'].append(frame)

    def set_direction(self, horizontal_flip, vertical_flip) -> None:
        '''method used to flip the image based on given boolean value.'''
        self.__horizontal_flip = horizontal_flip 
        self.__vertical_flip = vertical_flip

    def get_anim_length(self, anim_name) -> int:
        '''This will return a length of given animation'''
        return len(self.__animations[anim_name]['frames'])

    def get_anim_index(self) -> int:
        '''This will return a current animation\'s index value'''
        return int(self.__index)

    def play_anim(self, dt=1) -> None:
        '''This method used for assigning currect frame to image variable'''
        no_of_frames = len(self.__animations[self.__current_animation]['frames'])
        if int(self.__index) >= no_of_frames:
            if self.__animations[self.__current_animation]['repeat']:
                self.__index = 0
            else: self.__index = no_of_frames - 1
        self.image = self.__animations[self.__current_animation]['frames'][int(self.__index)]
        self.image = pygame.transform.flip(self.image, self.__horizontal_flip, self.__vertical_flip)
        self.__index += self.__animations[self.__current_animation]['time'] * dt * FPS

    def play_anim_reverse(self, dt = 1)  -> None:
        '''This method used for assigning currect frame to image variable in reverse order'''
        no_of_frames = len(self.__animations[self.__current_animation]['frames'])
        if int(self.__index) >= no_of_frames:
            if self.__animations[self.__current_animation]['repeat']:
                self.__index = 0
            else: self.__index = no_of_frames - 1
        self.image = self.__animations[self.__current_animation]['frames'][-int(self.__index+1)]
        self.image = pygame.transform.flip(self.image, self.__horizontal_flip, self.__vertical_flip)
        self.__index += self.__animations[self.__current_animation]['time'] * dt * FPS


class Player(AnimatedSprite):
    def __init__(self) -> None:
        super().__init__()
        # load all animation frames
        self.load_spritesheet('idle', './scr/image/Player/Idle (32x32).png', (32, 32), .45, SCALE_RATIO)
        self.load_spritesheet('run', './scr/image/Player/Run (32x32).png', (32, 32), .48, SCALE_RATIO)
        self.load_spritesheet('jump', './scr/image/Player/Jump (32x32).png', (32, 32), scale=SCALE_RATIO)
        self.load_spritesheet('fall', './scr/image/Player/Fall (32x32).png', (32, 32), scale=SCALE_RATIO)
        self.load_spritesheet('hit', './scr/image/Player/Hit (32x32).png', (32, 32), scale= SCALE_RATIO, repeat=False)

        #load all sfx 
        self.sfx_jump = pygame.mixer.Sound('./scr/audio/SFX/player_jump.ogg')
        self.sfx_hit = pygame.mixer.Sound('./scr/audio/SFX/game_over.ogg')

        # rect used for render the image on the screen
        self.rect = pygame.Rect((0, 0, 0, 0))
        self.rect.size = (32 * SCALE_RATIO, 32 * SCALE_RATIO)

        # body_rect used for player physics
        self.body_rect = pygame.Rect((0, 0, 0, 0))
        self.body_rect.size = (18 * SCALE_RATIO, 26 * SCALE_RATIO)

        
        self.X_OFFSET = self.body_rect.centerx - self.body_rect.left
        self.Y_OFFSET = self.body_rect.centery - self.body_rect.top

        # constants for physics simulation
        self.X_ACCELERATION = 1
        self.Y_ACCELERATION = 2
        self.X_MAX_SPEED = 3.5
        self.Y_MAX_SPEED = 7
        self.JUMP_HEIGHT = 15

        self.reset((0, 0))

    def reset(self, position) -> None:
        # input key for input key binding
        self.input_key = {'left' : False, 'right': False, 'jump':False}

        # set position of the player
        self.rect.topleft = position
        self.body_rect.topleft = (position[0] + 7.5 * SCALE_RATIO, position[1] + 12 * SCALE_RATIO)

        # set the current animation
        self.set_anim('idle')

        # variables for physics simulation
        self.x_direction = 0
        self.y_direction = 1
        self.x_speed = 0
        self.y_speed = 0
        self.dist_jump_height = 0
        
        # variables for other game entities to know player's state
        self.score = 0
        self.is_on_ground = False
        self.is_alive = True
        self.is_complete_level = False

    def input(self, event) -> None:
        if self.is_alive:
            if event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == K_a:
                    self.input_key['left'] = True
                elif event.key == K_RIGHT or event.key == K_d:
                    self.input_key['right'] = True
                elif event.key == K_UP or event.key == K_w:
                    self.input_key['jump'] = True

            if event.type == KEYUP:
                if event.key == K_LEFT or event.key == K_a:
                    self.input_key['left'] = False
                elif event.key == K_RIGHT or event.key == K_d:
                    self.input_key['right'] = False

    def animation(self, dt) -> None:
        # flip the player horizontaly
        if self.x_speed < 0: 
            self.set_direction(True, False)
        if self.x_speed > 0: 
            self.set_direction(False, False)

        # set the animation based on player movement
        if self.is_alive:
            if self.y_speed == 0:
                if self.x_direction == 0:
                    self.set_anim('idle')
                else:
                    self.set_anim('run')
            else:
                if self.y_speed < 0:
                    self.set_anim('jump')
                if self.y_speed > 0:
                    self.set_anim('fall')
        else:
            self.set_anim('hit')

        # play the animation
        self.play_anim(dt)

    def move(self, rects_dic, dt) -> None:
        # set the horizontal diraction
        if self.input_key.get('right'):
            self.x_direction = 1
        elif self.input_key.get('left'):
            self.x_direction = -1
        else: 
            self.x_direction = 0

        # code block for jump 
        if self.input_key['jump'] and self.is_on_ground:
            self.y_direction = -1
            self.dist_jump_height = self.JUMP_HEIGHT
            self.input_key['jump'] = False
            self.sfx_jump.play()

        # calculate the height range of jump
        if self.y_direction < 0:
            self.dist_jump_height += self.y_speed # y speed have negative value 
            if self.dist_jump_height < 0:
                self.dist_jump_height = 0
                self.y_direction = 1

        # when player is not on ground and not jump then gravity works
        if self.dist_jump_height == 0: 
            self.y_direction = 1

        # horizontal movement and collision detection
        self.x_speed = lerp(self.X_MAX_SPEED * self.x_direction, self.x_speed, self.X_ACCELERATION)
        self.body_rect.x += self.x_speed * dt * FPS
        for collision_part, rects_list in rects_dic.items():
            collided_rects = collision_list(self.body_rect, rects_list)
            if collision_part == 'all':
                for rect in collided_rects:
                    if self.x_speed > 0:
                        self.body_rect.right = rect.left 
                        self.x_speed = 0
                        
                    elif self.x_speed < 0:
                        self.body_rect.left = rect.right 
                        self.x_speed = 0


        # vertical movement and collision detection
        self.is_on_ground = False
        self.y_speed = lerp(self.Y_MAX_SPEED * self.y_direction, self.y_speed, self.Y_ACCELERATION)
        self.body_rect.y += self.y_speed * dt * FPS
        for collision_part, rects_list in rects_dic.items():
            if collision_part == 'all':
                collided_rects = collision_list(self.body_rect, rects_list)
                for rect in collided_rects:
                    if self.y_speed > 0:
                        self.body_rect.bottom = rect.top
                        self.is_on_ground = True
                        self.y_speed = self.y_direction = self.dist_jump_height = 0

                    elif self.y_speed < 0:
                        self.body_rect.top = rect.bottom
                        self.y_direction = self.y_speed = 1

            if collision_part == 'top':
                for rect in rects_list:
                    if rect.colliderect(self.body_rect.left, self.body_rect.centery + 1, self.body_rect.width, self.Y_OFFSET):
                        self.body_rect.bottom = rect.top
                        self.is_on_ground = True
                        self.y_speed = self.y_direction = self.dist_jump_height = 0

        # set body_rect values to rect
        self.rect.topleft = (self.body_rect.x - 7.5 * SCALE_RATIO, self.body_rect.y - 6 * SCALE_RATIO)

    def hit(self) -> None:
        '''This method used by obstacles for kill the player'''
        if not self.is_complete_level:
            self.is_alive = False
        self.input_key['left'] = False
        self.input_key['right'] = False
        self.y_speed = self.y_direction = 0
        self.x_speed = self.x_direction = 0
        self.sfx_hit.play()

    def update(self, dt, object_layers) -> None:
        if self.is_alive:
            self.move(object_layers, dt)
        self.animation(dt)
        

class Spike(AnimatedSprite):
    def __init__(self, position, player, active = True, rotation_angle = 0) -> None:
        super().__init__()
        self.load_spritesheet('spikes', './scr/image/Obstacle/spikes.png', (16, 16), .45, SCALE_RATIO, repeat=False)
        self.set_anim('spikes')

        self.rect = pygame.Rect(0, 0, 0, 0)
        self.rect.topleft = position
        self.rect.size = (16 * SCALE_RATIO, 16 * SCALE_RATIO)

        self.player = player
        self.is_active = active
        self.time_to_active = 0
        self.rotation_angle = rotation_angle

    def update(self, dt) -> None:
        if self.player.is_alive:
            # change the active state of spike
            if self.is_active:
                self.play_anim_reverse(dt)
                # after 9 ms spike will check the collision 
                if int(self.time_to_active) < 9:
                    self.time_to_active += dt * FPS
                else:
                    # check the player is hit on the spike or not
                    if (self.rect.colliderect(self.player.body_rect) and self.is_active) and self.player.is_alive:
                        self.player.hit()
            else: 
                self.time_to_active = 0
                self.play_anim(dt)
            
        # change the active state depands on player state
        if self.player.input_key['jump'] and self.player.is_on_ground:
            self.is_active = not self.is_active
            self.set_anim_index(0)
        
        self.image = pygame.transform.rotate(self.image, self.rotation_angle)


class EndPoint(AnimatedSprite):
    def __init__(self, pos, player, total_coins = 0) -> None:
        super().__init__()
        self.rect = pygame.Rect((0, 0, 0, 0))
        self.body_rect = pygame.Rect((0, 0, 0, 0))
        self.rect.topleft = pos
        self.rect.size = (64 * SCALE_RATIO, 64 * SCALE_RATIO)
        self.body_rect.topleft = (pos[0] + 20 * SCALE_RATIO, pos[1] + 18 * SCALE_RATIO)
        self.body_rect.size = (7 * SCALE_RATIO, 48 * SCALE_RATIO)

        self.load_spritesheet('no_flag', './scr/image/Endpoint/No_flag.png', (64, 64), 1, SCALE_RATIO, False)
        self.load_spritesheet('flag_out', './scr/image/Endpoint/Flag_out.png', (64, 64), 1, SCALE_RATIO, False)
        self.load_spritesheet('idle', './scr/image/Endpoint/Idle.png', (64, 64), .45, SCALE_RATIO)
        self.set_anim('no_flag')

        self.total_coins = total_coins
        self.player = player

    def update(self, dt) -> None:
        # check player is complete a level or not
        if (not self.player.is_complete_level and self.player.score == self.total_coins) and self.body_rect.colliderect(self.player.body_rect):
            self.set_anim('flag_out')
            self.player.is_complete_level = True

        # if flag out animation completely played then play next animation
        if self.get_anim_length('flag_out') - 1 == self.get_anim_index():
            self.set_anim('idle')

        self.play_anim(dt)


class FallingPlatform(AnimatedSprite):
    def __init__(self, pos, player) -> None:
        super().__init__()
        self.rect = Rect(pos[0], pos[1], (32 * SCALE_RATIO), (10 * SCALE_RATIO))
        self.load_spritesheet('on', './scr/image/FallingPlatforms/On.png', (32, 10), .3, SCALE_RATIO)
        self.load_spritesheet('off', './scr/image/FallingPlatforms/Off.png', (32, 10), scale= SCALE_RATIO, repeat=False)
        self.sfx = pygame.mixer.Sound('./scr/audio/SFX/falling_floor.ogg')
        self.set_anim('on')

        self.y_speed = 0
        self.timer = 21
        self.timer_is_on = False
        self.is_fall = False
        self.player = player

    def update(self, dt) -> None:
        # when the player is on the falling platform the timer will on
        if self.rect.colliderect(self.player.body_rect.x, self.player.body_rect.bottom, self.player.body_rect.width, 3) and self.player.is_on_ground:
                    self.timer_is_on = True

        if self.timer_is_on and self.timer > 0:
            self.timer -= dt * FPS
            if int(self.timer) <= 0:
                self.is_fall = True
                self.sfx.play()
                self.set_anim('off')
        
        if self.is_fall: self.y_speed = lerp(10, self.y_speed, 2)
        self.rect.y += self.y_speed 
        self.play_anim(dt)


class StaticSpike(pygame.sprite.Sprite):
    def __init__(self, position, rotation, player) -> None:
        super().__init__()
        self.rect = Rect(0, 0, 0, 0)
        self.body_rect = Rect(0, 0, 0, 0)
        self.rect.topleft = position
        self.rect.size = (16 * SCALE_RATIO, 16 * SCALE_RATIO)

        # this will set size and position of body_rect
        if rotation == 90: # facing left side
            self.body_rect.topleft = position[0] + 9 * SCALE_RATIO, position[1] + 2 * SCALE_RATIO
            self.body_rect.size = (8 * SCALE_RATIO, 13 * SCALE_RATIO)
        elif rotation == 180: # facing down side
            self.body_rect.topleft = position[0], position[1]
            self.body_rect.size = (13 * SCALE_RATIO, 8 * SCALE_RATIO)
        elif rotation == 270: # facing right side
            self.body_rect.topleft = position[0], position[1] + 2
            self.body_rect.size = (8 * SCALE_RATIO, 13 * SCALE_RATIO)
        else: # facing bottom side
            self.body_rect.topleft = position[0] + 1 * SCALE_RATIO, position[1] + 9 * SCALE_RATIO
            self.body_rect.size = (13 * SCALE_RATIO, 8 * SCALE_RATIO)

        self.image = pygame.image.load('./scr/image/Obstacle/static_spikes.png')
        self.image = pygame.transform.scale(self.image, self.rect.size)
        self.image = pygame.transform.rotate(self.image, rotation)

        self.player = player
    
    def update(self, dt) -> None:
        # check if the player hit spike or not
        if self.body_rect.colliderect(self.player.body_rect) and self.player.is_alive:
            self.player.hit()


class GoldCoin(AnimatedSprite):
    def __init__(self, position, player) -> None:
        super().__init__()
        self.load_frames('coin', './scr/image/Gold Coin/Coin/', .25, SCALE_RATIO)
        self.load_frames('coin_FX', './scr/image/Gold Coin/Coin Effect/', .27, SCALE_RATIO, False)
        self.set_anim('coin')

        self.sfx = pygame.mixer.Sound('./scr/audio/SFX/coin_collected.ogg')

        self.rect = self.image.get_rect()
        self.rect.center = position

        self.is_collected = False
        self.player = player

    def update(self, dt) -> None:
        # check if the player collect the coin or not
        if self.player.is_alive and not self.is_collected and self.rect.colliderect(self.player.body_rect):
            self.set_anim('coin_FX')
            self.is_collected = True
            self.sfx.play()
            self.player.score += 1

        self.play_anim(dt)


class MovingPlatform(AnimatedSprite):
    def __init__(self, position, path, direction, speed, player) -> None:
        super().__init__()
        self.load_spritesheet('moving_platform', './scr/image/MovingPlatforms/moving_platforms.png', (32, 8), .3, SCALE_RATIO)
        self.set_anim('moving_platform')

        self.rect = self.image.get_rect()
        self.rect.topleft = position

        self.body_rect = self.rect.copy()
        self.body_rect.y = self.body_rect.y + 2
        
        self.path = path
        self.x_speed = speed * direction[0]
        self.y_speed = speed * direction[1]
        self.player = player
        pass

    def update(self, dt) -> None:
        # below code block used for contorling moving_platform movement direction of both x and y
        if self.x_speed != 0:
            if self.path[0][0] >= self.rect.centerx or self.path[1][0] <= self.rect.centerx:
                self.x_speed = self.x_speed * -1

        if self.y_speed != 0:
            if self.path[0][1] >= self.rect.centery or self.path[1][1] <= self.rect.centery:
                self.y_speed = self.y_speed * -1

        # this statements are used to move the moving_platform
        self.body_rect.centerx += self.x_speed 
        self.body_rect.centery += self.y_speed 

        self.rect.centerx += self.x_speed 
        self.rect.centery += self.y_speed 

        # this code block is used for move player based on this moving_platform movement
        if self.body_rect.colliderect(self.player.body_rect.x, self.player.body_rect.bottom - 2, self.player.body_rect.width, 3):
            if self.x_speed !=  0 :
                self.player.body_rect.x += self.x_speed
            if self.y_speed != 0:
                self.player.body_rect.y += self.y_speed

        self.play_anim(dt)


class Saw(AnimatedSprite):
    def  __init__(self, position, path, direction, player) -> None:
        super().__init__()
        self.load_spritesheet('saw', './scr/image/Saw/saw.png', (38, 38), .6, SCALE_RATIO)
        self.set_anim('saw')
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.path = path
        self.x_speed = 2 * direction[0]
        self.y_speed = 2 * direction[1]
        self.player = player

    def update(self, dt) -> None:
        # below code block is use to check the player collide or not
        if self.player.is_alive and collide_circle(self.player.body_rect, self.rect.centerx, self.rect.centery, self.rect.size[0] / 2):
            self.player.hit()

        # below code blocks are used to change the direction of the saw
        if self.x_speed != 0:
            if self.path[0][0] >= self.rect.centerx or self.path[1][0] <= self.rect.centerx:
                self.x_speed *= -1

        if self.y_speed != 0:
            if self.path[0][1] >= self.rect.centery or self.path[1][1] <= self.rect.centery:
                self.y_speed *= -1

        # these statements are used to move the saw
        self.rect.centerx += self.x_speed 
        self.rect.centery += self.y_speed 

        self.play_anim(dt)
