import numpy as np

class UnionFinder():

    GroupIDs = None

    def __init__(self,List):
        """Set up leader and group dictionaries"""
        self.leader = {}  # maps member to group leader
        self.group = {}   # maps group leader to set of members
        self.List  = List

    def _makeSet(self, elements):
        """Insert elements as new group"""
        assert type(elements) is list

        group = set(elements)
        self.group[elements[0]] = group
        for i in group:
            self.leader[i] = elements[0]

    def _find(self, element):
        """Return the group associated with an element"""
        return self.leader[element]

    def _union(self, element1, element2):
        """Merge the groups containing two different elements"""
        leader1 = self.leader[element1]
        leader2 = self.leader[element2]

        # If both elements are in same group, do nothing
        if leader1 == leader2:
            return

        # Otherwise, merge the two groups
        group1 = self.group[leader1]
        group2 = self.group[leader2]

        # Swap names if group1 is smaller than group2
        if len(group1) < len(group2):
            element1, leader1, group1, \
                    element2, leader2, group2 = \
                    element2, leader2, group2, \
                    element1, leader1, group1

        # Merge group1 with group2, delete group2 and update leaders
        group1 |= group2
        del self.group[leader2]
        for i in group2:
            self.leader[i] = leader1

    def _initial(self):

        self.leader = {}  # maps member to group leader
        self.group = {}   # maps group leader to set of members


        for self.x,self.y in self.List:

            try:
                self._find(self.x)
            except KeyError:
                self._makeSet([self.x])

            try:
                self._find(self.y)
            except KeyError:
                self._makeSet([self.y])

    def _calcUnions(self):

        for self.x,self.y in self.List:
            if self._find(self.x)!=self._find(self.y):
                self._union(self._find(self.x),self._find(self.y))

    def calcGroupIDs(self):

        if self.List!=None:
            self._initial()
            self._calcUnions()

            res={}
            for self.x,self.y in self.List:
                res[self.x]=self._find(self.x)
                res[self.y]=self._find(self.y)
            self.GroupIDs=res

