import pygame
from GameEngine.helpers import *
from _elementtree import XMLParser

class GameHelper :
    @staticmethod
    def load_game_properties_from_file(propertiesDir):
        properties = XMLHelper.get_tags_values(propertiesDir + Default.PROPERTIES_FILE_NAME) 
        return properties

class MainMenuHelper :
    
    @staticmethod
    def new_game(gameObject, propertiesDir):
        print "creating menu"
        gameObject.prepare_new_game(propertiesDir)
    
    @staticmethod
    def save_game(gameObject, saveName = None):
        if saveName == None :
            now = datetime.now()
            saveName = now.strftime("%Y-%m-%d_%H-%M-%S")
        fullpath = gameObject.GAME_SAVES_DIRECTORY + saveName + "/"
        
        FileDirHelper.make_dir(fullpath)
        
        pygame.image.save(gameObject.currGameScreen.surface, fullpath + "/screenshot.jpg" )
        
        gameScreens = GameScreenFactoryHelper.get_game_screens(gameObject.GAME_SCREENS_DIRECTORY)
        for screenName in gameScreens :
            if screenName != gameObject.currGameScreenName :
                path = gameScreens[screenName]
                GameScreenFactoryHelper.copy_screen_file(screenName, path, fullpath)
        
        GameScreenFactoryHelper.dump_game_screen(gameObject.currGameScreenName, gameObject.currGameScreen, fullpath)
        
        newGameProperties = {}
        newGameProperties[Default.PROPERTY_KEY_GAME_DIRECTORY] = gameObject.GAME_DIRECTORY
        newGameProperties[Default.PROPERTY_KEY_GAME_SAVES_DIRECTORY] = gameObject.GAME_SAVES_DIRECTORY
        newGameProperties[Default.PROPERTY_KEY_GAME_SCREENS_DIRECTORY] = fullpath
        newGameProperties[Default.PROPERTY_KEY_START_SCREEN_NAME] = gameObject.currGameScreenName


        XMLHelper.dump_dict_to_xml({"Properties" : newGameProperties}, fullpath + "/" + Default.PROPERTIES_FILE_NAME)
        
        MainMenuHelper.load_game(gameObject, fullpath)

        
    @staticmethod
    def get_saved_games(propertiesDir):
        savesPath = XMLHelper.get_tag_value(propertiesDir + Default.PROPERTIES_FILE_NAME, Default.PROPERTY_KEY_GAME_DIRECTORY) +\
            XMLHelper.get_tag_value(propertiesDir + Default.PROPERTIES_FILE_NAME, Default.PROPERTY_KEY_GAME_SAVES_DIRECTORY)

        return FileDirHelper.get_dir_list(savesPath)
        
    
    @staticmethod
    def load_game(gameObject, savepath):
        gameObject.currGameScreen = None
        gameObject.prepare_new_game(savepath)

class GameScreenFactoryHelper :
    
    @staticmethod
    def get_game_screens(gameScreensDirectory):
        screens = {}
        files = FileDirHelper.load_file_list(gameScreensDirectory)
        for file in files :
            ext = "." + file.rpartition(".")[2]
            name = file.rpartition("/")[2].split(".")[0]
            if ext == Default.GAME_SCREEN_EXT :
                screens[name] = file.rpartition(".")[0]
        return screens
    
    @staticmethod
    def dump_game_screen(name, gameScreen, path):
        f = open(path + name + Default.GAME_SCREEN_EXT, 'w')
        gameScreen.clear()
        pickle.dump(gameScreen, f)
        f.close()
        
        
    @staticmethod
    def get_screen(path):
        f = open(path +  Default.GAME_SCREEN_EXT, 'r')
        gameScreen = pickle.load(f) 
        f.close()
        
        gameScreen.prepare()    
            
        return gameScreen
    
    @staticmethod
    def copy_screen_file(name, path, targetDir):
        copyfile(path + Default.GAME_SCREEN_EXT, targetDir + name + Default.GAME_SCREEN_EXT)
  
class ResourceManager :

    def __init__(self):
        self.tPid = 0
        self.sPid = 0
        self.texturesPaths = []
        self.soundsPaths = []
        self.textureSurfaces = []
        self. sounds = []
  
    def allocate_sound(self, path):
        self.soundsPaths.insert(self.sPid, path)
        self.sPid += 1
        return self.sPid - 1
    
    def allocate_texture(self, path):
        self.texturesPaths.insert(self.tPid, path)
        self.tPid += 1
        return self.tPid - 1

    def get_surface_id(self, surface):
        if surface in self.textureSurfaces :
            return self.textureSurfaces.index(surface) 
        
    def get_sound_id(self, sound):
        if sound in self.sounds :
            return self.sounds.index(sound)

    def prepare(self):
        self.textureSurfaces = TextureHelper.load_textures(self.texturesPaths)
        self.sounds = SoundHelper.load_sounds(self.soundsPaths)

    def clear(self):
        self.textureSurfaces = []
        self.sounds = []     
    
class DebugHelper :
    @staticmethod
    def draw_borders(surface, extGO, colour = Colours.WHITE):
        borders = ExtendedGameObjectHelper.get_borders(extGO)
        for borderLines in borders.values() :
            for line in borderLines :
                pygame.draw.line(surface, colour, line[0], line[1], 3) 
        pygame.display.update()
    
    @staticmethod
    def debug_mode():
        while True :
            __command = raw_input(">>>")
            if __command != "exit" :
                try :
                    exec __command
                except :
                    print  "Error:\n\t" + sys.exc_info().__str__()
            else :
                return
        
    @staticmethod
    def run_debugger() :  
        thread = Thread(target = DebugHelper.debug_mode, args = ())
        thread.start()
        while thread != None and thread.is_alive() :
            pass
 
class TextureHelper:
    @staticmethod
    def allocate_texture(screen, path):
        return screen.resourceManager.allocate_texture(path)
     
    @staticmethod
    def allocate_textures(screen, paths):
        result = []
        for path in paths :
            result.append(TextureHelper.allocate_texture(screen, path)) 
        return result
      
    @staticmethod
    def allocate_textures_from_dir(screen, dirPath):
        return TextureHelper.allocate_textures(screen, FileDirHelper.load_file_list(dirPath))  
        
    @staticmethod
    def get_texture(screen, ID):
        return screen.resourceManager.textureSurfaces[ID]
    
    @staticmethod
    def get_textures(screen, ids):
        result = []
        for ID in ids :
            result.append(TextureHelper.get_texture(screen, ID))
        return result     
        
    @staticmethod
    def load_texture(path):
        #print "Loading texture : " + path.__str__()
        result = pygame.image.load(path)
        if path.rpartition(".")[2] == "png":
            result = result.convert_alpha()
        else :
            result = result.convert()
        return result
    
    @staticmethod
    def load_textures(paths):
        loaded = []
        for path in paths:
            loaded.append(TextureHelper.load_texture(path))
        return loaded

class SoundHelper:
    nextId = 0
    
    @staticmethod
    def allocate_sound(screen, path):
        return screen.resourceManager.allocate_sound(path)
     
    @staticmethod
    def alllocate_sounds(screen, paths):
        result = []
        for path in paths :
            result.append(SoundHelper.allocate_sound(screen, path)) 
        return result
        
    @staticmethod
    def get_sound(screen, ID):
        return screen.resourceManager.sounds[ID]
    
    @staticmethod
    def get_sounds(screen, ids):
        result = []
        for ID in ids :
            result.append(SoundHelper.get_sound(screen, ID))
        return result   
        
    @staticmethod    
    def play_sound(sound):
        sound.play()    
        
    @staticmethod    
    def stop_sound(sound):
        if sound != None :
            sound.stop()        
        
    @staticmethod 
    def load_sound(path):
        if path != None :
            #print "Loading sound : " + path.__str__()
            return pygame.mixer.Sound(path)
        return None
    
    @staticmethod
    def load_sounds(paths):
        loaded = []
        for path in paths :
            loaded.append(SoundHelper.load_sound(path))
        return loaded

class ExtendedGameObjectHelper:
    @staticmethod
    def get_non_relative_point(extGO, point):
        center = extGO.get_center()
        diffX = point[0] - center[0]
        diffY = point[1] - center[1]
        return (extGO.posX + diffX, extGO.posY + diffY)
    
    @staticmethod
    def get_borders(extGO):
        borders = {}
        rotationPoint = (extGO.posX, extGO.posY)
        angleInDegrees = extGO.currAngle
        
        if extGO.collisionGroups == None :
            x1 = extGO.get_left()
            x2 = extGO.get_right()
            y1 = extGO.get_bottom()
            y2 = extGO.get_top()
            
            borders[Side.LEFT] = [MathHelper.rotate_line(((x1,y1),(x1,y2)), rotationPoint, angleInDegrees)] 
            borders[Side.TOP] = [MathHelper.rotate_line(((x1,y2),(x2,y2)), rotationPoint, angleInDegrees)]
            borders[Side.RIGHT] = [MathHelper.rotate_line(((x2,y2),(x2,y1)), rotationPoint, angleInDegrees)]
            borders[Side.BOTTOM] = [MathHelper.rotate_line(((x2,y1),(x1,y1)), rotationPoint, angleInDegrees)]
            
        else :
            
            for collisionGroupKey in extGO.collisionGroups :
                collisionGroup = extGO.collisionGroups[collisionGroupKey]
                
                if collisionGroup.__len__() <= 1 :
                    raise Exception("incorrect number of collisionGroups for object. must be |collisionGroups| >=1 ")
            
                for i in  range(0, collisionGroup.__len__() ) :
                    point1 = ExtendedGameObjectHelper.get_non_relative_point(extGO, collisionGroup[i])
                    point2 = ExtendedGameObjectHelper.get_non_relative_point(extGO, collisionGroup[(i + 1) % collisionGroup.__len__()])
                    line = (point1, point2)
                    if collisionGroupKey in borders : 
                        borders[collisionGroupKey].append(MathHelper.rotate_line(line, rotationPoint, angleInDegrees))
                    else :
                        borders[collisionGroupKey] = [(MathHelper.rotate_line(line, rotationPoint, angleInDegrees))]
        return borders
    
    @staticmethod
    def objects_collide(extGO1, extGO2) :
        borders1 = ExtendedGameObjectHelper.get_borders(extGO1)
        borders2 = ExtendedGameObjectHelper.get_borders(extGO2)
        
        collisionGroups = []
        
        for b1key in borders1 :
            b1lines = borders1[b1key]
            for b2key in borders2 :
                b2lines = borders2[b2key]
                for b1 in b1lines :
                    for b2 in b2lines:
                        if MathHelper.crosses(b1, b2) :
                            collisionGroups.append(b1key)
        return collisionGroups
     
class AnimationHelper:
    @staticmethod
    def default_animation_behaviour(extDrawableGO):
        
        if extDrawableGO.nextActionsI.__len__() != 1 :
            raise Exception("default_animation_behaviour works only for one aciton to be invoked")
        
        extDrawableGO.move_graphics_to_logic_position()
        
        nextTexture = AnimationHelper.get_next_texture(extDrawableGO)
        if nextTexture != None :
            if extDrawableGO.lastTexture == None :
                extDrawableGO.stepsSinceAnimRefresh = 0
                extDrawableGO.source = extDrawableGO.textures[nextTexture[0]][nextTexture[1]]
                extDrawableGO.lastTexture = nextTexture
            elif (extDrawableGO.lastTexture[0] == nextTexture[0] and extDrawableGO.stepsSinceAnimRefresh >= extDrawableGO.animationDelay)\
                or extDrawableGO.lastTexture[0] != nextTexture[0] :
                extDrawableGO.stepsSinceAnimRefresh = 0
                extDrawableGO.source = extDrawableGO.textures[nextTexture[0]][nextTexture[1]]
                extDrawableGO.lastTexture = nextTexture
            else :
                extDrawableGO.stepsSinceAnimRefresh += 1
            
        nextSound = AnimationHelper.get_next_sound(extDrawableGO)
        
        if nextSound != None :
            if extDrawableGO.lastSound == None :
                extDrawableGO.stepsSinceSoundRefresh = 0
                SoundHelper.play_sound(extDrawableGO.sounds[nextSound[0]][nextSound[1]])
                extDrawableGO.lastSound = nextSound
            elif (extDrawableGO.lastSound[0] == nextSound[0] and extDrawableGO.stepsSinceSoundRefresh >= extDrawableGO.soundDelay)\
                or extDrawableGO.lastSound[0] != nextSound[0] :
                extDrawableGO.stepsSinceSoundRefresh = 0
                SoundHelper.play_sound(extDrawableGO.sounds[nextSound[0]][nextSound[1]])
                extDrawableGO.lastSound = nextSound
            else :
                extDrawableGO.stepsSinceSoundRefresh += 1      
                        
    @staticmethod
    def get_next_texture(extDrawableGO):
        if extDrawableGO.textures != None :
            if ( extDrawableGO.lastTexture == None or extDrawableGO.lastTexture[0] != extDrawableGO.nextActionsI[0] ) and extDrawableGO.nextActionsI[0] in extDrawableGO.textures and extDrawableGO.textures[extDrawableGO.nextActionsI[0]][0] != None :
                return (extDrawableGO.nextActionsI[0], 0)
            elif extDrawableGO.lastTexture != None and extDrawableGO.lastTexture[0] == extDrawableGO.nextActionsI[0] and extDrawableGO.textures[extDrawableGO.lastTexture[0]].__len__() > extDrawableGO.lastTexture[1] + 1:
                return (extDrawableGO.lastTexture[0], extDrawableGO.lastTexture[1] + 1)
            elif extDrawableGO.lastTexture != None and  extDrawableGO.lastTexture[0] == extDrawableGO.nextActionsI[0] :
                return (extDrawableGO.lastTexture[0], 0)
            elif (extDrawableGO.nextActionsI[0][0], Default.DEFAULT_ACTION) in extDrawableGO.textures and extDrawableGO.textures[(extDrawableGO.nextActionsI[0][0], Default.DEFAULT_ACTION)] != None :
                if extDrawableGO.lastTexture != None and extDrawableGO.textures[(extDrawableGO.nextActionI[0], Default.DEFAULT_ACTION)].__len__() > extDrawableGO.lastTexture[1] + 1 :
                    return ((extDrawableGO.nextActionsI[0][0], Default.DEFAULT_ACTION), extDrawableGO.lastTexture[1] + 1)
                return ((extDrawableGO.nextActionsI[0][0], Default.DEFAULT_ACTION), 0)
            else :
                return None
       
    @staticmethod   
    def get_next_sound(extDrawableGO):
        if extDrawableGO.sounds != None :
            if ( extDrawableGO.lastSound == None or extDrawableGO.lastSound[0] != extDrawableGO.nextActionsI[0] ) and extDrawableGO.nextActionsI[0] in extDrawableGO.sounds and extDrawableGO.sounds[extDrawableGO.nextActionsI[0]][0] != None :
                return (extDrawableGO.nextActionsI[0], 0)
            elif extDrawableGO.lastSound != None and extDrawableGO.lastSound[0] == extDrawableGO.nextActionsI[0] and extDrawableGO.sounds[extDrawableGO.lastSound[0]].__len__() > extDrawableGO.lastSound[1] + 1:
                return (extDrawableGO.lastSound[0], extDrawableGO.lastSound[1] + 1)
            elif extDrawableGO.lastSound != None and extDrawableGO.lastSound[0] == extDrawableGO.nextActionsI[0] :
                return (extDrawableGO.lastSound[0], 0)
            elif (extDrawableGO.nextActionsI[0][0], Default.DEFAULT_ACTION) in extDrawableGO.sounds and extDrawableGO.sounds[(extDrawableGO.nextActionsI[0][0], Default.DEFAULT_ACTION)] != None :
                if extDrawableGO.lastSound != None and extDrawableGO.sounds[(extDrawableGO.nextActionsI[0][0], Default.DEFAULT_ACTION)].__len__() > extDrawableGO.lastSound[1] + 1 :
                    return ((extDrawableGO.nextActionsI[0][0], Default.DEFAULT_ACTION), extDrawableGO.lastSound[1] + 1)
                return ((extDrawableGO.nextActionsI[0][0], Default.DEFAULT_ACTION), 0)
            else :
                return None
        