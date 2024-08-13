import tkinter as tk
import mod_screen
import mod_coordinates
import numpy as np

class Dots():
    def __init__(self) -> None:
        self.number_of_dots = 3
        self.game = mod_screen.GameScreen(self.number_of_dots)
        self.game.window.bind("<Button-1>", self.click)
                # self.window.bind("<Button-1>", self.click)
        self.player_A = 1
        self.player_B = -1
        self.current_player = self.player_A
        self.score_player_A = 0
        self.score_player_B = 0
        # self.current_player_id = self.game.canvas.create_text([10,10], tags="current_player", 
        #                                                       font="cmr 15 bold", fill="black", text=" ")
        
        self.player_line_color = [0, "green", "red"]

        # self.score_text_id = self.game.canvas.create_text([0.5*self.game.board_size,10], tags="score", 
        #                                                   font="cmr 15 bold", fill="black", text=" ")

        self.game_over = False

        self.print_starting_message()
        # mod_coordinates.print_col_row_indices(self.game)

    def mainloop(self):
        self.game.window.mainloop()

    def click(self, event):
        # self.game.canvas.create_line(event.x, event.y, self.game.board_size/2,self.game.board_size/2)
        pixel_xy = np.array([event.x, event.y])
        # Detect which row or column has been clicked. If neither has been clicked, do nothing, wait for more clicks
        grid_xy, type = mod_coordinates.convert_pixel_to_grid(self.game, pixel_xy)
        if self.game_over == False:
            if type:                #checks if the player clicked on an area recognized as a line
                #updates arrays row and column 
                if not mod_coordinates.is_board_colrow_occupied(self.game, grid_xy, type):
                    mod_coordinates.update_board_colrow(self.game, grid_xy, type, self.current_player)
                    self.game.mark_line(grid_xy, type, self.player_line_color[self.current_player])

                    mod_coordinates.update_board_status(self.game)
                    self.print_score()

                    self.print_current_player()
                    self.change_player()
                    if self.is_game_over():
                        self.print_game_over()
                        self.game_over = True
        else:
            self.restart_game()

    def restart_game(self):
        self.game.new_game()
        self.game_over = False
        self.score_player_A = 0
        self.score_player_B = 0
        self.print_starting_message()

    def print_starting_message(self):
        self.current_player_id = self.game.canvas.create_text([10,10], tags="current_player", 
                                                              font="cmr 15 bold", fill="black", text="current player: A")
        score_text = "Player A   " + str(0) + " : " + str(0) + "   Player B"
        self.score_text_id = self.game.canvas.create_text([0.5*self.game.board_size,10], tags="score", 
                                                          font="cmr 15 bold", fill="black", text=score_text)

    def print_current_player(self):
        text_player = ["current player: ", "A", "B"]
        self.game.canvas.itemconfig(tagOrId="current_player", text=text_player[0]+text_player[self.current_player])
        
    def change_player(self):
        self.current_player *= -1

    def print_score(self):
        self.score_player_A = np.sum(self.game.board_status[:,:]==1)
        self.score_player_B = np.sum(self.game.board_status[:,:]==-1)
        score_text = "Player A   " + str(self.score_player_A) + ":" + str(self.score_player_B) + "   Player B"
        self.game.canvas.itemconfig(tagOrId="score", text=score_text)

    def is_game_over(self):
        if np.sum(self.game.board_rows==0) == 0 and np.sum(self.game.board_columns==0) == 0:
            return True
        else:
            return False

    def print_game_over(self):
        self.game.canvas.delete(self.score_text_id)
        self.game.canvas.delete(self.current_player_id)
        text_final_score = str(self.score_player_A) + ":" + str(self.score_player_B)
        if self.score_player_A > self.score_player_B:
            text_winner_is = "Player A wins!" 
        elif self.score_player_A < self.score_player_B:
            text_winner_is = "Player B wins!"
        elif self.score_player_A == self.score_player_B:
            text_winner_is = "Its a tie!"
        self.game.canvas.create_text([0.5*self.game.board_size,100], tags="score", 
                                    font="cmr 15 bold", fill="black", text=text_winner_is)
        self.game.canvas.create_text([0.5*self.game.board_size,130], tags="score", 
                                    font="cmr 15 bold", fill="black", text=text_final_score)
        self.game.canvas.create_text([0.5*self.game.board_size,160], tags="score", 
                                    font="cmr 15 bold", fill="black", text="(Click to play again)")