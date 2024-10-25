from practica import agent, joc


def main():
    mida = (6, 6)

    agents = [
        agent.Viatger("Agent 1", mida_taulell=mida),
        agent.Viatger("Agent 2", mida_taulell=mida),
    ]

    lab = joc.Laberint(agents, mida_taulell=mida)

    lab.comencar()


if __name__ == "__main__":
    main()
