from practica import agent, joc, agent_profunditat


def main():
    mida = (6, 6)

    agents = [
        agent_profunditat.ViatgerProdunditat("Agent 1", mida_taulell=mida)
    ]

    lab = joc.Laberint(agents, mida_taulell=mida)

    lab.comencar()


if __name__ == "__main__":
    main()
