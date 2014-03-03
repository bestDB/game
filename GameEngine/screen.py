import pygame
from GameEngine.gamehelpers import TextureHelper, ResourceManager, GameHelper, GameScreenFactoryHelper
from commons import Default, SerializableObject
from helpers import MathHelper


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
 
 
class TiledGameScreen :
    
    XY_1 = "xy1"
    XY_2 = "xy2"
    XY_3 = "xy3"
    XY_4 = "xy4"
    
    def __init__(self, width, height):
        self.width = width
        self.height = height 
        self.horizontalLines = []
        self.verticalLines = [] 
        self.rowCount = 1
        self.colCount = 1 
        self.tiles = {} 
            
    def tiles_from_x_y_coords(self, xList, yList):
        xMax = self.width
        yMax = self.height

        xList.append(0)
        yList.append(0)
        xList.append(xMax)
        yList.append(yMax)
        
        xList = list(set(xList))
        yList = list(set(yList))
            
        xList.sort()
        yList.sort()
        
        self.colCount = (xList.__len__() - 2) * 2
        self.rowCount = (yList.__len__() - 2) * 2 
        
        if (xList.__len__() - 2) % 2 == 1:
            self.colCount = (xList.__len__() - 2) * 2
        else :
            self.colCount = (xList.__len__() - 2) * 2 - 1
            
        if (yList.__len__() - 2) % 2 == 1:
            self.rowCount = (yList.__len__() - 2) * 2
        else :
            self.rowCount = (yList.__len__() - 2) * 2 - 1 
        
        if self.colCount <= 0 :
            self.colCount = 1
        if self.rowCount <= 0 :
            self.rowCount = 1
        
        for i in range(1, self.colCount * self.rowCount + 1) :
            self.tiles[i] = {}
        
        for xCoord in xList:
            self.verticalLines.append( ((xCoord,0),(xCoord,yMax)) )
        for yCoord in yList:
            self.horizontalLines.append( ((0,yCoord),(xMax,yCoord)) )
            
        print self.tiles
        
        self.make_tiles()    
            
    def make_tiles(self):
        currHorizontal = 0
        currVertical = 0
        
        print self.verticalLines
        print self.horizontalLines
        
        for vertical in self.verticalLines :
            for horizontal in self.horizontalLines :
                intersectionPoint = MathHelper.line_intersection(horizontal, vertical)
                upRight = None
                upLeft = None
                downLeft = None
                downRight = None
                
                
                print intersectionPoint
                print "currVertical = " + currVertical.__str__()
                print "currHorizontal = " + currHorizontal.__str__()
                
                
                if currVertical > 0 :
                    if currHorizontal > 0 :
                        upLeft = self.get_tile_index(currHorizontal, currVertical)
                    if currHorizontal < self.rowCount :
                        downLeft = self.get_tile_index(currHorizontal + 1 , currVertical + 1)
                
                if currHorizontal > 0 :
                    if currVertical >= 0 and currVertical < self.colCount:
                        upRight = self.get_tile_index(currHorizontal, currVertical + 1)
                if currVertical < self.colCount and currHorizontal < self.rowCount:
                        downRight = self.get_tile_index(currHorizontal + 1, currVertical + 1) 
                
                if upRight != None :
                    self.tiles[upRight][TiledGameScreen.XY_3] = intersectionPoint
                if upLeft != None :
                    self.tiles[upLeft][TiledGameScreen.XY_4] = intersectionPoint
                if downRight != None :
                    self.tiles[downRight][TiledGameScreen.XY_1] = intersectionPoint
                if downLeft != None :
                    self.tiles[downLeft][TiledGameScreen.XY_2] = intersectionPoint
                
                 
                print "upRight = " + upRight.__str__()
                print "upLeft = " + upLeft.__str__()
                print "downLeft = " + downLeft.__str__()
                print "downRight = " + downRight.__str__()
                print "\n\n"
                
 
                
                currHorizontal += 1
            currHorizontal = 0
            currVertical += 1
            
        
        print "tiles = " + self.tiles.__str__()
        
    def get_tile_by_row_col(self, row, col):
        return self.tiles[self.get_tile_index(row, col)]
    
    def get_tile_index(self, row, col):
        return  (row - 1) * self.rowCount + col  
     
    def get_tile_by_index(self, index):
        if index in self.tiles :
            return self.tiles[index]
        else :
            return {} 
        
    def get_right_tile(self, index):
        return self.tiles[index + 1]
        
    def get_left_tile(self, index):
        return self.tiles[index - 1]
        
    def get_top_tile(self, index):
        return self.tiles[index - self.colCount]
        
    def get_bottom_tile(self, index):
        return self.tiles[index + self.colCount]