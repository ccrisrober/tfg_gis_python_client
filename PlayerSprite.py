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

class PlayerSprite(sf.TransformableDrawable):
    
    def __init__(self, ident):
        self.id = ident
        self.visibility = True
        self.shape = sf.RectangleShape()
        self.shape.size = sf.Vector2(64, 64)
        color = sf.Color.BLACK
        
        c = ident % 5
        
        if c == 0:
            color = sf.Color.RED
        elif c == 1:
            color = sf.Color.BLUE
        elif c == 2:
            color = sf.Color.GREEN
        elif c == 3:
            color = sf.Color.YELLOW
        elif c == 4:
            color = sf.Color.MAGENTA
            
        self.shape.fill_color = color
    '''
    def get_id(self):
        return self.__id


    def get_visibility(self):
        return self.__visibility


    def set_visibility(self, value):
        self.__visibility = value
    '''
    def local_bounds (self):
        return sf.Rectangle(0, 0, 64, 64)
    
    def global_bounds (self):
        return self.transform.transform_rectangle(self.local_bounds())
            
    def draw(self, target, states):
        states.transform *= self.transform
        target.draw(self.shape, states)

    '''
    id = property(get_id)
    visibility = property(get_visibility, set_visibility)
    '''
    
    