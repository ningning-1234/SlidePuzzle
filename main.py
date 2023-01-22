import random

import pygame

run = True

pygame.init()
pygame.font.init()

WIN_SIZE = 500
WIN_WIDTH = WIN_SIZE
WIN_HEIGHT = WIN_SIZE
window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

clock = pygame.time.Clock()
FPS = 60
# x = 17
# if(x > 15 and x < 20):
#     print('test')
BG_COLOR = pygame.color.Color('0x505050')

class Slide():
    def __init__(self, image, pos, size):
        self.full_image = image
        self.pos = pos
        self.size = size
        self.image = pygame.Surface((self.size, self.size))
        self.image.blit(self.full_image, (-self.pos[0], -self.pos[1]))
        self.empty = False
        self.hover = False
        self.next_to_empty = False
        self.grid_pos = (int(self.pos[0] / self.size), int(self.pos[1] / self.size))
        self.correct_grid_pos = self.grid_pos

    def __str__(self):
        return 'slide at ' + str(self.grid_pos)

    def check_next_to_empty(self):
        grid_posx = self.grid_pos[0]
        grid_posy = self.grid_pos[1]
        if (grid_posx != len(slide_lst)-1):
            if (slide_lst[grid_posx+1][grid_posy].empty == True):
                return slide_lst[grid_posx + 1][grid_posy]
        if (grid_posy != len(slide_lst)-1):
            if (slide_lst[grid_posx][grid_posy+1].empty == True):
                return slide_lst[grid_posx][grid_posy + 1]
        if (grid_posx != 0):
            if (slide_lst[grid_posx-1][grid_posy].empty == True):
                return slide_lst[grid_posx - 1][grid_posy]
        if (grid_posy != 0):
            if (slide_lst[grid_posx][grid_posy-1].empty == True):
                return slide_lst[grid_posx][grid_posy - 1]
        return self

    def swap(self, slide):
        pos = self.pos
        self.pos = slide.pos
        slide.pos = pos
        slide_lst[self.grid_pos[0]][self.grid_pos[1]] = slide
        slide_lst[slide.grid_pos[0]][slide.grid_pos[1]] = self
        self.grid_pos = (int(self.pos[0] / self.size), int(self.pos[1] / self.size))
        slide.grid_pos = (int(slide.pos[0] / slide.size), int(slide.pos[1] / slide.size))

        # todo
        #  Change where the slide is in the slide lst.
        #  Grid_pos is the same index in the slide lst.

    def draw(self, surface):
        # draw blue border
        if(self.empty == True):
            pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(self.pos[0], self.pos[1], self.size, self.size))
        else:
            pygame.draw.rect(self.image, (0, 0, 0), pygame.Rect(0, 0, self.size, self.size), 2)
            if (self.hover):
                pygame.draw.rect(self.image, (125, 125, 125), pygame.Rect(0, 0, self.size, self.size), 2)
            surface.blit(self.image, self.pos)

def create_puzzle(image, size):
    global puzzle_size
    puzzle_size = size
    img = pygame.image.load('assets/' + image + '.png')
    global slide_size
    slide_size = WIN_SIZE / puzzle_size
    global new_image
    new_image = pygame.transform.scale(img, (WIN_SIZE, WIN_SIZE))
    global slide_lst
    slide_lst = []
    for x in range(0, puzzle_size):
        x_lst = []
        slide_lst.append(x_lst)
        for y in range(0, puzzle_size):
            slide = Slide(new_image, (x * slide_size, y * slide_size), slide_size)
            if (x == 0 and y == 0):
                slide.empty = True
            x_lst.append(slide)
    global hover
    hover = get_slide_from_coords((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))

def check_puzzle_completed():
    for x in range(0, puzzle_size):
        for y in range(0, puzzle_size):
            if(slide_lst[x][y].grid_pos != slide_lst[x][y].correct_grid_pos):
                return False
    return True

def get_slide_from_coords(coord):
    x = int(coord[0] / slide_size)
    if(x<0 or x>puzzle_size-1):
        x=0
    y = int(coord[1] / slide_size)
    if(y<0 or y>puzzle_size-1):
        y=0
    # for x in range(0, PUZZLE_SIZE):
    #     for y in range(0, PUZZLE_SIZE):
    #         slide_x = slide_lst[x][y].pos[0]
    #         slide_y = slide_lst[x][y].pos[1]
    #         if (slide_x < coord[0] and slide_x + SLIDE_SIZE > coord[0]):
    #             if (slide_y < coord[1] and slide_y + SLIDE_SIZE > coord[1]):
    #                 return slide_lst[x][y]
    return slide_lst[x][y]

def scramble(lst, scramble_amount):
    previous_slide = None
    empty_slide = lst[0][0]
    for g in range(0, scramble_amount):
        swap_lst = []
        if (empty_slide.grid_pos[0] != 0):
            swap_lst.append(lst[empty_slide.grid_pos[0] - 1][empty_slide.grid_pos[1]])
        if (empty_slide.grid_pos[1] != 0):
            swap_lst.append(lst[empty_slide.grid_pos[0]][empty_slide.grid_pos[1] - 1])
        if (empty_slide.grid_pos[0] != len(lst) - 1):
            swap_lst.append(lst[empty_slide.grid_pos[0] + 1][empty_slide.grid_pos[1]])
        if (empty_slide.grid_pos[1] != len(lst) - 1):
            swap_lst.append(lst[empty_slide.grid_pos[0]][empty_slide.grid_pos[1] + 1])
        random_slide = random.randint(0, len(swap_lst)-1)
        empty_slide.swap(swap_lst[random_slide])
    '''
    while(scramble_amount != 0):
        slide = lst[random.randint(0, PUZZLE_SIZE-1)][random.randint(0, PUZZLE_SIZE-1)]
        if slide.check_next_to_empty() != slide and previous_slide != slide:
            previous_slide = slide
            slide.swap(slide.check_next_to_empty())
            scramble_amount = scramble_amount - 1
        print(scramble_amount)
    '''

move_counter = 0
game_run = False
start_button = pygame.Rect(200, 225, 100, 50)
bowser_slide = pygame.Rect(50, 125, 100, 100)
cuphead_slide = pygame.Rect(50, 275, 100, 100)
puzzle_size_3 = pygame.Rect(350, 125, 100, 50)
puzzle_size_4 = pygame.Rect(350, 225, 100, 50)
puzzle_size_5 = pygame.Rect(350, 325, 100, 50)
img = 'Bowser_Slide'
size = 4

def press_button(button):
    if pygame.mouse.get_pos()[0] > button[0] \
            and pygame.mouse.get_pos()[1] > button[1] \
            and pygame.mouse.get_pos()[0] < button[0] + button[2] \
            and pygame.mouse.get_pos()[1] < button[1] + button[3]:
        return True
    return False

while (run):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            if game_run == True:
                slide = get_slide_from_coords((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
                if slide.check_next_to_empty() != slide:
                    slide.swap(slide.check_next_to_empty())
                    move_counter = move_counter + 1
                    print(check_puzzle_completed())
            else:
                if press_button(bowser_slide) == True:
                    img = 'Bowser_Slide'
                if press_button(cuphead_slide) == True:
                    img = 'Cuphead_Slide'
                if press_button(puzzle_size_3) == True:
                    size = 3
                if press_button(puzzle_size_4) == True:
                    size = 4
                if press_button(puzzle_size_5) == True:
                    size = 5
                if press_button(start_button) == True:
                    create_puzzle(img, size)
                    scramble(slide_lst, 500)
                    game_run = True

    if game_run == True:
        hover.hover = False
        get_slide_from_coords((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])).hover = True
        hover = get_slide_from_coords((pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))

    '''
    for x in range(0, PUZZLE_SIZE):
        for y in range(0, PUZZLE_SIZE):
            slide_x = slide_lst[x][y].pos[0]
            slide_y = slide_lst[x][y].pos[1]
            if (slide_x < mouse_x and slide_x + SLIDE_SIZE > mouse_x):
                if (slide_y < mouse_y and slide_y + SLIDE_SIZE > mouse_y):
                    slide_lst[x][y].hover = True
                else:
                    slide_lst[x][y].hover = False
            else:
                slide_lst[x][y].hover = False
            if (slide_x < mouse_x and slide_x + SLIDE_SIZE > mouse_x):
                if (slide_y < mouse_y and slide_y + SLIDE_SIZE > mouse_y and pygame.mouse.get_pressed()[0] == True):
                    if (slide_lst[x][y].check_next_to_empty() != slide_lst[x][y]):
                        slide_lst[x][y].swap(slide_lst[x][y].check_next_to_empty())
                    #print(str(slide_lst[x][y]) + ' Next to empty slide ' + str(temp_var))
                    print(check_puzzle_completed())
    '''
    # if(completed_puzzle == slide_lst):
    #     print('Completed')

    #_____Draw_____
    window.fill(BG_COLOR)
    if game_run == True:
        for s in slide_lst:
            for x in s:
                x.draw(window)

        if check_puzzle_completed() == True:
            game_over_font = pygame.font.Font('freesansbold.ttf', 32)
            text = game_over_font.render('Game Over', False, (150, 150, 150))
            window.blit(text, (WIN_WIDTH / 2 - 75, WIN_HEIGHT / 2 - 20))

        move_counter_amount = pygame.font.Font('freesansbold.ttf', 32)
        text = move_counter_amount.render(str(move_counter), False, (150, 150, 150))
        window.blit(text, (0, 0))
    else:
        pygame.draw.rect(window, (175, 175, 175), start_button)
        start_button_text = pygame.font.Font('freesansbold.ttf', 32)
        text = start_button_text.render(('Start'), False, (125, 125, 125))
        window.blit(text, start_button)

        new_img = pygame.transform.scale(pygame.image.load('assets/Bowser_Slide.png'), (100, 100))
        window.blit(new_img, bowser_slide)
        new_img = pygame.transform.scale(pygame.image.load('assets/Cuphead_Slide.png'), (100, 100))
        window.blit(new_img, cuphead_slide)

        pygame.draw.rect(window, (175, 175, 175), puzzle_size_3)
        puzzle_size_3_text = pygame.font.Font('freesansbold.ttf', 32)
        text = puzzle_size_3_text.render(('3'), False, (125, 125, 125))
        window.blit(text,puzzle_size_3)
        pygame.draw.rect(window, (175, 175, 175), puzzle_size_4)
        puzzle_size_4_text = pygame.font.Font('freesansbold.ttf', 32)
        text = puzzle_size_3_text.render(('4'), False, (125, 125, 125))
        window.blit(text,puzzle_size_4)
        pygame.draw.rect(window, (175, 175, 175), puzzle_size_5)
        puzzle_size_5_text = pygame.font.Font('freesansbold.ttf', 32)
        text = puzzle_size_3_text.render(('5'), False, (125, 125, 125))
        window.blit(text,puzzle_size_5)

    pygame.display.flip()
    clock.tick(FPS)
