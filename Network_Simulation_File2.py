class Node:
    def __init__(self, name, network_name):
        self.name = name
        self.network_name = network_name
        self.type = 'Node'
        self.connections = []
        self.data_received = {}
        # data received could be stored in an array of data items or a dictionary with each key being
        # the node the data is from and the values being arrays storing an array of each data item
        # from that specific node

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
        super().__init__(name)
        self.connections = []
        self.type = 'Server'
        self.data = input('Please enter the data you want stored on the server: ')

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

    def send_data(self, incoming_node, destination_node): #only to right destination
        for node in self.connections:
            if node[0] == destination_node:




class Hub(Node):
    def __init__(self, network_name, name):
        super().__init__(name, network_name)
        self.connections = []
        self.type = 'Hub'

    def send_data(self, incoming_node, destination_node): #to all nodes
        pass
        for node in self.connections:
            nodes[node[0]].data_received.index()
            nodes[node[0]].data_received[incoming_node].append('Test Data')



nodes = {}

counters = {'Router': 1, 'Server': 1, 'Modem': 1}


def add_node(type):
    name_number = counters[type]
    name = type[0] + str(name_number)
    counters[type] += 1
    network_name = input('Please enter the name of the network this node will belong to')
    if type == 'Router':
        nodes[name] = Router(name, network_name)
    elif type == 'Server':
        nodes[name] = Server(name, network_name)
    elif type == 'Modem':
        speed = input('Please enter a speed for the modem: ')
        nodes[name] = Modem(name, network_name, speed)


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


def min_spanning_tree(nodes):
    all_connections = []
    for node in nodes.values():
        for node_connection in node.connections:
            new_connection = (node_connection[0], node.name, node_connection[0])
            all_connections.append(new_connection)

    for node_name, node in nodes.items():
        for curr_node in nodes.keys():
            node_name.remove_connection(curr_node.name)
    all_connections.sort(key=lambda x: x[2])
    current_cycle = []
    all_connected = False
    index = 0
    while not all_connected and index < len(all_connections):
        connection_node1, connection_node2, length = all_connections[index]
        nodes[connection_node1].add_connection(connection_node2, length)

def find_shortest_path(incoming_node, destination_node):
    pass

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
print(R1.connections)
print(R2.connections)
R1.remove_connection('R2')
print(R1.connections)
print(R2.connections)

print(check_devices_connected())
S2.add_connection('R2', 8)
print(check_devices_connected())
print(find_disconnected_devices())
