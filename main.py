import os
import sys
import pygame

pygame.init()
pygame.display.set_caption('X|')
size = width, height = 800, 800
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
fps = 60
show_menu = True


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def print_txt(message, x, y, font_clr=(255, 255, 255), font_t=None, font_size=30):
    font_type = pygame.font.SysFont(font_t, font_size)
    txt = font_type.render(message, True, font_clr)
    screen.blit(txt, (x, y))


class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.act_clr = (30, 30, 30)
        self.inact_clr = (0, 0, 0)

    def draw(self, x, y, message, font_size=30):
        self.x = x
        self.y = y
        mouse = pygame.mouse.get_pos()
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(screen, self.act_clr, (x, y, self.width, self.height))
        else:
            pygame.draw.rect(screen, self.inact_clr, (x, y, self.width, self.height))

        print_txt(message, x + 10, y + 10, font_size=font_size)

    def click(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height and click[0] == 1:
            pygame.draw.rect(screen, self.inact_clr, (self.x, self.y, self.width, self.height))
            return True
        return False


def menu():
    intro_text = ["Правила игры:"]
    start_button = Button(185, 50)
    quit_button = Button(185, 50)
    show_menu = True
    fon = pygame.transform.scale(load_image('menu_bkgrd.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 400
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while show_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        start_button.draw(190, 200, 'Start', 50)
        quit_button.draw(190, 260, 'Exit', 50)
        if start_button.click():
            return
        if quit_button.click():
            pygame.quit()
            quit()
        clock.tick(fps)
        pygame.display.flip()


def end_game():
    quit_button = Button(90, 50)
    go_to_menu = Button(212, 50)
    ending = True
    while ending:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.fill((105, 105, 105))
        go_to_menu.draw(294, 375, 'Go to Menu', 50)
        quit_button.draw(355, 445, 'Exit', 50)
        if go_to_menu.click():
            return
        if quit_button.click():
            pygame.quit()
            quit()
        clock.tick(fps)
        pygame.display.flip()


game_run = True
while game_run:
    menu()
    end_button = Button(100, 50)
    back_menu = Button(100, 50)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.fill((74, 74, 74))
        back_menu.draw(10, 10, 'Back', 49)
        end_button.draw(690, 10, 'End', 50)
        if back_menu.click():
            menu()
        if end_button.click():
            running = False
        clock.tick(fps)
        pygame.display.flip()
    end_game()