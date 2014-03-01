import pygame, pickle, sys
from shutil import copyfile
from helpers import TextureHelper, ResourceManager, GameHelper, GameScreenFactoryHelper
from commons import Default, SerializableObject


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
    
    def quickDraw(self, drawable):
        self.drawables[drawable.UID] = drawable
        drawable.draw(self)
        
    def draw(self, drawable):
        self.drawables[drawable.UID] = drawable   
        
    def refreshScreen(self):
        self.drawBackground()
        for drawable in self.drawables.values() :
            self.surface.blit(drawable.source, drawable.destRect)
        pygame.display.update()
    
    def clearScreen(self):
        self.drawables = {}
        
    def setBackground(self, path):    
        self.backgroundID = TextureHelper.allocate_texture(path)
        
    def drawBackground(self):
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
    
    def prepare(self):
        Screen.prepare(self)
        for obj in self.activeObjects.values() :
            obj.prepare()
        for obj in self.passiveObjects.values() : 
            obj.prepare()
            
    def clear(self):
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
    def prepare_screen_factory(propertiesDirectory):
        GameScreenFactory.gameScreensPath = GameHelper.load_game_properties(propertiesDirectory)["GAME_SCREENS_DIRECTORY"]
    
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

"""
class GameScreenFactory :
    gameScreens = {}
    gameScreensPath = Default.GAME_SCREENS_PATH
    
    @staticmethod
    def prepare_screen_factory(propertiesDirectory):
        GameScreenFactory.gameScreensPath = GameHelper.load_game_properties(propertiesDirectory)["GAME_SCREENS_DIRECTORY"]
    
    @staticmethod
    def get_screen_names():
        return GameScreenFactory.gameScreens.keys()
    
    @staticmethod
    def save_game_screen(name, gameScreen, path = None):
        if path == None :
            path = GameScreenFactory.gameScreensPath
        gameScreen.clear()
        GameScreenFactory.dump_game_screen(name, gameScreen, path)
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
        f = open(path + name + Default.GAME_SCREEN_EXT, 'w')
        pickle.dump(gameScreen, f)
        f.close()
        
        f = open(path + name + Default.RES_MAN_EXT, 'w')
        ResourceManager.unload_resources()
        pickle.dump(ResourceManager.manager, f)
        ResourceManager.reset()    
        f.close()
        
        
    @staticmethod
    def get_screen(name):
        f = open(GameScreenFactory.gameScreens[name] +  Default.GAME_SCREEN_EXT, 'r')
        gameScreen = pickle.load(f) 
        f.close()
        
        f = open(GameScreenFactory.gameScreens[name] + Default.RES_MAN_EXT)    
        ResourceManager.manager = pickle.load(f)
        ResourceManager.load_resources()
        f.close()
        
        gameScreen.prepare()    
            
        return gameScreen
    
    @staticmethod
    def copy_screen_file(name, targetDir):
        copyfile(GameScreenFactory.gameScreens[name] + Default.GAME_SCREEN_EXT, targetDir)
        copyfile(GameScreenFactory.gameScreens[name] + Default.RES_MAN_EXT, targetDir)
"""     