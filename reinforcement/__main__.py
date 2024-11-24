import logging

from reinforcement.agent import AgentQ
from reinforcement.joc import Laberint
from reinforcement.prova import Prova


def main():
    test = False

    # Set the logging level based on the value of 'test'
    log_level = logging.INFO if not test else logging.WARNING
    logging.basicConfig(
        format="%(levelname)-8s: %(asctime)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=log_level,
    )  # Only show messages *equal to or above* this level

    game = Laberint()
    if (test):
        Prova.prova(
            game=game,
            n=100,
            discount=0.8,
            exploration_rate=0.05,
            learning_rate=0.6,
            episodes=1000
        )
    else:
        agent = AgentQ(game)
        h, w, _ = agent.train_qlearning(
            discount=0.90,
            exploration_rate=0.10,
            learning_rate=0.6,
            episodes=1000,
            stop_at_convergence=True,
        )

        game.reset()
        game.set_agent([agent])
        game.comencar()


if __name__ == "__main__":
    main()
