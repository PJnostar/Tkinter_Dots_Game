import numpy as np
import mod_screen
#----------------------------------------------------------------------------------------------------------
#------------------------------------Position functions----------------------------------------------------
#----------------------------------------------------------------------------------------------------------

#   pixel_xy are xy coordinates in pixels (where players click on the screen)
#   grid_xy are xy coordinates in (0,1,2) values corresponding to row or columns in the game
def convert_pixel_to_grid(game_screen: mod_screen.GameScreen, pixel_xy: np.array):
    grid_xy = np.zeros(shape=(2))
    type = False
    L1 = game_screen.distance_between_dots/3
    L2 = game_screen.distance_between_dots/6
    #   Detect row
    """ srodek row:    x_mid = dist_betw_dots(1+i) || y_mid = dis_betw_dots*(0.5+j)
                   i = (x_sr-dist_betw_dots)/dist_betw_dots = x_sr/dist_betw_dots - 1
                   j = (y_sr-0.5*dist_betw_dots)/dist_betw_dots = y_sr/dist_betw_dots - 0.5
        if      x_sr - L < x < x_sr + L 
        and     y_sr - L < y < y_sr + L
        then    x,y -> i,j
    """
    for r in range(game_screen.board_rows.shape[0]):
        for c in range(game_screen.board_rows.shape[1]):
            x_center_rc = game_screen.distance_between_dots*(1+c)
            y_center_rc = game_screen.distance_between_dots*(0.5+r)
            if x_center_rc - L1 < pixel_xy[0] < x_center_rc + L1 and y_center_rc - L2 < pixel_xy[1] < y_center_rc + L2 :
                grid_xy = [r, c]
                type = "row"
                # print("grid_xy: ", grid_xy, type)
    
    #Detect column
    """ 
    middle column:  x_mid = dist_betw_dots(0.5+i) || y_mid = dis_betw_dots*(1+j)
    """
    for r in range(game_screen.board_columns.shape[0]):
        for c in range(game_screen.board_columns.shape[1]):
            x_center_rc = game_screen.distance_between_dots*(0.5+c)
            y_center_rc = game_screen.distance_between_dots*(1+r)
            if x_center_rc - L2 < pixel_xy[0] < x_center_rc + L2 and y_center_rc - L1 < pixel_xy[1] < y_center_rc + L1 :
                grid_xy = [r, c]
                type = "col"
                # print("grid_xy: ", grid_xy, type)
    return grid_xy, type

#This function takes the array board_column or row_column and updates its value, depending on a player
def update_board_colrow(game_screen: mod_screen.GameScreen, grid_xy: np.array, type, player):
    if type == "row":
        game_screen.board_rows[grid_xy[0], grid_xy[1]] = player
    elif type == "col":
        game_screen.board_columns[grid_xy[0], grid_xy[1]] = player

#This function return True (False) if board_column or board_row had (hadnt) already been marked
def is_board_colrow_occupied(game_screen: mod_screen.GameScreen, grid_xy: np.array, type):
    if type == "row":
        if game_screen.board_rows[grid_xy[0], grid_xy[1]] != 0:
            return True
        else:
            return False
    elif type == "col":
        if game_screen.board_columns[grid_xy[0], grid_xy[1]] != 0:
            return True
        else:
            return False


#This function looks for boxes marked by a single player and saves them in a list
def update_board_status(gs: mod_screen.GameScreen):
    """  
    board 00:       board 01:       board rc:
    b_up = 00       b_up = 01       b_up = r c
    b_down = 10     b_down = 11     b_down = r+1 c
    b_left = 00     b_left = 01     b_left = r c
    b_right = 01    b_right = 02    b_right = r c+1
    """
    for r in range(gs.number_of_dots-1):
       for c in range(gs.number_of_dots-1):
            u = [r,c]       #these are indexes of a box
            d = [r+1,c]
            l = [r,c]
            ri = [r,c+1]
            if gs.board_rows[u[0],u[1]] == 1 and gs.board_rows[d[0],d[1]] == 1 and gs.board_columns[l[0],l[1]] == 1 and gs.board_columns[ri[0],ri[1]] == 1:
                x0 = gs.distance_between_dots*(1+c)
                y0 = gs.distance_between_dots*(1+r)
                L = 0.5*gs.distance_between_dots
                gs.canvas.create_rectangle([x0-L,y0-L], [x0+L,y0+L], fill="#90EE90")
                gs.board_status[r,c] = 1
            elif gs.board_rows[u[0],u[1]] == -1 and gs.board_rows[d[0],d[1]] == -1 and gs.board_columns[l[0],l[1]] == -1 and gs.board_columns[ri[0],ri[1]] == -1:
                x0 = gs.distance_between_dots*(1+c)
                y0 = gs.distance_between_dots*(1+r)
                L = 0.5*gs.distance_between_dots
                gs.canvas.create_rectangle([x0-L,y0-L], [x0+L,y0+L], fill="#FF7F7F")
                gs.board_status[r,c] = -1
    gs.refresh_dots()
    
#Helper funtion to understand board_status and boxes logic
def print_col_row_indices(game_screen: mod_screen.GameScreen):
    for r in range(game_screen.board_rows.shape[0]):
        for c in range(game_screen.board_rows.shape[1]):
            x_rc = game_screen.distance_between_dots*(1+c)
            y_rc = game_screen.distance_between_dots*(0.5+r)
            game_screen.canvas.create_text([x_rc, y_rc], text=str(r)+str(c), font="cmr 7 bold", fill="black")
    for r in range(game_screen.board_columns.shape[0]):
        for c in range(game_screen.board_columns.shape[1]):
            x_rc = game_screen.distance_between_dots*(0.5+c)
            y_rc = game_screen.distance_between_dots*(1+r)
            game_screen.canvas.create_text([x_rc, y_rc], text=str(r)+str(c), font="cmr 7 bold", fill="black")