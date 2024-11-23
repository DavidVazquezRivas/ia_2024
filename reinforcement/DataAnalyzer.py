from typing import List


class DataAnalyzer:
    @staticmethod
    def calculate_convergence_time(reward_cumulative_history: List[float], default_check_convergence_every=5, tolerance=0.05) -> int:
        """
        Calcula el temps de convergència a partir d'una llista de recompenses acumulatives.

        Aquesta funció determina en quin moment es produeix la convergència en la llista de recompenses acumulatives
        (basada en les recompenses per iteració) segons una tolerància especificada. La convergència es defineix com
        la estabilització del valor de les recompenses al llarg del temps, on el valor actual està dins d'un interval
        de tolerància respecte al valor anterior per un nombre de vegades consecutives especificat.

        Paràmetres:
        - reward_cumulative_history: List[float], historial de recompenses acumulatives on cada element és la suma
          de les recompenses fins a un cert punt.
        - default_check_convergence_every: int (opcional, per defecte 5), nombre mínim de vegades consecutives
          que la recompensa ha d'estar dins dels límits de tolerància per considerar que ha convergit.
        - tolerance: float (opcional, per defecte 0.05), percentatge de tolerància per determinar si dos valors
          consecutius són prou propers per considerar que han convergit. El valor està expressat com una fracció
          (0.05 vol dir un 5%).

        Retorna:
        - int, índex del temps de convergència dins de la llista de recompenses. Si no s'aconsegueix convergència,
          retorna -1.

        Excepcions:
        - Llança un ValueError si la llista de recompenses està buida.
        """


        if not reward_cumulative_history:
            raise ValueError("La llista de recompenses no pot ser buida.")

        reward_history = DataAnalyzer.calculate_reward_history(reward_cumulative_history)

        last_value = 0
        nums_range = 0
        lower_bound = last_value * (1 - tolerance)
        upper_bound = last_value * (1 + tolerance)

        for i, reward in enumerate(reward_history):
            if lower_bound <= reward <= upper_bound:
                nums_range += 1
            else:
                nums_range = 0
                last_value = reward
                lower_bound = last_value * (1 - tolerance)
                upper_bound = last_value * (1 + tolerance)

            if nums_range >= default_check_convergence_every:
                return i

        # No s'ha trobat convergència
        return -1

    @staticmethod
    def calculate_reward_history(reward_cumulative_history: List[float]) -> List[float]:
        last = 0
        reward_history = []

        for current in reward_cumulative_history:
            reward = current - last
            reward_history.append(reward)
            last = current

        return reward_history
