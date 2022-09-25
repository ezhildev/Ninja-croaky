from config import *
from pytmx.util_pygame import load_pygame
from entities import *

class Tile(pygame.sprite.Sprite):
    '''Tile class rendering a Tile with appropriate position and image'''
    def __init__(self, image, position=(0, 0)) -> None:
        super().__init__()
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.rect.topleft = position
        self.rect.size = (image.get_rect().width * SCALE_RATIO, image.get_rect().height * SCALE_RATIO)
        self.image = pygame.transform.scale(image, self.rect.size)


class TileObject:
    '''TileObjct is rectangle object that used for collision detection and others'''
    def __init__(self, object) -> None:
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.rect.topleft = (object.x * SCALE_RATIO, object.y * SCALE_RATIO)
        self.rect.size = (object.width * SCALE_RATIO, object.height * SCALE_RATIO)

    def draw(self, screen) -> None:
        pygame.draw.rect(screen, '#69ff69', self.rect, 1)


class TileLayer:
    '''TileLayer hold all tile images of the layer and render the images'''
    def __init__(self, tile_layer, level) -> None:
        self.tiles = pygame.sprite.Group()
        self.show_rect = False
        img_index = random.randint(0, len(Background.BG_IMGS)-1)

        # this load instance of tile or game entities
        for x, y, image in tile_layer.tiles():
            position = (x * GRID_SIZE, y * GRID_SIZE)
            if tile_layer.name == 'active_spikes':
                tile = Spike(position, level.player, rotation_angle = tile_layer.rotation)

            elif tile_layer.name == 'non_active_spikes':
                tile = Spike(position, level.player, False, tile_layer.rotation)

            elif tile_layer.name == 'background':
                tile = Background(position, Background.BG_IMGS[img_index])

            elif tile_layer.name == 'end_point':
                tile = EndPoint(position, level.player, level.total_coins)

            elif tile_layer.name == 'falling_platforms':
                tile = FallingPlatform(position, level.player)
                level.collided_rects.get('top').append(tile.rect)

            elif tile_layer.name == 'static_spikes':
                tile = StaticSpike(position, tile_layer.rotation, level.player)

            elif tile_layer.name == 'coins':
                tile = GoldCoin(position, level.player)
                level.total_coins += 1

            elif tile_layer.name == 'moving_platforms':
                tile = MovingPlatform(position, ((tile_layer.x_start, tile_layer.y_start),(tile_layer.x_end, tile_layer.y_end)), (tile_layer.x_direction, tile_layer.y_direction), tile_layer.speed,level.player)
                level.collided_rects.get('top').append(tile.body_rect)

            elif tile_layer.name == 'saw':
                tile = Saw(position, ((tile_layer.x_start, tile_layer.y_start),(tile_layer.x_end, tile_layer.y_end)), (tile_layer.x_direction, tile_layer.y_direction), level.player)

            else:
                tile = Tile(image, position)

            self.tiles.add(tile)

    def update(self, dt) -> None:
        self.tiles.update(dt)

    def draw(self, screen) -> None:
        self.tiles.draw(screen)

    def draw_rect(self, screen) -> None:
        if self.show_rect:
            for tile in self.tiles:
                try:
                    rect =  tile.body_rect
                except AttributeError:
                    rect = tile.rect
                pygame.draw.rect(screen, '#ff6993', rect, 1)


class ObjectGroup:
    '''ObjectGroup hold all objects of layer and render objects for debugging'''
    def __init__(self, object_group, level) -> None:
        self.objects = []
        for obj in object_group:
            tile_object = TileObject(obj)
            level.collided_rects.get('all').append(tile_object.rect)
            self.objects.append(tile_object)

    def draw(self, screen) -> None:
        for obj in self.objects:
            obj.draw(screen)


class Level:
    '''Level class responsible for load level from tmx file and render the level'''
    def __init__(self, file, player, show_objects = False) -> None:
        self.tile_map = load_pygame(file)
        self.show_objects = show_objects
        self.player = player

    def load_map(self) -> None:
        '''this method load a map and game entities'''
        self.tile_layers = []
        self.object_groups = []
        self.collided_rects = {'top':[], 'bottom':[], 'right':[], 'left':[], 'all':[]}
        self.total_coins = 0
        self.__is_completed = False
        
        for index in self.tile_map.visible_object_groups:
            object_group = self.tile_map.layers[index]
            if object_group.name == 'player':
                position = (object_group[0].x * SCALE_RATIO, object_group[0].y * SCALE_RATIO)
                self.player.reset(position)
            else:
                obj_group = ObjectGroup(object_group, self)
                self.object_groups.append(obj_group)

        for index in self.tile_map.visible_tile_layers:
            layer = self.tile_map.layers[index]
            tile_layer = TileLayer(layer, self)
            self.tile_layers.append(tile_layer)

    def reload(self) -> None:
        '''this method reload a level'''
        DARK_SCREEN.set_alpha(255)
        self.load_map()

    def is_completed(self) -> bool:
        '''this method will return True when the level is completed otherwise return False'''
        return self.__is_completed

    def input(self, event) -> None:
        self.player.input(event)

    def update(self, dt) -> None:
        # fade the screen based on player state
        if not self.player.is_alive: 
            fade_in(DARK_SCREEN, 10)
            if DARK_SCREEN.get_alpha() >= 255:
                self.reload()

        elif self.player.is_complete_level:
            fade_in(DARK_SCREEN, 10)
            if DARK_SCREEN.get_alpha() >= 255:
                self.__is_completed = True

        else: 
            fade_out(DARK_SCREEN, 10)

        # call the game entities update method
        if DARK_SCREEN.get_alpha() < 200:
            for tile_layer in self.tile_layers:
                tile_layer.update(dt)
                
            self.player.update(dt, self.collided_rects)

    def draw(self, screen) -> None:
        # this will render all tile images of the level
        for layer in self.tile_layers:
            layer.draw(screen)

        # this will render all objects of the level. this is only for debugging 
        if self.show_objects:
            for object_group in self.object_groups:
                object_group.draw(screen)

            for layer in self.tile_layers:
                layer.draw_rect(screen)

        screen.blit(self.player.image, self.player.rect)
        screen.blit(DARK_SCREEN, (0, 0))

    def exit(self) -> None:
        '''This delete all objects of level'''
        try:
            del self.tile_layers
            del self.object_groups
            del self.collided_rects
            del self.__is_completed
        except:
            print('somthing wrong!')
