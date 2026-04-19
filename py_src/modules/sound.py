import pygame
import os

class SoundManager:
    def __init__(self):
        self._sounds = {}
        self.is_muted = False
        self.active_sounds = {}
        self._sound_id_counter = 0

    def init(self, audio_dir):
        # Load individual audio files if available.
        # Howler in JS used audio sprite, but in Python it's easier if we use the loose MP3s.
        # I'll check src/assets/sounds/
        sounds = ['barkDucks', 'champ', 'gunSound', 'laugh', 'loserSound', 'ohYeah', 'quacking', 'quak', 'sniff', 'thud']
        for s in sounds:
            path = os.path.join(audio_dir, f"{s}.mp3")
            if os.path.exists(path):
                self._sounds[s] = pygame.mixer.Sound(path)

    def play(self, sound_name, loop=0):
        if sound_name not in self._sounds:
            return None
        
        if self.is_muted:
            return None

        sound = self._sounds[sound_name]
        channel = sound.play(loops=loop)
        
        self._sound_id_counter += 1
        self.active_sounds[self._sound_id_counter] = channel
        return self._sound_id_counter

    def stop(self, sound_id):
        if sound_id in self.active_sounds and self.active_sounds[sound_id] is not None:
            self.active_sounds[sound_id].stop()
            del self.active_sounds[sound_id]

    def pause(self, sound_id):
        if sound_id in self.active_sounds and self.active_sounds[sound_id] is not None:
            self.active_sounds[sound_id].pause()

    def resume(self, sound_id):
        if sound_id in self.active_sounds and self.active_sounds[sound_id] is not None:
            self.active_sounds[sound_id].unpause()

    def mute(self, is_muted):
        self.is_muted = is_muted
        if self.is_muted:
            for ch in self.active_sounds.values():
                if ch:
                    ch.set_volume(0)
        else:
            for ch in self.active_sounds.values():
                if ch:
                    ch.set_volume(1)

sound = SoundManager()
