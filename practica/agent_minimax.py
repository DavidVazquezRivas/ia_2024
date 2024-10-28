from typing import Tuple

from practica import joc
from practica.joc import Accions
from practica.estat_ma import Estat

class ViatgerMinimax(joc.Viatger):
    PODA = True

    def __init__(self, *args, **kwargs):
        super(ViatgerMinimax, self).__init__(*args, **kwargs)
        self.__visitats = None
        self._profunditat_maxima = 2 # establim una profunditat máxima per tenir un cost raonable


    def pinta(self, display):
        pass

    def avaluar(self, estat: Estat, torn_max: bool, profunditat: int):
        if estat.es_desti():
            return estat, (float("inf") if not torn_max else float("-inf"))
        elif profunditat >= self._profunditat_maxima:
            return estat, estat.diferencia()
        else:
            return None


    def cerca(self, estat: Estat, torn_max=True, alfa=-float("inf"), beta=float("inf"), profunditat=0) -> Tuple[Estat, float]:

        avaluacio = self.avaluar(estat, torn_max, profunditat)
        if avaluacio is not None:
            return avaluacio

        puntuacio_fills = []

        for fill in estat.genera_fill():
            if fill not in self.__visitats:
                punt_fill = self.cerca(fill, not torn_max, alfa, beta, profunditat + 1)

                if ViatgerMinimax.PODA:
                    if torn_max:
                        alfa = max(alfa, punt_fill[1])
                    else:
                        beta = min(beta, punt_fill[1])

                    if alfa > beta:
                        break

                self.__visitats[fill] = punt_fill
            puntuacio_fills.append(self.__visitats[fill])

        puntuacio_fills = sorted(puntuacio_fills, key=lambda x: x[1])
        if not torn_max:
            return puntuacio_fills[0]
        else:
            return puntuacio_fills[-1]

    def actua(self, percepcio: dict) -> Accions | tuple[Accions, str]:
        estat_inicial = Estat(
            nom_agent=self.nom,
            parets=percepcio['PARETS'],
            midax=len(percepcio['TAULELL']),
            miday=len(percepcio['TAULELL'][0]),
            desti=percepcio['DESTI'],
            agents=percepcio['AGENTS'],
        )

        self.__visitats = dict()
        res = self.cerca(estat_inicial, True, -float("inf"), float("inf"), 0)
        if len(res[0].cami(self.nom)) > 0:
            return res[0].cami(self.nom)[0]
        else:
            return Accions.ESPERAR