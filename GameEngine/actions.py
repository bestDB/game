from abc import ABCMeta, abstractmethod

class Action():
    __metaclass__ = ABCMeta
    
    def __init__(self):
        self.additionalInfo = None
        self.actionObject = None
    
    def set_action_object(self, actionObject):
        self.actionObject = actionObject
        
    def get_additional_info(self):
        return self.additionalInfo    
    
    @abstractmethod
    def invoke_actions(self):
        pass
    
    @abstractmethod
    def is_triggered(self, obj):
        "sprawdza czy akcja ma zostac wykonana i ustawia additionalInfo"    
        pass
    
    @abstractmethod    
    def has_ended(self, obj):
        pass  
    
    @abstractmethod
    def is_exclusive(self, obj):
        pass
            
class AnimatedAction(Action):
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def invoke_animated_actions(self):
        pass  
 