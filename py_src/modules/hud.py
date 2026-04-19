import pygame
from libs.assets import Assets

class TextBox:
    def __init__(self, text, style, location, anchor):
        self.text = text
        self.style = style
        self.location = location
        self.anchor = anchor
        font_name = style.get('fontFamily', 'Arial').lower()
        font_size = int(style.get('fontSize', '18px').replace('px', ''))
        self.font = pygame.font.SysFont(font_name, font_size)
        self.color = (255, 255, 255)
        
    def draw(self, surface, scale_x=1.0, scale_y=1.0):
        if not self.text: return
        text_surface = self.font.render(str(self.text), True, self.color)
        rect = text_surface.get_rect()
        
        x = int((self.location[0] - rect.width * self.anchor[0]) * scale_x)
        y = int((self.location[1] - rect.height * self.anchor[1]) * scale_y)
        
        surface.blit(text_surface, (x, y))

class TextureCounter:
    def __init__(self, texture_key, location, max_val, row_max):
        self.texture_key = texture_key
        self.location = location
        self.max_val = max_val
        self.row_max = row_max
        self.value = 0
        self.texture = Assets.get_texture(texture_key)
        
    def draw(self, surface, scale_x=1.0, scale_y=1.0):
        if not self.texture: return
        val = min(self.value, self.max_val) if self.max_val else self.value
        
        width = self.texture.get_width()
        height = self.texture.get_height()
        
        for i in range(val):
            y_pos = 0
            x_pos_delta = i
            if self.row_max and self.row_max < val:
                y_pos = height * (i // self.row_max)
                x_pos_delta = i % self.row_max
            
            x = int((self.location[0] + width * x_pos_delta) * scale_x)
            y = int((self.location[1] + y_pos) * scale_y)
            
            surface.blit(self.texture, (x, y))

class Hud:
    def __init__(self):
        self._items = {}
        self._values = {}

    def create_text_box(self, name, opts=None):
        if opts is None: opts = {}
        style = opts.get('style', {'fontFamily': 'Arial', 'fontSize': '18px', 'fill': 'white'})
        location = opts.get('location', (0, 0))
        anchor = opts.get('anchor', (0.5, 0.5))
        
        self._items[name] = TextBox("", style, location, anchor)
        self._values[name] = ""

    def create_texture_based_counter(self, name, opts=None):
        if opts is None: opts = {}
        texture = opts.get('texture', '')
        location = opts.get('location', (0, 0))
        max_val = opts.get('max', None)
        row_max = opts.get('rowMax', None)
        
        self._items[name] = TextureCounter(texture, location, max_val, row_max)
        self._values[name] = 0

    def __getattr__(self, name):
        if name in self._values:
            return self._values[name]
        raise AttributeError(f"'Hud' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        if name in ['_items', '_values']:
            super().__setattr__(name, value)
        elif hasattr(self, '_items') and name in self._items:
            self._values[name] = value
            if isinstance(self._items[name], TextBox):
                self._items[name].text = str(value)
            elif isinstance(self._items[name], TextureCounter):
                self._items[name].value = value
        else:
            super().__setattr__(name, value)

    def draw(self, surface, scale_x=1.0, scale_y=1.0):
        for item in self._items.values():
            item.draw(surface, scale_x, scale_y)
