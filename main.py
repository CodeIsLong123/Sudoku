
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Line
import numpy as np
import random

def solve_board(board):
    find = find_empty(board)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1,10):
        if valid(board, i, (row, col)):
            board[row][col] = i

            if solve_board(board):
                return True     

            board[row][col] = 0

    return False

def valid(bo, num, pos):
    # Check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if bo[i][j] == num and (i,j) != pos:
                return False

    return True

def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  
    return None

def boardi(num_cells_to_fill):  #
    while True:
        # Generate a random first row
        first_row = random.sample(range(1, 10), 9)
        
        # Create the initial board with the first row and empty cells
        board = [first_row] + [[0 for _ in range(9)] for _ in range(8)]
        
        # Try to solve the board
        if solve_board(board):
            # If solvable, remove numbers to create the puzzle
            cells = [(i, j) for i in range(9) for j in range(9)]
            for _ in range(81 - num_cells_to_fill):
                cell = random.choice(cells)
                cells.remove(cell)
                board[cell[0]][cell[1]] = 0
            
            return board  

def create_random_board(diff):
        
        if diff == "Easy": 

            return boardi(35)
            
        elif diff == "Medium":
            return boardi(25)
        
        elif diff == "Hard":
            return boardi(17)
                    
        else: 
            raise Exception("This is not a valid Input")
            
    
    
    

class SudokuCell(Button):
    def __init__(self, is_base=False, is_occupied = False, **kwargs):
        super(SudokuCell, self).__init__(**kwargs)
        self.font_name = 'Arial'
        self.font_size = '20sp'
        self.background_normal = ''
        self.background_color = [0.9, 0.9, 0.9, 1]
        self.color = [0, 0, 0, 1]  # Black color for all numbers
        self.is_base = is_base
        self.is_occupied = is_occupied
        self.update_font()

    def update_font(self):
        if self.is_base:
            self.bold = True
            self.font_size = '25sp'  
        else:
            self.bold = False
            self.font_size = '20sp'
            

class SudokuGrid(GridLayout):
    def __init__(self, **kwargs):
        super(SudokuGrid, self).__init__(**kwargs)
        self.cols = 9
        self.cells = []
        self.cell = set()
        self.selected_cell = None
        self.spacing = [2, 2]
        self.board = self.generate_valid_board("Hard")
        self.player_input = []

        with self.canvas.before:
            Color(0.7, 0.7, 0.7, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        for i in range(9):
            for j in range(9):
                value = self.board[i][j]
                is_base = value != 0
                cell = SudokuCell(text=str(value) if value != 0 else '', is_base=is_base)
                if not is_base:
                    cell.bind(on_press=self.cell_pressed)
                self.cells.append(cell)
                self.add_widget(cell)
        
        Window.bind(on_key_down=self.on_keyboard_down)
    def generate_valid_board(self, difficulty):
        board = create_random_board(difficulty)
        if board is None:
            print("Failed to generate a valid board. Retrying...")
            return self.generate_valid_board(difficulty)
        return board
    
    def on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        
        print(keycode)
        if self.selected_cell and not self.selected_cell.is_base:
            if text and text in '123456789':
                    
                self.selected_cell.text = text
                row, col = self.cells.index(self.selected_cell) // 9, self.cells.index(self.selected_cell) % 9
                print(row, col)
                self.board[row][col] = int(text)
                self.selected_cell.is_occupied = True

            elif keycode == 42:  # Use keycode[1] for string representation
                self.selected_cell.text = ''
                row, col = self.cells.index(self.selected_cell) // 9, self.cells.index(self.selected_cell) % 9
                self.board[row][col] = 0
                
                self.selected_cell.is_occupied = False
        print(self.player_input)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        self._draw_grid_lines()

    def _draw_grid_lines(self):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.7, 0.7, 0.7, 1)
            Rectangle(size=self.size, pos=self.pos)
            Color(0, 0, 0, 1)
            for i in range(1, 3):
                Line(points=[self.x + i * self.width / 3, self.y, self.x + i * self.width / 3, self.top], width=2)
                Line(points=[self.x, self.y + i * self.height / 3, self.right, self.y + i * self.height / 3], width=2)

    def cell_pressed(self, instance):
        if self.selected_cell:
            self.selected_cell.background_color = [0.9, 0.9, 0.9, 1]
        self.selected_cell = instance
        instance.background_color = [0.8, 0.8, 1, 1]

    def show_solution(self):
        if solve_board(self.board):
            for i, cell in enumerate(self.cells):
                row, col = i // 9, i % 9
                
                cell.text = str(self.board[row][col])
        else:
            print("No solution exists")

                
        
    

class SudokuGame(BoxLayout):
    def __init__(self, **kwargs):
        super(SudokuGame, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = 10

        self.add_widget(Label(text='Sudoku', font_size='30sp', size_hint_y=None, height=50))
        self.grid = SudokuGrid(size_hint_y=0.9)
        self.add_widget(self.grid)
        self.add_widget(Button(text='New Game', size_hint_y=None, height=50, on_press=self.new_game))
        self.add_widget(Button(text='Show solution', size_hint_y=None, height=50, on_press=self.show_solution))

    def new_game(self, instance):
        # Here you would implement logic to generate a new Sudoku puzzle
        for cell in self.grid.cells:
            if not cell.is_base:
                cell.text = ''
            

    def show_solution(self, instance):
        self.grid.show_solution()

class SudokuApp(App):
    def build(self):
        return SudokuGame()

if __name__ == '__main__':
    SudokuApp().run()
    # print(create_random_board("Easy"))
    # create_random_board("Easy")
    
    