from entities.grade import Grade
from entities.node import Node
from random import randint

class Simulation:

    def __init__(self, mesageDifs, mesageSifs, mesageRts, mesageCts, mesageAck, mesageData, sigma,
                 num_grades, size_buffer, ranuSleeping, lambda_pkt, maxMiniRanueras, num_nodos):
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
        self.maxMiniRanueras = maxMiniRanueras
        self.lambda_pkt = lambda_pkt
        self.size_buffer = size_buffer
        self.num_grades = num_grades
        self.sigma = sigma
        # Generacion de otras variables
        self.timeSlot = mesageDifs + (maxMiniRanueras * sigma) + mesageRts + (3 * mesageSifs) \
                        + mesageCts + mesageData + mesageAck
        self.timeCycleWork = (2 + ranuSleeping) * self.timeSlot

        # Setting nodes and grades
        self.network = self.setting_entities()



        # Variables performance
        self.numPktDiscart = [0 for i in range(num_grades)]

    def setting_entities(self):
        list_grades = []
        for index_grade in range(self.num_grades):
            list_nodes = []
            for index_node in range(self.num_nodos):
                node = Node(
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
        # Choosing
        ramdom_grade = randint(0,self.num_grades-1)
        ramdom_node = randint(0,self.num_nodos-1)
        print("Number Grade" + str(ramdom_grade))
        print("Number Node" + str(ramdom_node))

        # Selecting
        grade = self.network[ramdom_grade]
        node = grade.get_node_by_number_node(ramdom_node)
        # Adding
        node.adding_pkt_to_buffer()

    def contention_process(self, num_grade):
        list_nodes_with_pkt = self.get_nodes_with_pkt_to_transmit(num_grade)
        winner_node = self.choosing_node_to_transmit(list_nodes_with_pkt)

    def get_nodes_with_pkt_to_transmit(self, num_grade):
        grade_in_contention = self.network[num_grade]
        list_nodes_with_pkt = []
        for node in grade_in_contention.list_nodes:
            if node.is_buffer_with_pkt_to_transmit():
                list_nodes_with_pkt.append(node)
        return list_nodes_with_pkt

    def choosing_node_to_transmit(self, list_nodes_with_pkt):
        random_grade = randint(0, len(list_nodes_with_pkt)-1)
        winner_node = list_nodes_with_pkt[random_grade]
        return winner_node

    def transmit_pkt_to_next_grade(self):
        pass

    def print_network(self):
        print(len(self.network))
        for grade in self.network:
            print(grade)
            for node in grade.list_nodes:
                print(node)




