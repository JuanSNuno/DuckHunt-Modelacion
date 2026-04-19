import pygame
from libs.assets import Assets
from libs.tweening import Timeline, TweenManager

class Character(pygame.sprite.Sprite):
    def __init__(self, sprite_id, states):
        super().__init__()
        self.states = states
        self.sprite_id = sprite_id
        
        all_textures = Assets.get_all_textures()
        
        for state_obj in self.states:
            state_name = state_obj['name']
            textures = []
            prefix = f"{sprite_id}/{state_name}/"
            
            matching_keys = sorted([k for k in all_textures.keys() if k.startswith(prefix)])
            for k in matching_keys:
                textures.append(all_textures[k])
                
            state_obj['textures'] = textures

            if len(state_obj['textures']) == 1:
                state_obj['textures'] = state_obj['textures'] + state_obj['textures']
        
        self.textures = self.states[0]['textures']
        self.animation_speed = self.states[0]['animationSpeed']
        self.loop = self.states[0].get('loop', True)
        
        self.image = self.textures[0]
        self.rect = self.image.get_rect()
        
        self.x = 0.0
        self.y = 0.0
        self.anchor = (0.5, 0.5)
        
        self.timeline = Timeline()
        TweenManager.add(self.timeline)
        
        self._state_val = self.states[0]['name']
        self.current_frame = 0.0
        self.playing = True
        self.visible = True

    def stop_and_clear_timeline(self):
        self.timeline.kill()
        self.timeline = Timeline()
        TweenManager.add(self.timeline)
        return self

    def is_active(self):
        return self.timeline.is_active()

    @property
    def state(self):
        return self._state_val

    @state.setter
    def state(self, value):
        state_obj = next((s for s in self.states if s['name'] == value), None)
        if not state_obj:
            raise ValueError(f"The requested state ({value}) is not available.")
        
        self._state_val = value
        self.textures = state_obj['textures']
        self.animation_speed = state_obj['animationSpeed']
        self.loop = state_obj.get('loop', True)
        self.current_frame = 0.0
        self.play()

    def play(self):
        self.playing = True

    def pause(self):
        self.playing = False

    def update(self, dt):
        if self.playing and len(self.textures) > 0:
            self.current_frame += self.animation_speed * (dt * 60)
            
            if self.current_frame >= len(self.textures):
                if self.loop:
                    self.current_frame %= len(self.textures)
                else:
                    self.current_frame = len(self.textures) - 1
                    self.playing = False
                    
            self.image = self.textures[int(self.current_frame)]
            
        # Update rect position based on anchor
        self.rect.x = int(self.x - self.rect.width * self.anchor[0])
        self.rect.y = int(self.y - self.rect.height * self.anchor[1])
