from GameEngine.gamehelpers import TextureHelper, ResourceManager, SoundHelper 
from commons import Default, GlobalParams, SerializableObject
from abc import ABCMeta, abstractmethod
from game import Game


class BasicGameObject(SerializableObject):
    __metaclass__ = ABCMeta    
    
    UID = 0 
    
    def __init__(self):
        self.UID = BasicGameObject.UID
        BasicGameObject.UID += 1
    
    @abstractmethod
    def interpret_state(self):
        pass
    
    @abstractmethod
    def analyze_state(self):
        pass
    
class BasicDrawable(BasicGameObject):
    def __init__(self, posX, posY, screen, texturePath):
        BasicGameObject.__init__(self)
        self.screen = screen; 
        print screen
        self.sourceID = TextureHelper.allocate_texture(screen, texturePath)
        self.__posX = posX
        self.__posY = posY
        
    def prepare(self):
        self.source = TextureHelper.get_texture(self.screen, self.sourceID)    
        self.destRect = self.source.get_rect() 
        self.move_graphic_to_position(self.__posX, self.__posY)
        
    def clear(self):    
        self.source = None
        self.destRect = None
    
    def analyze_state(self):
        BasicGameObject.analyze_state(self)
    
    def interpret_state(self):
        BasicGameObject.interpret_state(self)
        self.draw()

    def draw(self):
        if self.source != None and self.destRect != None :
            Game.game.currGameScreen.draw(self)
        else :
            print "unable to draw object UID = " + self.UID.__str__()
    
    def set_new_source(self, surface):
        self.sourceID = self.screen.resourceManager.get_surface_id(surface)
        self.source = surface
        self.destRect = self.source.get_rect()
    
    def move_graphic_to_position(self, posX, posY):
        self.destRect.centerx = posX
        self.destRect.centery = posY


class ExtendedDrawable(BasicDrawable):
    def __init__(self, posX, posY, screen, texturePath = None):
        if texturePath == None:
            texturePath = Default.EXTENDED_DRAWABLE_TEXTURE 
        BasicDrawable.__init__(self, posX, posY, screen, texturePath)
        self.graphicPosX = posX
        self.graphicPosY = posY
    
    def move_graphic_to_position(self, posX, posY):
        BasicDrawable.move_graphic_to_position(self,posX,posY)
        self.graphicPosX = posX
        self.graphicPosY = posY
        
        
class ExtendedGameObject(BasicGameObject):
    
    def __init__(self, posX, posY, maxWidth, maxHeight):
        BasicGameObject.__init__(self)
        self.posX = posX
        self.posY = posY
        self.additionalAttributes = {} 
        self.actions = {}
        self.previousActionsI = []
        self.nextActionsI = []
        #szerokosc w maksymalnym miejscu
        self.maxWidth = maxWidth
        #wysokosc w maksymalnym miejscu
        self.maxHeight = maxHeight
        
        #slownik {sekcja : [wspolrzedne pktow]} ---- DO ZROBIENIA
        
        #wspolrzedne punktow tworzacych krawedzie obiektu, jezeli None to krawedzie obiektu
        #sa brane z jego posX,posY i maxWidth, maxHeight, czyli obiekt jest prostokatem
        #collisionGroups.len >= 2, punktem odniesienia jest punkt (top,left) = (0,0), 
        #wspolrzedne x,y > 0, rosna w kierunku (bottom,right) tak jak wspolrzedne ekranu
        self.collisionGroups = None
        #kat nachylenia obiektu 0 = pionowo
        self.currAngle = 0.0
        """
        do dodania w przyszlosci
        self.activeGameObjects = {}
        self.passiveGameObjects = {}
        """
        
    def analyze_state(self):
        newActions = []

        for action in self.nextActionsI :
            if not self.actions[action[0]].has_ended(self):
                newActions.append(action)        
                
        for actionCode in self.actions :
            if self.actions[actionCode].is_triggered(self) :  
                newActions.append((actionCode, self.actions[actionCode].get_additional_info()))
                
        self.nextActionsI = newActions
       
    def interpret_state(self):
        
        for actionI in self.nextActionsI :
            if self.actions[actionI[0]].is_exclusive(self) :
                self.nextActionsI = [actionI]
                break
        
        for actionI in self.nextActionsI :
            action = self.actions[actionI[0]]
            action.set_action_object(self)
            action.invoke_actions()
        if self.nextActionsI.__len__() != 0 :
            if self.previousActionsI.__len__() == GlobalParams.PREVIOUS_ACTIONS_CACHE_SIZE :
                self.previousActionsI.__delslice__(0,1)
            self.previousActionsI.append(self.nextActionsI)
    
    def get_center(self):
        return (self.maxWidth/2, self.maxHeight/2)
     
    def get_top(self):
        return self.posY - self.maxHeight/2
    
    def get_bottom(self):
        return self.posY + self.maxHeight/2
    
    def get_left(self):
        return self.posX - self.maxWidth/2
    
    def get_right(self):
        return self.posX + self.maxWidth/2
    
    #funkcje pomocnicze START
    def previous_actions_empty(self):
        if self.previousActionsI.__len__() == 0:
            return True
        return False
        
    def was_invoked_previously(self, actionCode):
        if self.previousActionsI.__len__() != 0 :
            prevActions = self.previousActionsI[-1]
            for actionI in prevActions :
                if actionI[0] == actionCode :
                    return True
        return False    
     
    def is_to_be_invoked(self, actionCode):
        for actionI in self.nextActionsI :
            if actionI[0] == actionCode :
                return True
        return False    
    
    def move_by_offset(self, offX, offY):
        self.posX += offX
        self.posY += offY
    
    def move_to_position(self, posX, posY):
        self.posX = posX
        self.posY = posY


class ExtendedDrawableGameObject(ExtendedGameObject, ExtendedDrawable):
   
    def __init__(self, posX, posY, maxWidth, maxHeight, screen,  texturePath = None):
        self.texturesIDs = {}
        self.soundsIDs = {}
        self.textures = {}
        self.sounds = {}
        self.animationDelay = 0
        self.stepsSinceAnimRefresh = 0
        self.soundDelay = 0
        self.stepsSinceSoundRefresh = 0
        self.lastTexture = None
        self.lastSound = None
        if texturePath == None :
            texturePath = Default.EXTENDED_DRAWABLE_OBJECT_TEXTURE
        ExtendedGameObject.__init__(self, posX, posY, maxWidth, maxHeight)
        ExtendedDrawable.__init__(self, posX, posY, screen, texturePath)
   
    def prepare(self):
        ExtendedGameObject.prepare(self)
        ExtendedDrawable.prepare(self)
        self.prepare_sounds()
        self.prepare_textures()
        self.move_graphics_to_logic_position()
   
    def clear(self):
        ExtendedDrawable.clear(self)
        ExtendedGameObject.clear(self)
        self.sounds = {}
        self.textures = {}
   
    def prepare_textures(self):
        for actionInfo in self.texturesIDs :
            self.textures[actionInfo] = TextureHelper.get_textures(self.screen, self.texturesIDs[actionInfo])
         
    def prepare_sounds(self):
        for actionInfo in self.soundsIDs :
            self.sounds[actionInfo] = SoundHelper.get_sounds(self.screen, self.soundsIDs[actionInfo]) 
   
    def interpret_state(self):
        ExtendedGameObject.interpret_state(self)
        for actionI in self.nextActionsI :
            action = self.actions[actionI[0]]
            action.invoke_animated_actions()
    
    def analyze_state(self):
        ExtendedGameObject.analyze_state(self)
        self.interpret_state()
 
    def move_graphics_to_logic_position(self):
        ExtendedDrawable.move_graphic_to_position(self,self.posX, self.posY)
         
    
