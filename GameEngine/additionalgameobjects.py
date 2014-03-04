from basichelpers import *
from gamehelpers import *
from commons import * 
from abc import ABCMeta, abstractmethod

class Tile(SerializableObject):
    __metaclass__ = ABCMeta  
 
    @abstractmethod
    def __init__(self):
        self.centerx = None
        self.centery = None
 
    @abstractmethod 
    def draw_tile(self):
        pass
 
class TiledSpace(Tile) :
    def __init__(self, width, height, showBorders = True):
        self.width = width
        self.height = height 
        self.horizontalLines = []
        self.verticalLines = [] 
        self.rowCount = 1
        self.colCount = 1 
        self.tilesCoords = {} 
        self.showBorders = showBorders
        self.tiles = {}
        self.offX = 0
        self.offY = 0
    
    def clear(self):
        pass
    
    def prepare(self):
        pass   
    
    def add_tile(self, index, tileObject):
        self.tiles[index] = tileObject
        tileCenter = self.get_tile_center(index,self.offX,self.offY)
        tileObject.centerx = tileCenter[0]
        tileObject.centery = tileCenter[1]
    
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
    
    def draw_tile(self, surface, offX = None, offY = None, showBorders = None, showNums = None):
        
        for tileNum in self.tiles :
            tile = self.tiles[tileNum]
            if tile != None :
                try :
                    #rysowanie TiledSpace
                    tiledSpaceOffX = self.tilesCoords[tileNum][Corners.TOP_LEFT][0]
                    tiledSpaceOffY = self.tilesCoords[tileNum][Corners.TOP_LEFT][1]
                    tile.draw_tile(surface, offX + tiledSpaceOffX, offY + tiledSpaceOffY, showBorders, showNums)
                except TypeError :
                    print "Tile" + tileNum.__str__() + "is not a tiledSpace"
                    
                    tileCenterCoords = self.get_tile_center(tileNum, offX, offY)
                    tile.centerx = tileCenterCoords[0] 
                    tile.centery = tileCenterCoords[1]
                    tile.draw_tile()
        
        if showBorders == True or (showBorders == None and self.showBorders == True):
            self.draw_borders(surface, offX, offY)
        
        if showNums == True :
            for tileNum in self.tilesCoords :
                DrawingHelper.draw_simple_text(tileNum.__str__(), surface, self.get_tile_center(tileNum, offX-2, offY-2), Colours.RED)
        
                
        
    
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