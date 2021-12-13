import matplotlib.pyplot as plt

class Graph:

    def __init__(self):
        pass

    def plot_thougthput_simulation(self, list_lambda, list_throughtput):
        plt.plot(list_lambda, list_throughtput)
        plt.xlabel('grados')
        plt.ylabel('Paquetes/ciclo')
        plt.title('throughput W=64')
        plt.show()

    def plot_number_pkt_generated(self, list_pkt_generated_grade, list_pkt_discarted_grade):
        pass


    def plot_delay_pkt_generated(self):
        pass