from practica import joc
from practica.joc import Accions
from practica.estat import Estat

class ViatgerProdunditat(joc.Viatger):
    def __init__(self, *args, **kwargs):
        super(ViatgerProdunditat, self).__init__(*args, **kwargs)
        self.__per_visitar = None
        self.__visitats = None
        self.__cami_exit = None


    def pinta(self, display):
        pass

    def cerca(self, estat_inicial: Estat) -> bool:
        self.__per_visitar = []
        self.__visitats = set()
        exit = False

        self.__per_visitar.append(estat_inicial)
        while self.__per_visitar:
            estat_actual = self.__per_visitar.pop(-1)
            if estat_actual in self.__visitats:
                continue
            if estat_actual.es_desti():
                break

            for f in estat_actual.genera_fill():
                self.__per_visitar.append(f)

            self.__visitats.add(estat_actual)

        if estat_actual.es_desti():
            self.__cami_exit = estat_actual.cami
            exit = True

        return exit


    def actua(self, percepcio: dict) -> Accions | tuple[Accions, str]:
        if self.__cami_exit is None:
            estat_inicial = Estat(
                nom_agent=self.nom,
                parets=percepcio['PARETS'],
                midax=len(percepcio['TAULELL']),
                miday=len(percepcio['TAULELL'][0]),
                desti=percepcio['DESTI'],
                agents=percepcio['AGENTS'],
            )

            self.cerca(estat_inicial)

        if self.__cami_exit:
            return self.__cami_exit.pop(0)
        else:
            return Accions.ESPERAR