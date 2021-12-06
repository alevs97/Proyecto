import enum
import copy

class Node:



    def __init__(self, size_buffer, lambda_pkt, num_node):
        self.num_node = num_node
        self.lambda_pkt = lambda_pkt
        self.size_buffer = size_buffer
        self.buffer = [0 for i in range(size_buffer)]

    def __str__(self):
        return "Buffer: " + str(self.buffer) + ", Num_Node: " + str(self.num_node)

    def is_buffer_with_pkt_to_transmit(self):
        if self.buffer[0] == 1:
            return True
        else:
            return False

    def adding_pkt_to_buffer(self):
        """
        Description:
        Function simulate when a node generate a pkt. Could be generating o receibing
        """
        for i in range(self.size_buffer):
            if self.buffer[i] == 0:
                # Available space in buffer
                self.buffer[i] = 1
                return True


    def transmiting_pkt_to_next_grade(self):
        """
        Description:
         Function to simulate when a node is tranmiting data
        """
        for i in range(self.sizeBuffer-1, 0, -1):
            if self.buffer[i] == 1:
                self.buffer[i] = 0
                return True







