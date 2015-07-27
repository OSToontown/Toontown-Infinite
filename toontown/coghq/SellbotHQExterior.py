from toontown.coghq.CogHQExterior import CogHQExterior


class SellbotHQExterior(CogHQExterior):
    notify = directNotify.newCategory('SellbotHQExterior')

    def enter(self, requestStatus):
        CogHQExterior.enter(self, requestStatus)

        self.loader.hood.startSky()

    def exit(self):
        self.loader.hood.stopSky()

        CogHQExterior.exit(self)
