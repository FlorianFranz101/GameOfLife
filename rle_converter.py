import numpy as np
def read_board_from_string(board):
    board = remove_comments(board)
    lines = board.split("\n")
    lines = list(filter(lambda a: a!="", lines))
    sizex = int(lines[0].split(",")[0].replace("x", "").replace("=", "").strip())
    sizey = int(lines[0].split(",")[1].replace("y", "").replace("=", "").strip())
    lines = lines[1:]
    cells = np.zeros((sizey, sizex))
    current_number = ""
    x_index = 0
    y_index = 0
    for line in lines:
        for c in line:
            if(c.isdigit()):
                current_number += c
            else:
                if(current_number != ""):
                    if(c == "b"):
                        set_cells(cells, 0, x_index, y_index, y_index+int(current_number))
                    if(c == "o"):
                        set_cells(cells, 1, x_index, y_index, y_index+int(current_number))
                    y_index+=int(current_number)
                    current_number = ""
                    continue
                else:
                    if(c == "b"):
                        cells[x_index][y_index] = 0
                        y_index+=1
                    if(c == "o"):
                        cells[x_index][y_index] = 1
                        y_index+=1
                    if(c == "$"):
                        x_index+=1
                        y_index= 0
                    if(c == "!"):
                        return cells
    
#def convert_board_to_string(board):
def set_cells(cells, value, line, from_y, to_y):
    for i in range(len(cells[line])):
        if(i>= from_y and i<=to_y):
            cells[line][i] = value

def remove_comments(board):
    reading_comment = False
    out_lp = ""
    for char in board:
        if(char == "#"):
            reading_comment = True
            continue
        if(char =="\n"):
            reading_comment = False
            out_lp+="\n"
            continue
        if(not reading_comment):
            out_lp += char
    return out_lp
def convert_board_to_string(board):
    maxr, maxc = board.shape
    out = "x = {} , y = {}\n".format(maxc, maxr)
    print(out)
    current_count = 0
    current_status = 0
    for r in range(len(board)):
        for c in range(len(board[r])):
            if(current_status != board[r][c]):
                if(current_count > 1):
                    out+=str(current_count)
                out+=get_symbol_from_int(current_status)
                current_count = 0
            current_status = board[r][c]
            current_count +=1
        if(current_count > 1):
            out+=str(current_count)
        out+=get_symbol_from_int(current_status)
        current_count = 0
        out+="$"
    return out+"!"
def get_symbol_from_int(number):
    if(number == 0):
        return "b"
    else:
        return "o"