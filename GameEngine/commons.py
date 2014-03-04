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

class Corners :
    TOP_LEFT = "TOP_LEFT"
    TOP_RIGHT = "TOP_RIGHT"
    BOTTOM_LEFT = "BOTTOM_LEFT"
    BOTTOM_RIGHT = "BOTTOM_RIGHT"
      
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
    TMP_FOLDER = "tmp/"
    
    PROPERTIES_FILE_NAME = "properties.xml"
    PROPERTY_KEY_GAME_DIRECTORY = "GAME_DIRECTORY"
    PROPERTY_KEY_GAME_SCREENS_DIRECTORY = "GAME_SCREENS_DIRECTORY"
    PROPERTY_KEY_GAME_SAVES_DIRECTORY = "GAME_SAVES_DIRECTORY"
    PROPERTY_KEY_START_SCREEN_NAME = "START_SCREEN_NAME"
    