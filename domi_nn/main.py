import numpy as np
import os
import matplotlib.pyplot as plt
import pygame
import sys
import button

weight_input_to_hidden1 = np.load(os.path.join(os.path.dirname(os.path.abspath(__file__)),"Data/weight_ith1.npy"))
weight_hidden2_to_output = np.load(os.path.join(os.path.dirname(os.path.abspath(__file__)),"Data/weight_h2to.npy"))
weight_hidden1_to_hidden2 = np.load(os.path.join(os.path.dirname(os.path.abspath(__file__)),"Data/weight_h1th2.npy"))

bias_input_to_hidden1= np.load(os.path.join(os.path.dirname(os.path.abspath(__file__)),"Data/bias_ith1.npy"))
bias_hidden2_to_output = np.load(os.path.join(os.path.dirname(os.path.abspath(__file__)),"Data/bias_h2to.npy"))
bias_hidden1_to_hidden2 = np.load(os.path.join(os.path.dirname(os.path.abspath(__file__)),"Data/bias_h1th2.npy"))
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

pygame.init()

screen = pygame.display.set_mode((1200, 800))
screen.fill((230, 230, 230))

draw_area = pygame.Rect(400, 0, 800, 800) 
grid_surface = pygame.Surface((28, 28)) # NEW: create a new surface for drawing the grid
grid_surface.fill((0, 0, 0)) # NEW: fill the grid surface with white color

def clear_screen():
    grid_surface.fill((0, 0, 0)) # NEW: fill the grid surface with white color
    screen.blit(pygame.transform.scale(grid_surface, (abs(800), abs(800))), draw_area) # NEW: blit the scaled grid surface onto the screen
    pygame.display.update(draw_area) # CHANGED: update only the drawing area

clear_screen()

def check_number():
    global grid_surface
    screen.fill ((230, 230, 230), (0, 300, 300, 500)) # очищает область под кнопками
    grid_surface = pygame.transform.flip(grid_surface, False, True)
    grid_surface = pygame.transform.rotate(grid_surface, 270)
    screen.blit(pygame.transform.scale(grid_surface, (abs(800), abs(800))), draw_area) # NEW: blit the scaled grid surface onto the screen
    image = pygame.surfarray.array3d(grid_surface) # NEW: use the grid surface as the image array
    image = np.mean(image, axis=2) # Усреднение цветов по каналам
    image = image / 255 # Нормализация значений от 0 до 1
    image = np.reshape(image, (-1, 1)) # Изменение формы массива для подачи в нейронную сеть

      #Forward propagation
    hidden1_raw = bias_input_to_hidden1 + weight_input_to_hidden1 @ image
    hidden1 = sigmoid(hidden1_raw)

    hidden2_raw = bias_hidden1_to_hidden2 + weight_hidden1_to_hidden2 @ hidden1
    hidden2 = sigmoid(hidden2_raw)

    output_raw = bias_hidden2_to_output + weight_hidden2_to_output @ hidden2
    output = sigmoid(output_raw)
    number = output.argmax()
    print(output)
    print(f"NN suggest, the number is: {number}")
    grid_surface = pygame.transform.flip(grid_surface, False, True)
    grid_surface = pygame.transform.rotate(grid_surface, 270)
    screen.blit(pygame.transform.scale(grid_surface, (abs(800), abs(800))), draw_area) # NEW: blit the scaled grid surface onto the screen


     # NEW: create and display the number surface
    number_font = pygame.font.SysFont('Arial', 50)
    number_surface = number_font.render(str(number), True, (0, 0, 0))
    number_rect = number_surface.get_rect()
    number_rect.center = (150, 400)
    screen.blit(number_surface, number_rect)

while True:
    for event in pygame.event.get():
        pygame.display.flip()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        left_button = pygame.mouse.get_pressed()[0]
         # Если мышь нажата, установить mouse_pressed в True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pressed = True
        # Если мышь отпущена, установить mouse_pressed в False
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pressed = False
        # Если мышь нажата и движется, закрашивать клетки
        if left_button:
        # Получение координат курсора
            x, y = pygame.mouse.get_pos()
            if draw_area.collidepoint(x, y): 
                grid_x = (x - draw_area.x) // 29
                grid_y = (y - draw_area.y) // 29
                # NEW: draw a black rectangle on the grid surface
                #pygame.draw.rect(grid_surface, (255, 255, 255), (grid_x, grid_y, 1, 1))
                # NEW: blit the scaled grid surface onto the scree
                # Задать разные оттенки серого для разных клеток
                white = (255, 255, 255)
                light_grey = (200, 200, 200)
                dark_grey = (100, 100, 100)
        
                # Нажатая клетка становится белой
                pygame.draw.rect(grid_surface, white, (grid_x, grid_y, 1, 1))
        
                # Две клетки, которые выше и левее, становятся светло-серыми
                pygame.draw.rect(grid_surface, white, (grid_x - 1, grid_y, 1, 1))
                pygame.draw.rect(grid_surface, white, (grid_x, grid_y - 1, 1, 1))
                pygame.draw.rect(grid_surface, white, (grid_x, grid_y + 1, 1, 1))
                pygame.draw.rect(grid_surface, white, (grid_x + 1, grid_y, 1, 1))

                if grid_surface.get_at((grid_x - 1, grid_y - 1)) != (255, 255, 255):        
                    # Клетка, которая левее второй или выше третьей, становится темно-серой
                    pygame.draw.rect(grid_surface, dark_grey, (grid_x - 1, grid_y - 1, 1, 1))
                    pygame.draw.rect(grid_surface, light_grey, (grid_x - 1, grid_y + 1, 1, 1))
                pygame.draw.rect(grid_surface, light_grey, (grid_x + 1, grid_y - 1, 1, 1))
                screen.blit(pygame.transform.scale(grid_surface, (800, 800)), draw_area)
        clear_button = button.Button(50, 50, 200, 100, (255, 255, 255), (200, 200, 200), "Очистить", clear_screen)
        check_button = button.Button(50, 200, 200, 100, (255, 255, 255), (200, 200, 200), "Проверить", check_number)
        clear_button.handle_event(event) 
        check_button.handle_event(event) # Обработка событий для кнопки
        clear_button.draw(screen)
        check_button.draw(screen)
        pygame.display.flip()
