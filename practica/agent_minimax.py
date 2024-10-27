from practica import joc
from practica.joc import Accions
from practica.estat import Estat


class ViatgerMinimax(joc.Viatger):
    def __init__(self, *args, **kwargs):
        super(ViatgerMinimax, self).__init__(*args, **kwargs)
        self.__cami = None
        self.__visitats = []

    def evaluar(self,estat: Estat):
        posicions_agents: dict = estat.posicio_agents()
        posicio_desti: tuple[int, int] = estat.posicio_desti()
        x_1 = posicions_agents["Agent 1"][0]
        y_1 = posicions_agents["Agent 1"][1]
        distancia_un = abs(posicio_desti[0] - x_1) + abs(posicio_desti[1] - y_1)
        x_2 = posicions_agents["Agent 2"][0]
        y_2 = posicions_agents["Agent 2"][1]
        distancia_dos = abs(posicio_desti[0] - x_2) + abs(posicio_desti[1] - y_2)
        if estat.get_nom_agent() == "Agent 1":
            return distancia_dos - distancia_un
        return distancia_un - distancia_dos

    def minimax(self, estat: Estat, alpha, beta, profunditat, torn_max=True):
        if profunditat == 0 or estat.es_desti():
            return estat, self.evaluar(estat)
        if torn_max:
            max_puntuacio = -float('inf')
            estat_return = estat
            for fill in estat.genera_fill():

                puntuacio = self.minimax(fill, alpha, beta, profunditat-1, False)
                max_puntuacio = max(max_puntuacio, puntuacio[1])
                if max_puntuacio == puntuacio[1]:
                    estat_return = puntuacio[0]
                alpha = max(alpha, puntuacio[1])
                if beta <= alpha:
                    break
            return estat_return,max_puntuacio
        else:
            min_puntuacio = float('inf')
            estat_return = estat
            for fill in estat.genera_fill():

                puntuacio = self.minimax(fill, alpha, beta, profunditat-1, True)
                min_puntuacio = min(min_puntuacio, puntuacio[1])
                if puntuacio[1]==min_puntuacio:
                    estat_return = puntuacio[0]
                beta = min(beta,puntuacio[1])
                if beta <= alpha:
                    break
            return estat_return,min_puntuacio

    def actua(self, percepcio: dict) -> Accions | tuple[Accions, str]:
        self.__visitats = dict()
        estat_inicial = Estat(
                nom_agent=self.nom,
                parets=percepcio['PARETS'],
                midax=len(percepcio['TAULELL']),
                miday=len(percepcio['TAULELL'][0]),
                desti=percepcio['DESTI'],
                agents=percepcio['AGENTS'],
            )
        if estat_inicial.es_desti():
            return Accions.ESPERAR
        accio:tuple[Estat,int] = self.minimax(estat_inicial,-float('inf'),float('inf'), 2)
        res = accio[0].cami[0]
        return res
