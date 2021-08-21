import pygame as pg
import random
 
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]
 
Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]
 
I = [['.....',
      '0000.',
      '.....',
      '.....',
      '.....'],
     ['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....']]
 
O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]
 
J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]
 
L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]
 
T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

pg.init()
pg.mixer.init()

width, height = 600, 700
play_width, play_height = 300, 600
play_start_width, play_start_height = int((width - play_width)/2), int((height - play_height)/2) 
block_size = int(play_width/10)

window = pg.display.set_mode((width,height))
pg.display.toggle_fullscreen()
pg.display.set_caption("Tetris")
icon = pg.image.load("tetris_game\\tetris icon.jpg")
pg.display.set_icon(icon)

pg.mixer.music.load("tetris_game\\Tetris 99 - Main Theme.mp3")
pg.mixer.music.set_volume(0.04)
pg.mixer.music.play(-1)

single = pg.mixer.Sound("tetris_game\\Nintendo Switch - Tetris 99 - General Sounds\\General Sounds\\se_game_single.wav")
tetris_sound = pg.mixer.Sound("tetris_game\\Nintendo Switch - Tetris 99 - General Sounds\\General Sounds\\se_game_tetris.wav")
single.set_volume(0.08)
tetris_sound.set_volume(0.03)

WHITE = (255,255,255)
BLUE = (0,0,255)
RED = (255,0,0)
YELLOW = (255, 255, 0)
BLACK = (0,0,0)
PURPLE = (255,0,255)
GREEN = (0,255,0)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
 
shapes = [S, Z, I, O, J, L, T]
shape_colors = [GREEN, RED, CYAN, YELLOW, ORANGE, BLUE, PURPLE]
grid = [[(0,0,0) for i in range(10)] for i in range(20)] # j, i is rows and columns : for the colors on the grid
all_stagnant_rects = []
game_running = True
score = 0

def grid_index(x_pos, y_pos):
    row = int((x_pos - play_start_width)/block_size)
    column = int((y_pos - play_start_height)/block_size) # 2*play_start_height + play_height = height
    return row, column

def grid_coordinates(row, column):
    x_cor = int(row*block_size) + play_start_width
    y_cor = int(column * block_size) + play_start_height
    return x_cor, y_cor

def draw_static_board():
    window.fill(BLACK)
    pg.font.init()
    font = pg.font.SysFont("Verdana", 40)
    smallfont = pg.font.SysFont("Verdana", 20)
    label = font.render("TETRIS", 1, (255,255,255))
    window.blit(label, (int((width - label.get_width())/2), 2))

    next_label = font.render("Next:", 1, (255,255,255))
    window.blit(next_label, (int(play_start_width + play_width + block_size/2), int(play_start_height + block_size)))
    
    hold_label = smallfont.render("HOLD:", 1, (255,255,255))
    window.blit(hold_label, (int(play_start_width/2 - hold_label.get_width()/2), int(play_start_height + block_size/2)))

    pg.draw.rect(window, WHITE, (0,0,width,height),4)
    pg.draw.rect(window, WHITE, (play_start_width,play_start_height,play_width,play_height),4)
    pg.draw.rect(window, WHITE, (450,play_start_height,play_start_width-10,int(height/2)),4)
    pg.draw.rect(window, WHITE, (10,play_start_height,play_start_width-10,150),4)

def show_next(shape):
    rect_coor = []
    for x, line in enumerate(shape[0]):
        for y, value in enumerate(line):
            if value == "0":
                rect_coor.append((y,x))

    for i, m in enumerate(rect_coor):
        my_rect = pg.Rect(int(play_start_width + play_width + m[0]*block_size), int(2*play_start_height + m[1]*block_size), block_size, block_size)
        pg.draw.rect(window, shape_colors[shapes.index(shape)], my_rect)

def draw_board():
    for i in range(len(grid)):
        pg.draw.line(window, WHITE, (play_start_width, int((block_size*i)+play_start_height)), (play_width + play_start_width, int((block_size*i)+play_start_height)), 2) # rows
    for i in grid:
        for j in range(len(i)):
            pg.draw.line(window, WHITE, (int((block_size*j)+play_start_width), play_start_height), (block_size*j + play_start_width, int(play_height + play_start_height)), 2) # columns

def get_piece():
    return random.choice(shapes)

def text_to_shape(shape_list, rotation, x_inc, y_inc):
    rect_coor = []
    for x, line in enumerate(shape_list[rotation % len(shape_list)]):
        for y, value in enumerate(line):
            if value == "0":
                rect_coor.append((y,x)) # gets location in list of blocks

    rects = []
    for i, m in enumerate(rect_coor):
        my_rect = pg.Rect(play_start_width + (m[0] + 3 + x_inc)*block_size, play_start_height + (m[1] - 2 + y_inc)*block_size, block_size, block_size)
        rects.append(my_rect) # converted location in list to location on screen

    total_rects = len(rects)

    allowed, stop_order = allowed_positions(rects)

    if len(allowed) == total_rects and not stop_order: # no errors, free to move
        draw_shape(rects, shape_list, rect_coor)
        return True, rects
    elif len(allowed) != total_rects and not stop_order: # fixes error encountered in main()
        return False, rects
    elif stop_order: # stops movement
        stuck_positions()
        return None, rects

def draw_shape(rects, shape_list, positions):
    x_values = []
    y_values = []
    for i in positions:
        x_values.append(i[0])
        y_values.append(i[1])
    for i in rects:
        pg.draw.rect(window, shape_colors[shapes.index(shape_list)], i)

def allowed_positions(rects, x_inc = 0, y_inc = 0):
    possible_bool = []
    stop_order = False
    for rect in rects:
        rows, columns = grid_index(rect.x + x_inc * block_size, rect.y + y_inc * block_size)
        if play_start_width <= rect.x + x_inc * block_size < play_start_width + play_width:
            if play_start_height <= rect.y + y_inc * block_size < play_height + play_start_height:
                if grid[columns][rows] == BLACK:
                    possible_bool.append(True)
                else:
                    stop_order = True
    
    return possible_bool, stop_order

def grid_update(rects, shape_list):
    try:
        if allowed_positions(rects):
            for rect in (rects):
                row, column = grid_index(rect.x, rect.y)
                grid[column][row] = shape_colors[shapes.index(shape_list)] # updates grid in right position and color
    except IndexError:
        print("An error was encountered due to too many inputs")

def stuck_positions():
    for i, column in enumerate(grid):
        for j, row in enumerate(column):
            if grid[i][j] != BLACK:
                x_cor, y_cor = grid_coordinates(j, i)
                stagnant_rect = pg.Rect(x_cor, y_cor, block_size, block_size)
                all_stagnant_rects.append(stagnant_rect)
                pg.draw.rect(window, grid[i][j], stagnant_rect)

def clear_rows():
    global score
    color_list = []
    filled_colors = 0
    row_cleared = []

    for i, row in enumerate(grid): # i is the column
        min_x_useless, min_y = grid_coordinates(0, i)
        color_list.append(row)
        for x in color_list:
            for y in x:
                if y != BLACK:
                    filled_colors += 1
        if filled_colors == 10:
            for z in range(filled_colors):
                grid[i][z] = BLACK
            row_cleared.append(i)

        filled_colors = 0
        color_list.clear()# Makes rows Black

    for i, row in enumerate(grid): # moves rows down
        if i in row_cleared:
            if len(row_cleared) < 4:
                single.play()
                score += 100
            else:
                tetris_sound.play()
                score += 800
            for x in range(i-1):
                for n in range(10):
                    grid[i-x][n] = grid[i-x-1][n]
                    grid[i-x-1][n] = BLACK
   
    row_cleared.clear()

def show_hold(shape):
    if shape == None:
        return
    rect_coor = []
    for x, line in enumerate(shape[0]):
        for y, value in enumerate(line):
            if value == "0":
                rect_coor.append((y,x))

    for i, m in enumerate(rect_coor):
        my_rect = pg.Rect(int(play_start_width/8 + m[0]*block_size), int(3*play_start_height/2 + m[1]*block_size), block_size, block_size)
        pg.draw.rect(window, shape_colors[shapes.index(shape)], my_rect)

def lose_screen():
    pg.mixer.music.pause()
    pg.mixer.music.load("tetris_game\\Nintendo Switch - Tetris 99 - General Sounds\General Sounds\me_game_gameover.wav")
    pg.mixer.music.set_volume(0.05)
    pg.mixer.music.play()
    global game_running, score
    while not game_running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
    
        window.fill(BLACK)

        pg.font.init()
        font = pg.font.SysFont("Verdana", 40)
        label = font.render("YOU LOSE", 1, (255,255,255))
        window.blit(label, (int((width - label.get_width())/2), int(height/2 - label.get_height()/2)))
        score_label = font.render(f"Score: {score}", 1, (255,255,255))
        window.blit(score_label, (int((width - label.get_width())/2), int(height/2 - label.get_height()/2 + 2*play_start_height)))

        pg.display.update()
        
def main():
    global game_running, score
    clock = pg.time.Clock()
    clock.tick(60)

    current_piece = get_piece()
    next_piece = get_piece()
    held_piece = None
    hold_piece_count = 1
    held = False
    change_piece = False

    fall_time = 0
    collisions = 0
    fall_speed = 500
    fall_y = 0
    horizontal_movement = 0
    rotation = 0

    while game_running:
        fall_time += clock.get_rawtime()
        clock.tick()

        if collisions >= 17: # increase collisions to make it easier
            fall_speed /= 2
            collisions = 0

        if change_piece:
            collisions += 1
            score += 10
            current_piece = next_piece
            next_piece = get_piece()
            hold_piece_count = 1

        for rect in all_stagnant_rects:
            if rect.y <= play_start_height + block_size:
                game_running = False
                all_stagnant_rects.clear()
                horizontal_movement = 0
                fall_y = 0
                fall_time = 0
                rotation = 0

        change_piece = False
        attached = False

        draw_static_board()

        show_next(next_piece)
        show_hold(held_piece)

        stuck_positions()

        confirmation, rects = text_to_shape(current_piece, rotation, horizontal_movement, fall_y)

        if confirmation == None:
            attached = True
            for rect in rects:
                rect.y -= block_size
            grid_update(rects, current_piece)
            horizontal_movement = 0
            fall_y = 0
            rotation = 0
            change_piece = True
            continue

        if not confirmation:
            for rect in rects:
                if rect.x > 9*block_size + play_start_width:
                    horizontal_movement -= 1
                    break
                elif rect.x < play_start_width:
                    horizontal_movement += 1
                    break
            confirmation, rects = text_to_shape(current_piece, rotation, horizontal_movement, fall_y)


        draw_board()

        y_values = []
        if not attached:
            for rect in rects:
                if rect.y >= 620:
                    y_values.append(False)

        if fall_time >= fall_speed:
            if len(y_values) == 0 and not attached:
                fall_time = 0
                fall_y += 1
            else: 
                grid_update(rects, current_piece)
                horizontal_movement = 0
                fall_y = 0
                rotation = 0
                change_piece = True

        

        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_running = False
                quit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    game_running = False
                    quit()

                elif event.key == pg.K_a or event.key == pg.K_LEFT:
                    grid_coors = []
                    move = 0
                    for rect in rects:
                        rows, columns = grid_index(rect.x, rect.y)
                        grid_coors.append((rows, columns))
                    for coordinates in (grid_coors):
                        if grid[coordinates[1]][coordinates[0] - 1] == BLACK:
                            move += 1
                    if move == 4:
                        horizontal_movement -= 1

                elif event.key == pg.K_d or event.key == pg.K_RIGHT:
                    grid_coors = []
                    move = 0
                    for rect in rects:
                        rows, columns = grid_index(rect.x, rect.y)
                        grid_coors.append((rows, columns))
                    for coordinates in (grid_coors):
                        try:
                            if grid[coordinates[1]][coordinates[0] + 1] == BLACK:
                                move += 1
                        except IndexError:
                            move = -5   
                    if move == 4:
                        horizontal_movement += 1

                elif event.key == pg.K_s or event.key == pg.K_DOWN:
                    grid_coors = []
                    move = 0
                    for rect in rects:
                        rows, columns = grid_index(rect.x, rect.y)
                        grid_coors.append((rows, columns))
                    for coordinates in (grid_coors):
                        try:
                            if grid[coordinates[1] + 1][coordinates[0]] == BLACK:
                                move += 1
                        except IndexError:
                            move = -5   
                    if move == 4:
                        if len(y_values) == 0:
                            fall_y += 1
                
                elif event.key == pg.K_w or event.key == pg.K_UP:
                    rect_coor = []
                    for x, line in enumerate(current_piece[(rotation + 1) % len(current_piece)]):
                        for y, value in enumerate(line):
                            if value == "0":
                                rect_coor.append((y,x))
                    rects_more = []
                    for i, m in enumerate(rect_coor):
                        my_rect = pg.Rect(play_start_width + (m[0] + 3 + horizontal_movement)*block_size, play_start_height + (m[1] - 2 + fall_y)*block_size, block_size, block_size)
                        rects_more.append(my_rect)

                    grid_coors = []
                    move = 0
                    for rect in rects:
                        rows, columns = grid_index(rect.x, rect.y)
                        grid_coors.append((rows, columns))
                    for coordinates in (grid_coors):
                        try:
                            if grid[coordinates[1]][coordinates[0]] == BLACK:
                                move += 1
                        except IndexError:
                            move = -5   
                    if move == 4:
                        rotation += 1
                
                elif event.key == pg.K_e:
                    held = True
                    if hold_piece_count == 1:
                        if held_piece == None:
                            held_piece = current_piece
                            change_piece = True
                            fall_y = 0
                            horizontal_movement = 0
                            rotation = 0
                            fall_time = 0
                        else:
                            intermediate = held_piece
                            held_piece = current_piece
                            current_piece = intermediate
                            fall_y = 0
                            horizontal_movement = 0
                            rotation = 0
                            fall_time = 0
                        hold_piece_count = 0

                elif event.key == pg.K_SPACE:
                    distance = (19 - fall_y)
                    fall_y += distance

        clear_rows()

        pg.display.update()

main()
lose_screen()
pg.quit()