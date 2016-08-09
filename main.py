'''
Copyright (c) 2015, maldicion069 (Cristian Rodríguez) <ccrisrober@gmail.con>
//
Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.
//
THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
'''

import sfml as sf
import json
import sys
import TCP.ClientToServer
import TCP.ServerToClient
from Animation import Animation
from TileMap import TileMap
from AnimatedSprite import AnimatedSprite
from PlayerSprite import PlayerSprite
import math
from random import randint

# CONST
UP = 0
LEFT = 1
RIGHT = 2
DOWN = 3
FIGHT = 4
#PORT = 8081
MAXBUFFINIT = 3072
SEMIBUFF = 512
TILESETNAME = "tileset.png"
WIDTH = 768
HEIGHT = 576
DEFAULT_OBJECTS_TEXT = "Objects: "
DEFAULT_HEADER_TEXT = "Soltar con P + Num(x)"
MAX_OPACITY = 15

# Global vars
sendToServerTime = 1/50
ident = -1
id_fight = -1
texture = None
textureSwim = None
textureEven = None
textureOdd = None
texture_fight = None
players = {}
keyboard = []
keyObjects = {}
userObjects = {}


tFinishBattle_toClient = TCP.ServerToClient.TFinishBattle()
tMove_toClient = TCP.ServerToClient.TMove()
tNew_toClient = TCP.ServerToClient.TNew()
tExit_toClient = TCP.ServerToClient.TExit()
tHide_toClient = TCP.ServerToClient.THide()
tRemObj_toClient = TCP.ServerToClient.TRemObject()
tAddObj_toClient = TCP.ServerToClient.TAddObj() 
tGetObjFromServer_toClient = TCP.ServerToClient.TGetObjFromServer()
tLiberateFromServer_toClient = TCP.ServerToClient.TLiberateObj()

# Simulamos enum porque solo existen a partir de la 3.4
def enum(**enums):
    return type("Enum", (), enums)

FightStates = enum(NOT_BATTLE=-1, INIT=1, DIE_RANDOM=2, FINISH=3, DIE_PLAYER=4)

def send_exit_client(socket):
    socket.send(TCP.ClientToServer.generateTExit().encode("utf-8"))
    socket.disconnect()

def fix_color5(v, color, speed):
    if color == 5:
        v += speed / 2
    else:
        v += speed
    return v

def split_(strg, delim):
    split = strg.split(delim)
    ret = []
    for e in split:
        if e != '':
            ret.append(int(e))
    return ret

def load_texture(texture, name):
    try:
        texture = sf.Texture.from_file(name)
        return texture
    except IOError: return False
 
def add_key(id, color, px, py):
    k = None
    if color == "Red":
        k = Key(Red, id, sf.Vector2(px, py))
    elif color == "Green":
        k = Key(Green, id, sf.Vector2(px, py))
    elif color == "Yellow":
        k = Key(Yellow, id, sf.Vector2(px, py))
    elif color == "Blue":  
        k = Key(Blue, id, sf.Vector2(px, py)) 
    if k:
        keyObjects[id] = k   

def release_object(id_obj, animated_sprite, objectFooterString, objectFooterText, socket):
    socket.send( TCP.ClientToServer.generateTFreeObject(keyObjects[id_obj], id_obj).encode("utf-8"))
    pass
    
def get_map(decoded):
    global ident, players
    
    mapx = decoded["Map"]
    mapFields = mapx["MapFields"]
    
    key_objects = mapx["KeyObjects"]
    for k, v in key_objects.items():
        color = str(v["Color"])
        px = float(v["PosX"])
        py = float(v["PosY"])
        _id_ = int(v["Id"])
        add_key(_id_, color, px, py)
        
    map_j = split_(mapFields, ",")
    print (map_j)
    width = int(mapx["Width"])
    height = int(mapx["Height"])
    
    ident = int(decoded["Id"])
    pos_x = float(decoded["X"])
    pos_y = float(decoded["Y"])
    
    # Guardo las posiciones de los usuarios conectados con anterioridad
    users_ = decoded["Users"]
    for k, v in users_.items():
        print ("{0} => {1}".format(k, v))
        _id_ = int(v["Id"])
        if _id_ != ident:
            _x_ = float(v["PosX"])
            _y_ = float(v["PosY"])
            
            ps = PlayerSprite(_id_)
            ps.position = (_x_, _y_)
            players[_id_] = ps
            
    objects_ = decoded["Objects"]
    for k, v in objects_.items():
        _id_ = int(v["Id"])
        _x_ = float(v["PosX"])
        _y_ = float(v["PosY"])
        k = Key(Key.int_to_enum(_id_), _id_, sf.Vector2(_x_, _y_))
        k.disponible = True
        k.visible = False
        userObjects[_id_] = k
        key_objects[_id_] = k
            
    print ("WIDTH: {0} HEIGHT: {1}".format(width, height))
    return (width, height, pos_x, pos_y, map_j)

def set_animations(texture):
    
    walking_down = Animation()
    walking_up = Animation()
    walking_left = Animation()
    walking_right = Animation()
        
    walking_down.texture = texture
    walking_down.add_frame(sf.Rectangle((64, 0), (64, 64)))
    walking_down.add_frame(sf.Rectangle((128, 0), (64, 64)))
    walking_down.add_frame(sf.Rectangle((64, 0), (64, 64)))
    walking_down.add_frame(sf.Rectangle((0, 0), (64, 64)))

    walking_up.texture = texture
    walking_up.add_frame(sf.Rectangle((64, 192), (64, 64)))
    walking_up.add_frame(sf.Rectangle((128, 192), (64, 64)))
    walking_up.add_frame(sf.Rectangle((64, 192), (64, 64)))
    walking_up.add_frame(sf.Rectangle((0, 192), (64, 64)))

    walking_left.texture = texture
    walking_left.add_frame(sf.Rectangle((64, 64), (64, 64)))
    walking_left.add_frame(sf.Rectangle((128, 64), (64, 64)))
    walking_left.add_frame(sf.Rectangle((64, 64), (64, 64)))
    walking_left.add_frame(sf.Rectangle((0, 64), (64, 64)))

    walking_right.texture = texture
    walking_right.add_frame(sf.Rectangle((64, 128), (64, 64)))
    walking_right.add_frame(sf.Rectangle((128, 128), (64, 64)))
    walking_right.add_frame(sf.Rectangle((64, 128), (64, 64)))
    walking_right.add_frame(sf.Rectangle((0, 128), (64, 64)))
    
    return (walking_down, walking_left, walking_right, walking_up)

def fix_buffer_tcp(buffer):
    return buffer[:buffer.rfind('}')+1]

def get_port():
    with open("test.txt", "r") as f:
        return int(f.readline())

def define_keyboard(keyboard, ident): 
    if ident % 2 == 0:
        keyboard.append(sf.Keyboard.UP)
        keyboard.append(sf.Keyboard.LEFT)
        keyboard.append(sf.Keyboard.RIGHT)
        keyboard.append(sf.Keyboard.DOWN)
        keyboard.append(sf.Keyboard.R_CONTROL)
        print ("Configuracion normal")
        return textureEven
    else:
        keyboard.append(sf.Keyboard.W)
        keyboard.append(sf.Keyboard.A)
        keyboard.append(sf.Keyboard.D)
        keyboard.append(sf.Keyboard.S)
        keyboard.append(sf.Keyboard.Z)
        print ("Configuracion WASD")
        return textureOdd
     
def init_socket(socket):
    server = sf.IpAddress.from_string("127.0.0.1")
    # Read port from file
    socket.connect(server, get_port())
    
def init_game(socket, parser, map_j):
    msg = fix_buffer_tcp(socket.receive(MAXBUFFINIT).decode("utf-8"))
    
    print ("Received {0}".format(msg))
    
    decoded = json.loads(msg)
    
    ret = get_map(decoded)
    
    width_json = ret[0]
    height_json = ret[1]
    pos_x = ret[2]
    pos_y = ret[3]
    vv = ret[4]
    
    print ("VV: {0}".format(vv))
    
    print ("WIDTH: {0} HEIGHT: {1}".format(width_json, height_json))
    print ("ID: {0}".format(id))
    
    # create the tilemap from the level definition
    if not map_j.load(TILESETNAME, sf.Vector2(64, 64), vv, width_json, height_json):
        return False
    return (pos_x, pos_y)

if __name__ == '__main__':
    # setup window
    window = sf.RenderWindow(sf.VideoMode(WIDTH, HEIGHT), "Client Game")
    window.framerate_limit = 60
    window.vertical_synchronization = True
    window.key_repeat_enabled = False
    
    print ("TCP STLYE")
    
    buffer = None
    received = 0
    msg = ""
    parser = None
    socket = sf.TcpSocket()
    init_socket(socket)
    
    username = None
    if len(sys.argv) > 0:
        username = sys.argv[1]
    else:
        username = raw_input("Ingresa tu nombre: ")
        
    print "Cargando ..."
    
    msg = TCP.ClientToServer.generateTInitWName(username)
    
    try:
        map_j = TileMap()
        ret = init_game(socket, parser, map_j)
        pos_x = ret[0]
        pos_y = ret[1]
        
        # load textures
        textureEven = load_texture(textureEven, "Player.png")
        textureOdd = load_texture(textureOdd, "Player2.png")
        textureSwim = load_texture(textureSwim, "PlayerSwim.png")
        texture_fight = load_texture(texture_fight, "fight.png")
        
        font = sf.Font.from_file("arial.ttf")
        
        vDatoInt = 0
        
        # Asigno teclas segun si es par o impar
        texture = define_keyboard(keyboard, ident)
        
        animated_sprite = AnimatedSprite(sf.seconds(0.2), True, False)
        
        ret = set_animations(texture)
        walking_down = ret[0]
        walking_left = ret[1]
        walking_right = ret[2]
        walking_up = ret[3]
        current_animation = walking_down
        
        animated_sprite.texture = texture
        
        animated_sprite.position = (320, 320)
        
        final_tile = map_j.final_tile # TODO map_j.get_final_tile()
        
        frame_clock = sf.Clock()
        
        speed = 80
        no_key_was_pressed = True
        zoom = 1
        collision = False
        
        cam = window.default_view
        
        cam.center = animated_sprite.position
        window.view = cam
        
        orig_cam = window.default_view
        
        die_roll_label = sf.Text("", font)
        
        pulsa_y = False
        go_y = False
        
        socket.blocking = False
        
        buffer_ = None
        
        battle = False
        
        fight_bg = sf.Sprite(texture_fight)
        
        fight_state = FightStates.NOT_BATTLE
        
        collision_blocks = set()
        collision_blocks.update([1, 4])
        
        # Asigno identificador al AnimatedSprite
        animated_sprite.id = ident
        
        counter_battle_init = 0
        title_battle_init_opacity = MAX_OPACITY
        
        collision_key = -1
        collision_enemy = -1
        
        finish_game = False
        
        object_footer_bg = sf.RectangleShape(sf.Vector2(WIDTH, 75))
        object_footer_bg.fill_color = sf.Color.WHITE
        object_footer_bg.move(sf.Vector2(-64, HEIGHT))
        
        object_footer_string = DEFAULT_OBJECTS_TEXT
        
        object_footer_text = sf.Text("Objects: ", font)
        object_footer_text.color = sf.Color.BLACK
        object_footer_text.move(sf.Vector2(-58, HEIGHT))
        object_footer_text.scale(sf.Vector2(0.75, 0.75))
        
        object_header_bg = sf.RectangleShape(sf.Vector2(WIDTH/2 - 90, 75))
        object_header_bg.fill_color = sf.Color.WHITE
        object_header_bg.move(sf.Vector2(WIDTH/2 + 80, 0))
        
        object_header_text = sf.Text(DEFAULT_HEADER_TEXT, font)
        object_header_text.color = sf.Color.BLUE
        object_header_text.move(sf.Vector2(WIDTH/2 + 90, 40))
        object_header_text.scale(sf.Vector2(0.75, 0.75))
        
        animated_sprite.position = (320, 320)
        
        finish_game = False
        
        while window.is_open:
            if battle:
                for event in window.events:
                    if type(event) is sf.CloseEvent:
                        # window.close()
                        finish_game = True
                if fight_state == FightStates.INIT:
                    pass
                elif fight_state == FightStates.DIE_RANDOM:
                    if sf.Keyboard.is_key_pressed(sf.Keyboard.RETURN):
                        fight_state = FightStates.DIE_PLAYER
                elif fight_state == FightStates.DIE_PLAYER:
                    pass
                elif fight_state == FightStates.FINISH:
                    if sf.Keyboard.is_key_pressed(sf.Keyboard.RETURN):
                        fight_state = FightStates.QUIT
                elif fight_state == FightStates.QUIT:
                    pass
            else:
                fight_state = FightStates.NOT_BATTLE # Reset figth state
                
                # TODO TPC!!
                #if socket.receive(3072).decode("utf-8") == sf
                #if socket.receive(3072) == sf.Socket.DONE:
                #    pass
                
                for event in window.events:
                    if type(event) is sf.CloseEvent:
                        # window.close()
                        finish_game = True
                    if type(event) is sf.KeyEvent and event.pressed and event.code is sf.Keyboard.RETURN:
                        window.close()
                    
                    #if event.pressed and event.code is sf.Keyboard.Y:
                    #    if type(event) is sf.KeyEvent and event.pressed:
                    #        if not pulsa_y:
                    #            pulsa_y = True
                    #            go_y = not go_y
                    #            print(go_y)
                    #    elif type(event) is sf.KeyEvent and event.release:
                    #        pulsa_y = False
                    
                speed = 160 if go_y else 80
                
                frame_time = frame_clock.restart()
                
                # if a key was pressed, set the correct animation and move correctly
                movement = sf.Vector2(0.0, 0.0)
                
                if sf.Keyboard.is_key_pressed(keyboard[UP]):
                    color = map_j.types[round(animated_sprite.global_bounds.left / 64)][round((animated_sprite.global_bounds.top - 32) / 64)]
                    current_animation = walking_up
                    
                    # TODO: Queda color 7
                    
                    if not color in collision_blocks:
                        color = map_j.types[round(animated_sprite.global_bounds.left / 64)][round(animated_sprite.global_bounds.top / 64 + 0.5)]
                        movement.y = fix_color5(movement.y, color, -speed)
                        no_key_was_pressed = False
                        animated_sprite.texture = textureSwim if color == 8 else texture
                    else:
                        collision = True
                
                elif sf.Keyboard.is_key_pressed(keyboard[DOWN]):
                    color = map_j.types[round(animated_sprite.global_bounds.left / 64)][math.ceil((animated_sprite.global_bounds.top) / 64)]
                    current_animation = walking_down
                    
                    # TODO: Queda color 7
                    
                    if not color in collision_blocks:
                        color = map_j.types[round(animated_sprite.global_bounds.left / 64)][round(animated_sprite.global_bounds.top / 64 + 0.5)]
                        movement.y = fix_color5(movement.y, color, +speed)
                        no_key_was_pressed = False
                        animated_sprite.texture = textureSwim if color == 8 else texture
                    else:
                        collision = True
                elif sf.Keyboard.is_key_pressed(keyboard[LEFT]):
                    color = map_j.types[round((animated_sprite.global_bounds.left - 32) / 64)][round(animated_sprite.global_bounds.top / 64)]
                    current_animation = walking_left
                    
                    # TODO: Queda color 7
                    
                    if not color in collision_blocks:
                        color = map_j.types[round(animated_sprite.global_bounds.left / 64)][round(animated_sprite.global_bounds.top / 64)]
                        movement.x = fix_color5(movement.x, color, -speed)
                        no_key_was_pressed = False
                        animated_sprite.texture = textureSwim if color == 8 else texture
                    else:
                        collision = True
                elif sf.Keyboard.is_key_pressed(keyboard[RIGHT]):
                    color = map_j.types[math.ceil((animated_sprite.global_bounds.left + 1) / 64)][round(animated_sprite.global_bounds.top / 64)];
                    current_animation = walking_right
                    
                    # TODO: Queda color 7
                    
                    if not color in collision_blocks:
                        color = map_j.types[round(animated_sprite.global_bounds.left / 64)][round(animated_sprite.global_bounds.top / 64)];
                        movement.x = fix_color5(movement.x, color, +speed)
                        no_key_was_pressed = False
                        animated_sprite.texture = textureSwim if color == 8 else texture
                    else:
                        collision = True
                
                if sf.Keyboard.is_key_pressed(sf.Keyboard.Q):
                    if zoom < 15:
                        cam.zoom = 1.05
                        zoom += 1.05
                        print ("Zoom +: {0}".format(zoom))
                elif sf.Keyboard.is_key_pressed(sf.Keyboard.E):
                    if zoom > -15:
                        cam.zoom = 0.95
                        zoom -= 0.95
                        print ("Zoom -: {0}".format(zoom))
                elif sf.Keyboard.is_key_pressed(sf.Keyboard.L_CONTROL):
                    cam = orig_cam
                    cam.center = animated_sprite.position
                    zoom = 0
                
                if sf.Keyboard.is_key_pressed(sf.Keyboard.B):
                    movement.x *= 4
                    movement.y *= 4
                    
                # TODO: Objetos!!
                
                
                
                # //TODO: Objetos!!
                
                
                if sf.Keyboard.is_key_pressed(keyboard[FIGHT]):
                    for identf, p in players.items():
                        if p.visibility and p.global_bounds().intersection(animated_sprite.global_bounds):
                            print ("Colision enemiga")
                            collision_enemy = p.id
                            break
                
                animated_sprite.play(current_animation)
                
                pos = movement * frame_time.seconds
                animated_sprite.move(pos)
                cam.move(pos.x, pos.y)
                
                object_footer_bg.move(sf.Vector2(pos.x, pos.y))
                object_footer_text.move(sf.Vector2(pos.x, pos.y))
                object_header_bg.move(sf.Vector2(pos.x, pos.y))
                object_header_text.move(sf.Vector2(pos.x, pos.y))
                
                pos = animated_sprite.position
                
                if no_key_was_pressed:
                    animated_sprite.stop()
                else:
                    message = TCP.ClientToServer.generateTMove(animated_sprite.global_bounds, ident)
                    socket.send(message.encode("utf-8"))
                    
                no_key_was_pressed = True
                
                # Update animated_sprite
                animated_sprite.update(frame_time)
            
            # draw
            window.clear()
            window.draw(map_j)
            
            if collision_key >= 0:
                pass
            elif collision_enemy >= 0:
                message = TCP.ClientToServer.generateTFight(collision_enemy)
                socket.send(message.encode("utf-8"))
                collision_enemy = -1
                fight_state = FightStates.INIT
            # TODO : ARREGLAR!!
            #elif animated_sprite.global_bounds().container(sf.Vector2(final_tile.left, final_tile.top)):
            #    print ("Colisionando con fin del juego")
            #    finish_game = True
                
            # TODO: Imprimimos objetos!!
            
            
            # /// TODO: Imprimimos objetos!!
                
            window.draw(animated_sprite)
            
            window.draw(object_footer_bg)
            window.draw(object_footer_text)
            
            if userObjects:
                window.draw(object_header_bg)
                window.draw(object_header_text)
                
            if battle:
                color = sf.Color.BLACK
                color.a = title_battle_init_opacity
                window.clear(color)
                if fight_state == FightStates.INIT:
                    if frame_clock.elapsed_time.seconds  > 0.15:
                        print (frame_clock.elapsed_time.seconds)
                        title_battle_init_opacity -= 15
                        frame_clock.restart()
                    window.draw(fight_bg)
                    
                    if title_battle_init_opacity == 0:
                        fight_state = FightStates.DIE_RANDOM
                        
                        die_roll_label.position = animated_sprite.position
                        die_roll_label.scale(sf.Vector2(5, 5))
                        die_roll_label.move(sf.Vector2(0, 20))
                        
                elif fight_state == FightStates.INIT:
                    # TODO: center num
                    if frame_clock.elapsed_time.seconds  > 0.15:
                        vDatoInt = randint(1, 6)
                        die_roll_label.string = str(vDatoInt)
                        frame_clock.restart()
                    window.draw(die_roll_label)
                    
                elif fight_state == FightStates.DIE_PLAYER:
                    print ("Pedimos al server el valor final")
                    message = TCP.ClientToServer.generateTDiePlayer(id_fight)
                    socket.send(message.encode("utf-8"))
                    fight_state = FightStates.FINISH
                    
                elif fight_state == FightStates.FINISH:
                    pass
                    
                elif fight_state == FightStates.QUIT:
                    print ("And the winner is ... ")
                    message = socket.receive(SEMIBUFF)
                    message = fix_buffer_tcp(message)
                    
                    decoded = json.loads(message)
                    # TODO: Control errores!
                    
                    t_finish_battle = TCP.ServerToClient.TFinishBattle()
                    t_finish_battle.load(decoded)
                    
                    if t_finish_battle.winner == -1:
                        print ("TIE :D:")
                        battle = False
                    elif t_finish_battle.winner == ident:
                        print ("YOU WIN!!!")
                        battle = False
                    else:
                        finish_game = True
                
                fight_state = FightStates.NOT_BATTLE
                title_battle_init_opacity = MAX_OPACITY    
            if finish_game:
                break
            window.display()
        
                
        
        # Aviso al servidor de que me desconecto
        send_exit_client(socket)
        finish_texture = sf.Texture.from_file("finish.png")
        finish_sprite = sf.Sprite(finish_texture)
        finish_sprite.position = ((WIDTH - finish_texture.size.x - 90)/2, (HEIGHT - finish_texture.size.y)/2)
        animated_sprite.position = finish_sprite.position
        
        p = PlayerSprite(3)
        p.position = finish_sprite.position
        
        window.view = orig_cam
        
        while window.is_open:
            for event in window.events:
                if type(event) is sf.CloseEvent:
                    window.close()
                    
            if sf.Keyboard.is_key_pressed(sf.Keyboard.RETURN):
                window.close()
            window.clear(sf.Color.WHITE)
            window.draw(finish_sprite)
            window.draw(animated_sprite)
            window.draw(p)
            window.display()
    except Exception as e:
        # Aviso al servidor de que me desconecto
        send_exit_client(socket)
        print ("Exception {0}".format(e))
        raise e