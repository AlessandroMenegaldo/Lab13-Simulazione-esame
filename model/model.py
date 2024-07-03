import copy

import networkx as nx
from geopy import distance
from database.DAO import DAO


class Model:
    def __init__(self):
        self._idMap={}
        self._graph = nx.Graph()

        self._bestPath = []
        self._bestScore = 0

    def getBestPath(self):
        self._bestPath = []
        self._bestScore = 0

        parziale = []
        for n in self._graph.nodes:
            parziale.append(n)
            for n2 in self._graph.neighbors(n):
                parziale.append(n2)
                self.ricorsione(parziale)
                parziale.pop()
            parziale.pop()

        print(self._bestScore)

    def ricorsione(self, parziale):

        #controllo best soluzione
        score = self.getScorePath(parziale)
        if score > self._bestScore:
            self._bestScore = score
            self._bestPath = copy.deepcopy(parziale)

        #aggiungo nodi
        for n in self._graph.neighbors(parziale[-1]):
            if self.isNodoAmmissibile(parziale, n):
                parziale.append(n)
                self.ricorsione(parziale)
                parziale.pop()

    def getScorePath(self, listofStates):
        distTot = 0
        for i in range(0, len(listofStates)-1):
            coord1 = (listofStates[i].Lat,listofStates[i].Lng)
            coord2 = (listofStates[i+1].Lat,listofStates[i+1].Lng)

            distTot += distance.geodesic((coord1),(coord2)).km

        return distTot

    def isNodoAmmissibile(self, listOfNodes, newNode):
        lastWeight = self._graph[listOfNodes[-2]][listOfNodes[-1]]["weight"]
        newWeight = self._graph[listOfNodes[-1]][newNode]["weight"]

        if newWeight > lastWeight:
            return True

        return False





    def getAllYears(self):
        return DAO.getAllYears()

    def getShapes(self, anno):
        return DAO.getShapesByYear(anno)

    def buildGraph(self, year, shape):
        countries = DAO.getAllStates()
        print(len(countries))
        self._graph.add_nodes_from(countries)

        for c in countries:
            self._idMap[c.id] = c

        vicini = DAO.getAllNeighbors() #lista di tuple di di stati vicini

        for v in vicini:
            s1 = v[0]
            s2 = v[1]
            peso = DAO.getWeightNeighbors(s1, s2, year, shape)[0]
            self._graph.add_edge(self._idMap[s1],self._idMap[s2], weight = peso)

        return self.getListWeightNodes()

    def getListWeightNodes(self):
        listWeightNodes = []
        for n in self._graph.nodes:
            score = 0
            for s in self._graph.neighbors(n):
                score += self._graph[n][s]["weight"]
            listWeightNodes.append((n,score))

        return listWeightNodes


    def getNumNodi(self):
        return len(self._graph.nodes)

    def getNumArchi(self):
        return len(self._graph.edges)