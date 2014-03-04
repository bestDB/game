import pygame
from commons import *
from os import listdir, path, makedirs
from os.path import isfile, join, exists
from math import radians, sin, cos
from xml.dom.minidom import parse
from shutil import copy, rmtree

class DrawingHelper :
    @staticmethod
    def draw_lines(lines, surface, colour = Colours.WHITE):
        for line in lines :
                pygame.draw.line(surface, colour, line[0], line[1], 3) 

    @staticmethod
    def draw_simple_text(text, surface, coords, color = Colours.WHITE, fontSize = 10):
        pygame.font.init()
        myfont = pygame.font.SysFont("arial", fontSize)
        label = myfont.render(text, 1, color)
        surface.blit(label, coords)

class XMLHelper :
    
    @staticmethod
    def get_tags_values(fileName) :
        doc = parse(fileName)
        parsedTags = {}
        
        for firstLevelNod in doc.childNodes :
            for secondLevelNod in firstLevelNod.childNodes :
                if secondLevelNod.firstChild != None :
                    parsedTags[secondLevelNod.nodeName.__str__().strip()] = secondLevelNod.firstChild.nodeValue.__str__().strip()       
                    
        return parsedTags
    
    @staticmethod
    def get_tag_value(fileName, tagName):
        doc = parse(fileName)
        
        for node in doc.getElementsByTagName(tagName) :
            return node.firstChild.nodeValue.__str__().strip()
    
    @staticmethod
    def dump_dict_to_xml(dictionary, fileName):
        f = open(fileName, 'w')
        resultXml = XMLHelper.get_xml_from_dict(dictionary,"", "");
        f.write(resultXml)
        f.close
        
    @staticmethod
    def get_xml_from_dict(obj, xml, indent):
        if type(obj) is dict :
            for key in obj :
                xml += indent + "<" + key + ">\n" + XMLHelper.get_xml_from_dict(obj[key], xml, indent + "\t") + indent + "</" + key + ">\n"
            return xml
        else :
            return indent + obj.__str__() + "\n"
            
class FileDirHelper :
    @staticmethod
    def get_dir_list(dirPath):
        return listdir(dirPath)
    
    @staticmethod
    def load_file_list(dirPath):
        files = []
        for f in listdir(dirPath) :
            if isfile(join(dirPath,f)) :
                files.append(join(dirPath,f))
        return files
    
    @staticmethod
    def delete_dir(dirPath):
        if exists(dirPath) :
            rmtree(dirPath)
    
    @staticmethod
    def make_dir(dirPath):
        d = path.dirname(dirPath)
        if exists(dirPath) :
            FileDirHelper.delete_dir(dirPath) 
        makedirs(d)
        
    @staticmethod
    def copy_all_files(src, dest):
        src_files = listdir(src) 
        for file_name in src_files:
            full_file_name = path.join(src, file_name)
            if (path.isfile(full_file_name)):
                copy(full_file_name, dest)
      
class MathHelper:
    @staticmethod
    def get_line_center(line):
        return ( (line[0][0] + line[1][0])/2, (line[0][1] + line[1][1])/2 )
    
    @staticmethod
    def get_square_center(sideLine, topLine):
        y = MathHelper.get_line_center(sideLine)[1]
        x = MathHelper.get_line_center(topLine)[0]
        return (x,y)
    
    @staticmethod
    def move_lines_by_shift(linesList, shX, shY):
        moved = []
        for line in linesList :
            moved.append(MathHelper.move_line_by_shift(line, shX, shY))
        return moved
    
    @staticmethod
    def move_line_by_shift(line, shX, shY):
        return ( (MathHelper.move_point_by_shift(line[0], shX, shY)), (MathHelper.move_point_by_shift(line[1], shX, shY)) )
    
    @staticmethod
    def move_point_by_shift(point, shX, shY):
        return (point[0] + shX, point[1] + shY)
    
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
 