import copy
from typing import Tuple, Dict, Set

from practica.joc import Accions


class Estat:
    moviments_possibles = [
        (Accions.MOURE, "E"),
        (Accions.MOURE, "S"),
        (Accions.MOURE, "N"),
        (Accions.MOURE, "O"),
        (Accions.BOTAR, "S"),
        (Accions.BOTAR, "N"),
        (Accions.BOTAR, "E"),
        (Accions.BOTAR, "O"),
        (Accions.POSAR_PARET, "S"),
        (Accions.POSAR_PARET, "N"),
        (Accions.POSAR_PARET, "E"),
        (Accions.POSAR_PARET, "O"),
    ]

    def __init__(self, nom_agent: str, parets: Set[Tuple[int, int]], midax: int, miday: int, desti: Tuple[int, int],agents: Dict[str, Tuple[int, int]],cami = []):
        self._nom_agent = nom_agent
        self._parets = parets
        self._rangx = midax
        self._rangy = miday
        self._desti = desti
        self._agents = agents
        self._posicio = self._agents[self._nom_agent]
        self.cami = cami
        self._invalid = False

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False


        parets_igual = sorted(self._parets) == sorted(other._parets)
        agents_igual = sorted((clau, valor) for clau, valor in self._agents.items()) == sorted(
            (clau, valor) for clau, valor in other._agents.items())

        return parets_igual and agents_igual

    def __hash__(self):
        parets_hash = hash(tuple(self._parets))
        agents_hash = hash(tuple(sorted((clau, valor) for clau, valor in self._agents.items())))
        return hash((parets_hash, agents_hash))

    def __str__(self):
        return (f"Estat de l'agent: {self._nom_agent}\n"
                f"Posició: {self._posicio}\n"
                f"Destí: {self._desti}\n"
                f"Parets: {self._parets}\n"
                f"Agents: {self._agents}\n"
                f"Camí: {self.cami}\n"
                )

    def es_desti(self) -> bool:
        return self._posicio[0] == self._desti[0] and self._posicio[1] == self._desti[1]

    def es_valid(self) -> bool:
        """ Mètode per detectar si un estat és valid

        Un estat es vàlid si no n'hi ha cap paret ni agent fora del taulell ni cap agent sobre una paret o altre agent.

        Returns:
            Booleà indicant si es vàlid o no
        """
        if self._posicio[0] < 0 or self._posicio[0] >= self._rangx or self._posicio[1] < 0 or self._posicio[1] >= self._rangy: #está fora del taulell
            return False

        if self._invalid: # hi ha parets duplicades, s'actualitza en crear l'estat
            return False

        for x, y in self._parets:
            if x < 0 or x >= self._rangx or y < 0 or y >= self._rangy: # hi ha parets fora de rang
                return False
            if x == self._posicio[0] and y == self._posicio[1]: # l'agent es troba sobre una paret
                return False
            if x == self._desti[0] and y == self._desti[1]: # hi ha una paret sobre la meta
                return False

        for nom, posicio in self._agents.items():
            if self._nom_agent != nom and self._posicio == posicio: # l'agent está damunt un altre
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
            nou_estat.cami.append(moviment)

            # Calcular x, y
            desp = (0, 0)
            if moviment[0] == Accions.BOTAR:
                desp = desp_botar.get(moviment[1], (0, 0))
            elif moviment[0] in (Accions.MOURE, Accions.POSAR_PARET):
                desp = desp_moure.get(moviment[1], (0, 0))
            x, y = self._posicio[0] + desp[0], self._posicio[1] + desp[1]

            # Fer canvis
            if moviment[0] == Accions.POSAR_PARET:
                if (x, y) in nou_estat._parets:
                    nou_estat._invalid = True
                else:
                    nou_estat._parets.add((x, y))

            elif moviment[0] in (Accions.MOURE, Accions.BOTAR):
                nou_estat._posicio = (x, y)
                nou_estat._agents[nou_estat._nom_agent] = (x, y)

            if nou_estat.es_valid():
                estats_generats.append(nou_estat)

        return estats_generats