class PopupLevelPrepare:
    def __init__(self, poco):
        self.root = poco("PopupLevelPrepareInfo(Clone)")
    @property
    def btn_start(self):
        return self.root.offspring("B_Start")