from basichelpers import *
from gamehelpers import *
from commons import * 
from abc import ABCMeta, abstractmethod
from time import sleep
from mouse import Mouse

class Tile(SerializableObject):
    __metaclass__ = ABCMeta  
 
    def __init__(self):
        self.focused = False
        self.active = False
        self.is_visible = False
        self.tileThread = None
        self.offX = 0
        self.offY = 0
 
    def focus(self):
        self.focused = True
    
    def unfocus(self):
        self.focused = False      
        
    def activate(self):    
        self.active = True
            
    def deactivate(self):
        self.active = False
    
    def hide_tile(self):
        self.is_visible = False    
        
    def show_tile(self,surface):
        self.is_visible = True
        self.tileThread = Thread(target = Tile.on_visible, args = (self, surface) )
        self.tileThread.start()

    @staticmethod
    def on_visible(obj, surface):
        while obj.is_visible :
            if obj.active:
                obj.on_activated_action(surface)
            elif obj.focused:
                obj.on_focus_action(surface)
            else:
                obj.on_not_focused_action(surface)
        
 
    @abstractmethod 
    def on_not_focused_action(self, surface):
        pass
    
    @abstractmethod
    def on_focus_action(self,surface):
        pass
    
    @abstractmethod
    def on_activated_action(self,surface):
        pass
        
class Button(Tile):
    def prepare(self):
        pass
    
    def clear(self):
        pass
    
    def on_not_focused_action(self, surface):
        pass
    
    def on_focus_action(self,surface):
        pass
    
    def on_activated_action(self,surface):
        pass

        
class TiledSpace(Tile) :
    def __init__(self, width, height, showBorders = True, showNums = False):
        Tile.__init__(self)
        self.width = width
        self.height = height 
        self.horizontalLines = []
        self.verticalLines = [] 
        self.rowCount = 1
        self.colCount = 1 
        self.tilesCoords = {} 
        self.showBorders = showBorders
        self.showNums = showNums
        self.tiles = {}
        self.is_main_tile = False
    
    def clear(self):
        pass
    
    def prepare(self):
        pass   
        
    def on_focus_action(self,surface):       
        while self.focused :
            index = self.get_tile_index_from_mouse_position()
            isMouseOver = self.is_mouse_over_screen()
            if index != None :
                print "index " + index.__str__()
                self.unfocus()
                self.tiles[index].focus()
                self.tiles[index].on_focus_action(surface)
            elif not isMouseOver :
                print "mouse not over " + self.__str__() 
                sleep(1)
                self.unfocus()
                self.unfocus_all()
            elif index == None :
                print "index == None " + self.__str__()
                sleep(1)
                self.unfocus_all()
        
        if self.is_main_tile and not self.is_any_tile_focused():
            print "here"
            self.focus()
        
        
    def on_activated_action(self,surface):
        pass
    
    def on_not_focused_action(self, surface):
        offX = self.offX
        offY = self.offY
        
        for tileNum in self.tiles :
            tile = self.tiles[tileNum]
            if tile != None :
                tile.offX  = offX + self.tilesCoords[tileNum][Corners.TOP_LEFT][0]
                tile.offY = offY + self.tilesCoords[tileNum][Corners.TOP_LEFT][1]    
                tile.on_not_focused_action(surface)

        if self.showBorders == True:
            self.draw_borders(surface, offX, offY)
        
        if self.showNums == True :
            for tileNum in self.tilesCoords :
                DrawingHelper.draw_simple_text(tileNum.__str__(), surface, self.get_tile_center(tileNum, offX-2, offY-2), Colours.RED)    
    
        if self.is_main_tile and not self.is_any_tile_focused():
            print "no tile focused"
            self.focus()
        else :
            print "other focused"
    
        pygame.display.update()
        
    
    def add_tile(self, index, tileObject):
        tileObject.offX = self.tilesCoords[index][Corners.TOP_LEFT][0]
        tileObject.offY = self.tilesCoords[index][Corners.TOP_LEFT][1]
        self.tiles[index] = tileObject

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
        
        self.colCount = xList.__len__() - 1
        self.rowCount = yList.__len__() - 1
        
        for i in range(1, self.colCount * self.rowCount + 1) :
            self.tilesCoords[i] = {}
            self.tiles[i] = None
        
        for xCoord in xList:
            self.verticalLines.append( ((xCoord,0),(xCoord,yMax)) )
        for yCoord in yList:
            self.horizontalLines.append( ((0,yCoord),(xMax,yCoord)) )
        
        self.make_tiles()    
    
    def get_tile_index_from_mouse_position(self):
        position = Mouse.position
        if position != None :
            for tileNum in self.tilesCoords :
                if self.tiles[tileNum] != None :
                    tileCoords = self.tilesCoords[tileNum]
                    A = MathHelper.move_point_by_shift(tileCoords[Corners.TOP_LEFT], self.offX, self.offY)
                    B = MathHelper.move_point_by_shift(tileCoords[Corners.TOP_RIGHT], self.offX, self.offY)
                    D = MathHelper.move_point_by_shift(tileCoords[Corners.BOTTOM_LEFT], self.offX, self.offY)
                    if MathHelper.check_if_point_inside_rectangle(position, A , B, D) :
                        return tileNum
        return None
            
    def is_mouse_over_screen(self):
        A = (self.offX, self.offY)
        B = (self.offX + self.width, self.offY)
        D = (self.offX, self.offY + self.height)
        position = Mouse.position
        if position != None and MathHelper.check_if_point_inside_rectangle(position, A, B, D) :
            return True
        return False
    
    def is_any_tile_focused(self):
        for tileNum in self.tiles :
            tile = self.tiles[tileNum]
            if tile != None :
                if tile.focused :
                    return True
                else:
                    try:
                        return tile.is_any_tile_focused()
                    except Exception:
                        return False
        return False
                
    
    def unfocus_all(self):
        for tileNum in self.tiles :
            tile = self.tiles[tileNum]
            if tile != None :
                tile.unfocus()
    
    def draw_borders(self, surface, offX = None, offY = None):
        if offX == None :
            offX = self.offX
        if offY == None :
            offY = self.offY
        tilesBorders = self.get_tiles_borders()
        toDraw = []
        for tileNum in tilesBorders:
            for border in tilesBorders[tileNum].values() :
                toDraw.append(MathHelper.move_line_by_shift(border, offX, offY))
        DrawingHelper.draw_lines(toDraw, surface)
        
                
    def make_tiles(self):
        currHorizontal = 0
        currVertical = 0
        
        for vertical in self.verticalLines :
            for horizontal in self.horizontalLines :
                intersectionPoint = MathHelper.line_intersection(horizontal, vertical)
                upRight = None
                upLeft = None
                downLeft = None
                downRight = None
                
                if currVertical == 0 :
                    if currHorizontal == 0 :
                        downRight = self.get_tile_index(1, 1)
                    elif currHorizontal == self.rowCount :
                        upRight = self.get_tile_index(self.rowCount, 1)
                    else :
                        upRight = self.get_tile_index(currHorizontal, currVertical + 1)
                        downRight = self.get_tile_index(currHorizontal + 1, currVertical + 1)
                elif currVertical == self.colCount :
                    if currHorizontal == 0 :
                        downLeft = self.get_tile_index(1, self.colCount)
                    elif currHorizontal == self.rowCount :
                        upLeft = self.get_tile_index(self.rowCount, self.colCount)
                    else :
                        upLeft = self.get_tile_index(currHorizontal, currVertical)
                        downLeft = self.get_tile_index(currHorizontal + 1, currVertical)
                elif currHorizontal == 0 :
                    downLeft = self.get_tile_index(1, currVertical)
                    downRight = self.get_tile_index(1, currVertical + 1)
                elif currHorizontal == self.rowCount :
                    upLeft = self.get_tile_index(self.rowCount, currVertical)
                    upRight = self.get_tile_index(self.rowCount, currVertical + 1)
                else : 
                    upLeft = self.get_tile_index(currHorizontal, currVertical)
                    upRight = self.get_tile_index(currHorizontal, currVertical + 1)
                    downLeft = self.get_tile_index(currHorizontal + 1, currVertical)
                    downRight = self.get_tile_index(currHorizontal + 1, currVertical + 1)
                
                if upRight != None :
                    self.tilesCoords[upRight][Corners.BOTTOM_LEFT] = intersectionPoint
                if upLeft != None :
                    self.tilesCoords[upLeft][Corners.BOTTOM_RIGHT] = intersectionPoint
                if downRight != None :
                    self.tilesCoords[downRight][Corners.TOP_LEFT] = intersectionPoint
                if downLeft != None :
                    self.tilesCoords[downLeft][Corners.TOP_RIGHT] = intersectionPoint
  
                currHorizontal += 1
            currHorizontal = 0
            currVertical += 1
     
    def get_tile_borders(self, index):
        tile = self.tilesCoords[index]
        result= {}
        result[Side.TOP] = (tile[Corners.TOP_LEFT], tile[Corners.TOP_RIGHT])
        result[Side.RIGHT] = (tile[Corners.TOP_RIGHT], tile[Corners.BOTTOM_RIGHT])
        result[Side.BOTTOM] = (tile[Corners.BOTTOM_RIGHT], tile[Corners.BOTTOM_LEFT])
        result[Side.LEFT] = (tile[Corners.BOTTOM_LEFT], tile[Corners.TOP_LEFT])
        return result
    
    def get_tiles_borders(self):
        result = {}
        for tileNum in self.tilesCoords :
            result[tileNum] = self.get_tile_borders(tileNum)
            
        return result
    
    def get_tile_center(self, tileNum, offX, offY):
        tileBorders = self.get_tile_borders(tileNum)
        tileCenterCoords = MathHelper.get_square_center(MathHelper.move_line_by_shift(tileBorders[Side.LEFT], offX, offY)\
                                                        ,MathHelper.move_line_by_shift(tileBorders[Side.TOP], offX, offY) )
        
        return tileCenterCoords
     
        
    def get_tile_by_row_col(self, row, col):
        return self.tilesCoords[self.get_tile_index(row, col)]
    
    def get_tile_index(self, row, col):
        return  (row - 1) * self.colCount + col  
     
    def get_tile_by_index(self, index):
        if index in self.tilesCoords :
            return self.tilesCoords[index]
        else :
            return {} 
        
    def get_right_tile(self, index):
        return self.tilesCoords[index + 1]
        
    def get_left_tile(self, index):
        return self.tilesCoords[index - 1]
        
    def get_top_tile(self, index):
        return self.tilesCoords[index - self.colCount]
        
    def get_bottom_tile(self, index):
        return self.tilesCoords[index + self.colCount]