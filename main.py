from simulation.simulation import Simulation

if __name__ == '__main__':
    simulation = Simulation(
        
        mesageDifs=10e-3,
        mesageSifs=5e-3,
        mesageRts=11e-3,
        mesageCts=11e-3,
        mesageAck=11e-3,
        mesageData=45e-3,
        num_nodos=5,
        ranuSleeping=18,
        max_mini_ranuras=16,
        lambda_pkt=0.0005,
        size_buffer=15,
        num_grades=7,
        sigma=1e-3
    )
    for i in range(300):
        simulation.generating_pkt_ramdom_grade_and_node()


    simulation.print_network()

    for i in range(6,-1,-1):
        print(i)
        simulation.transmit_pkt_to_next_grade(i)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
