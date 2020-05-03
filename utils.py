class Queue:
    def __init__(self):
        self.queue = []

    def size(self):
        return len(self.queue)

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None


class Stack:
    def __init__(self):
        self.stack = []

    def size(self):
        return len(self.stack)

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    def remove_item(self, index):
        return self.stack.pop(index)


class Graph:
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        # Add a vertex to the graph
        self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        # Add a directed edge
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)
        else:
            raise IndexError("That vertex does not exist!")

    def get_neighbors(self, vertex_id):
        # Get neighbors (edges) of a vertex
        return self.vertices[vertex_id]

    def bft(self, starting_vertex):
        # Print each vertex in breadth-first order, beginning from the starting_vertex
        queue = Queue()
        queue.enqueue(starting_vertex)
        # Create a set for visited_vertices
        visited = set()
        # While queue is not empty
        while queue.size() > 0:
            # Dequeue the first vertex on the queue
            current_vertex = queue.dequeue()
            # If it has not been visited
            if current_vertex not in visited:
                # Print the current vertex
                print(current_vertex)
                # Mark it as visited, (add it to visited)
                visited.add(current_vertex)
                # Add all unvisited neighbors to the queue
                for neighbor in self.get_neighbors(current_vertex):
                    if neighbor not in visited:
                        queue.enqueue(neighbor)

    def dfs(self, starting_vertex):
        # Print each vertex in depth-first order, beginning from the starting_vertex
        stack = Stack()
        stack.push(starting_vertex)
        # Create a set for visited vertices
        visited = set()
        # While stack is not empty
        while stack.size() > 0:
            # pop first vertex
            current_vertex = stack.pop()
            # If it has not been visited
            visited.add(current_vertex)
            # Add all unvisited neighbors to the stack
            for neighbor in self.get_neighbors(current_vertex):
                if neighbor not in visited:
                    stack.push(neighbor)
