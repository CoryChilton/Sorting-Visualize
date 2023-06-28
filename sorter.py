#at 39:46
from asyncio import wait_for
from heapq import merge
import pygame
import random
import math
pygame.init()

class DrawInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BLUE = 0, 0, 255
    BACKGROUND_COLOR = WHITE

    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    FONT = pygame.font.SysFont('arial', 20)
    LARGE_FONT = pygame.font.SysFont('arial', 30)

    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Sorting Algorithm Visualization')
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2

def draw(draw_info, algo_name, ascending, n):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.GREEN)
    draw_info.window.blit(title, ((draw_info.width/2 - title.get_width()/2, 5)))

    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
    draw_info.window.blit(controls, ((draw_info.width/2 - controls.get_width()/2, 40)))

    sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort | M - Merge Sort | Q - Quick Sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, ((draw_info.width/2 - sorting.get_width()/2, 100)))

    numBars = draw_info.FONT.render(f"Number of Bars: {n} | N - Change Number of Bars to {100 if n == 50 else 50}", 1, draw_info.BLACK)
    draw_info.window.blit(numBars, ((draw_info.width/2 - numBars.get_width()/2, 70)))

    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info, color_positions = {}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, 
                        draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)


    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

    if clear_bg:
        pygame.display.update()

def generate_starting_list(n, min_val, max_val):
    lst = []
    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)
    
    return lst

def bubble_sort(draw_info, ascending = True):
    lst = draw_info.lst
    print(ascending)
    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                yield True
    return lst

def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break
            
            lst[i] = lst[i-1]
            i = i - 1
            lst[i] = current
            draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
            yield True

    return lst

def merge_sort(draw_info, ascending=True):
    lst = draw_info.lst
    width = 1
    n = len(lst)
    while (width < n):
        l = 0
        while l < n:
            r = min(l + (width * 2 - 1), n - 1)
            m = min(l + width - 1, n - 1)

            #merging
            n1 = m - l + 1
            n2 = r - m
            L = [0] * n1
            R = [0] * n2
            for i in range(0, n1):
                L[i] = lst[l + i]
            for i in range(0, n2):
                R[i] = lst[m + i + 1]
        
            i, j, k = 0, 0, l
            while i < n1 and j < n2:
                if (L[i] <= R[j] and ascending) or (L[i] >= R[j] and not ascending):
                    lst[k] = L[i]
                    i += 1
                else:
                    lst[k] = R[j]
                    j += 1
                k += 1
                draw_list(draw_info, {k: draw_info.GREEN}, True)
                yield True
        
            while i < n1:
                lst[k] = L[i]
                i += 1
                k += 1
                draw_list(draw_info, {k: draw_info.GREEN}, True)
                yield True
        
            while j < n2:
                lst[k] = R[j]
                j += 1
                k += 1
                draw_list(draw_info, {k: draw_info.GREEN}, True)
                yield True
            #end merging

            l += width * 2
        width *= 2
    return lst

def quick_sort(draw_info, ascending=True):
    lst = draw_info.lst
    
    size = len(lst)
    stack = [0] * (size)
  
    # initialize top of stack
    top = -1
  
    # push initial values of l and r to stack
    top = top + 1
    stack[top] = 0
    top = top + 1
    stack[top] = len(lst) - 1
  
    # Keep popping from stack while is not empty
    while top >= 0:
  
        # Pop r and l
        r = stack[top]
        top = top - 1
        l = stack[top]
        top = top - 1

        #partition
        i = ( l - 1 )
        x = lst[r]
    
        for j in range(l, r):
            draw_list(draw_info, {j: draw_info.GREEN, i: draw_info.RED, r: draw_info.BLUE}, True)
            yield True
            if (lst[j] <= x and ascending) or (lst[j] >= x and not ascending):
                i = i + 1
                lst[i], lst[j] = lst[j], lst[i]

    
        lst[i + 1], lst[r] = lst[r], lst[i + 1]
        draw_list(draw_info, {r: draw_info.GREEN, i: draw_info.RED}, True)
        yield True
        p = i + 1
  
        # If there are elements on left side of pivot,
        # then push left side to stack
        if p-1 > l:
            top = top + 1
            stack[top] = l
            top = top + 1
            stack[top] = p - 1
  
        # If there are elements on right side of pivot,
        # then push right side to stack
        if p + 1 < r:
            top = top + 1
            stack[top] = p + 1
            top = top + 1
            stack[top] = r

    return lst

def main():
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(800, 600, lst)
    sorting = False
    ascending = True

    sorting_algorithm = quick_sort
    sorting_algo_name = "Quick Sort"
    sorting_algorithm_generator = None

    while run:
        clock.tick(60)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending, n)


        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_n:
                n = 100 if n == 50 else 50
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and not sorting:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"
            elif event.key == pygame.K_m and not sorting:
                sorting_algorithm = merge_sort
                sorting_algo_name = "Merge Sort"
            elif event.key == pygame.K_q and not sorting:
                sorting_algorithm = quick_sort
                sorting_algo_name = "Quick Sort"
            

    
    pygame.quit()
        
if __name__ == "__main__":
    main()
