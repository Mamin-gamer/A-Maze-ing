from random import shuffle, random, choice

#class that declares a cell that will store position and boolean values 
class Cell:
    def __init__(self, row, column, is_start = False, is_end = False, is_wall = False, is_empty = True, value = 'empty'):
        self.row = row
        self.column = column

        self.is_start = is_start
        self.is_end = is_end
        
        self.is_wall = is_wall
        self.is_empty = is_empty

        self.is_child = False
        self.is_parent = False
        self.is_solved = False
        
        self.value = value # value that will be displayed
    #getter method to return position of a node
    def get_pos(self):
        return (self.row, self.column)

#class grid that contains 2D array of Node classes
class Grid:
    def __init__(self):
        self.generator = None
        self.grid = None
        self.start = None
        self.end = None
        
        self.solver = None
    #function that generates a maze with a given algorithm
    def generate(self, start = None, end = None):
        if self.generator:
            self.grid = self.generator.generate(start) # for later use
            self.HEIGHT = len(self.grid)
            self.WIDTH = len(self.grid[0])

            self.start = start
            self.end = end
            self.solutions = None
        else:
            pass
    #function that generates entrances
    def generate_entrance(self, start = None, end = None):
        if start:
            self.start = start
        else:
            self.start = (1,0)

        if end:
            self.end = end
        else:
            self.end = (self.HEIGHT-2, self.WIDTH-1)


        self[self.start].is_start = True
        self[self.end].is_end = True
        self[self.start].is_wall = True
        self[self.end].is_wall = True


    #funcion that searches through maze and deletes dead-ends
    #makes more holes in a maze -> easier to solve + more routes available
    def braid(self, probability = 1):
        deads = self.deadends()
        shuffle(deads)
        if deads:
            for cell in deads:
                if len(self.get_links(cell)) <= 1 or random() <= probability:

                    neighbours = []
                    for link in self.get_neighbours(cell):
                        if not self.linked_to(cell, link):
                            neighbours.append(link)

                    best = []
                    for neighbour in neighbours:
                        if len(self.get_links(neighbour)) == 1:
                            best.append(neighbour)

                    if len(best) == 0:
                        best = neighbours

                    if len(neighbours) == 0:
                        continue

                    neighbour = choice(best)
                    neighbour.is_wall = False
                    neighbour.is_empty = True

    
    # function that returns a list of deadends in a grid
    def deadends(self):
        deads = []
        for row in range(1, self.HEIGHT, 2):
            for col in range(1, self.WIDTH, 2):
                cell = self.grid[row][col]
                if len(self.get_links(cell)) == 1:                    
                    deads.append(cell)
        
        return deads
    #functon that returns if a cell lined to another cell
    def linked_to(self, cell, link):
        if link in self.get_links(cell):
            return True
        return False

    #function that returns neighbours nodes including walls
    def get_links(self, cell):
        link = []
        neighbours = self.get_neighbours(cell)
        for node in neighbours:
            if not node.is_wall:
                link.append(node)

        return link

    #functon that returns neighbours 
    def get_neighbours(self, cell):
        links = []
        cell_row, cell_col = cell.get_pos()
        position = [(0,1), (0,-1), (1,0), (-1,0)]

        for row, col in position:
            if 1 < row + cell_row < self.HEIGHT-1 and 1 < col + cell_col < self.WIDTH-1:
                try:
                    neighbour = self.grid[row+cell_row][col+cell_col]
                    links.append(neighbour)
                except:
                    continue

        return links
    #function that exports maze in binary to be stored in a database
    def export(self):
        #array will consist of 1 and 0 where 1 is a wall and 0 is empty cell
        array = ''

        start = ()
        end = ()
        for row in range(1, self.HEIGHT-1):
            for column in range(1, self.WIDTH-1):
                
                cell = self.grid[row][column]

                if cell.is_start:
                    start = cell.get_pos()
                if cell.is_end:
                    end = cell.get_pos()
                
                if cell.is_empty:
                    val = 0
                elif cell.is_wall:
                    val = 1
        
                array += str(val)

        if not start or not end:
            for row in range(self.HEIGHT):
                for column in range(self.WIDTH):
                    cell = self.grid[row][column]
                    if cell.is_start:
                        start = cell.get_pos()
                    if cell.is_end:
                        end = cell.get_pos()


        #returns array of 1s and 0s, height and width of initial array, coordinates of start and end 
        return(array, self.HEIGHT, self.WIDTH, start, end)
    #function that searches one by one in a maze and returns a position of start/end node
    def get_node_pos(self, node):
        for r in range(self.HEIGHT):
            for c in range(self.WIDTH):
                
                cell = self.grid[r][c]
                if cell.is_start and node == 'start':
                    return (r,c)
                if cell.is_end and node == 'end':
                    return (r,c)
        
        return None
    #funciton that allows to move start and end nodes to a position specified by a cursor
    def move_cells(self, cell, position):
        if cell.is_start:
            self.follow_start = True
            self.follow_end = False
        if cell.is_end:
            self.follow_end = True
            self.follow_start = False
            
     
        y,x = position
        
        if not self.grid[y][x].is_start and not self.grid[y][x].is_end:

            if self.follow_start:
                cords = self.get_node_pos('start')
                if cords:
                    row, column = cords
                self.grid[y][x].is_start = True
                self.grid[row][column].is_start = False

            if self.follow_end:
                cords = self.get_node_pos('end')
                if cords:
                    row, column = cords
                self.grid[row][column].is_end = False
                self.grid[y][x].is_end = True



    def __getitem__(self, key):
        row, column = key
        if not (0 <= row < self.HEIGHT):
            return None
        if not (0 <=column < self.WIDTH):
            return None
        #if row is in between 0 and maximum index it can take, it returns cell at position row, columns, otherwise None as a neighbour
        return self.grid[row][column]

