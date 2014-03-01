import pygame, sys, pickle
from os import listdir, path, makedirs
from os.path import isfile, join
from math import radians, sin, cos
from threading import Thread
from commons import Default, Colours, Side
from xml.dom.minidom import parse
from datetime import datetime
from shutil import copyfile, copy, rmtree

class CommonHelper :
    @staticmethod
    def load_file_list(dirPath):
        files = []
        for f in listdir(dirPath) :
            if isfile(join(dirPath,f)) :
                files.append(join(dirPath,f))
        return files
    
    @staticmethod
    def delete_dir(dirPath):
        rmtree(dirPath)
    
    @staticmethod
    def make_dir(dirPath):
        d = path.dirname(dirPath) 
        makedirs(d)
        
    @staticmethod
    def copy_all_files(src, dest):
        src_files = listdir(src) 
        for file_name in src_files:
            full_file_name = path.join(src, file_name)
            if (path.isfile(full_file_name)):
                copy(full_file_name, dest)

class GameHelper :
    @staticmethod
    def load_game_properties(propertiesFilePath):
        doc = parse(propertiesFilePath)
        properties = {}
        
        for node in doc.getElementsByTagName("GAME_DIRECTORY") :
            properties["GAME_DIRECTORY"] = node.firstChild.nodeValue.__str__()
        
        for node in doc.getElementsByTagName("GAME_SAVES_DIRECTORY") :
            properties["GAME_SAVES_DIRECTORY"] = properties["GAME_DIRECTORY"] + node.firstChild.nodeValue.__str__()
            
        for node in doc.getElementsByTagName("GAME_SCREEN_DIRECTORY") :
            properties["GAME_SCREENS_DIRECTORY"] = properties["GAME_DIRECTORY"] + node.firstChild.nodeValue.__str__()
            
        for node in doc.getElementsByTagName("START_SCREEN_NAME") :
            properties["START_SCREEN_NAME"] = node.firstChild.nodeValue.__str__()
        
        return properties
    
    @staticmethod
    def get_game_screens(gameScreensDirectory):
        screens = {}
        files = CommonHelper.load_file_list(gameScreensDirectory)
        for file in files :
            ext = "." + file.rpartition(".")[2]
            name = file.rpartition("/")[2].split(".")[0]
            if ext == Default.GAME_SCREEN_EXT :
                screens[name] = file.rpartition(".")[0]
        return screens

class MainMenuHelper :
    
    @staticmethod
    def new_game():
        pass
    
    @staticmethod
    def save_game(dir, gameScreens, currScreenName, currScreen, saveName = None):
        
        currGameProperties = {}
        
        if saveName == None :
            now = datetime.now()
            saveName = now.strftime("%Y-%m-%d_%H-%M-%S")
        fullpath = dir + saveName + "/"
        CommonHelper.make_dir(fullpath)
    
        currGameProperties["GAME_SCREENS"] = {}
    
        for screenName in gameScreens :
            path = gameScreens[screenName]
            GameScreenFactoryHelper.copy_screen_file(screenName, path, fullpath)
            currGameProperties["GAME_SCREENS"][screenName] = fullpath + screenName
        
        currScreen.clear() 
        GameScreenFactoryHelper.dump_game_screen(currScreenName, currScreen, fullpath)
        
        currGameProperties["CURR_GAME_SCREEN"] = GameScreenFactoryHelper.get_screen(fullpath + currScreenName)
        currGameProperties["GAME_SCREENS_DIRECTORY"] = fullpath
        
        return currGameProperties
    
    
    @staticmethod
    def load_game():
        pass

class GameScreenFactoryHelper :
    
    @staticmethod
    def dump_game_screen(name, gameScreen, path):
        f = open(path + name + Default.GAME_SCREEN_EXT, 'w')
        pickle.dump(gameScreen, f)
        f.close()
        
        f = open(path + name + Default.RES_MAN_EXT, 'w')
        ResourceManager.unload_resources()
        pickle.dump(ResourceManager.manager, f)
        ResourceManager.reset()    
        f.close()
        
        
    @staticmethod
    def get_screen(path):
        f = open(path +  Default.GAME_SCREEN_EXT, 'r')
        gameScreen = pickle.load(f) 
        f.close()
        
        f = open(path + Default.RES_MAN_EXT)    
        ResourceManager.manager = pickle.load(f)
        ResourceManager.load_resources()
        f.close()
        
        gameScreen.prepare()    
            
        return gameScreen
    
    @staticmethod
    def copy_screen_file(name, path, targetDir):
        copyfile(path + Default.GAME_SCREEN_EXT, targetDir + name + Default.GAME_SCREEN_EXT)
        copyfile(path + Default.RES_MAN_EXT, targetDir + name + Default.RES_MAN_EXT)
  

class ResourceManager :
    
    manager = None

    def __init__(self):
        self.tPid = 0
        self.sPid = 0
        self.texturesPaths = []
        self.soundsPaths = []
        self.textureSurfaces = []
        self. sounds = []
    
    @staticmethod
    def initialize():
        ResourceManager.manager = ResourceManager() 
        
    @staticmethod    
    def set_manager(manager) :
        ResourceManager.manager = manager   
    
    @staticmethod
    def reset():
        ResourceManager.manager.tPid = 0
        ResourceManager.manager.sPid = 0
        ResourceManager.manager.texturesPaths = []
        ResourceManager.manager.soundsPaths = []
        ResourceManager.manager.textureSurfaces = []
        ResourceManager.manager.sounds = []
    
    @staticmethod
    def load_resources():
        ResourceManager.manager.textureSurfaces = TextureHelper.load_textures(ResourceManager.manager.texturesPaths)
        ResourceManager.manager.sounds = SoundHelper.load_sounds(ResourceManager.manager.soundsPaths)

    @staticmethod        
    def allocate_sound(path):
        ResourceManager.manager.soundsPaths.insert(ResourceManager.manager.sPid, path)
        ResourceManager.manager.sPid += 1
        return ResourceManager.manager.sPid - 1
    
    @staticmethod
    def allocate_texture(path):
        ResourceManager.manager.texturesPaths.insert(ResourceManager.manager.tPid, path)
        ResourceManager.manager.tPid += 1
        return ResourceManager.manager.tPid - 1

    @staticmethod
    def unload_resources():
        ResourceManager.manager.textureSurfaces = []
        ResourceManager.manager.sounds = []    
        
    @staticmethod    
    def get_surface_id(surface):
        if surface in ResourceManager.manager.textureSurfaces :
            return ResourceManager.manager.textureSurfaces.index(surface)
        
    @staticmethod
    def get_sound_id(sound):
        if sound in ResourceManager.manager.sounds :
            return ResourceManager.manager.sounds.index(sound)

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
    def allocate_texture(path):
        return ResourceManager.allocate_texture(path)
     
    @staticmethod
    def allocate_textures(paths):
        result = []
        for path in paths :
            result.append(TextureHelper.allocate_texture(path)) 
        return result
      
    @staticmethod
    def allocate_textures_from_dir(dirPath):
        return TextureHelper.allocate_textures(CommonHelper.load_file_list(dirPath))  
        
    @staticmethod
    def get_texture(ID):
        return ResourceManager.manager.textureSurfaces[ID]
    
    @staticmethod
    def get_textures(ids):
        result = []
        for ID in ids :
            result.append(TextureHelper.get_texture(ID))
        return result     
        
    @staticmethod
    def load_texture(path):
        print "Loading texture : " + path.__str__()
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
    def allocate_sound(path):
        return ResourceManager.allocate_sound(path)
     
    @staticmethod
    def alllocate_sounds(paths):
        result = []
        for path in paths :
            result.append(SoundHelper.allocate_sound(path)) 
        return result
        
    @staticmethod
    def get_sound(ID):
        return ResourceManager.manager.sounds[ID]
    
    @staticmethod
    def get_sounds(ids):
        result = []
        for ID in ids :
            result.append(SoundHelper.get_sound(ID))
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
            print "Loading sound : " + path.__str__()
            return pygame.mixer.Sound(path)
        return None
    
    @staticmethod
    def load_sounds(paths):
        loaded = []
        for path in paths :
            loaded.append(SoundHelper.load_sound(path))
        return loaded
    
    @staticmethod
    def create_channel(path):
        sound = pygame.mixer.Sound(path)
        channel = pygame.mixer.Channel(SoundHelper.nextId)
        channel.queue(sound)
        SoundHelper.nextId += 1
        return channel  

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
        
class MathHelper:
    @staticmethod
    def calculate_shift(angle, direction, speedX, speedY):  
        angle = radians(angle % 360)
        shiftY = cos(angle) * speedY
        shiftX = sin(angle) * speedX
        if direction > 0 :
            shiftY *= -1
            shiftX *= -1
        return (shiftX, shiftY)
    
    @staticmethod
    def rotate_line(line, rotationPoint, angleInDegrees):
        "line - ((x1,y1),(x2,y2))"
        if angleInDegrees == 0 :
            return line
        return ( MathHelper.rotate_point(line[0], rotationPoint, angleInDegrees) , MathHelper.rotate_point(line[1], rotationPoint, angleInDegrees))
    
    @staticmethod
    def rotate_point(point, rotationPoint, angleInDegrees):
        """point - wspolrzedne pktu (x,y) do obrocenia
        rotationPoint - wspolrzedne punktu (x,y) wzgledem ktorego ma zostac obrocone"""
        if angleInDegrees == 0 :
            return point
        x = point[0]
        y = point[1]
        x_u = rotationPoint[0]
        y_u = rotationPoint[1]
        angle = radians(-1* angleInDegrees)
        x1 = (x - x_u) * cos(angle) - (y - y_u) * sin(angle) + x_u
        y1 = (x - x_u) * sin(angle) + (y - y_u) * cos(angle) + y_u
        return (x1,y1)
    
    
    @staticmethod
    def line_intersection(line1, line2):
        """
        Return the coordinates of a point of intersection given two lines.
        Return None if the lines are parallel, but non-collinear.
        Return an arbitrary point of intersection if the lines are collinear.
    
        Parameters:
        line1 and line2: lines given by 2 points (a 2-tuple of (x,y)-coords).
        """
        (x1,y1), (x2,y2) = line1
        (u1,v1), (u2,v2) = line2
        (a,b), (c,d) = (x2-x1, u1-u2), (y2-y1, v1-v2)
        e, f = u1-x1, v1-y1
        # Solve ((a,b), (c,d)) * (t,s) = (e,f)
        denom = float(a*d - b*c)
        if MathHelper.near(denom, 0):
            # parallel
            # If collinear, the equation is solvable with t = 0.
            # When t=0, s would have to equal e/b and f/d
            if MathHelper.near(float(e)/b, float(f)/d):
                # collinear
                px = x1
                py = y1
            else:
                return None
        else:
            t = (e*d - b*f)/denom
            # s = (a*f - e*c)/denom
            px = x1 + t*(x2-x1)
            py = y1 + t*(y2-y1)
        return px, py
    
    
    
    @staticmethod
    def crosses(line1, line2):
        """
        Return True if line segment line1 intersects line segment line2 and 
        line1 and line2 are not parallel.
        """
        (x1,y1), (x2,y2) = line1
        (u1,v1), (u2,v2) = line2
        (a,b), (c,d) = (x2-x1, u1-u2), (y2-y1, v1-v2)
        e, f = u1-x1, v1-y1
        denom = float(a*d - b*c)
        if MathHelper.near(denom, 0):
            # parallel
            return False
        else:
            t = (e*d - b*f)/denom
            s = (a*f - e*c)/denom
            # When 0<=t<=1 and 0<=s<=1 the point of intersection occurs within the
            # line segments
            return 0<=t<=1 and 0<=s<=1
    
    @staticmethod
    def near(a, b, rtol=1e-5, atol=1e-8):
        return abs(a - b) < (atol + rtol * abs(b))
    
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
        