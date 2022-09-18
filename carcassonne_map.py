''' Author: Victoria Santos
    Program: carcassonne_map.py
    Purpose: This program works in conjunction with
    carcassonne_tile.py to recreate the Carcassonne
    game digitally. It allows the user to place created
    tiles in certain locations, following the rules
    of the game. It contains one class, CarcassonneMap.
    Course: CSC 120 FA 001
'''


from carcassonne_tile import *


class CarcassonneMap:
    ''' This class represents the Carcassonne Map game
        board. It contains some of the functions 
        necessary to properly play the game and add
        tiles according to the rules.

        The constructor simply creates the game board with 
        tile01 at (0, 0).
    '''


    def __init__(self):
        ''' This constructor initializes the Map with
            tile01 at (0, 0).
            Arguments: self
            Return Value: none
        '''
        self._map = {(0, 0): tile01}


    def get_all_coords(self):
        ''' This function returns all the coordinates
            of placed tiles as a set.
            Arguments: self
            Return Value: set of tuple coords 
        '''
        all_coords = self._map.keys()
        all_coords = set(all_coords)
        return all_coords


    def find_map_border(self):
        ''' This function checks to see where 
            the player is able to place tiles on 
            the board. Available spots are around 
            the 'border' of the map and are 
            returned as a set of tuples.
            Arguments: self
            Return Value: set of tuple coords
        '''
        border_coords = set()
        for coord in self._map:
            if (coord[0] + 1, coord[1]) not in self._map:
                border_coords.add((coord[0] + 1, coord[1]))
            if (coord[0] - 1, coord[1]) not in self._map:
                border_coords.add((coord[0] - 1, coord[1]))
            if (coord[0], coord[1] + 1) not in self._map:
                border_coords.add((coord[0], coord[1] + 1))
            if (coord[0], coord[1] - 1) not in self._map:
                border_coords.add((coord[0], coord[1] - 1))

        return border_coords


    def get(self, x, y):
        ''' This function returns the tile at a 
            specified location on the board. If
            the tile is not on the board, it
            returns None.
            Arguments: self, int coords x and y
            Return Value: tile object or None
        '''
        coords = (x, y)
        if coords in self._map:
            return self._map[coords]
        else:
            return None


    def add(self, x, y, tile, confirm = True, tryOnly = False):
        ''' This function allows the player to add a tile
            to the game board. The function runs a series of
            checks to whether or not the tile can be added
            to the map by rule, and it can check before actually
            adding the tile. Preference is specified in the 
            parameters.
            Arguments: self, int coords x and y, bools confirm
            and tryOnly for specifying checks
            Return Value: bool for whether or not tile was
            successfully added to board
        '''
        border_coords = self.find_map_border()
        flag, coord = True, (x,y)
        x, y = coord[0], coord[1]
        if (x, y) in border_coords:
            if (x + 1, y) in self._map:
                if self._map[(x + 1, y)].get_edge(3) != tile.get_edge(1):
                    flag = False
            if (x - 1, y) in self._map:
                if self._map[(x - 1, y)].get_edge(1) != tile.get_edge(3):
                    flag = False
            if (x, y + 1) in self._map:
                if self._map[(x, y + 1)].get_edge(2) != tile.get_edge(0):
                    flag = False
            if (x, y - 1) in self._map:
                if self._map[(x, y - 1)].get_edge(0) != tile.get_edge(2):
                    flag = False
        else:
            flag = False

        if confirm == True and tryOnly == False:
            if flag == True:
                self._map[(x, y)] = tile
                return True
            return False
        elif confirm == True and tryOnly == True:
            if flag == True:
                return True
            return False
        elif confirm == False and tryOnly == False:
            self._map[(x, y)] = tile
            return True


    def trace_road_one_direction(self, x, y, side):
        ''' This function allows the player trace a given
            road in one direction. It will trace the road
            until there is no tile left at the end or if
            the road hits a crossroads.
            Arguments: self, int coords x and y, int side
            Return Value: list of tuples with
            tile coords and directions of road
        '''
        tiles, cur_x, cur_y = [], x, y
        
        while True:
            if side == -1:
                break
            elif side == 0:
                if (cur_x, cur_y + 1) in self._map:
                    cur_y, side = cur_y + 1, 2
                else:
                    break
            elif side == 1:
                if (cur_x + 1, cur_y) in self._map:
                    cur_x, side = cur_x + 1, 3
                else:
                    break
            elif side == 2:
                if (cur_x, cur_y - 1) in self._map:
                    cur_y, side = cur_y - 1, 0
                else:
                    break
            elif side == 3:
                if (cur_x - 1, cur_y) in self._map:
                    cur_x, side = cur_x - 1, 1
                else:
                    break

            tiles.append((cur_x, cur_y, side, \
                self._map[(cur_x, cur_y)].road_get_connection(side)))
            side = self._map[(cur_x, cur_y)].road_get_connection(side)

        return tiles


    def trace_road(self, x, y, side):
        ''' This function allows the player trace a given
            road in both directions. It will trace the road
            until there is no tile left at either end or if
            the roads hit crossroads. It uses 
            trace_road_one_direction as a helper function.
            Arguments: self, int coords x and y, int side
            Return Value: list of tuples with
            tile coords and directions of road
        '''
        both_dir = []
        given_dir = self.trace_road_one_direction(x, y, side)
        other_side = self._map[(x, y)].road_get_connection(side)
        other_dir = self.trace_road_one_direction(x, y, other_side)
        
        if len(other_dir) != 0:
            end = other_dir[-1]
            right_way = self.trace_road_one_direction(end[0], end[1], end[2])
            right_way.insert(0, (end[0], end[1], end[3], end[2]))

            for ele in right_way:
                both_dir.append(ele)
        else:
            both_dir.append((x, y, other_side, side))
            for ele in given_dir:
                both_dir.append(ele)

        return both_dir


    def trace_city(self, x, y, side):
        ''' This function allows the player trace an entire
            city. It takes a given location within a city
            and extends out into the given tile and 
            surrounding tiles to find all portions of 
            the connected city.
            Arguments: self, int coords x and y, int side
            Return Value: tuple: bool of whether or not
            city is complete, tuples with
            tile coords and city edges
        '''
        city, keep_searching, completed = {(x, y, side)}, True, True

        while keep_searching:
            keep_searching, dup = False, list(city)
            for tile in dup:
                cur_x, cur_y, edge = tile[0], tile[1], tile[2]
                for edge2 in range(4):
                    if self._map[(cur_x, cur_y)].edge_has_city(edge2) == True\
                    and self._map[(cur_x, cur_y)].city_connects(edge, edge2)\
                    and (cur_x, cur_y, edge2) not in city:
                        city.add((cur_x, cur_y, edge2))
                        keep_searching = True

                if edge == 0:
                    neigh = (cur_x, cur_y + 1, 2)
                elif edge == 1:
                    neigh = (cur_x + 1, cur_y, 3)
                elif edge == 2:
                    neigh = (cur_x, cur_y - 1, 0)
                elif edge == 3:
                    neigh = (cur_x - 1, cur_y, 1)

                if (neigh[0], neigh[1]) in self._map and \
                self._map[(neigh[0], neigh[1])].edge_has_city(neigh[2]) \
                and neigh not in city:
                    city.add(neigh)
                    keep_searching = True
                else:
                    completed = False
        return (completed, city)