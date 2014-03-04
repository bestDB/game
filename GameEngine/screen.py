import pygame
from gamehelpers import *
from commons import *
from GameEngine.basichelpers import *


class Screen(SerializableObject) :
    
    width = 0
    height = 0
    background = None
    backgroundRect = None
    surface = None
    opts = None
    backgroundID = None

    def __init__(self, width, height, opts = 0):
        self.width = width
        self.height = height
        self.opts = opts  
        self.drawables = {} 
    
    def prepare(self):
        self.surface = pygame.display.set_mode([self.width, self.height], self.opts) 
        if self.backgroundID != None :
            self.background = TextureHelper.get_texture(self.backgroundID)
            self.backgroundRect = self.background.get_rect()
            self.backgroundRect.centerx = self.getCenter()[0]
            self.backgroundRect.centery = self.getCenter()[1]
    
    def clear(self):
        self.surface = None
        self.background = None
        self.backgroundRect = None
    
    def quick_draw(self, drawable):
        self.drawables[drawable.UID] = drawable
        drawable.draw(self)
        
    def draw(self, drawable):
        self.drawables[drawable.UID] = drawable   
        
    def refresh_screen(self):
        self.draw_background()
        for drawable in self.drawables.values() :
            self.surface.blit(drawable.source, drawable.destRect)
        pygame.display.update()
    
    def clear_screen(self):
        self.surface = pygame.display.set_mode([self.width, self.height], self.opts)
        self.drawables = {}
        
    def set_background(self, path):    
        self.backgroundID = TextureHelper.allocate_texture(path)
        
    def draw_background(self):
        if self.background != None and self.backgroundRect != None :
            self.surface.blit(self.background, self.backgroundRect)
    
    def remove(self, drawable):
        try :
            self.drawables.pop(drawable.UID)
        except KeyError :
            pass
            
    def getCenter(self):
        return (self.width/2, self.height/2)        

class GameScreen(Screen) :   
    def __init__(self, width, height, opts = 0):
        Screen.__init__(self, width, height, opts)
        self.activeObjects = {}
        self.passiveObjects = {}
        self.resourceManager = ResourceManager()
    
    def prepare(self):
        self.resourceManager.prepare()
        Screen.prepare(self)
        for obj in self.activeObjects.values() :
            obj.prepare()
        for obj in self.passiveObjects.values() : 
            obj.prepare()
            
    def clear(self):
        self.resourceManager.clear();
        Screen.clear(self)
        for obj in self.activeObjects.values() :
            obj.clear()
        for obj in self.passiveObjects.values() :
            obj.clear()
    
    def add_active_game_object(self, obj):
        self.activeObjects[obj.UID] = obj
    
    def add_passive_game_object(self, obj):
        self.passiveObjects[obj.UID] = obj

class GameScreenFactory :
    gameScreens = {}
    gameScreensPath = Default.GAME_SCREENS_PATH
    
    @staticmethod
    def prepare_screen_factory_for_creation(propertiesDirectory):
        GameScreenFactory.gameScreensPath = GameHelper.load_game_properties_from_file(propertiesDirectory)[Default.PROPERTY_KEY_GAME_SCREENS_DIRECTORY]
    
    @staticmethod
    def prepare_screen_factory_for_game(screensDirectory):
        GameScreenFactory.gameScreensPath = screensDirectory
        GameScreenFactory.gameScreens = GameScreenFactoryHelper.get_game_screens(screensDirectory)

    
    @staticmethod
    def get_screen_names():
        return GameScreenFactory.gameScreens.keys()
    
    @staticmethod
    def save_game_screen(name, gameScreen, path = None):
        if path == None :
            path = GameScreenFactory.gameScreensPath
        gameScreen.clear()
        GameScreenFactoryHelper.dump_game_screen(name, gameScreen, path)
        GameScreenFactory.gameScreens[name] = path + name
        result = GameScreenFactory.get_screen(name)
        return result
    
    
    @staticmethod
    def add_game_screen(name, gameScreen, path = None):
        if path == None :
            path = GameScreenFactory.gameScreensPath
        GameScreenFactory.gameScreens[name] = path + name
        GameScreenFactory.dump_game_screen(name, gameScreen, path)
    
    @staticmethod
    def dump_game_screen(name, gameScreen, path = None):
        if path == None :
            path = GameScreenFactory.gameScreensPath
        GameScreenFactoryHelper.dump_game_screen(name, gameScreen, path)      
        
    @staticmethod
    def get_screen(name):
        path = GameScreenFactory.gameScreens[name]
        return GameScreenFactoryHelper.get_screen(path)    
