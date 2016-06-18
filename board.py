from utils import *


class Board():

    def __init__(self, surf, dimensions, cell_size, start_point):
        self.surf = surf
        self.data = []
        self.cell_size = cell_size
        self.start_point = start_point
        self.dimensions = dimensions
        for y in range(dimensions[1]):
            row = []
            self.data.append(row)
            for x in range(dimensions[0]):
                row.append((0,0,0))

    def draw(self, cells, colour, stamp=False):
        for cell in cells:
            x = self.start_point[0] + cell[0] * self.cell_size
            y = self.start_point[1] + cell[1] * self.cell_size
            self.surf.fill(colour, (x,y,self.cell_size,self.cell_size))
            if stamp:
                self.data[cell[1]][cell[0]] = colour

    def can_place(self, cells):
        for cell in cells:
            if cell[0]<0 or cell[1]==self.dimensions[1] or cell[0]==self.dimensions[0]:
                return False
            try:
                if not(self.data[cell[1]][cell[0]]==(0,0,0)):
                    return False
            except:
                pass
        return True

    def check_lines(self):
        rows_to_remove=[]
        for row_no in range(len(self.data)):
            if not((0,0,0) in self.data[row_no]):
                rows_to_remove.append(row_no)
        if len(rows_to_remove)>0:
            self.remove_rows(rows_to_remove)
            self.update_board()

    def remove_rows(self, rows_to_remove):
        new_data = []
        for row in rows_to_remove:
            row = []
            new_data.append(row)
            for x in range(self.dimensions[0]):
                row.append((0, 0, 0))
        for row_no in range(self.dimensions[1]):
            if not(row_no in rows_to_remove):
                new_data.append(self.data[row_no])
        self.data = new_data

    def update_board(self):
        self.surf.fill((0,0,0), (0, 0, self.dimensions[0]*self.cell_size, self.dimensions[1]*self.cell_size))
        for y, row in enumerate(self.data):
            for x,cell in enumerate(row):
                self.draw([(x,y)], cell)
