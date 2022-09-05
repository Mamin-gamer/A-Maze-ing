#all algorithms are explained in a write-up in Algorithm section 

from random import randrange, shuffle, choice, random
from MakeGrid import Cell
from Utils import Stack

class GenerateAlgo:
    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.HEIGHT = (2*self.height) + 1
        self.WIDTH = (2*self.width) + 1

    def find_neighbours(self, row, column, grid, wall = False):
        neighbours = []
        if row > 1 and grid[row-2][column].is_wall == wall:
            neighbours.append(grid[row-2][column])
        if row < self.HEIGHT - 2 and grid[row + 2][column].is_wall == wall:
            neighbours.append(grid[row + 2][column])
        if column > 1 and grid[row][column - 2].is_wall == wall:
            neighbours.append(grid[row][column - 2])
        if column < self.WIDTH - 2 and grid[row][column + 2].is_wall == wall:
            neighbours.append(grid[row][column + 2])

        shuffle(neighbours)

        return neighbours
        

class EmptyGrid(GenerateAlgo):
    def __init__(self, width, height, clear = False):
        self.clear = clear
        super().__init__(width, height) #refering to GenerateAlgo, it will make WIDTH and HEIGHT variables

    def generate(self, *args):
        grid =  [[Cell(row, column, is_wall = True, is_empty = False) for column in range(self.WIDTH)] for row in range(self.HEIGHT)]

        for row in range(1, self.HEIGHT-1):
            for col in range(1, self.WIDTH-1):
                if self.clear:
                    grid[row][col].is_start = False
                    grid[row][col].is_end = False
                    grid[row][col].is_start = False
                    grid[row][col].is_solved_by_user = False
                    grid[row][col].is_solved_by_algo = False

                grid[row][col].is_wall = False
                grid[row][col].is_empty = True
        
        
        return (grid)

class BinaryTree(GenerateAlgo):
    def __init__(self, width, height, skew = None):
        super().__init__(width, height)
        skewes = {
            "NW": [(1, 0), (0, -1)],
            "NE": [(1, 0), (0, 1)],
            "SW": [(-1, 0), (0, -1)],
            "SE": [(-1, 0), (0, 1)],
        }
        if skew in skewes:
            self.skew = skewes[skew]
        else:
            key = choice(list(skewes.keys()))
            self.skew = skewes[key]

    def generate(self, *args):
        grid =  [[Cell(row, column, is_wall = True, is_empty = False) for column in range(self.WIDTH)] for row in range(self.HEIGHT)]
        for row in range(1, self.HEIGHT, 2):
            for col in range(1, self.WIDTH, 2):
                grid[row][col].is_wall = False
                grid[row][col].is_empty = True
                neigh_row, neigh_col = self.find_neighbours(row, col)
                grid[neigh_row][neigh_col].is_wall = False
                grid[neigh_row][neigh_col].is_empty = True
    
        return (grid)

    def find_neighbours(self, row, column):
        neighbours = []

        north = (1, 0)
        east = (0,1)

        if 1 < row + north[0] < self.HEIGHT-1:
            neighbours.append((row + north[0], column + north[1]))
        
        if 1 < column + east[1] < self.WIDTH-1:
            neighbours.append((row + east[0], column + east[1]))

        if len(neighbours) == 0:
            return (row, column)
        
        return choice(neighbours)



class BackTracker(GenerateAlgo):
    def __init__(self, width, height):
        super().__init__(width, height)

    def generate(self, *args):
        grid =  [[Cell(row, column, is_wall = True, is_empty = False) for column in range(self.WIDTH)] for row in range(self.HEIGHT)]
       
        row = randrange(1, self.HEIGHT, 2)
        column = randrange(1, self.WIDTH, 2)
        track = Stack()
        track.push((row, column))

        grid[row][column].is_wall = False
        grid[row][column].is_empty = True
    
        while not track.is_empty():
            crow, ccol = track.peek()
            neighbours = self.find_neighbours(crow, ccol, grid, wall=True)

            if len(neighbours) == 0:
                track.pop()
            else:
                nrow, ncol = neighbours[0].get_pos()

                grid[nrow][ncol].is_wall = False
                grid[nrow][ncol].is_empty = True


                between = ((crow + nrow) // 2, (ccol + ncol) // 2)

                grid[between[0]][between[1]].is_wall = False
                grid[between[0]][between[1]].is_empty = True

                track.push((nrow, ncol))

        return grid
            

class Sidewinder(GenerateAlgo):
    def __init__(self, width, height, skew = 0.5):
        #higher the skew, more vertical the maze is 
        #lower the skew, more horizontal the maze is
        super().__init__(width, height)
        self.skew = skew

    def generate(self, *args):
        grid = [[Cell(row, column, is_wall = True, is_empty = False) for column in range(self.WIDTH)] for row in range(self.HEIGHT)]
        
        for col in range(1, self.WIDTH-1):
            #the first row is always empty, because you can't carve North
            grid[1][col].is_wall = False
            grid[1][col].is_empty = True

        for row in range(3, self.HEIGHT, 2):
            run = []

            for col in range(1, self.WIDTH, 2):

                grid[row][col].is_wall = False
                grid[row][col].is_empty = True

                run.append(grid[row][col])
                carve = random() > self.skew

                if carve and col < (self.WIDTH-2):
                    grid[row][col+1].is_wall = False
                    grid[row][col+1].is_empty = True
                else:
                    north = choice(run)
                    pos = north.get_pos()
                    grid[pos[0]-1][pos[1]].is_wall = False
                    grid[pos[0]-1][pos[1]].is_empty = True

                    run = []

        return grid


    def get_links(self, cell):

        links = []
        cell_row, cell_col = cell.get_pos()
        position = [(0,1), (0,-1), (1,0), (-1,0)]

        for row, col in position:
            try:
                neighbour = self.grid[row+cell_row][col+cell_col]
                if neighbour.is_empty and not neighbour.is_wall:
                    links.append(neighbour)
            except:
                continue
        
        return links

class CellularAutomaton(GenerateAlgo):
    def __init__(self, width, height, complexity = 1, density = 1):
        super().__init__(width, height)
        self.complexity = complexity
        self.density = density

    def generate(self, *args):
        grid = EmptyGrid(self.width, self.height).generate()

        if self.complexity <=1:
            self.complexity = self.complexity * (self.width+self.height)
        if self.density <=1:
            self.density = self.density * (self.width+self.height) *2 #*2 to make denser
        

        for i in range(int(2*self.density)):
            if i < self.density:
                if choice([0,1]):
                    y = choice([0, self.HEIGHT-1])
                    x = randrange(0, self.WIDTH, 2)
                else:
                    x = choice([0, self.WIDTH-1])
                    y = randrange(0, self.HEIGHT, 2)
            else:
                y, x = randrange(0, self.HEIGHT, 2), randrange(0, self.WIDTH, 2)

            grid[y][x].is_wall = True
            grid[y][x].is_empty = False

            for j in range(int(self.complexity*2)):
                neighbors = self.find_neighbours(y, x, grid, True)
                if 0 < len(neighbors) < 4:
                    neighbors = self.find_neighbours(y, x, grid, False)

                    if not len(neighbors):
                        continue
                
                    neighbour = choice(neighbors)
                    row, column = neighbour.get_pos()
                    
                    if grid[row][column].is_empty:
                        grid[row][column].is_empty = False
                        grid[row][column].is_wall = True

                        grid[row + (y - row) // 2][column + (x - column) // 2].is_wall = True
                        grid[row + (y - row) // 2][column + (x - column) // 2].is_empty = False

                        x, y = column, row

        return grid



class Pims(GenerateAlgo):
    def __init__(self, width, height):
        super().__init__(width, height)

    def generate(self, *args):
        grid = [[Cell(row, column, is_wall = True, is_empty = False) for column in range(self.WIDTH)] for row in range(self.HEIGHT)]
        
        current_row = randrange(1, self.HEIGHT, 2)
        current_col = randrange(1, self.WIDTH, 2)
        grid[current_row][current_col].is_empty = True
        grid[current_row][current_col].is_wall = False

        neighbours = self.find_neighbours(current_row, current_col, grid, True)

        visited = 1

        while visited < self.height*self.width:
            ##nn = nearest neighbour

            nn = randrange(len(neighbours))
            current_row, current_col = neighbours[nn].get_pos()
            visited += 1
            grid[current_row][current_col].is_empty = True
            grid[current_row][current_col].is_wall = False
            neighbours = neighbours[:nn] + neighbours[nn + 1 :]

            nearest_n0, nearest_n1 = self.find_neighbours(current_row, current_col, grid)[0].get_pos()

            grid[(current_row + nearest_n0) // 2][(current_col + nearest_n1) // 2].is_wall = False
            grid[(current_row + nearest_n0) // 2][(current_col + nearest_n1) // 2].is_empty = True

            unvisited = self.find_neighbours(current_row, current_col, grid, True)
            neighbours = list(set(neighbours + unvisited))

        return grid
