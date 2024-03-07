class WaveHandler:
    def __init__(self, scene):
        self.scene = scene

        # state
        self.time = 0
        self.nextSpawn = self.time
        self.nextSpeedIncrease = 10

        self.enemyDelay = 3

    def update(self, dt):
        self.time += dt

        if self.time > self.nextSpeedIncrease:
            self.nextSpeedIncrease += 10
            self.enemyDelay *= 0.9
            print("faster", self.enemyDelay)

        while self.time > self.nextSpawn:
            self.spawnEnemy()
            self.nextSpawn += self.enemyDelay

    def spawnEnemy(self):
        self.scene.spawnEnemy()

    def reset(self):
        self.time = 0
        self.nextSpawn = self.time
