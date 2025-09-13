class HomeSquad:
    def __init__(self,poco):
        self.root = poco("HomeSquads")
    @property
    def squad_0(self):
        node = self.root.offspring("HomeSquad_0")
        return Squad(node) if node.exists() else None
    @property
    def squad_1(self):
        node = self.root.offspring("HomeSquad_1")
        return Squad(node) if node.exists() else None
    @property
    def squad_2(self):
        node = self.root.offspring("HomeSquad_2")
        return Squad(node) if node.exists() else None

class Squad:
    def __init__(self,node):
        self.root = node
    @property
    def circle(self):
        return self.root.child("sCircle")
    @property
    def aircraft(self):
        node= self.root.offspring("BtnAircraft")
        return node if node.exists() else None
    @property
    def drone_left(self):
        node = self.root.offspring("BtnLeftDrone")
        return node if node.exists() else None
    @property
    def drone_right(self):
        node = self.root.offspring("BtnRightDrone")
        return node if node.exists() else None
    @property
    def wing(self):
        node = self.root.offspring("BtnWing")
        return node if node.exists() else None
