from commons import Side, Direction, Default
from actions import AnimatedAction
from keyboard import Keyboard
from GameEngine.gamehelpers import TextureHelper, SoundHelper, MathHelper, AnimationHelper
from gameobjects import ExtendedDrawableGameObject
import pygame

class BasicMovingCharacter(ExtendedDrawableGameObject):
    
    MOVE_ACTION = "MOVE_ACTION"
    STOP_ACTION = "STOP_ACTION"
    TEXTURES = Default.GAME_ENGINE_TEXTURES_PATH + "basicMovingCreature/"
    SOUNDS = Default.GAME_ENGINE_SOUNDS_PATH + "basicMovingCreature/"
      
    def __init__(self, posX, posY, maxWidth, maxHeight, screen, texturePath = None):
        ExtendedDrawableGameObject.__init__(self, posX, posY, maxWidth, maxHeight, screen, texturePath)
        
        self.animationDelay = 50
        self.soundDelay = 50
        self.steering = { Direction.UP : pygame.K_UP, Direction.DOWN : pygame.K_DOWN, Direction.LEFT : pygame.K_LEFT, Direction.RIGHT : pygame.K_RIGHT }
        self.moveSpeeds = {Direction.UP : 0.5, Direction.DOWN : 0.5, Direction.LEFT : 0.5, Direction.RIGHT : 0.5}
        
        self.texturesIDs[(BasicMovingCharacter.MOVE_ACTION, Direction.UP)] = TextureHelper.allocate_textures(self.screen, [BasicMovingCharacter.TEXTURES + "hbs1.png", BasicMovingCharacter.TEXTURES + "hbs2.png"])
        self.texturesIDs[(BasicMovingCharacter.MOVE_ACTION, Direction.DOWN)] = TextureHelper.allocate_textures(self.screen, [BasicMovingCharacter.TEXTURES + "hfs1.png", BasicMovingCharacter.TEXTURES + "hfs2.png"])
        self.texturesIDs[(BasicMovingCharacter.MOVE_ACTION, Direction.LEFT)] = TextureHelper.allocate_textures(self.screen, [BasicMovingCharacter.TEXTURES + "hs2s.png", BasicMovingCharacter.TEXTURES + "hs2s1.png"])
        self.texturesIDs[(BasicMovingCharacter.MOVE_ACTION, Direction.RIGHT)] = TextureHelper.allocate_textures(self.screen, [BasicMovingCharacter.TEXTURES + "hss.png", BasicMovingCharacter.TEXTURES + "hss1.png"])
        self.texturesIDs[(BasicMovingCharacter.MOVE_ACTION, Direction.UP_LEFT)] = TextureHelper.allocate_textures(self.screen, [BasicMovingCharacter.TEXTURES + "hs2s.png", BasicMovingCharacter.TEXTURES + "hs2s1.png"])
        self.texturesIDs[(BasicMovingCharacter.MOVE_ACTION, Direction.UP_RIGHT)] = TextureHelper.allocate_textures(self.screen, [BasicMovingCharacter.TEXTURES + "hss.png", BasicMovingCharacter.TEXTURES + "hss1.png"])
        self.texturesIDs[(BasicMovingCharacter.MOVE_ACTION, Direction.DOWN_LEFT)] = TextureHelper.allocate_textures(self.screen, [BasicMovingCharacter.TEXTURES + "hs2s.png", BasicMovingCharacter.TEXTURES + "hs2s1.png"])
        self.texturesIDs[(BasicMovingCharacter.MOVE_ACTION, Direction.DOWN_RIGHT)] = TextureHelper.allocate_textures(self.screen, [BasicMovingCharacter.TEXTURES + "hss.png", BasicMovingCharacter.TEXTURES + "hss1.png"])
        self.texturesIDs[(BasicMovingCharacter.STOP_ACTION, Side.FRONT)] = TextureHelper.allocate_textures(self.screen, [BasicMovingCharacter.TEXTURES + "hbs.png"])
        
        self.soundsIDs[(BasicMovingCharacter.MOVE_ACTION, Default.DEFAULT_ACTION)] = SoundHelper.alllocate_sounds(self.screen, [BasicMovingCharacter.SOUNDS + "step.wav"])
        

class BasicMovingCharacter_MoveAction(AnimatedAction):
    
    def map_directions(self, directions):
        if Direction.UP in directions :
            if Direction.RIGHT in directions :
                return Direction.UP_RIGHT
            if Direction.LEFT in directions :
                return Direction.UP_LEFT
            return Direction.UP
        if Direction.DOWN in directions :
            if Direction.RIGHT in directions :
                return Direction.DOWN_RIGHT
            if Direction.LEFT in directions :
                return Direction.DOWN_LEFT
            return Direction.DOWN
        if Direction.LEFT in directions : 
            return Direction.LEFT
        if Direction.RIGHT in directions :
            return Direction.RIGHT
        return None
    
    def invoke_actions(self):
        if self.additionalInfo == Direction.UP or self.additionalInfo == Direction.UP_LEFT or self.additionalInfo == Direction.UP_RIGHT :
            self.actionObject.move_by_offset(0, -1 * self.actionObject.moveSpeeds[Direction.UP])
        if self.additionalInfo == Direction.DOWN or self.additionalInfo == Direction.DOWN_LEFT or self.additionalInfo == Direction.DOWN_RIGHT :
            self.actionObject.move_by_offset(0, self.actionObject.moveSpeeds[Direction.DOWN])    
        if self.additionalInfo == Direction.RIGHT or self.additionalInfo == Direction.DOWN_RIGHT or self.additionalInfo == Direction.UP_RIGHT :
            self.actionObject.move_by_offset(self.actionObject.moveSpeeds[Direction.RIGHT] , 0) 
        if self.additionalInfo == Direction.LEFT or self.additionalInfo == Direction.DOWN_LEFT or self.additionalInfo == Direction.UP_LEFT :
            self.actionObject.move_by_offset(-1 * self.actionObject.moveSpeeds[Direction.LEFT] , 0)
        
    def is_triggered(self, obj):
        
        directions = []
        
        for direction in obj.steering :
            if(Keyboard.is_down(obj.steering[direction])) :
                directions.append(direction)

        finalDirection = self.map_directions(directions)
        if finalDirection != None :
            self.additionalInfo = finalDirection
            return True
        
        return False
     
    def has_ended(self, obj):
        return True   
    
    def invoke_animated_actions(self):
        AnimationHelper.default_animation_behaviour(self.actionObject)
        self.actionObject.draw()
    
    def is_exclusive(self, obj):
        return False
    
class BasicMovingCharacter_StopAction(AnimatedAction):
    def invoke_actions(self):
        pass
        
    def is_triggered(self, obj):
        
        directions = []
        
        for direction in obj.steering :
            if(Keyboard.is_down(obj.steering[direction])) :
                directions.append(direction)
        if directions.__len__() != 0 :
            return False
        
        if obj.previous_actions_empty() or not obj.was_invoked_previously(BasicMovingCharacter.STOP_ACTION):
            self.additionalInfo = Side.FRONT
            return True
        else :
            return False
        
        return False
     
    def has_ended(self, obj):
        return True   
    
    def invoke_animated_actions(self):
        AnimationHelper.default_animation_behaviour(self.actionObject)
        if self.actionObject.lastSound != None :
            SoundHelper.stop_sound(self.actionObject.sounds[self.actionObject.lastSound[0]][self.actionObject.lastSound[1]])
        self.actionObject.draw()
    
    def is_exclusive(self, obj):
        return False
  
class BasicRotatingCharacter(ExtendedDrawableGameObject):
    
    MOVE_ACTION = "MOVE_ACTION"
    ROTATE_STOP_ACTION = "ROTATE_STOP_ACTION"
    TEXTURES = Default.GAME_ENGINE_TEXTURES_PATH + "basicRotatingCreature/"
    SOUNDS = Default.GAME_ENGINE_SOUNDS_PATH + "basicRotatingCreature/"
      
    def __init__(self, posX, posY, maxWidth, maxHeight, screen, texturePath = None):
        ExtendedDrawableGameObject.__init__(self, posX, posY, maxWidth, maxHeight, screen, texturePath)

        self.steering = { Direction.FORWARD : pygame.K_UP, Direction.BACKWARD : pygame.K_DOWN, Direction.LEFT : pygame.K_LEFT, Direction.RIGHT : pygame.K_RIGHT }
        self.moveSpeeds = {Direction.FORWARD : 1.0, Direction.BACKWARD : 1.0}
        self.rotationSpeeds = {Direction.LEFT : 1.0, Direction.RIGHT : 1.0}

        self.texturesIDs[(BasicRotatingCharacter.ROTATE_STOP_ACTION, Default.DEFAULT_ACTION)] = TextureHelper.allocate_textures_from_dir(self.screen, BasicRotatingCharacter.TEXTURES + "stop/")
        
    def get_texture_index_from_angle(self):
        rotationStep = 360 / self.textures[(BasicRotatingCharacter.ROTATE_STOP_ACTION, Default.DEFAULT_ACTION)].__len__()
        if float(self.currAngle).is_integer() and int(self.currAngle)%rotationStep == 0 :
            if int(self.currAngle) / rotationStep >= self.textures[(BasicRotatingCharacter.ROTATE_STOP_ACTION, Default.DEFAULT_ACTION)].__len__()\
            or int(self.currAngle) / rotationStep <= -1 * self.textures[(BasicRotatingCharacter.ROTATE_STOP_ACTION, Default.DEFAULT_ACTION)].__len__():
                return 0
            return int(self.currAngle) / rotationStep
        return None
    
class BasicRotatingCharacter_MoveAction(AnimatedAction):
    
    def invoke_actions(self):
        shift = None
        if Direction.FORWARD in self.additionalInfo :
            speed = self.actionObject.moveSpeeds[Direction.FORWARD]
            shift = MathHelper.calculate_shift(self.actionObject.currAngle, 1 , speed, speed)
        elif Direction.BACKWARD in self.additionalInfo :
            speed = self.actionObject.moveSpeeds[Direction.BACKWARD]
            shift = MathHelper.calculate_shift(self.actionObject.currAngle, -1 , speed, speed)
        
        self.actionObject.move_by_offset(shift[0], shift[1])
        
    def is_triggered(self, obj):
        directions = []
        
        for direction in obj.steering :
            if(Keyboard.is_down(obj.steering[direction])) :
                directions.append(direction)
        if Direction.FORWARD in directions or Direction.BACKWARD in directions :
            self.additionalInfo = directions
            return True
        
        return False        
                
    def has_ended(self, obj):
        return True
    
    def invoke_animated_actions(self):
        self.actionObject.move_graphics_to_logic_position()
        self.actionObject.draw()
    
    def is_exclusive(self, obj):
        return False
    

class BasicRotatingCharacter_RotateStopAction(AnimatedAction):
    def invoke_actions(self):
        toSet = self.actionObject.currAngle
        if Direction.LEFT in self.additionalInfo:
            toSet += self.actionObject.rotationSpeeds[Direction.LEFT]
        elif Direction.RIGHT in self.additionalInfo:
            toSet -= self.actionObject.rotationSpeeds[Direction.RIGHT]
        if toSet > 360.0 or toSet < -360.0:
            self.actionObject.currAngle = 0.0
        else :
            self.actionObject.currAngle = toSet 
                
    def is_triggered(self, obj):
        
        directions = []
        
        for direction in obj.steering :
            if(Keyboard.is_down(obj.steering[direction])) :
                directions.append(direction)
        
        if Direction.LEFT in directions or Direction.RIGHT in directions or\
                (directions.__len__() == 0 and obj.previous_actions_empty()) or\
               (directions.__len__() == 0 and obj.was_invoked_previously(BasicRotatingCharacter.ROTATE_STOP_ACTION)) :
            self.additionalInfo = directions
            return True
        
        return False
     
    def has_ended(self, obj):
        return True   
    
    def invoke_animated_actions(self):
        if  self.actionObject.lastTexture == None :
            self.actionObject.lastTexture = ((BasicRotatingCharacter.ROTATE_STOP_ACTION, Default.DEFAULT_ACTION), 0)
            self.actionObject.set_new_source(self.actionObject.textures[self.actionObject.lastTexture[0]][self.actionObject.lastTexture[1]])
        else :
            toSetTextureI = (BasicRotatingCharacter.ROTATE_STOP_ACTION, Default.DEFAULT_ACTION)
            toSetTextureIndex = self.actionObject.get_texture_index_from_angle()
            
            if toSetTextureIndex != None :
                self.actionObject.lastTexture = ( toSetTextureI , toSetTextureIndex )
                self.actionObject.set_new_source(self.actionObject.textures[self.actionObject.lastTexture[0]][self.actionObject.lastTexture[1]])
          
        self.actionObject.move_graphics_to_logic_position()
        self.actionObject.draw()
    
    def is_exclusive(self, obj):
        return False
                                                        
                    


    
    
