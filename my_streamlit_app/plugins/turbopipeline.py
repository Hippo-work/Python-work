class TurboPipeline:
    def __init__(self):
        self.randomizer = Randomizer()
        self.fec = FEC()
        self.visualizer = Visualizer()

    def run(self, data):
        data = self.randomizer.process(data)
        data = self.fec.encode(data)
        self.visualizer.display(data)
        return data