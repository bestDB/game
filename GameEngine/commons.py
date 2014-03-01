from abc import ABCMeta, abstractmethod
class SerializableObject(object):
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def clear(self):
        pass
    
    @abstractmethod
    def prepare(self):
        pass

class GlobalParams :
    PREVIOUS_ACTIONS_CACHE_SIZE = 10

class Colours :
    RED = (255,0,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)
    WHITE = (255,255,255)
    BLACK = (0,0,0)
    
    
class Side:
    FRONT = "FRONT"
    BACK = "BACK"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    TOP = "TOP"
    BOTTOM = "BOTTOM"

class Direction: 
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    UP_RIGHT = "UP_RIGHT"
    UP_LEFT = "UP_LEFT"
    DOWN_RIGHT = "DOWN_RIGHT"
    DOWN_LEFT = "DOWN_LEFT"
    FORWARD = "FORWARD"
    BACKWARD = "BACKWARD"
    
class Default:
    DEFAULT_ACTION = "DEFAULT_ACTION"
    GAME_ENGINE_PATH = "../GameEngine/"
    GAME_SCREENS_PATH = GAME_ENGINE_PATH + "game_screens/"
    GAME_SAVE_PATH = GAME_ENGINE_PATH + "game_saves/" 
    GAME_ENGINE_TEXTURES_PATH = GAME_ENGINE_PATH + "textures/"
    GAME_ENGINE_SOUNDS_PATH = GAME_ENGINE_PATH + "sounds/"
    EXTENDED_DRAWABLE_OBJECT_TEXTURE = GAME_ENGINE_TEXTURES_PATH + "gameObjectDefault.png"
    EXTENDED_DRAWABLE_TEXTURE = GAME_ENGINE_TEXTURES_PATH + "object.jpg"
    
    GAME_SCREEN_EXT = ".gameScr"
    RES_MAN_EXT = ".rsMan"
    TMP_FOLDER = "tmp/"