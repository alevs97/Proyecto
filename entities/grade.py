class Grade:

    def __init__(self, num_grade, list_nodes):
        self.num_grade = num_grade
        self.list_nodes = list_nodes

    def __str__(self):
        return "List Node: " +str(self.list_nodes) +", Num_Grade: "+str(self.num_grade)

    def get_node_by_number_node(self, num_node):
        return self.list_nodes[num_node]


