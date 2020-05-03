from room import Room
from player import Player
from world import World
from utils import Stack

import random
from ast import literal_eval

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
reverse = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}


def traverse(world, traversal_path):
    # Instantiate a new stack, visited rooms dictionary, starting point, and current room
    stack = Stack()
    visited = {0: {}}
    vertex = 0
    current_room = world.rooms[vertex]

    # Returns possible paths
    def get_paths(already_visited, current):
        # Get current room by ID
        you_are_here = current.id
        exits = already_visited[you_are_here]
        # For all possible edges and accounting for rooms having been visited in the past
        for possible in exits:
            # If an exist is possible and has not been visited
            if exits[possible] == '?' and current.get_room_in_direction(possible).id not in already_visited:
                # Return the possible direction
                return possible
        return None

    # Returns room ID for a new room
    def get_rooms(path, dictionary, given_stack, current):
        ######################################
        # while stack.size() > 0:            #
        #     pop first vertex                #
        #     current_vertex = stack.pop()   #
        #     If it has not been visited     #
        #     visited.add(current_vertex)    #
        ######################################
        while True:
            # Similarly to previous graph works, pop and append/push pattern
            new_move = given_stack.pop()
            path.append(new_move)
            # Set new room to room in direction from popped value
            new_room = current.get_room_in_direction(new_move)
            # Return the ID if '?' is found within the room
            if '?' in dictionary[new_room.id].values():
                return new_room.id
            # Set current room to new room
            current = new_room

    ########################################################
    # for neighbor in self.get_neighbors(current_vertex):  #
    #     if neighbor not in visited:                      #
    #         stack.push(neighbor)                         #
    ########################################################
    for direction in current_room.get_exits():
        visited[current_room.id][direction] = '?'

    # While the length of visited rooms is less than the length of rooms
    while len(visited) < len(world.rooms):
        # set current room to the room associated with the given vertex
        current_room = world.rooms[vertex]

        # If the current room is not inside of the visited dictionary
        if current_room not in visited:
            # Add the current room ID to the dictionary
            visited[current_room.id] = {}
            # For exit directions available in the current room, add the available directions to visited
            for direction in current_room.get_exits():
                visited[current_room.id][direction] = '?'

        # Figure out our next move by getting unvisited directions
        next_move = get_paths(visited, current_room)

        # If next move is not available, scope ahead and find unvisited room IDs
        if not next_move:
            vertex = get_rooms(traversal_path, visited, stack, current_room)
        # if a move is available
        else:
            # Append the available path
            traversal_path.append(next_move)
            # Get move in a potential direction
            next = current_room.get_room_in_direction(next_move)
            # Set current vertex and path to next id
            visited[vertex][next_move] = next.id

            # if next.id not found in visited dictionary
            if next.id not in visited:
                # Add next room ID to the dictionary
                visited[next.id] = {}
                # For each direction available in the next room
                for direction in next.get_exits():
                    # Add '?' to the dictionary for each possible direction
                    visited[next.id][direction] = '?'

            # Going in the reverse direction
            visited[next.id][reverse[next_move]] = current_room.id
            # Push the next moves reversal onto the stack
            stack.push(reverse[next_move])
            # set the current room(vertex) to the next.id
            vertex = next.id


print('None: ', traverse(world, traversal_path))

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
