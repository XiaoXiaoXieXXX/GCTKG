class GroupSet:
    def __init__(self, grouplist:list, center:int, cost:float, newadd:int):
        self.grouplist = grouplist
        self.center = center
        self.cost = cost
        self.newadd = newadd

    def __lt__(self, other):
        return self.cost < other.cost

    def __le__(self, other):
        return self.cost <= other.cost
