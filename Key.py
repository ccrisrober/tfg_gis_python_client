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

def enum(**enums):
    return type("Enum", (), enums)

class Key(sf.TransformableDrawable):
    
    TKey = enum(NOT_COLOR=-1, RED=1, BLUE=2, YELLOW=3, GREEN=4)

    def __init__(self, key_color, id, position = sf.Vector2(0, 0)):
        self.m_sprite = sf::Sprite(Key::m_texture, Key::m_positions[key]);
        self.position = position
        self.id = id
        self.disponible = True
    
    def local_bounds (self):
        return sf.Rectangle(0, 0, 64, 64)
    
    def global_bounds (self):
        return self.transform.transform_rectangle(self.local_bounds())
            
        