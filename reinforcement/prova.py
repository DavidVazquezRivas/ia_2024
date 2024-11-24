from reinforcement.agent import AgentQ
from reinforcement.joc import Laberint
import matplotlib.pyplot as plt
import numpy as np

class Prova:
    @staticmethod
    def prova(
            game: Laberint,
            n: int,
            discount=0.90,
            exploration_rate=0.1,
            learning_rate=0.6,
            episodes=1000,
    ):
        # Lists to store the values of _ from both loops
        values_sarsa = []
        values_qlearning = []

        # First loop: training with SARSA
        for i in range(n):
            agent = AgentQ(game)
            h, w, _ = agent.train_sarsa(
                discount=discount,
                exploration_rate=exploration_rate,
                learning_rate=learning_rate,
                episodes=episodes,
                stop_at_convergence=True,
            )
            values_sarsa.append(_)  # Save the convergence time
            print(i)

        # Second loop: training with Q-learning
        for i in range(n):
            agent = AgentQ(game)
            h, w, _ = agent.train_qlearning(
                discount=discount,
                exploration_rate=exploration_rate,
                learning_rate=learning_rate,
                episodes=episodes,
                stop_at_convergence=True,
            )
            values_qlearning.append(_)  # Save the convergence time
            print(i)

        # Calculate the means
        mean_sarsa = np.mean(values_sarsa)
        mean_qlearning = np.mean(values_qlearning)
        median_sarsa = np.median(values_sarsa)
        median_qlearning = np.median(values_qlearning)

        # Create the box plots with matplotlib
        plt.figure(figsize=(10, 6))
        box = plt.boxplot([values_sarsa, values_qlearning],
                          vert=True,  # Box plots in vertical position
                          patch_artist=True,  # To fill the boxes
                          labels=[
                                    f'SARSA\nMitja: {mean_sarsa:.2f}\nMitjana: {median_sarsa:.2f}',
                                    f'Q-learning\nMitja: {mean_qlearning:.2f}\nMitjana: {median_qlearning:.2f}'
                                 ])  # Labels

        # Show the value of n
        plt.text(0.05, 01.00, f'n = {n}\nϵ = {exploration_rate}\nα = {discount}', transform=plt.gca().transAxes, fontsize=12, verticalalignment='bottom')

        # Title and labels
        plt.title('Comparació de rendiment: SARSA vs Q-learning')
        plt.ylabel('Temps de convergència')

        # Show the plot
        plt.show()
