import sys
import statistics as stat
import time


class BranchPoint:
    def __init__(self, vertex, predecessor_branch_point=0, distance_to_source=0):
        self.__vertex = vertex
        self.__distance_to_source = distance_to_source

    def get_vertex(self):
        return self.__vertex

    def get_distance_to_source(self):
        return self.__distance_to_source


class BreadthFirstSearchTree:
    def __init__(self, source_vertex):
        """source is the source vertex"""
        self.__source = BranchPoint(source_vertex)
        self.__branch_point_list = []
        self.__branch_point_list += [self.__source]

    def insert(self, vertex, predecessor_branch_point=None, distance_to_source=0, with_return=False):
        new_branch_point = BranchPoint(vertex, predecessor_branch_point, distance_to_source)
        self.__branch_point_list += [new_branch_point]
        if with_return:
            return new_branch_point

    def get_source_branch_point(self):
        return self.__source

    def get_size(self):
        return len(self.__branch_point_list)

    def __iter__(self):
        for b in self.__branch_point_list:
            yield b


class Vertex:
    def __init__(self, key):
        self.__key = key
        self.__color = 'white'
        self.__neighbours = {}

    def set_color(self, colour):
        self.__color = colour

    def get_key(self):
        return self.__key

    def get_color(self):
        return self.__color

    def add_neighbour(self, neighbour):
        self.__neighbours[neighbour.get_key()] = [neighbour]

    def get_neighbours(self):
        neighbour_list = []
        for key in self.__neighbours.keys():
            neighbour_list += [self.__neighbours[key][0]]
        return neighbour_list


class Graph:
    """Graph creates a graph object from a graph dictionary of the form graph_dictionary[vertex_key] = {neighbour1_key,
    n2_key, ...} where key is an immutable value, unique for every vertex"""
    def __init__(self, graph_dictionary):
        self.vertex_dictionary = {}
        self.__component_trees = []
        for key in graph_dictionary.keys():                     # adds vertices
            vertex = Vertex(key)
            self.vertex_dictionary[key] = vertex
        for key in graph_dictionary.keys():                     # adds edges
            key_vertex = self.vertex_dictionary[key]
            for value in graph_dictionary[key]:
                value_vertex = self.vertex_dictionary[value]
                key_vertex.add_neighbour(value_vertex)

    def color_reset(self):
        for vertex in self.vertex_dictionary.values():
            vertex.set_color('white')

    def get_vertex_dict(self):
        return self.vertex_dictionary

    def get_component_trees(self):
        return self.__component_trees

    def compartmentalize(self):
        """"Creates a list of breadth_first_search_tree_objects, one for each component of the graph object"""
        self.color_reset()
        for vertex in self.vertex_dictionary.values():
            if vertex.get_color() != 'black':
                bfs_tree = self.__breadth_first_search(vertex)
                self.__component_trees += [bfs_tree]


    def write_trees_to_file(self):
        size = str(len(self.__component_trees))
        filename1 = 'Partitions_'+size+'.txt'
        file1 = open(filename1, 'w')
        sizes = []
        for tree in self.__component_trees:
            size = tree.get_size()
            sizes.append(size)
            keys = []
            for branch in tree:
                key = branch.get_vertex().get_key()
                keys.append(key)
            file1.write(str(size)+'\n')
            for key in keys:
                file1.write(key+'\n')
            file1.write('\n')
        file1.close()

    @classmethod
    def __breadth_first_search(cls, source_vertex):
        """A breadth first search algorithm, returning a breadth_first_search_tree_object"""
        source_vertex.set_color('gray')
        the_tree = BreadthFirstSearchTree(source_vertex)
        queue = []
        queue += [the_tree.get_source_branch_point()]
        while queue:
            branch_point = queue.pop()
            vertex = branch_point.get_vertex()
            for neighbour in vertex.get_neighbours():
                if neighbour.get_color() is 'white':
                    neighbour.set_color('gray')
                    distance_to_source = branch_point.get_distance_to_source() + 1
                    neighbour_branch_point = the_tree.insert(neighbour, branch_point,
                                                             distance_to_source, with_return=True)
                    queue += [neighbour_branch_point]
            vertex.set_color('black')
        return the_tree


def graph_dictionary_creator(file, n_o_lines=None):
    """Creates a graph dictionary of the form graph_dictionary[vertex_key] = {neighbour1_key,
    n2_key, ...} where key is an immutable value, unique for every vertex"""
    graph_dictionary = {}
    if not n_o_lines:
        for line in file.readlines():
            line_list = line.split()
            if len(line_list) > 1:
                line_list_to_dict(line_list, graph_dictionary)
            else:
                print('line list: {}\nhas too few elements'.format(line_list))
    else:
        for i in range(n_o_lines):
            line_list = file.readline().split()
            if len(line_list) > 1:
                line_list_to_dict(line_list, graph_dictionary)
            else:
                print('line list: {}\nhas too few elements'.format(line_list))
    return graph_dictionary

def line_list_to_dict(line_list, graph_dictionary):
    """Takes a line from the file split by ' ' and turned int a list and adds it to the graph dictionary"""
    v = line_list[0]
    n = line_list[1]
    if v not in graph_dictionary.keys():
        graph_dictionary[v] = {n}
    else:
        graph_dictionary[v] |= {n}
    if n not in graph_dictionary.keys():
        graph_dictionary[n] = {v}
    else:
        graph_dictionary[n] |= {v}


def main():
    t1 = time.time()
    argument_list = sys.argv
    lines = None
    for argument in argument_list:
        if argument[:6] == 'lines=':
            lines = int(argument[6:])
    try:
        with sys.stdin as file:
            graph_dictionary = graph_dictionary_creator(file, lines)
    except:
        raise  # except: raise pattern raises whatever error occurs
    graph = Graph(graph_dictionary)
    del graph_dictionary
    graph.compartmentalize()
    graph.write_trees_to_file()
    t2 = time.time()
    print(t2-t1)

if __name__ == '__main__':  # ensures that the main run isn't run when this file is imported
    main()
