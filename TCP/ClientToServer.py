'''
Created on 24/1/2015

@author: maldicion069
'''
import json
    
def generateTInitWName(name):
    return json.dumps({"Action": "initWName", "Name": name})
    
def generateTDiePlayer(id_enemy):
    return json.dumps({"Action": "finishBattle", "Id_enemy": id_enemy})

def generateTFight(id_enemy):
    return json.dumps({"Action": "fight", "Id_enemy": id_enemy})

def generateTExit():
    return json.dumps({"Action": "exit"})

def generateTMove(fr, ident):
    return json.dumps({"Action": "move", "Pos": {"X": fr.top, "Y": fr.left}, "Id": ident})

def generateTGetObject(id_obj, id_user):
    return json.dumps({"Action": "getObj", "Id_obj": id_obj, "Id_user": id_user})

def generateTFreeObject(key, id_user):
    return json.dumps({"Action": "freeObj", "Obj": {"Id_obj": key.id, "PosX": key.position.x, "PosY": key.position.y}, "Id_user": id_user})