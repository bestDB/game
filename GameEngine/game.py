import pygame, sys
from keyboard import Keyboard
from helpers import DebugHelper, ExtendedGameObjectHelper, GameHelper, MainMenuHelper, CommonHelper
from screen import GameScreenFactory
from commons import Default
from time import sleep


class Game:
    
    GAME_DIRECTORY = ""
    GAME_SCREENS_DIRECTORY = Default.GAME_SCREENS_PATH
    GAME_SAVES_DIRECTORY = Default.GAME_SAVE_PATH 
    
    params = None
    currGameScreen = None
    currGameScreenName = None
    toSetGameScreen = None
    game = None
    gameThread = None
    
    def __init__(self, propertiesFilePath):
        pygame.init()   
        pygame.display.init()
        pygame.display.set_mode([100, 100]) 
        
        properties = GameHelper.load_game_properties(propertiesFilePath)
        
        Game.GAME_DIRECTORY = properties["GAME_DIRECTORY"]
        Game.GAME_SCREENS_DIRECTORY = properties["GAME_SCREENS_DIRECTORY"]
        Game.GAME_SAVES_DIRECTORY = properties["GAME_SAVES_DIRECTORY"]
        
        tmpPath = Game.GAME_DIRECTORY + Default.TMP_FOLDER
        CommonHelper.make_dir(tmpPath)
        CommonHelper.copy_all_files(Game.GAME_SCREENS_DIRECTORY, tmpPath)
        Game.GAME_SCREENS_DIRECTORY = tmpPath
        
        GameScreenFactory.gameScreensPath = tmpPath
        GameScreenFactory.gameScreens = GameHelper.get_game_screens(tmpPath)
        
        self.set_screen(properties["START_SCREEN_NAME"])
        
        Game.game = self
    
    def set_screen(self, gameScreenName): 
        if not gameScreenName in GameScreenFactory.get_screen_names() :
            raise Exception(gameScreenName.__str__() + " not in gameScreenFactory")
        
        Game.currGameScreenName = gameScreenName
        
        if Game.currGameScreen == None :
            Game.currGameScreen = GameScreenFactory.get_screen(gameScreenName)
            return

        GameScreenFactory.save_game_screen(Game.currGameScreenName, Game.currGameScreen, Game.GAME_DIRECTORY + Game.GAME_SCREENS_DIRECTORY)         
        Game.toSetGameScreen = GameScreenFactory.get_screen(gameScreenName)
        
    def start_game(self):
        
        while 1 :
            if Game.toSetGameScreen != None :
                Game.currGameScreen = Game.toSetGameScreen
                Game.toSetGameScreen = None
                
            if Game.currGameScreen == None :
                raise Exception("currGameScreen for game is not set")
            
            for event in pygame.event.get() :
                if event.type == pygame.QUIT: 
                    CommonHelper.delete_dir(Game.GAME_DIRECTORY + Default.TMP_FOLDER)
                    sys.exit()
                    
            Keyboard.get_pressed()
            
            if Keyboard.is_down(pygame.K_LCTRL) and Keyboard.is_down(pygame.K_d) :
                DebugHelper.run_debugger()
            
            
            if Keyboard.is_down(pygame.K_LCTRL) and Keyboard.is_down(pygame.K_s) :
                newProperties =  MainMenuHelper.save_game(Game.GAME_SAVES_DIRECTORY, GameScreenFactory.gameScreens, Game.currGameScreenName, Game.currGameScreen)
                Game.currGameScreen = newProperties["CURR_GAME_SCREEN"]
                Game.GAME_SCREENS_DIRECTORY = newProperties["GAME_SCREENS_DIRECTORY"]
                GameScreenFactory.gameScreensPath = newProperties["GAME_SCREENS_DIRECTORY"]
                GameScreenFactory.gameScreens = newProperties["GAME_SCREENS"]
                Keyboard.get_pressed()
            
            for gameObject in Game.currGameScreen.activeObjects.values() :
                gameObject.analyze_state()
            for gameObject in Game.currGameScreen.activeObjects.values() :
                gameObject.interpret_state()
                
            Game.currGameScreen.refreshScreen()
            
            
            #obj1 = Game.currGameScreen.activeObjects[2]
            #obj2 = Game.currGameScreen.activeObjects[4]
            #DebugHelper.draw_borders(Game.currGameScreen.surface, obj1)
            #DebugHelper.draw_borders(Game.currGameScreen.surface, obj2)
               