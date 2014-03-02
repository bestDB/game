import pygame, sys
from keyboard import Keyboard
from GameEngine.gamehelpers import DebugHelper, GameHelper, MainMenuHelper
from GameEngine.helpers import FileDirHelper
from screen import GameScreenFactory
from commons import Default


class Game:
    
    game = None
    
    def __init__(self):
        pygame.init()   
        pygame.display.init()
        pygame.display.set_mode([100, 100]) 
        
        self.GAME_DIRECTORY = ""
        self.GAME_SCREENS_DIRECTORY = Default.GAME_SCREENS_PATH
        self.GAME_SAVES_DIRECTORY = Default.GAME_SAVE_PATH 
        self.START_GAME_SCREEN = ""
        
        self.params = None
        self.currGameScreen = None
        self.currGameScreenName = None
        self.toSetGameScreen = None
        self.gameThread = None
        
    
    def prepare_new_game(self, propertiesDir):
        self.set_game_properties(GameHelper.load_game_properties_from_file(propertiesDir))
        tmpPath = self.init_tmp_dir()
        GameScreenFactory.prepare_screen_factory_for_game(tmpPath)
        self.set_screen(self.START_GAME_SCREEN)
        Game.game = self
        
    
    def init_tmp_dir(self):
        tmpPath = self.GAME_DIRECTORY + Default.TMP_FOLDER
        FileDirHelper.make_dir(tmpPath)
        FileDirHelper.copy_all_files(self.GAME_SCREENS_DIRECTORY, tmpPath)
        self.GAME_SCREENS_DIRECTORY = tmpPath
        return tmpPath
        
    
    def set_game_properties(self, propertiesDictionary):
        if Default.PROPERTY_KEY_GAME_DIRECTORY in propertiesDictionary :
            self.GAME_DIRECTORY = propertiesDictionary[Default.PROPERTY_KEY_GAME_DIRECTORY]
        if Default.PROPERTY_KEY_GAME_SCREENS_DIRECTORY in propertiesDictionary :
            self.GAME_SCREENS_DIRECTORY = propertiesDictionary[Default.PROPERTY_KEY_GAME_SCREENS_DIRECTORY]
        if Default.PROPERTY_KEY_GAME_SAVES_DIRECTORY in propertiesDictionary :
            self.GAME_SAVES_DIRECTORY = propertiesDictionary[Default.PROPERTY_KEY_GAME_SAVES_DIRECTORY]
        if Default.PROPERTY_KEY_START_SCREEN_NAME in propertiesDictionary :
            self.START_GAME_SCREEN = propertiesDictionary[Default.PROPERTY_KEY_START_SCREEN_NAME]
        
    
    def set_screen(self, gameScreenName): 
        if not gameScreenName in GameScreenFactory.get_screen_names() :
            raise Exception(gameScreenName.__str__() + " not in gameScreenFactory")
        
        self.currGameScreenName = gameScreenName
        
        if self.currGameScreen == None :
            self.currGameScreen = GameScreenFactory.get_screen(gameScreenName)
            return

        GameScreenFactory.save_game_screen(self.currGameScreenName, self.currGameScreen, self.GAME_DIRECTORY + self.GAME_SCREENS_DIRECTORY)         
        self.toSetGameScreen = GameScreenFactory.get_screen(gameScreenName)
        
    def start_game(self):
        
        while 1 :
            if self.toSetGameScreen != None :
                self.currGameScreen = self.toSetGameScreen
                self.toSetGameScreen = None
                
            if self.currGameScreen == None :
                raise Exception("currGameScreen for game is not set")
            
            for event in pygame.event.get() :
                if event.type == pygame.QUIT: 
                    FileDirHelper.delete_dir(self.GAME_DIRECTORY + Default.TMP_FOLDER)
                    sys.exit()
                    
            Keyboard.get_pressed()
            
            if Keyboard.is_down(pygame.K_LCTRL) and Keyboard.is_down(pygame.K_d) :
                DebugHelper.run_debugger()
            
            
            if Keyboard.is_down(pygame.K_LCTRL) and Keyboard.is_down(pygame.K_s) :
                MainMenuHelper.save_game(self)

                Keyboard.get_pressed()
            
            for gameObject in self.currGameScreen.activeObjects.values() :
                gameObject.analyze_state()
            for gameObject in self.currGameScreen.activeObjects.values() :
                gameObject.interpret_state()
                
            self.currGameScreen.refreshScreen()
            
            
            #obj1 = Game.currGameScreen.activeObjects[2]
            #obj2 = Game.currGameScreen.activeObjects[4]
            #DebugHelper.draw_borders(Game.currGameScreen.surface, obj1)
            #DebugHelper.draw_borders(Game.currGameScreen.surface, obj2)
               