import json
import pygame

class Assets:
    _textures = {}
    _spritesheet = None

    @classmethod
    def load(cls, json_path, img_path):
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        cls._spritesheet = pygame.image.load(img_path).convert_alpha()
        
        for key, val in data['frames'].items():
            frame = val['frame']
            rect = pygame.Rect(frame['x'], frame['y'], frame['w'], frame['h'])
            sub_surface = cls._spritesheet.subsurface(rect)
            
            if val.get('trimmed'):
                # Reconstruct the original untrimmed size
                source_size = val['sourceSize']
                sprite_source_size = val['spriteSourceSize']
                
                # Create a transparent surface of original size
                untrimmed_surface = pygame.Surface((source_size['w'], source_size['h']), pygame.SRCALPHA)
                
                # Blit the trimmed texture at the correct offset
                dest = (sprite_source_size['x'], sprite_source_size['y'])
                untrimmed_surface.blit(sub_surface, dest)
                
                cls._textures[key] = untrimmed_surface
            else:
                cls._textures[key] = sub_surface

    @classmethod
    def get_texture(cls, key):
        return cls._textures.get(key)
    
    @classmethod
    def get_all_textures(cls):
        return cls._textures
