''' Author: Victoria Santos
    Program: carcassonne_tile.py
    Purpose: This program contains functions for
    creating and getting information about the
    Carcassonne game tiles. They are all a part 
    of the CarcassonneTile class used to make
    create each tile.
    Course: CSC 120 FA 001
'''


class CarcassonneTile:
    ''' This class represents the Carcassonne Tiles
        of the game. It contains the functions 
        necessary for creating complete tiles which can 
        be properly placed on the Carcassonne Map.

        The constructor creates each Tile object
        with its four edges and a bool for whether
        or not its city connects. It also has
        a list for all of the edges in one place.
    '''


    def __init__(self, n, e, s, w, city_connects):
        ''' This constructor initializes each Tile
            with its n, e, s, and w edge types.
            It also has a bool for whether or not
            its city connects and a list of
            the four direction types.
            Arguments: self, strings n, e, s, w,
            bool city_connects
            Return Value: none
        '''
        self._n = n
        self._e = e
        self._s = s
        self._w = w
        self._city_connects = city_connects

        self._edges = [n, e, s, w]


    def get_edge(self, side):
        ''' This function returns the type of
            a given tile side.
            Arguments: self, int side
            Return Value: string side type
        '''
        if side == 0:
            return self._n
        elif side == 1:
            return self._e
        elif side == 2:
            return self._s
        elif side == 3:
            return self._w


    def edge_has_road(self, side):
        ''' This function returns a bool for
            whether or not a given Tile edge
            has a road.
            Arguments: self, int side
            Return Value: bool
        '''
        return self._edges[side] == 'grass+road'


    def edge_has_city(self, side):
        ''' This function returns a bool for
            whether or not a given Tile edge
            has a city.
            Arguments: self, int side
            Return Value: bool
        '''
        return self._edges[side] == 'city'


    def has_crossroads(self):
        ''' This function checks to see if a
            given tile has a crossroads. It
            can detect both three-way and
            four-way crossroads, and will
            return True if either are
            detected.
            Arguments: self
            Return Value: bool
        '''
        ns = (self._edges[0] == 'grass+road' and \
            self._edges[2] == 'grass+road')
        ew = (self._edges[1] == 'grass+road' and \
            self._edges[3] == 'grass+road')

        if ns and ew:
            return True
        elif ns and (self._edges[1] == 'grass+road' or \
            self._edges[3] == 'grass+road'):
            return True
        elif ew and (self._edges[0] == 'grass+road' or \
            self._edges[2] == 'grass+road'):
            return True
        else:
            return False


    def road_get_connection(self, from_side):
        ''' This function returns the side at which
            the given road connects. If the Tile has
            a crossroads, it returns -1. Otherwise,
            it will return the side that has the
            rest of the Tile's road.
            Arguments: self, int from_side
            Return Value: int -1 or int 0-3 for
            specific side
        '''
        if self.has_crossroads():
            return -1
        else:
            i = 0
            while i < 4:
                if self._edges[i] == 'grass+road' and i != from_side:
                    return i
                i += 1


    def city_connects(self, sideA, sideB):
        ''' This function checks a variety of cases to
            see if a Tile's city connects. It may
            connect along the given edges or across the
            middle of the tile. It will return
            a bool for whether or not the city
            connects in any way.
            Arguments: self, int sideA, int sideB
            Return Value: bool
        '''
        if self._edges[sideA] == self._edges[sideB]:
            if sideA == sideB:
                return True

            if self._city_connects == False:
                return False

            if sideA == sideB:
                return True
            elif sideA == 0 and (sideB == 1 or sideB == 3):
                return True
            elif sideA == 1 and (sideB == 0 or sideB == 2):
                return True
            elif sideA == 2 and (sideB == 1 or sideB == 3):
                return True
            elif sideA == 3 and (sideB == 0 or sideB == 2):
                return True
            elif (sideA == 1 and sideB == 3) or (sideA == 3 and sideB == 1):
                if self._city_connects == True:
                    return True
            elif (sideA == 0 and sideB == 2) or (sideA == 2 and sideB == 0):
                if self._city_connects == True:
                    return True

        return False


    def rotate(self):
        ''' This function allows a user to rotate a
            Tile before placing it. It creates new
            objects so as to not alter other
            duplicate tiles on the board.
            Arguments: self
            Return Value: new rotated Tile object
        '''
        rotated = CarcassonneTile(self._w, self._n, self._e, \
            self._s, self._city_connects)
        return rotated


c = 'city'
g = 'grass'
gr = 'grass+road'

tile01 = CarcassonneTile(c, gr, g, gr, False)
tile02 = CarcassonneTile(c, c, g, c, True)
tile03 = CarcassonneTile(gr, gr, gr, gr, False)
tile04 = CarcassonneTile(c, gr, gr, g, False)
tile05 = CarcassonneTile(c, c, c, c, True)
tile06 = CarcassonneTile(gr, g, gr, g, False)
tile07 = CarcassonneTile(g, c, g, c, False)
tile08 = CarcassonneTile(g, c, g, c, True)
tile09 = CarcassonneTile(c, c, g, g, True)
tile10 = CarcassonneTile(g, gr, gr, gr, False)
tile11 = CarcassonneTile(c, gr, gr, c, True)
tile12 = CarcassonneTile(c, g, gr, gr, False)
tile13 = CarcassonneTile(c, gr, gr, gr, False)
tile14 = CarcassonneTile(c, c, g, g, False)
tile15 = CarcassonneTile(g, g, gr, gr, False)
tile16 = CarcassonneTile(c, g, g, g, False)