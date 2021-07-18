#! /usr/bin/env python3
''' Run cool maze generating algorithms. '''
import random

class Cell:
    ''' Represents a single cell of a maze.  Cells know their neighbors
        and know if they are linked (connected) to each.  Cells have
        four potential neighbors, in NSEW directions.
    '''  
    def __init__(self, row, column):
        assert row >= 0
        assert column >= 0
        self.row = row
        self.column = column
        self.links = {}
        self.north = None
        self.south = None
        self.east  = None
        self.west  = None
        
    def link(self, cell, bidirectional=True):
        ''' Carve a connection to another cell (i.e. the maze connects them)'''
        assert isinstance(cell, Cell)
        self.links[cell] = True
        if bidirectional:
            cell.link(self, bidirectional=False)
        
    def unlink(self, cell, bidirectional=True):
        ''' Remove a connection to another cell (i.e. the maze 
            does not connect the two cells)
            
            Argument bidirectional is here so that I can call unlink on either
            of the two cells and both will be unlinked.
        '''
        assert isinstance(cell, Cell)
        #del self.links[cell]
        self.links[cell]=False
        if bidirectional:
            cell.unlink(self, bidirectional=False)
            
    def is_linked(self, cell):
        ''' Test if this cell is connected to another cell.
            
            Returns: True or False
        '''
        assert isinstance(cell, Cell)
        return self.links[cell]
        
    def all_links(self):
        ''' Return a list of all cells that we are connected to.'''
        return self.links
        
    def link_count(self):
        ''' Return the number of cells that we are connected to.'''
        i=0
        for item in self.links:
            if item==True:
                i=i+1
        return i
        
    def neighbors(self):
        ''' Return a list of all geographical neighboring cells, regardless
            of any connections.  Only returns actual cells, never a None.
        '''
        result=[]
        if self.north != None:
            result.append(self.north)
        if self.south != None:
            result.append(self.south)
        if self.east != None:
            result.append(self.east)
        if self.west != None:
            result.append(self.west)
        return result
                
    def __str__(self):
        return f'Cell at {self.row}, {self.column}'
        

class Grid:
    ''' A container to hold all the cells in a maze. The grid is a 
        rectangular collection, with equal numbers of columns in each
        row and vis versa.
    '''
    
    def __init__(self, num_rows, num_columns):
        assert num_rows > 0
        assert num_columns > 0
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.grid = self.create_cells()
        self.connect_cells()
        
    def create_cells(self):
        ''' Call the cells into being.  Keep track of them in a list
            for each row and a list of all rows (i.e. a 2d list-of-lists).
            
            Do not connect the cells, as their neighbors may not yet have
            been created.
        '''
        grid=[[0 for i in range(self.num_columns)] for j in range (self.num_rows)]
        for i in range(self.num_rows):
            for j in range(self.num_columns):
                grid[i][j]=Cell(i,j)
        return grid
            
    def connect_cells(self):
        ''' Now that all the cells have been created, connect them to 
            each other. 
        '''
        for i in range(self.num_rows):
            for j in range(self.num_columns):
                if i!=self.num_rows-1:
                    self.grid[i][j].link(self.grid[i+1][j])
                    self.grid[i][j].south=self.grid[i+1][j]
                if i!=0:
                    self.grid[i][j].link(self.grid[i-1][j])
                    self.grid[i][j].north=self.grid[i-1][j]
                if j!=self.num_columns-1:
                    self.grid[i][j].link(self.grid[i][j+1])
                    self.grid[i][j].east=self.grid[i][j+1]
                if j!=0:
                    self.grid[i][j].link(self.grid[i][j-1])
                    self.grid[i][j].west=self.grid[i][j-1]
    def unlink_all(self):
        for i in range(self.num_rows):
            for j in range(self.num_columns):
                if i!=self.num_rows-1:
                    self.grid[i][j].unlink(self.grid[i+1][j])
                    
                if i!=0:
                    self.grid[i][j].unlink(self.grid[i-1][j])
                    
                if j!=self.num_columns-1:
                    self.grid[i][j].unlink(self.grid[i][j+1])
                    
                if j!=0:
                    self.grid[i][j].unlink(self.grid[i][j-1])


                    
    def cell_at(self, row, column):
        ''' Retrieve the cell at a particular row/column index.'''
        return self.grid[row][column]
        
    def deadends(self):
        ''' Return a list of all cells that are deadends (i.e. only link to
            one other cell).
        '''
        result=[]
        for item in self.grid:
            if item.link_count==1:
                result.append(item)
        return result
                            
    def each_cell(self):
        ''' A generator.  Each time it is called, it will return one of 
            the cells in the grid.
        '''
        for row in range(self.num_rows):
            for col in range(self.num_columns):
                c = self.cell_at(row, col)
                yield c
                
    def each_row(self):
        ''' A row is a list of cells.'''
        for row in self.grid:
            yield row
               
    def random_cell(self):
        ''' Chose one of the cells in an independent, uniform distribution. '''
        i=random.randint(0,self.num_rows-1)
        j=random.randint(0,self.num_columns-1)
        return self.grid[i][j]
        
    def size(self):
        ''' How many cells are in the grid? '''
        return self.num_columns*self.num_rows
        
    def set_markup(self, markup):
        ''' Warning: this is a hack.
            Keep track of a markup, for use in representing the grid
            as a string.  It is used in the __str__ function and probably
            shouldn't be used elsewhere.
        '''
        self.markup = markup
        
    def __str__(self):
        ret_val = '+' + '---+' * self.num_columns + '\n'
        for row in self.grid:
            ret_val += '|'
            for cell in row:
                cell_value = self.markup[cell]
                ret_val += '{:^3s}'.format(str(cell_value))
                if not cell.east:
                    ret_val += '|'
                elif cell.east.is_linked(cell):
                    ret_val += ' '
                else:
                    ret_val += '|'
            ret_val += '\n+'
            for cell in row:
                if not cell.south:
                    ret_val += '---+'
                elif cell.south.is_linked(cell):
                    ret_val += '   +'
                else:
                    ret_val += '---+'
            ret_val += '\n'
        return ret_val
        
class Markup:
    ''' A Markup is a way to add data to a grid.  It is associated with
        a particular grid.
        
        In this case, each cell can have a single object associated with it.
        
        Subclasses could have other stuff, of course
    '''
    
    def __init__(self, grid, default=' '):
        self.grid = grid
        self.marks = {}  # Key: cell, Value = some object
        self.default = default
        
    def reset(self):
        self.marks = {}
        
    def __setitem__(self, cell, value):
        self.marks[cell] = value
        
    def __getitem__(self, cell):
        return self.marks.get(cell, self.default)
        
    def set_item_at(self, row, column, value):
        assert row >= 0 and row < self.grid.num_rows
        assert column >= 0 and column < self.grid.num_columns
        cell = self.grid.cell_at(row, column)
        if cell:
            self.marks[cell]=value
        else:
            raise IndexError
    
    def get_item_at(self, row, column):
        assert row >= 0 and row < self.grid.num_rows
        assert column >= 0 and column < self.grid.num_columns
        cell = self.grid.cell_at(row, column)
        if cell:
            return self.marks.get(cell)
        else:
            raise IndexError
            
    def max(self):
        ''' Return the cell with the largest markup value. '''
        return max(self.marks.keys(), key=self.__getitem__)

    def min(self):
        ''' Return the cell with the largest markup value. '''
        return min(self.marks.keys(), key=self.__getitem__)

class DijkstraMarkup(Markup):
    ''' A markup class that will run Djikstra's algorithm and keep track
        of the distance values for each cell.
    '''

    def __init__(self, grid, root_cell, default=0):
        ''' Execute the algorithm and store each cell's value in self.marks[]
        '''
        super().__init__(grid, default)
        pass
            
    def farthest_cell(self):
        ''' Find the cell with the largest markup value, which will
            be the one farthest away from the root_call.
            
            Returns: Tuple of (cell, distance)
        '''
        pass

class ShortestPathMarkup(DijkstraMarkup):
    ''' Given a starting cell and a goal cell, create a Markup that will
        have the shortest path between those two cells marked.  
    '''

    def __init__(self, grid, start_cell, goal_cell, 
                 path_marker='*', non_path_marker=' '):
        super().__init__(grid, start_cell)
        
        pass

class LongestPathMarkup(ShortestPathMarkup):
    ''' Create a markup with the longest path in the graph marked.
        Note: Shortest path is dependent upon the start and target cells chosen.
              This markup is the longest path to be found _anywhere_ in the maze.
    '''

    def __init__(self, grid, path_marker='*', non_path_marker=' '):
        start_cell = grid.random_cell()
        dm = DijkstraMarkup(grid, start_cell)
        farthest, _ = dm.farthest_cell()
        dm = DijkstraMarkup(grid, farthest)
        next_farthest, _ = dm.farthest_cell()   
        super().__init__(grid, farthest, next_farthest, path_marker, non_path_marker)

class ColorizedMarkup(Markup):
    ''' Markup a maze with various colors.  Each value in the markup is
        an RGB triplet.
    '''

    def __init__(self, grid, channel='R'):
        assert channel in 'RGB'
        super().__init__(grid)
        self.channel = channel
        
    def colorize_dijkstra(self, start_row = None, start_column = None):
        ''' Provide colors for the maze based on their distance from
            some cell.  By default, from the center cell.
        '''
        if not start_row:
            start_row = self.grid.num_rows // 2
        if not start_column:
            start_column = self.grid.num_columns // 2
        start_cell = self.grid.cell_at(start_row, start_column)
        dm = DijkstraMarkup(self.grid, start_cell)
        self.intensity_colorize(dm)
                
    def intensity_colorize(self, markup):
        ''' Given a markup of numeric values, colorize based on
            the relationship to the max numeric value.
        '''
        max = markup.max()
        max_value = markup[max]
        for c in self.grid.each_cell():
            cell_value = markup[c]
            intensity = (max_value - cell_value) / max_value
            dark   = round(255 * intensity)
            bright = round(127 * intensity) + 128
            if self.channel == 'R':
                self.marks[c] = [bright, dark, dark]
            elif self.channel == 'G':
                self.marks[c] = [dark, bright, dark]
            else:
                self.marks[c] = [dark, dark, bright]   
                                       
def binary_tree(grid):
    ''' The Binary Tree Algorithm.
      
        This algorithm works by visiting each cell and randomly choosing
        to link it to the cell to the east or the cell to the north.
        If there is no cell to the east, then always link to the north
        If there is no cell to the north, then always link to the east.
        Except if there are no cells to the north or east (in which case
        don't link it to anything.)
    '''
    i=grid.num_rows-1
    j=0
    while(i>=0):
        j=0
        while(j<=grid.num_columns-1):
            #if grid.cell_at(i,j).north==None:
            if i==0 and j==grid.num_columns-1:
                print()
            elif i==0:
                grid.cell_at(i,j).link(grid.cell_at(i,j+1))
            #if grid.cell_at(i,j).east==None:
            elif j==grid.num_columns-1:
                grid.cell_at(i,j).link(grid.cell_at(i-1,j))
            else:
                r=random.randint(0,1)
                if r==0:
                    #grid.cell_at(i,j).link(grid.cell_at(i-1,j))
                    grid.cell_at(i,j).unlink(grid.cell_at(i,j+1))
                if r==1:
                    #grid.cell_at(i,j).link(grid.cell_at(i,j+1))
                    grid.cell_at(i,j).unlink(grid.cell_at(i-1,j))
            j=j+1
        i=i-1


    print("finish binary")

            
def sidewinder(grid, odds=.5):
    ''' The Sidewinder algorithm.
    
        Considers each row, one at a time.
        For each row, start with the cell on the west end and an empty list 
        (the run).  Append the cell to the run list.
        Choose a random number between 0 and 1.  If it is greater 
        than the odds parameter, then add the eastern cell to the run list and
        link it to the current cell.  That eastern cell then becomes the 
        current cell.
        If the random number was less than the odds parameter, then you are
        done with the run.  Choose one of the cells in the run and link it to 
        the cell to the north.
        
        Be careful, these instructions don't cover the cases where the row
        is the northernmost one (which will need to be a single, linked run) 
        or for cells at the far east (which automatically close the run)
    '''
    assert odds >= 0.0
    assert odds < 1.0 
    i=grid.num_rows-1
    while(i>=1):
        j=0
        run=[]
        while(j<=grid.num_columns-1):
            r=random.randrange(0,10,1)/10
            if(r<=odds and j!=grid.num_columns-1):
                run.append(grid.cell_at(i,j))
            else:
                run.append(grid.cell_at(i,j))
                r1=random.randrange(0,len(run))
                for a in range(len(run)):
                    if(j!=grid.num_columns-1):
                        run[a].link(run[a].east)
                    if a!=r1:
                        run[a].unlink(run[a].north)
                    else:
                        run[a].link(run[a].north)

                if run[len(run)-1].column != grid.num_columns - 1:
                    run[len(run)-1].unlink(run[len(run)-1].east)
                #if run[len(run)-1].column != 0:
                 #   run[0].unlink(run[0].west)
                
                run[r1].link(run[r1].north)
                run.clear()

            j=j+1
        i=i-1
    print("finish sidewinder")
                
def aldous_broder(grid):
    ''' The Aldous-Broder algorithm is a random-walk algorithm.
    
        Start in a random cell.  Choose a random direction.  If the cell
        in that direction has not been visited yet, link the two cells.
        Otherwise, don't link.
        Move to that randomly chosen cell, regardless of whether it was
        linked or not.
        Continue until all cells have been visited.
    '''
    grid.unlink_all()
    linked_cells={}
    iteration_count=0
    r1=random.randrange(0,grid.num_rows)
    r2=random.randrange(0,grid.num_columns)
    next_cell=grid.cell_at(r1,r2)
    while(len(linked_cells)<=grid.size()):
        iteration_count=iteration_count+1
        if(len(linked_cells)==grid.size()):
            break
        if(linked_cells.get(next_cell,1)==1):
            linked_cells[next_cell]=next_cell
        print(next_cell)
        ct=True
        if ct:
            
            again=True
            while(again==True):
                
                r=random.randint(1,4)
                cell=next_cell
                again=False
                if(r==1 and cell.north!=None):
                    if(linked_cells.get(cell.north,1)==1):
                            cell.link(cell.north)
                    #else:
                    #        cell.unlink(cell.north)
                    next_cell=cell.north
                elif(r==2 and cell.south!=None):
                    if(linked_cells.get(cell.south,1)==1):
                            cell.link(cell.south)
                    #else:
                    #        cell.unlink(cell.south)
                    next_cell=cell.south
                elif(r==3 and cell.east!=None):
                    if(linked_cells.get(cell.east,1)==1):
                            cell.link(cell.east)
                    #else:
                    #        cell.unlink(cell.east)
                    next_cell=cell.east
                elif(r==4 and cell.west!=None):
                    if(linked_cells.get(cell.west,1)==1):
                            cell.link(cell.west)
                    #else:
                    #       cell.unlink(cell.west)
                    next_cell=cell.west
                else:
                    again=True




    print(f'Aldous-Broder executed on a grid of size {grid.size()} in {iteration_count} steps.')
    
def wilson(grid):
    ''' Wilson's algorithm is a random-walk algorithm.
    
        1) Choose a random cell.  Mark it visited.
        2) Choose a random unvisited cell (note, this will necessarily not be the 
          same cell from step 1).  Perform a "loop-erased" random walk until
          running into a visited cell.  The cells chosen during this random
          walk are not yet marked as visited.
        3) Add the path from step 2 to the maze.  Mark all of the cells as visited.
          Connect all the cells from the path, one to each other, and to the 
          already-visited cell it ran into.
        4) Repeat steps 2 and 3 until all cells are visited.
        
        Great.  But, what is a "loop-erased" random walk?  At each step, one 
        random neighbor gets added to the path (which is kept track
        of in order).  Then, check if the neighbor is already in the path.  If 
        so, then the entire loop is removed from the path.  So, if the 
        path consisted of cells at locations (0,0), (0,1), (0,2), (1,2), (1,3),
        (2,3), (2,2), and the random neighbor is (1,2), then there is a loop.
        Chop the path back to (0,0), (0,1), (0,2), (1,2) and continue 
        
        BTW, it  may be easier to manage a  list of unvisited cells, which 
        makes it simpler to choose a random unvisited cell, for instance.   
    '''
    unvisited=[]
    visited=[]
    random_choices=0
    loops_removed=0
    grid.unlink_all()
 
    for i in range(grid.num_rows):
        for j in range(grid.num_columns):
            unvisited.append(grid.cell_at(i,j))
        
    a=random.choice(unvisited)
    unvisited.remove(a)
    visited.append(a)
    while(len(visited)<=grid.size()):
        if len(visited)==grid.size():
            break
        start=random.choice(unvisited)
        path=[]
        i=0
        path.append(start)
        q=False
        while q==False:
            i=i+1
            redo=True
            while(redo==True):
                r = random.randint(1,4)
                random_choices=random_choices+1
                temp=path[i-1]
                redo=False
                if(r==1 and temp.north != None):
                    path.append(temp.north)
                elif(r==2 and temp.south != None):
                    path.append(temp.south)
                elif(r==3 and temp.east != None):
                    path.append(temp.east)
                elif(r==4 and temp.west != None):
                    path.append(temp.west)
                else:
                    redo=True
            for t in range(len(path)):
                    if path[t]==path[i]:
                        for m in range(t+1,i+1):
                            del path[t+1]
                        i=t
                        loops_removed=loops_removed+1
                        break
            for item in visited:
                if path[i]==item:
                    q=True
                    break
        for t in range(0,len(path)-1):
            visited.append(path[t])
            unvisited.remove(path[t])
            path[t].link(path[t+1])


                 
    print(f'Wilson executed on a grid of size {grid.size()} with {random_choices}', end='')
    print(f' random cells choosen and {loops_removed} loops removed')


          
def recursive_backtracker(grid, start_cell=None):
    ''' Recursive Backtracker is a high-river maze algorithm.
    
        1) if start_cell is None, choose a random cell for the start
        2) Examine all neighbors and make a list of those that have not been visited
           Note: you can tell it hasn't been visited if it is not linked to any cell
        3) Randomly choose one of the cells from this list.  Link to and move to that 
           neighbor
        3a) If there are no neighbors in the list, then you must backtrack to the last
            cell you visited and repeat.
            
        Suggestion: Use an explicit stack.  You can write this implicitly (in fact,
        the code will be quite short), but for large mazes you will be making lots of 
        function calls and you risk running out of stack space.
    '''
    stack=[]
    visited=[]
    if start_cell==None:
        start_cell=grid.random_cell()
    i=0
    stack.append(start_cell)
    visited.append(start_cell)
    grid.unlink_all()
    while(len(visited)<=grid.size()):
        if len(visited)==grid.size():
            break
        #redo=True
        print("this loop:{0}".format(stack[i]))
        #判断四周是否被占用
        N,S,E,W=False,False,False,False
 
        for item in visited:
                if stack[i].north == item or stack[i].north==None:
                    N=True
                    continue
                if stack[i].south == item or stack[i].south==None:
                    S=True
                    continue
                if stack[i].east == item or stack[i].east==None:
                    E=True
                    continue
                if stack[i].west == item or stack[i].west==None:
                    W=True
                    continue
        if N==True and S==True and E==True and W==True:
            print("popped stack{0}".format(stack[i]))
            stack.pop(i)                    
            i=len(stack)-1
            print("now last of order stack{0}".format(stack[i]))

            continue

        #随机选择一个方向(以判断占用）
        #while(redo==True):
        #redo=False
        r=random.randint(1,4)
        i=len(stack)-1
        if(r==1 and stack[i].north!=None and N==False):
            stack.append(stack[i].north)
            visited.append(stack[i].north)
            stack[i].link(stack[i].north)
        elif(r==2 and stack[i].south!=None and S==False):
            stack.append(stack[i].south)
            visited.append(stack[i].south)
            stack[i].link(stack[i].south)
        elif(r==3 and stack[i].east!=None and E==False):
            stack.append(stack[i].east)
            visited.append(stack[i].east)
            stack[i].link(stack[i].east)
        elif(r==4 and stack[i].west!=None and W==False):
            stack.append(stack[i].west)
            visited.append(stack[i].west)
            stack[i].link(stack[i].west)
        elif(N==True and S==True and E==True and W==True):
            print("error")

        i=len(stack)-1
    print("finish")

