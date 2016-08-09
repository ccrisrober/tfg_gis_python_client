'''
Created on 24/1/2015

@author: maldicion069
'''

class TMove:
    
    def __init__(self):
        pass
    
    def load(self, node):
        pos = node["Pos"]
        self.x = float(pos["X"])
        self.y = float(pos["Y"])
        self.id = int(node["Id"])
        

class TNew:
    
    def __init__(self):
        pass
    
    def load(self, node):
        self.x = float(node["PosX"])
        self.y = float(node["PosY"])
        self.id = int(node["Id"])
        
    
class TExit:
    
    def __init__(self):
        pass
    
    def load(self, node):
        self.id = int(node["Id"])
    
    
class THide:
    
    def __init__(self):
        pass
    
    def load(self, node):
        return node["Ids"]
    
    
class TFinishBattle:
    
    def __init__(self):
        pass
    
    def load(self, node):
        self.winner = int(node["Winner"])
        self.valueMe = int(node["ValueClient"])
        self.valueEnemy = int(node["ValueEnemy"])
        
class TRemObject:
    
    def __init__(self):
        pass
    
    def load(self, node):
        self.obj = int(node["Id_obj"])
        
class TAddObj:
    
    def __init__(self):
        pass
    
    def load(self, node):
        self.id_obj = int(node["Id"])
        self.posx = float(node["PosX"])
        self.posy = float(node["PosY"])
        self.color = str(node["Color"])
    
class TGetObjFromServer:
    
    def __init__(self):
        pass
    
    def load(self, node):
        self.id = int(node["Id"])
        self.ok = int(node["OK"])
    
class TLiberateObj:
    
    def __init__(self):
        pass
    
    def load(self, node):
        self.id = int(node["Id"])
        self.ok = int(node["OK"])
    