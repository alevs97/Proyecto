from simulation.simulation import Simulation
import matplotlib.pyplot as plt

if __name__ == '__main__':

    list_lambda = [0.3]
    list_simulation = []
    list_throughtput = []
    list_grade = [i for i in range(0,7)]

    list_discard_pkt_simulation = []
    list_generated_pkt_simulation = []


    for lambda_pkt in list_lambda:
        simulation_recursive = Simulation(
            mesageDifs=10e-3,
            mesageSifs=5e-3,
            mesageRts=11e-3,
            mesageCts=11e-3,
            mesageAck=11e-3,
            mesageData=43e-3,
            num_nodos=2,
            ranuSleeping=18,
            max_mini_ranuras=3,
            lambda_pkt=lambda_pkt,
            size_buffer=15,
            num_grades=5,
            sigma=1e-3,
        )
        list_simulation.append(simulation_recursive)
        simulation_recursive.ini_sim()
        throughtput_simulation = simulation_recursive.get_pkt_ciclo_throughtput()
        list_throughtput.append(throughtput_simulation)
        list_discard_pkt_simulation.append(simulation_recursive.num_pkt_discart)
        list_generated_pkt_simulation.append(simulation_recursive.num_pkt_generated)

        print(simulation_recursive.num_pkt_discart)

        print(list_generated_pkt_simulation)
        print(list_discard_pkt_simulation)

    plt.plot(list_lambda,list_throughtput)
    plt.xlabel('grados')
    plt.ylabel('Paquetes/ciclo')
    plt.title('throughput W=64')
    plt.show()
