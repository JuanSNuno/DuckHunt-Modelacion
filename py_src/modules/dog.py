from modules.character import Character
from modules.sound import sound

class Dog(Character):
    def __init__(self, options):
        states = [
            {'name': 'double', 'animationSpeed': 0.1},
            {'name': 'single', 'animationSpeed': 0.1},
            {'name': 'find', 'animationSpeed': 0.1},
            {'name': 'jump', 'animationSpeed': 0.1, 'loop': False},
            {'name': 'laugh', 'animationSpeed': 0.1},
            {'name': 'sniff', 'animationSpeed': 0.1}
        ]
        super().__init__('dog', states)
        self.to_retrieve = 0
        self.max_retrieve = 3
        self.anchor = (0.5, 0.0)
        self.options = options
        self.sniff_sound_id = None
        self.visible = False

    def sniff(self, opts=None):
        if opts is None: opts = {}
        start_point = opts.get('startPoint', (self.x, self.y))
        end_point = opts.get('endPoint', (self.x, self.y))
        on_start = opts.get('onStart', lambda: None)
        on_complete = opts.get('onComplete', lambda: None)

        def sit_pre():
            self.visible = False
        self.sit({'point': start_point, 'pre': sit_pre})

        def start_func():
            self.visible = True
            self.state = 'sniff'
            self.sniff_sound_id = sound.play('sniff')
            on_start()

        def complete_func():
            sound.stop(self.sniff_sound_id)
            on_complete()

        self.timeline.to(self, 2, x=end_point[0], y=end_point[1], ease='none', onStart=start_func, onComplete=complete_func)
        return self

    def up_down_tween(self, opts=None):
        if opts is None: opts = {}
        start_point = opts.get('startPoint', self.options.get('downPoint', (self.x, self.y)))
        end_point = opts.get('endPoint', self.options.get('upPoint', (self.x, self.y)))
        on_start = opts.get('onStart', lambda: None)
        on_complete = opts.get('onComplete', lambda: None)

        self.sit({'point': start_point})

        def start_func():
            self.visible = True
            on_start()

        self.timeline.to(self, 0.4, y=end_point[1], yoyo=True, repeat=1, repeatDelay=0.5, ease='none', onStart=start_func, onComplete=on_complete)
        return self

    def find(self, opts=None):
        if opts is None: opts = {}
        on_start = opts.get('onStart', lambda: None)
        on_complete = opts.get('onComplete', lambda: None)

        def call_func():
            sound.play('barkDucks')
            self.state = 'find'
            on_start()
        self.timeline.call(call_func)

        def start_func():
            self.state = 'jump'
        
        def complete_func():
            self.visible = False
            on_complete()
            
        self.timeline.to(self, 0.2, y='-=100', ease='power4.out', delay=0.4, onStart=start_func, onComplete=complete_func)
        return self

    def sit(self, opts=None):
        if opts is None: opts = {}
        point = opts.get('point', (self.x, self.y))
        on_start = opts.get('onStart', lambda: None)
        on_complete = opts.get('onComplete', lambda: None)
        pre = opts.get('pre', lambda: None)

        def call_func():
            pre()
            on_start()
            self.x, self.y = point[0], point[1]
            on_complete()
        self.timeline.call(call_func)
        return self

    def retrieve(self):
        if self.to_retrieve + 1 >= self.max_retrieve:
            return self
        self.to_retrieve += 1

        def start_func():
            if self.to_retrieve >= 2:
                self.state = 'double'
                self.to_retrieve -= 2
            elif self.to_retrieve == 1:
                self.state = 'single'
                self.to_retrieve -= 1

        self.up_down_tween({'onStart': start_func})
        return self

    def laugh(self):
        self.to_retrieve = 0
        def start_func():
            self.state = 'laugh'
            sound.play('laugh')
        self.up_down_tween({'onStart': start_func})
        return self

    def is_active(self):
        return super().is_active() and self.to_retrieve > 0
