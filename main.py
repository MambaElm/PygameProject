import os
import sys
import pygame
import csv

pygame.init()
pygame.display.set_caption('X|')
size = width, height = 800, 800
elem_size = 65  # указать размеры для элементов
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
fps = 60
show_menu = True
visible_sprites = pygame.sprite.Group()  ## все видимые спрайты
invisible_sprites = pygame.sprite.Group()  ## в этой группе всех элементов по 1, вероятно можно использоать в шкафу
elements, reactions = {}, {}  ## словарь элементов по номерам
tile_width = tile_height = 50


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


class Closet:
    def __init__(self, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y
        self.name_all_el = []
        self.elem = pygame.sprite.Group()
        for i in range(1, 5):
            Element(self.elem, 60 + (elem_size + 10) * (len(self.elem) // 2) + self.x,
                    10 + (elem_size + 15) * (len(self.elem) % 2) + self.y, str(i))
            self.name_all_el.append(str(i))
        self.color = (130, 130, 130)
        self.color_fon_elem = (100, 100, 100)
        self.width = (len(self.elem) // 2 + len(self.elem) % 2) * (elem_size + 15) + 5
        self.height = (elem_size + 15) * 2 + 5
        self.rect = pygame.Rect(self.x, self.y, self.width + 100, self.height)
        self.left_button = Button(50, self.height)
        self.right_button = Button(50, self.height)

    def draw(self, canvas):
        pygame.draw.rect(canvas, self.color, (self.x, self.y, self.width + 100, self.height))
        for i, el in enumerate(self.elem):
            pygame.draw.rect(canvas, self.color_fon_elem,
                             (60 + (elem_size + 10) * (i // 2) + self.x, 10 + (elem_size + 10) * (i % 2) + self.y,
                              elem_size + 5, elem_size + 5))
        self.elem.draw(canvas)
        self.left_button.draw(0, self.y, '***')
        if self.width + 50 < 750:
            self.right_button.draw(self.width + 50, self.y, '***')
        else:
            self.right_button.draw(750, self.y - 10, '***')

    def scroll(self):
        if self.right_button.click() and self.x > 800 - self.width:
            self.x -= 200 / fps
            for i, el in enumerate(self.elem):
                el.rect.x = 60 + (elem_size + 10) * (i // 2) + self.x
                el.rect.y = 10 + (elem_size + 15) * (i % 2) + self.y
        if self.left_button.click() and self.x < 0:
            self.x += 200 / fps
            for i, el in enumerate(self.elem):
                el.rect.x = 60 + (elem_size + 10) * (i // 2) + self.x
                el.rect.y = 10 + (elem_size + 15) * (i % 2) + self.y

    def new_elem(self, element):
        self.name_all_el.append(element.name)
        Element(self.elem, 60 + (elem_size + 10) * (len(self.elem) // 2) + self.x,
                10 + (elem_size + 15) * (len(self.elem) % 2) + self.y, element.name)
        self.width = (len(self.elem) // 2 + len(self.elem) % 2) * (elem_size + 15) + 5


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
        print_txt(f'Вот твой результат:{len(closet.elem)})  <3 Спасибо *_*', 20, 100)
        if go_to_menu.click():
            for s in visible_sprites:
                s.kill()
            closet.name_all_el = []
            closet.elem = pygame.sprite.Group()
            for i in range(1, 5):
                Element(closet.elem, 60 + (elem_size + 10) * (len(closet.elem) // 2) + closet.x,
                        10 + (elem_size + 15) * (len(closet.elem) % 2) + closet.y, str(i))
                closet.name_all_el.append(str(i))
            return
        if quit_button.click():
            pygame.quit()
            quit()
        clock.tick(fps)
        pygame.display.flip()


class Element(pygame.sprite.Sprite):  ##  класс элемента
    def __init__(self, group, pos_x, pos_y, name):
        super().__init__(group)
        self.name = str(name)
        self.image = load_image(self.name + '.png')
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.md = False

    def mdn(self, xy, cl):
        if self.md:
            a = pygame.sprite.spritecollideany(self, visible_sprites)
            x, y = xy
            if a:
                for i in [a]:
                    if (i.name, self.name) in reactions and i != self:
                        inv_to_v(elements[reactions[(i.name, self.name)]], x, y)
                        if elements[reactions[(i.name, self.name)]].name not in cl.name_all_el:
                            cl.new_elem(elements[reactions[(i.name, self.name)]])
                        visible_sprites.remove(i, self)
        self.md = False

    def update(self, xy):
        self.md = self.rect.collidepoint(xy)

    def get_elem(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            inv_to_v(self, self.rect.x, self.rect.y - 200)


def inv_to_v(elem, pos_x, pos_y):  ## создание видимого спрайта, по номеру и желаемому положению
    visible_sprites.add(Element(invisible_sprites, pos_x, pos_y, elem.name))


with open('data/elements.csv', encoding="utf8") as csvfile:  ## Создаю по одному спрайту каждого элемента
    reader = csv.reader(csvfile, delimiter=';', quotechar='"')
    for i in reader:
        elements[str(i[1][1:])] = Element(invisible_sprites, 100, 100, i[1][1:])
        a = i[2].split()
        reactions[(a[0], a[1])] = i[1][1:]
        reactions[(a[1], a[0])] = i[1][1:]

##  inv_to_v(elements[str(1)], 50, 50)  ## примеры использования функции
##  inv_to_v(elements[str(1)], 100, 100)
game_run = True

while game_run:
    menu()
    end_button = Button(100, 50)
    back_menu = Button(100, 50)
    running = True
    closet = Closet(0, 600)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                visible_sprites.update(event.pos)
                for el in closet.elem:
                    el.get_elem(event)
            if event.type == pygame.MOUSEMOTION:  ## перемещение спрайта
                for i in visible_sprites:
                    if i.md:
                        x, y = event.pos
                        i.rect.topleft = (x - 25, y - 25)
            if event.type == pygame.MOUSEBUTTONUP:
                for i in visible_sprites:
                    i.mdn(event.pos, closet)
        screen.fill((74, 74, 74))
        back_menu.draw(10, 10, 'Back', 49)
        end_button.draw(690, 10, 'End', 50)
        closet.draw(screen)
        closet.scroll()
        if back_menu.click():
            menu()
        if end_button.click():
            running = False
        visible_sprites.draw(screen)
        clock.tick(fps)
        pygame.display.flip()
    end_game()
