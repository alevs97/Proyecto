from entities.grade import Grade
#from entities.grade import Grade
from entities.node import Node
from random import randint
from math import log


class Simulation:

    def __init__(self, mesageDifs, mesageSifs, mesageRts, mesageCts, mesageAck, mesageData, sigma,
                 num_grades, size_buffer, ranuSleeping, lambda_pkt, max_mini_ranuras, num_nodos, ):
        # Message variables
        self.mesageDifs = mesageDifs
        self.mesageRts = mesageRts
        self.mesageSifs = mesageSifs
        self.mesageCts = mesageCts
        self.mesageAck = mesageAck
        self.mesageData = mesageData
        # Other variables
        self.num_nodos = num_nodos
        self.ranuSleeping = ranuSleeping
        self.max_mini_ranuras = max_mini_ranuras
        self.lambda_pkt = lambda_pkt
        self.size_buffer = size_buffer
        self.num_grades = num_grades
        self.sigma = sigma
        # self.var_u= var_u

        # Generacion de otras variables
        self.timeSlot = mesageDifs + (max_mini_ranuras * sigma) + mesageRts + (3 * mesageSifs) \
                        + mesageCts + mesageData + mesageAck
        self.timeCycleWork = (2 + ranuSleeping) * self.timeSlot
        self.time_simulation = 0
        self.lambda_pkt_2 = self.num_grades * self.num_nodos * self.lambda_pkt

        # Setting nodes and grades
        self.network = self.setting_entities()

        # Colision total
        self.number_colision_pkt = 0
        self.number_pkt_descarter_full_buffer = 0
        self.pkt_arribed_sink = 0

        self.time_arribe = 0

        self.new_time_arribe = 0

        # Variables performance [6,5,4,...-1]
        # for i in range(6,-1,-1)
        self.num_pkt_discart = [0 for i in range(num_grades)]
        self.num_pkt_generated = [0 for i in range(num_grades)]

    def setting_entities(self):
        """
        Buildeing the LSN with nodes and grades
        :param: void
        :return: void
        """
        list_grades = []
        for index_grade in range(self.num_grades):
            list_nodes = []
            for index_node in range(self.num_nodos):
                node = Node(
                    max_mini_ranuras=self.max_mini_ranuras,
                    size_buffer=self.size_buffer,
                    lambda_pkt=self.lambda_pkt,
                    num_node=index_node
                )
                print("Creado nodo" + str(node))
                list_nodes.append(node)
            grade = Grade(
                num_grade=index_grade,
                list_nodes=list_nodes
            )
            print("Creado grado" + str(grade))

            list_grades.append(grade)
        return list_grades

    def generating_pkt_ramdom_grade_and_node(self):
        """
        Process to generate random pkt in the LSN
        :param: void
        :return: void
        """
        # Choosing
        ramdom_grade = randint(0, self.num_grades - 1)
        ramdom_node = randint(0, self.num_nodos - 1)
        print("Number Grade" + str(ramdom_grade))
        print("Number Node" + str(ramdom_node))

        # Selecting
        grade = self.network[ramdom_grade]
        node = grade.get_node_by_number_node(ramdom_node)
        self.num_pkt_generated[ramdom_grade] = self.num_pkt_generated[ramdom_grade] + 1
        # Adding
        status_buffer = node.adding_pkt_to_buffer()
        if status_buffer == True:
            # print("No problem")
            pass
        else:
            self.number_pkt_descarter_full_buffer = self.number_pkt_descarter_full_buffer + 1
            self.num_pkt_discart[ramdom_grade] = self.num_pkt_discart[ramdom_grade] + 1

    def transmit_pkt_to_next_grade(self, num_grade):
        """
        :param num_grade: Grade that is transmiting a pkt
        :return: void
        """
        # Call cantention process
        node_to_trasmit = self.contention_process(num_grade)
        if node_to_trasmit == False:
            pass
            # print("buffer vacio")
        elif node_to_trasmit == None:
            self.number_colision_pkt = self.number_colision_pkt + 1
            self.num_pkt_discart[num_grade] = self.num_pkt_discart[num_grade] + 1
            # print("colision")
        else:
            node_to_trasmit.transmiting_pkt_to_next_grade()
            index_node_transmit = node_to_trasmit.get_num_node()
            print("Grado " + str(num_grade))
            print(node_to_trasmit)

            next_num_grade = num_grade - 1
            val_grade_cero = self.verify_grade_zero_receive(next_num_grade, index_node_transmit)
            if val_grade_cero == True:
                print("Recibio sink")
                pass
            else:
                pass
                print("Recibio grado")

    def contention_process(self, num_grade):
        """
        Make the contention process in a specific grade
        :param num_grade: Index of grade
        :return: winner_node: Node that wins contention process
        """
        list_nodes_with_pkt = self.get_nodes_with_pkt_to_transmit(num_grade)
        winner_node = self.choosing_node_to_transmit(list_nodes_with_pkt)

        # Return Node
        return winner_node

    def get_nodes_with_pkt_to_transmit(self, num_grade):
        """
        Return the nodes with pkt in buffer
        :param num_grade: index of the grade that will transmit
        :return: list_nodes_with_pkt: List of nodes with pkt to transmit
        """
        grade_in_contention = self.network[num_grade]
        list_nodes_with_pkt = []
        for node in grade_in_contention.list_nodes:
            if node.is_buffer_with_pkt_to_transmit():
                list_nodes_with_pkt.append(node)
        return list_nodes_with_pkt

    def choosing_node_to_transmit(self, list_nodes_with_pkt):
        """
        Select the the node wich is going to transmit
        :param list_nodes_with_pkt: List of nodes with pkt to transmit
        :return: winner_node: node that wins the contention process
        """
        list_value_mini_ranuras = []
        for node in list_nodes_with_pkt:
            node.set_value_mini_ranura()
            list_value_mini_ranuras.append(node.get_value_mini_ranura())
        try:
            min_value_ranura = min(list_value_mini_ranuras)
        except ValueError:
            print("No pkt to transmit")
            return False

        number_nodes_with_min_value = 0
        index_node_transmit = 0

        for value_min_ranura in range(0, len(list_value_mini_ranuras)):
            if list_value_mini_ranuras[value_min_ranura] == min_value_ranura:
                number_nodes_with_min_value = number_nodes_with_min_value + 1
                index_node_transmit = value_min_ranura

        if number_nodes_with_min_value != 1:
            return None
        else:
            winner_node = list_nodes_with_pkt[index_node_transmit]
            print(winner_node)
            return winner_node

    def verify_grade_zero_receive(self, num_grade, index_node_receive):
        if num_grade == -1:
            self.pkt_arribed_sink = self.pkt_arribed_sink + 1
            return True
        else:
            self.receive_pkt_in_grade(num_grade, index_node_receive)
            return False

    def receive_pkt_in_grade(self, num_grade, index_node_receive):
        """
        Process when receive a ptk for a superior grade
        :param num_grade: Number grade in LSN
        :param index_node_receive: Node in superior grade index
        :return: void
        """
        # Getting node
        grade_to_receive = self.network[num_grade]
        node_to_receive = grade_to_receive.list_nodes[index_node_receive]
        verifi_space_node = node_to_receive.adding_pkt_to_buffer()
        if (verifi_space_node == False):
            self.number_pkt_descarter_full_buffer = self.number_pkt_descarter_full_buffer + 1
            self.num_pkt_discart[num_grade] = self.num_pkt_discart[num_grade] + 1
            print("Buffer " + str(node_to_receive) + "FULL")
        else:
            print("Grado " + str(num_grade))
            print(node_to_receive)
            pass

    def ini_sim(self):
        while self.time_simulation < 1e4 * self.timeCycleWork:
            while self.time_arribe < self.time_simulation:
                # self.variable = 0

                # Todo: u , nuevo t , ta
                var_u = (randint(0, 1e6)) / 1e6
                # self.new_t=-(1/self.lambda_pkt)*log(1-self.var_u)
                new_t = -1 * (1 / self.lambda_pkt) * log(1 - var_u)  # *(self.lambda_pkt_2)
                self.time_arribe = self.time_simulation + new_t

                print(var_u)
                print(new_t)
                print(self.time_arribe)
                print(self.time_simulation)

                self.generating_pkt_ramdom_grade_and_node()
            for num_grade in range(6, -1, -1):
                self.transmit_pkt_to_next_grade(num_grade)

            self.time_simulation = self.time_simulation + self.timeCycleWork

    def print_network(self):
        """
        Display the node network
        :param:void
        :return:void
        """
        # print("El valor de u es: ", self.var_u)
        # print("El valor de la nueva t es:", self.new_t)
        # print ("El nuevo tiempo de arribo es:", self.new_time_arribe)
        print(len(self.network))
        for grade in self.network:
            print(grade)
            for node in grade.list_nodes:
                print(node)

        # throughput son los pkt/ seg y los pkt/ciclo, va a depender de los calores que llegan al sink por
        # segundo o ciclo
        # Debemos encontrar cuantos paquetes llegaron al sink
        # Para graficar:
        # x= self.setting_entities()
        # y=self.pkt_arribed_sink/self.timeCycleWork
        # plt.plot(  self.num_grades, self.pkt_arribed_sink/1000)

    """
        plt.plot (x,y)
        plt.show()
        plt.xlabel('grados')
        plt.ylabel('Ppaquetes/ciclo')
        plt.title('throughput')
        """

    # Plotear pkts perdidos
    # intervalos= [0,1,2,3,4,5,6]
    # plot.hist(x=self.num_pkt_discart, bins=intervalos)
    # plot.xlabel('num de paquetes')
    # plot.ylabel('grados')

    def get_pkt_ciclo_throughtput(self):
        resultThorughtput = self.pkt_arribed_sink / self.timeCycleWork
        return resultThorughtput
