class GameState:
    def __init__(self):
        self.state = {
            'death': False,
            'gems': 0,
            'damage': 0
        }
        self.listeners: dict[str, list[classmethod]] = {subject: [] for subject in self.state}

    def listen(self, subject, call):
        self.listeners[subject].append(call)

    def signal(self, subject, message):
        for listener in self.listeners[subject]:
            listener(subject, message)

    def setValue(self, subject, value):
        self.state[subject] = value
        self.signal(subject, value)

    def getValue(self, subject):
        return self.state.get(subject)
