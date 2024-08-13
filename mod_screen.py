import tkinter as tk
import numpy as np

class GameScreen():
    def __init__(self, number_of_dots) -> None:
        self.number_of_dots = number_of_dots    #in a row and in a column
        self.board_size = self.number_of_dots*100
        self.window = tk.Tk()
        self.window.title("Game of Dots")
        self.canvas = tk.Canvas(self.window, width=self.board_size, height=self.board_size)
        self.canvas.pack()
        # self.window.bind("<Button-1>", self.click)

        self.distance_between_dots = self.board_size / self.number_of_dots
        self.dot_size = self.distance_between_dots / 10

        self.line_width = 10
        self.line_marked_width = 20

        self.create_board()
        self.new_game()

    def create_board(self):
        for i in range(self.number_of_dots):
            self.canvas.create_line([0,self.distance_between_dots*(i+0.5)], 
                                    [self.board_size,self.distance_between_dots*(i+0.5)], 
                                    fill="black")
            self.canvas.create_line([self.distance_between_dots*(i+0.5),0], 
                                    [self.distance_between_dots*(i+0.5),self.board_size], 
                                    fill="black")
        self.refresh_dots()
        
    def refresh_dots(self):
        for i in range(self.number_of_dots):
            for j in range(self.number_of_dots):
                self.canvas.create_oval([self.distance_between_dots*(i+0.5)-self.dot_size,self.distance_between_dots*(j+0.5)-self.dot_size], 
                                    [self.distance_between_dots*(i+0.5)+self.dot_size,self.distance_between_dots*(j+0.5)+self.dot_size], 
                                    fill="blue")
                
    def new_game(self):
        self.board_status = np.zeros(shape=(self.number_of_dots-1, self.number_of_dots-1))
        self.board_rows = np.zeros(shape=(self.number_of_dots, self.number_of_dots-1))
        self.board_columns = np.zeros(shape=(self.number_of_dots-1, self.number_of_dots))
        self.canvas.delete("all")
        self.create_board()

    def mark_line(self, grid_xy, type, player_line_color):
        L = 0.5*self.distance_between_dots
        if type == "row":
            # x_sr=dist_betw_dots(1+i) || y_sr=dis_betw_dots*(0.5+j)
            x = self.distance_between_dots*(1+grid_xy[1])
            y = self.distance_between_dots*(0.5+grid_xy[0])
            self.canvas.create_line([x-L,y], [x+L,y], fill=player_line_color, width=5)
        elif type == "col":
            # column:  x_mid = dist_betw_dots(0.5+i) || y_mid = dis_betw_dots*(1+j)
            x = self.distance_between_dots*(0.5+grid_xy[1])
            y = self.distance_between_dots*(1+grid_xy[0])
            self.canvas.create_line([x,y-L], [x,y+L], fill=player_line_color, width=5)