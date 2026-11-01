import random
import heapq

class Node:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.connections = []
        self.mac_address = ':'.join(f'{random.randint(0,255):02X}' for i in range(6))  # formats random number into a 2 digit hexadecimal number


    def add_connection(self, node_name, distance):
        self.connections.append((node_name, distance))
        nodes[node_name].connections.append((self.name, distance))

    def remove_node(self):
        for node_connection in self.connections:
            node_name = node_connection[0]
            for connection in nodes[node_name].connections:
                if connection[0] == self.name:
                    nodes[node_name].connections.remove(connection)
        del nodes[self.name]

    def remove_connection(self, node_name):
        for connection in nodes[node_name].connections:
            if connection[0] == self.name:
                nodes[node_name].connections.remove(connection)
        for connection in self.connections:
            if connection[0] == node_name:
                self.connections.remove(connection)

    def receive_packet(self, packet, incoming_node):
        if packet.destination == self.name:
            packet.received_packet()
        else:
            self.forward_packet(packet)

    def forward_packet(self, packet):
        pass



class Packet:
    def __init__(self, source, destination, data):
        self.source = source
        self.destination = destination
        self.source_mac = nodes[source].mac_address
        self.data = data
        self.connections = []
        self.received = False

    def received_packet(self):
        self.received = True


class Router(Node):
    def __init__(self, name, network_name):
        super().__init__(name, network_name)
        self.connections = []
        self.type = 'Router'
        # needs to have: - packet rerouting, data security system
        # could have a system where data packets travel in one of the three most optimal directions to simulate data traffic in
        # the routers are the only components then that pick the optimal path for the data packets

    def reroute_packets(self, destination_node):
        self.remove_connection(destination_node.name)
        # find_shortest_path(self.name, destination_node.name)



class Server(Node):
    def __init__(self, name, network_name):
        """

        Parameters
        ----------
        name
        network_name
        """
        super().__init__(name, network_name)
        self.connections = []
        self.type = 'Server'
        #self.data = input('Please enter the data you want stored on the server: ')

        # could have subclasses of server for different types: web server, file server etc.

    def get_data(self):
        return self.data


class Modem(Node):
    def __init__(self, name,network_name, speed):
        super().__init__(name, network_name)
        self.connections = []
        self.type = 'Modem'
        self.speed = speed


class Switch(Node):
    def __init__(self, network_name, name):
        super().__init__(name, network_name)
        self.connections = []
        self.type = 'Switch'
        self.mac_routing_table = {}  # node name followed by MAC address

    def receive_packet(self, packet, incoming_node): # uses its MAC address table to route data packets and if destination not in table, send to all neighbours
        self.mac_routing_table[packet.source_mac] = incoming_node

        if nodes[packet.destination].mac_address in self.mac_routing_table.keys():
            next_node = self.mac_routing_table[nodes[packet.destination].mac_address]
            nodes[next_node].receive_packet(packet, self.name)

        else:
            for neighbour in [connection[0] for connection in self.connections]:
                if neighbour != incoming_node:
                    nodes[neighbour].receive_packet(packet, self.name)


class Hub(Node):
    def __init__(self, network_name, name):
        super().__init__(name, network_name)
        self.connections = []
        self.type = 'Hub'

    def send_data(self, incoming_node, destination_node): #to all nodes
        for node in self.connections:
            node.receive_packet()


nodes = {}

counters = {'Router': 1, 'Server': 1}


def add_node(type, network_name='Temp Network'):
    nodes[type] = Node(type, network_name)
    name_number = counters[type]
    name = type[0] + str(name_number)
    counters[type] += 1
    #network_name = input('Please enter the name of the network this node will belong to')
    if type == 'Router':
        nodes[name] = Router(name, network_name)
    elif type == 'Server':
        nodes[name] = Server(name, network_name)
    elif type == 'Modem':
        #speed = input('Please enter a speed for the modem: ')
        nodes[name] = Modem(name, network_name, 100)


def check_devices_connected():
    start_node = next(iter(nodes.values()))
    checked = []
    checked = dfs(start_node, checked)
    if len(checked) == len(nodes):
        return True
    else:
        return False


def dfs(start_node, checked):
    checked.append(start_node.name)
    for connection in start_node.connections:
        if connection[0] not in checked:
            connected_node = nodes[connection[0]]
            dfs(connected_node, checked)
    return checked


def find_disconnected_devices():
    connection_groups = []
    for node_name, node in nodes.items():
        if all(node_name not in connection for connection in connection_groups):
            start_node = node
            checked = []
            checked = dfs(start_node, checked)
            connection_groups.append(checked)
    return connection_groups


def simulate_failures(node):
    temp = []
    for node_connection in node.connections:
        node_name = node_connection[0]
        for connection in nodes[node_name].connections:
            if connection[0] == node.name:
                node_connected_and_connection_info = node_name, connection
                temp.append(node_connected_and_connection_info)
                nodes[node_name].connections.remove(connection)
    del nodes[node.name]
    # ...
    connection_status = check_devices_connected()
    print('Devices all connected', connection_status)
    if not connection_status:
        print('Groups of devices connected together:', find_disconnected_devices())

    # ....
    for connection in temp:
        nodes[connection[0]].connections.append(connection[1])


def min_spanning_tree(nodes): # connects every device to every other device through intermediate devices whilst minimising the total connection cost
    # it avoids unnecessary connections that would create a cycle
    # uses Krustal's algorithm
    all_connections = []
    for node in nodes.values():
        for node_connection in node.connections:
            new_connection = (node_connection[0], node.name, node_connection[1])
            if (node.name, node_connection[0], node_connection[1]) not in all_connections:
                all_connections.append(new_connection)

    for node_name, node in nodes.items():
        for curr_node in nodes.keys():
            node.remove_connection(curr_node)
    all_connections.sort(key=lambda x: x[2])
    groups = [[node.name] for node in nodes.values()]
    all_connected = False
    index = 0
    while not all_connected and index < len(all_connections):
        connection_node1, connection_node2, length = all_connections[index]
        if len(groups) == 1:
            all_connected = True
        else:
            for i in range(len(groups)):
                if connection_node1 in groups[i]:
                    group_number = i
            if connection_node2 not in groups[group_number]:
                nodes[connection_node1].add_connection(connection_node2, length)
                for j in range(len(groups)):
                    if connection_node2 in groups[j]:
                        group_number_2 = j
                temp_group = groups[group_number] + groups[group_number_2]
                groups[group_number] = temp_group
                groups.remove(groups[group_number_2])
        index += 1
    final_connections = []
    for node in nodes.values():
        for connection in node.connections:
            final_connections.append(connection)
    return final_connections

def dijkstra(start_node, nodes):
    distances_dict = {}
    priority_queue = []
    previous_nodes = {}
    for node in nodes.values():
        distances_dict[node.name] = 999999999999999
    distances_dict[start_node] = 0
    heapq.heappush(priority_queue, (0, start_node))
    while len(priority_queue) > 0:
        current_distance, current_node = heapq.heappop(priority_queue)
        if current_distance <= distances_dict[current_node]:
            for neighbour, distance in nodes[current_node].connections:
                if distance + current_distance < distances_dict[neighbour]:
                    distances_dict[neighbour] = distance + current_distance
                    previous_nodes[neighbour] = current_node
                    heapq.heappush(priority_queue, (distance + current_distance, neighbour))
    return distances_dict







def create_test_network():
    add_node('Router')
    add_node('Router')
    add_node('Router')
    add_node('Router')
    add_node('Server')
    add_node('Server')

    R1 = nodes['R1']
    R2 = nodes['R2']
    R3 = nodes['R3']
    R4 = nodes['R4']
    S1 = nodes['S1']
    S2 = nodes['S2']

    R1.add_connection('R2', 5)
    S2.add_connection('R4', 10)
    S1.add_connection('R3', 7)
    R3.add_connection('R1', 9)


#print(R1.connections)
#print(R2.connections)
#R1.remove_connection('R2')
#print(R1.connections)
#print(R2.connections)

#print(check_devices_connected())
#S2.add_connection('R2', 8)
#print(check_devices_connected())

#print(find_disconnected_devices())
#print(min_spanning_tree(nodes))
