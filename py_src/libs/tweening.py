class Tween:
    def __init__(self, target, duration, properties, on_start=None, on_complete=None, delay=0, yoyo=False, repeat=0, repeat_delay=0):
        self.target = target
        self.duration = duration
        self.properties = properties
        self.on_start = on_start
        self.on_complete = on_complete
        self.delay = delay
        self.yoyo = yoyo
        self.repeat = repeat # 0 means run once, 1 means repeat once.
        self.repeat_delay = repeat_delay
        
        self.elapsed = 0.0
        self.started = False
        self.completed = False
        self.initial_values = {}
        self.current_repeat = 0
        self.is_yoyo_back = False
        self.wait_delay = delay

    def update(self, dt):
        if self.completed:
            return

        if self.wait_delay > 0:
            self.wait_delay -= dt
            if self.wait_delay > 0:
                return
            else:
                dt = -self.wait_delay
                self.wait_delay = 0
        
        if not self.started:
            self.started = True
            for k in self.properties:
                if isinstance(self.target, dict):
                    if k in self.target:
                        self.initial_values[k] = self.target[k]
                    else:
                        self.initial_values[k] = 0
                else:
                    if hasattr(self.target, k):
                        self.initial_values[k] = getattr(self.target, k)
                    else:
                        self.initial_values[k] = 0
            if self.on_start:
                self.on_start()

        self.elapsed += dt
        
        progress = self.elapsed / self.duration if self.duration > 0 else 1.0
        if progress >= 1.0:
            progress = 1.0

        if self.is_yoyo_back:
            t = 1.0 - progress
        else:
            t = progress

        for k, v in self.properties.items():
            if k in self.initial_values:
                start_val = self.initial_values[k]
                
                target_val = v
                if isinstance(target_val, str) and target_val.startswith('-='):
                    target_val = start_val - float(target_val[2:])
                elif isinstance(target_val, str) and target_val.startswith('+='):
                    target_val = start_val + float(target_val[2:])
                
                current_val = start_val + (target_val - start_val) * t
                if isinstance(self.target, dict):
                    self.target[k] = current_val
                else:
                    setattr(self.target, k, current_val)

        if progress >= 1.0:
            if self.current_repeat < self.repeat:
                self.current_repeat += 1
                self.elapsed = 0
                if self.yoyo:
                    self.is_yoyo_back = not self.is_yoyo_back
                self.wait_delay = self.repeat_delay
            else:
                self.completed = True
                if self.on_complete:
                    self.on_complete()

class CallTween:
    def __init__(self, func):
        self.func = func
        self.completed = False
    
    def update(self, dt):
        if not self.completed:
            self.func()
            self.completed = True

class Timeline:
    def __init__(self):
        self.tweens = []
        self.active = True
    
    def to(self, target, duration, **kwargs):
        props = {}
        on_start = kwargs.get('onStart')
        on_complete = kwargs.get('onComplete')
        delay = kwargs.get('delay', 0)
        yoyo = kwargs.get('yoyo', False)
        repeat = kwargs.get('repeat', 0)
        repeat_delay = kwargs.get('repeatDelay', 0)

        for k, v in kwargs.items():
            if k not in ['duration', 'onStart', 'onComplete', 'delay', 'yoyo', 'repeat', 'repeatDelay', 'ease']:
                props[k] = v

        tw = Tween(target, duration, props, on_start, on_complete, delay, yoyo, repeat, repeat_delay)
        self.tweens.append(tw)
        return self

    def call(self, func):
        self.tweens.append(CallTween(func))
        return self

    def update(self, dt):
        if not self.active:
            return
        
        if len(self.tweens) > 0:
            current_tween = self.tweens[0]
            current_tween.update(dt)
            if current_tween.completed:
                self.tweens.pop(0)

    def pause(self):
        self.active = False
    
    def play(self):
        self.active = True

    def kill(self):
        self.tweens = []

    def is_active(self):
        return len(self.tweens) > 0 and self.active

class TweenManager:
    _timelines = []

    @classmethod
    def add(cls, timeline):
        if timeline not in cls._timelines:
            cls._timelines.append(timeline)

    @classmethod
    def remove(cls, timeline):
        if timeline in cls._timelines:
            cls._timelines.remove(timeline)

    @classmethod
    def update(cls, dt):
        for tl in cls._timelines:
            tl.update(dt)
