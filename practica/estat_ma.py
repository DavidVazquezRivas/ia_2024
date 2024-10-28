import copy
from msilib.schema import Property
from typing import Set, Tuple, Dict, List

from practica.joc import Accions


class Estat:
    moviments_possibles = [ # aquest ordre optimitza la cerca per profunditat
        (Accions.BOTAR, "S"),
        (Accions.BOTAR, "N"),
        (Accions.BOTAR, "E"),
        (Accions.BOTAR, "O"),
        (Accions.MOURE, "E"),
        (Accions.MOURE, "S"),
        (Accions.MOURE, "N"),
        (Accions.MOURE, "O"),
        (Accions.POSAR_PARET, "S"),
        (Accions.POSAR_PARET, "N"),
        (Accions.POSAR_PARET, "E"),
        (Accions.POSAR_PARET, "O"),
    ]

    def __init__(self, nom_agent: str, parets: Set[Tuple[int, int]], midax: int, miday: int, desti: Tuple[int, int],agents: Dict[str, Tuple[int, int]],cami = []):
        self._torn = nom_agent
        self._parets = parets
        self._rangx = midax
        self._rangy = miday
        self._desti = desti
        self._agents = agents
        self._camins = {key: [] for key in agents.keys()}
        self._invalid = False

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        parets_hash = hash(tuple(self._parets))
        agents_hash = hash(tuple(sorted((clau, valor) for clau, valor in self._agents.items())))
        return hash((parets_hash, agents_hash))

    def __str__(self):
        resultat = ""
        for nom, posicio in self._agents.items():
            resultat += (f"Estat de l'agent: {nom}\n"
                f"Posició: {posicio}\n"
                f"Destí: {self._desti}\n"
                f"Parets: {self._parets}\n"
                f"Camí: {self._camins[nom]}\n"
                f"Heuristica: {(self.heuristica(nom))}\n"
                )
        resultat += f"Torn: {self._torn}"
        return resultat

    def es_desti(self) -> bool:
        for posicio in self._agents.values():
            if posicio == self._desti:
                return True

        return False

    def es_valid(self) -> bool:
        """ Mètode per detectar si un estat és valid

        Un estat es vàlid si no n'hi ha cap paret ni agent fora del taulell ni cap agent sobre una paret o altre agent.

        Returns:
            Booleà indicant si es vàlid o no
        """
        for posicio in self._agents.values():
            if posicio[0] < 0 or posicio[0] >= self._rangx or posicio[1] < 0 or posicio[1] >= self._rangy:  # agent está fora del taulell
                return False

            for pos in self._parets:
                if posicio[0] == pos[0] and posicio[1] == pos[1]: # hi ha un agent sobre una paret
                    return False

        pos_agents = list(self._agents.values())
        if len(pos_agents) != len(set(pos_agents)): # hi ha més d'un agent a la mateixa posició
            return False

        if self._invalid: # hi ha parets duplicades, s'actualitza en crear l'estat
            return False

        for x, y in self._parets:
            if x < 0 or x >= self._rangx or y < 0 or y >= self._rangy: # hi ha parets fora de rang
                return False

            if x == self._desti[0] and y == self._desti[1]: # hi ha una paret sobre la meta
                return False

        return True

    def genera_fill(self) -> list:
        """ Mètode per generar els estats fills.

        Genera tots els estats fills a partir de l'estat actual.

        Returns:
            Llista d'estats fills generats.
        """
        desp_moure = {
            "N": (0, -1),
            "S": (0, 1),
            "E": (1, 0),
            "O": (-1, 0)
        }
        desp_botar = {
            "N": (0, -2),
            "S": (0, 2),
            "E": (2, 0),
            "O": (-2, 0)
        }

        estats_generats = []

        for moviment in self.moviments_possibles:
            nou_estat = copy.deepcopy(self)
            nou_estat.pare = self
            nou_estat._camins[self._torn].append(moviment)

            # Establir torn nou estat
            agents = list(self._agents.keys())
            index = agents.index(self._torn)
            nou_estat._torn = agents[(index + 1) % len(agents)]

            # Calcular x, y
            desp = (0, 0)
            if moviment[0] == Accions.BOTAR:
                desp = desp_botar.get(moviment[1], (0, 0))
            elif moviment[0] in (Accions.MOURE, Accions.POSAR_PARET):
                desp = desp_moure.get(moviment[1], (0, 0))
            x, y = self._agents[self._torn][0] + desp[0], self._agents[self._torn][1] + desp[1]

            # Fer canvis
            if moviment[0] == Accions.POSAR_PARET:
                if (x, y) in nou_estat._parets:
                    nou_estat._invalid = True
                else:
                    nou_estat._parets.add((x, y))

            elif moviment[0] in (Accions.MOURE, Accions.BOTAR):
                nou_estat._agents[self._torn] = (x, y)

            if nou_estat.es_valid():
                estats_generats.append(nou_estat)
        return estats_generats

    def heuristica(self, nom=None) -> int:
        # L'heuristica definida serà la distancia entre l'agent i el destí
        # L'heuristica és admisible, garantint trobar la solució òptima per A*
        if nom is None:
            nom = self._torn
        return abs(self._agents[nom][0] - self._desti[0]) + abs(self._agents[nom][1] - self._desti[1])

    @property
    def agents(self):
        return self._agents

    @property
    def desti(self):
        return self._desti

    @property
    def torn(self):
        return self._torn

    def cami(self, nom=None) -> List[Tuple[Accions, str]]:
        if nom is None:
            nom = self._torn
        return self._camins[nom]

    def diferencia(self):
        resultat = -self.heuristica()

        for nom in self._agents.keys():
            if nom != self._torn:
                resultat += self.heuristica(nom)

        return resultat