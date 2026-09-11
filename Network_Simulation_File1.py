class Node:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.connections = []

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


nodes = {}

counters = {'Router': 1, 'Server': 1}


def add_node(type):
    name_number = counters[type]
    name = type[0] + str(name_number)
    counters[type] += 1
    node = Node(name, type)
    nodes[name] = node


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
