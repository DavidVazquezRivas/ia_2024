from practica import agent, joc, agent_profunditat, agent_informat, agent_minimax


def main():
    mida = (12, 12)

    agents = [
        agent_minimax.ViatgerMinimax("Agent 1", mida_taulell=mida),
        agent_minimax.ViatgerMinimax("Agent 2", mida_taulell=mida)
    ]

    lab = joc.Laberint(agents, mida_taulell=mida)

    lab.comencar()


if __name__ == "__main__":
    main()
