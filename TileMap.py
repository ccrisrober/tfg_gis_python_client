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

class TileMap(sf.TransformableDrawable):
    
    def __init__(self):
        self.tileset = None
        self.final_tile = None
        #vertices = sf.VertexArray()
        self.vertices = sf.VertexArray(sf.PrimitiveType.QUADS)
        self.types = []
    
    def load(self, tileset, tile_size, tiles, width, height):
        # load the tileset texture
        try:
            self.tileset = sf.Texture.from_file(tileset)
            
            # resize the vertex array to fit the level size
            self.vertices.resize(width * height * 4)
            
            # populate the vertex array, with one quad per tile
            print ("Inicio cargo del mapa {0}-{1}".format(width, height))
            for i in range(width):
                self.types.append([])
                print ("Fila {0}".format(i))
                for j in range(height):
                    print ("Columna {0}".format(j))
                    # get the current tile number
                    tile_number = tiles[i + j * width]
                    
                    self.types[i].append(tile_number)
                    
                    # find its position in the tileset texture
                    s = int(self.tileset.size.x)
                    tu = int(tile_number % (s / tile_size.x))
                    tv = int(tile_number / (s / tile_size.x))
            
                    if tile_number == 6:
                        self.final_tile = sf.Rectangle(sf.Vector2(i * tile_size.x, j * tile_size.y), sf.Vector2(tile_size.x, tile_size.y))
            
                    p = (i + j * width) * 4
                    self.vertices[p + 0].position = sf.Vector2(i * tile_size.x, j * tile_size.y)
                    self.vertices[p + 1].position = sf.Vector2((i + 1) * tile_size.x, j * tile_size.y)
                    self.vertices[p + 2].position = sf.Vector2((i + 1) * tile_size.x, (j + 1) * tile_size.y)
                    self.vertices[p + 3].position = sf.Vector2(i * tile_size.x, (j + 1) * tile_size.y)
                    
                    self.vertices[p + 0].tex_coords = sf.Vector2(tu * tile_size.x, tv * tile_size.y)
                    self.vertices[p + 1].tex_coords = sf.Vector2((tu + 1) * tile_size.x, tv * tile_size.y)
                    self.vertices[p + 2].tex_coords = sf.Vector2((tu + 1) * tile_size.x, (tv + 1) * tile_size.y)
                    self.vertices[p + 3].tex_coords = sf.Vector2(tu * tile_size.x, (tv + 1) * tile_size.y)
            
            
                    # get a pointer to the current tile´s quad
                    #quad = self.vertices[(i + j * width) * 4]
                    #print ("Obtenido tile quad {0}".format(quad))
                    
                    # define its 4 corners
                    
                    
                    '''
                    quad[0].position = sf.Vector2(i * tile_size.x, j * tile_size.y);
                    quad[1].position = sf.Vector2((i + 1) * tile_size.x, j * tile_size.y);
                    quad[2].position = sf.Vector2((i + 1) * tile_size.x, (j + 1) * tile_size.y);
                    quad[3].position = sf.Vector2(i * tile_size.x, (j + 1) * tile_size.y);
    
                    # define its 4 texture coordinates
                    quad[0].texCoords = sf.Vector2(tu * tile_size.x, tv * tile_size.y);
                    quad[1].texCoords = sf.Vector2((tu + 1) * tile_size.x, tv * tile_size.y);
                    quad[2].texCoords = sf.Vector2((tu + 1) * tile_size.x, (tv + 1) * tile_size.y);
                    quad[3].texCoords = sf.Vector2(tu * tile_size.x, (tv + 1) * tile_size.y);
                    '''
            print ("Cargado")
            return True
        except IOError: 
            print ("No cargado")
            return False
    
    
    
    
    def draw(self, target, states):
        # apply the transform
        states.transform *= self.transform
        
        # apply the tileset texture
        states.texture = self.tileset
        
        # draw the vertex array
        target.draw(self.vertices, states)

        # print ("Pinta")