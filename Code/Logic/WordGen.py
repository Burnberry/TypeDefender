from random import choice


class WordGen:
    def __init__(self):
        self.loadWords()

    def loadWords(self):
        self.words = [
            'appeal', 'fat', 'yard', 'wear', 'sport', 'plant', 'pier', 'thread', 'elect', 'fog', 'bean', 'deport', 'brick', 'veil', 'drown', 'call', 'delete', 'medium', 'lace', 'skate', 'lion', 'banner', 'drop', 'pen', 'fault', 'dump', 'swarm', 'vote', 'paint', 'half', 'bride', 'store', 'hover', 'cream', 'depart', 'pace', 'gloom', 'rage', 'gain', 'bomber', 'spirit', 'add', 'begin', 'team', 'refer', 'hard', 'fur', 'cheque', 'style', 'ear', 'visual', 'cereal', 'low', 'jungle', 'bite', 'flash', 'trunk', 'pipe', 'frog', 'refer', 'time', 'coerce', 'lazy', 'crude', 'reduce', 'sound', 'sum', 'berry', 'behave', 'bare', 'rise', 'roll', 'debt', 'kick', 'rest', 'kettle', 'hide', 'voter', 'import', 'poll', 'slot', 'beer', 'coma', 'burial', 'betray', 'speech', 'rider', 'occupy', 'green', 'van', 'kill', 'tough', 'ferry', 'dealer', 'beam', 'lung', 'grace', 'learn', 'valley', 'bee', 'earwax', 'stress', 'file', 'raise', 'scale', 'glory', 'crop', 'mosque', 'bin', 'child', 'spoil', 'virus', 'brave', 'proof', 'rent', 'shadow', 'speed', 'sell', 'curve', 'palace', 'noble', 'need', 'rank', 'is', 'real', 'solo', 'obese', 'evoke', 'object', 'season', 'pour', 'bet', 'sale', 'debt', 'we', 'misery', 'reduce', 'arrest', 'hold', 'mask', 'good', 'brag', 'weapon', 'orgy', 'mobile', 'stock', 'free', 'guess', 'time', 'sting', 'crash', 'trail', 'foot', 'maid', 'side', 'pony', 'lazy', 'poem', 'corner', 'eaux', 'TRUE', 'turkey', 'tablet', 'prize', 'sow', 'touch', 'faint', 'owl', 'reach', 'loop', 'size', 'poison', 'knock', 'blonde', 'summer', 'sting', 'sign', 'key', 'sugar', 'queue', 'block', 'thread', 'salon', 'sit', 'peace', 'slave', 'awful', 'bury', 'system', 'object', 'nature', 'jewel', 'revive', 'death', 'rent', 'jail', 'speech', 'empire', 'piece', 'glow'
        ]

    def getWord(self):
        return choice(self.words)
