from typing import NamedTuple
import pygame
from pygame import Surface, math
from pygame import mouse
from pygame import sprite
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION
import pygame.freetype
from itertools import cycle
import time
from collections import namedtuple
import json

BUTTON_CLICK = pygame.event.custom_type()
LABEL_CLICK = pygame.event.custom_type()
MATCHFIELD_CLICK = pygame.event.custom_type()


class PlayerShowField(pygame.sprite.Sprite):
    def __init__(self, size, color, surface):
        super().__init__()
        self.color = color
        self.surface = surface
        self.font = pygame.freetype.Font(None, size)
        self.image, self.rect = self.font.render("Showfield Init", (255, 255, 255))
        self.rect = self.image.get_rect(midbottom=surface.get_rect().midbottom)

    def show_x(self):
        self.image, self.rect = self.font.render("X", self.color)
        self.rect = self.image.get_rect(midbottom=self.surface.get_rect().midbottom)

    def show_o(self):
        self.image, self.rect = self.font.render("O", self.color)
        self.rect = self.image.get_rect(midbottom=self.surface.get_rect().midbottom)

    def update(self, sign):
        if sign == "Cross":
            self.show_x()
        elif sign == "Circle":
            self.show_o()


class Cross(pygame.sprite.Sprite):
    def __init__(self, width, pos, color=(255, 255, 255)):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((width, width), pygame.SRCALPHA)

        # line 1
        self.line_1 = pygame.Surface((15,180), pygame.SRCALPHA)
        self.line_1.fill(self.color)
        self.line_1 = pygame.transform.rotozoom(self.line_1, 45, 1)
        self.line_1_rect = self.line_1.get_rect(center=self.image.get_rect().center)
        self.image.blit(self.line_1, (0, 0))

        # line 2
        self.line_2 = pygame.Surface((15,180), pygame.SRCALPHA)
        self.line_2.fill(self.color)
        self.line_2 = pygame.transform.rotozoom(self.line_2, 135, 1)
        self.image.blit(self.line_2, (0, 0))

        self.rect = self.image.get_rect(center=pos)


class Circle(pygame.sprite.Sprite):
    def __init__(self, diameter, pos, color=(255, 255, 255), thickness=15):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, self.color, self.rect.center, diameter/2, thickness)
        self.rect = self.image.get_rect(center=pos)

        
class Hitbox(pygame.sprite.Sprite):
    def __init__(self, width, pos):
        super().__init__()
        self.pos = pos
        self.image = pygame.Surface((width, width))
        self.rect = self.image.get_rect(center=pos)

    def update(self, event):
        if event.type == MOUSEBUTTONDOWN and self.rect.collidepoint(pygame.mouse.get_pos()):
            matchfield_click_event = pygame.event.Event(MATCHFIELD_CLICK, id=id(self), rect=self.rect)
            pygame.event.post(matchfield_click_event)


class Button(pygame.sprite.Sprite):
    def __init__(self, text, size, pos, color=(50, 50, 50), width = 10):
        super().__init__()
        self.text = text
        self.size = size
        self.pos = pos
        self.color = color
        self.image = Surface(self.size)
        self.image.fill((self.color))
        self.width = width

        self.rect = self.image.get_rect(center=pos)

        self.middle_rectangle = Surface((self.size[0] - self.width, self.size[1] - self.width))
        
        self.font = pygame.freetype.Font(None, 40)
        self.text_surface, self.text_surface_rect = self.font.render(self.text, fgcolor=(50, 50, 50))

        self.image.blit(self.middle_rectangle, self.middle_rectangle.get_rect(center=self.image.get_rect().center))
        self.text_surface_rect.center = self.middle_rectangle.get_rect().center
        self.image.blit(self.text_surface, self.text_surface_rect)

    def hover(self, color=(255, 255, 255)):
        self.image.fill(color)
        self.image.blit(self.middle_rectangle, self.middle_rectangle.get_rect(center=self.image.get_rect().center))
        self.font.render_to(self.image, self.text_surface_rect, self.text, color)
        self.rect = self.image.get_rect(center=self.pos)

    def unhover(self):
        self.image.fill(self.color)
        self.image.blit(self.middle_rectangle, self.middle_rectangle.get_rect(center=self.image.get_rect().center))
        self.font.render_to(self.image, self.text_surface_rect, self.text, self.color)

    def update(self, event):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.hover()
        else:
            self.unhover()
        if event.type == MOUSEBUTTONDOWN and self.rect.collidepoint(pygame.mouse.get_pos()) and event.button == 1:
            self.click()
        if event.type == MOUSEBUTTONUP and self.rect.collidepoint(pygame.mouse.get_pos()) and event.button == 1:
            self.unclick()
            button_click_event = pygame.event.Event(BUTTON_CLICK, text=self.text)
            pygame.event.post(button_click_event)
    
    def click(self):
        self.image.fill((255, 0, 0))
        self.image.blit(self.middle_rectangle, self.middle_rectangle.get_rect(center=self.image.get_rect().center))
        self.font.render_to(self.image, self.text_surface_rect, self.text, (255, 0, 0))
        self.rect = self.image.get_rect(center=self.pos)

    def unclick(self):
        pass


class Label(pygame.sprite.Sprite):
    def __init__(self, text, size, pos, color=(255, 255, 255)):
        super().__init__()
        self.text = text
        self.size = size
        self.pos = pos
        self.color = color

        self.font = pygame.freetype.Font(None, self.size)
        self.image, self.rect = self.font.render(self.text, self.color)
        self.rect = self.image.get_rect(center=self.pos)


class TextField(pygame.sprite.Sprite):
    def __init__(self, pos, dimensions=(200, 30), bg_color=(255, 255, 255), size=30):
        super().__init__()
        self.dimensions = dimensions
        self.pos = pos
        self.text = ""
        self.bg_color = bg_color

        self.font = pygame.freetype.Font(None, size)

        self.image = pygame.Surface(self.dimensions)
        self.image.fill(self.bg_color)
        self.rect = self.image.get_rect(center=pos)
        self.font.render_to(self.image, (0,0), str(self.text))

        self.focus = False

    def add_letter(self, letter):
        self.text += letter

    def update(self, event):
        self.image.fill(self.bg_color)
        if event.type == MOUSEBUTTONDOWN:
            self.focus = False
        if event.type == MOUSEBUTTONDOWN and self.rect.collidepoint(pygame.mouse.get_pos()):
            self.focus = True
        if event.type == 771 and self.focus and self.focus:
            self.text += event.text
        if event.type == 768 and event.key == 8 and self.focus:
            self.text = self.text[:-1]
        self.font.render_to(self.image, (0,5), str(self.text))


class Matchfield(pygame.sprite.Sprite):
    def __init__(self, width, surface, sign_width=140):
        super().__init__()
        self.width = width
        self.name_1 = "reserved"
        self.name_2 = "reserved"
        self.image = pygame.Surface((width, width))
        self.rect = self.image.get_rect(center = surface.get_rect().center)
        self.sign_width = sign_width
        self.postitions = self.calculate_matchfield_positions()
        self.draw_matchfield_lines(5)
        self.hitbox_group = self.generate_hitboxes()
        self.hitbox_ids = self.set_hitbox_ids()
        
    def draw_matchfield_lines(self, thickness):
    # vertical lines
        for i in range(0, 3):
            pygame.draw.line(self.image, (255, 255, 255), (self.width/3 * i, 0), (self.width/3 * i, self.width), width=thickness)
        pygame.draw.line(self.image, (255, 255, 255), (self.width/3 * 3 - 1, 0), (self.width/3 * 3 - 1, self.width), width=thickness)

        # horizontal lines
        for i in range(0, 3):
            pygame.draw.line(self.image, (255, 255, 255), (0, self.width/3 * i), (self.width,self.width/3 *i ), width=thickness)
        pygame.draw.line(self.image, (255, 255, 255), (0, self.width/3*3-1), (self.width, self.width/3*3-1), width=thickness)

    def add_hitboxes(self):
        pass

    def calculate_matchfield_positions(self):
        positions = []

        # row 1
        for i in range (1, 6, 2):
            vector = pygame.math.Vector2(self.rect.topleft) + (self.sign_width/1.6 * i, self.sign_width/1.6)
            positions.append(vector)

        # row 2
        for i in range (1, 6, 2):
            vector = pygame.math.Vector2(self.rect.topleft) + (self.sign_width/1.6 * i, self.sign_width*1.85)
            positions.append(vector)

        # row 3
        for i in range (1, 6, 2):
            vector = pygame.math.Vector2(self.rect.topleft) + (self.sign_width/1.6 * i, self.sign_width*3.1)
            positions.append(vector)

        return positions

    def generate_hitboxes(self):
        hitbox_group = pygame.sprite.Group()
        for position in self.postitions:
            hitbox = Hitbox(self.sign_width, position)
            hitbox_group.add(hitbox)

        return hitbox_group

    def set_hitbox_ids(self):
        hitbox_ids = []
        for hitbox in self.hitbox_group:
            hitbox_ids.append(id(hitbox))

        return hitbox_ids

    def remove_hit_box(self, hitbox_id):
        for hitbox in self.hitbox_group:
            if id(hitbox) == hitbox_id:
                self.hitbox_group.remove(hitbox)

    def add_sign(self, event, i, sign_list, cross_group, circle_group):
        if sign_list[i] == "Cross":
            cross_group.add(Cross(140, event.rect.center))
        elif sign_list[i] == "Circle":
            circle_group.add(Circle(140, event.rect.center))


class Screen:
    def __init__(self, sprite_groups):
        # save all sprites from the sprite_groups in seperate sprite_lists
        # to have a save location, so that you can remove all sprites 
        # from the groups but can them put later back to the sprite groups
        self.sprite_lists = []
        self.sprite_groups = sprite_groups

        sprite_list = []
        for sprite_group in self.sprite_groups:
            for sprite in sprite_group:
                sprite_list.append(sprite)
            self.sprite_lists.append(sprite_list)
            sprite_list = []

        self.remove()
        self.buttons = {}

    def add(self):
        # add all sprites from the sprite_lists to the right sprite_group
        i = 0
        for sprite_group in self.sprite_groups:
            sprite_group.add(self.sprite_lists[i])
            i += 1

    def draw(self, surface):
        for sprite_group in self.sprite_groups:
            sprite_group.draw(surface)

    def update(self, event):
        for sprite_group in self.sprite_groups:
            sprite_group.update(event)

    def remove(self):
        for sprite_group in self.sprite_groups:
            sprite_group.empty()


def dict2obj(dict, classname):
    pass
    # using json.loads method and passing json.dumps
    # method and custom object hook as arguments
    return json.loads(json.dumps(dict), object_hook=classname)


def buttonObj_to_json(obj):
    obj = obj.__dict__
    obj['image'] = (obj['image'].get_width(), obj['image'].get_height())
    obj['rect'] = (obj['rect'].left, obj['rect'].top, obj['rect'].width, obj['rect'].height)
    obj['middle_rectangle'] = (obj['middle_rectangle'].get_width(), obj['middle_rectangle'].get_height())
    obj['font'] = obj['font'].path
    obj['text_surface'] = (obj['text_surface'].get_width(), obj['text_surface'].get_height())
    obj['text_surface_rect'] = (obj['text_surface_rect'].left, obj['text_surface_rect'].top, obj['text_surface_rect'].width, obj['text_surface_rect'].height)
    obj = json.dumps(obj)
    return obj


def main():
    pygame.init()
    try:
        screen_width = 720
        matchfield_width = screen_width - 200

        window = pygame.display.set_mode((screen_width, screen_width))
        pygame.display.set_caption("Clock")

        background = pygame.Surface((screen_width, screen_width))

        # Init cross and circle group
        cross_group = pygame.sprite.Group()
        circle_group = pygame.sprite.Group()

        # Init Game Screen
        matchfield = Matchfield(matchfield_width, background)

        player_showfield = PlayerShowField(50, (255, 255, 255), window)
        player_showfield_group = pygame.sprite.Group()
        player_showfield_group.add(player_showfield)

        matchfield_group = pygame.sprite.Group()
        matchfield_group.add(matchfield)

        game_screen = Screen([matchfield_group, matchfield.hitbox_group, cross_group, circle_group, player_showfield_group])

        # Init Menu Screen
        start_button = Button("Start", (200, 60), window.get_rect().center)
        settings_button = Button("Settings", (200, 60), (window.get_rect().centerx, window.get_rect().centery + 80))
        exit_button = Button("Exit", (200, 60), (window.get_rect().centerx, window.get_rect().centery + 240))
        menu_buttons = [start_button, exit_button, settings_button]

        button_group = pygame.sprite.Group()
        button_group.add(menu_buttons)

        cross = Cross(140, (window.get_rect().centerx - 70, window.get_rect().centery - 140))
        circle = Circle(140, (window.get_rect().centerx + 70, window.get_rect().centery - 140))
        label = Label("Tic Tac Toe", 70, (window.get_rect().centerx, window.get_rect().centery- 300))
        sign_sprites = [cross, circle, label]
        sign_sprites_group = pygame.sprite.Group()
        sign_sprites_group.add(sign_sprites)

        menu_screen = Screen([button_group, sign_sprites_group])
        menu_screen.add()
        
        #TESTING Serializing Button
        test_button = Button("Test", (200, 60), window.get_rect().center)
        jsonTestButton = buttonObj_to_json(test_button)
        print(jsonTestButton)

        # Init Settings Screen
        back_button = Button("Back", (200, 60), (window.get_rect().centerx, window.get_rect().centery + 160))
        settings_button_group = pygame.sprite.Group()
        settings_button_group.add(back_button)
        settings_screen = Screen([settings_button_group])

        # Init Gamemodes Screen
        one_vs_one_button = Button("1 VS 1", (200, 60), window.get_rect().center)
        gamemodes_button_group = pygame.sprite.Group()
        gamemodes_button_group.add(one_vs_one_button, back_button)
        gamemodes_screen = Screen([gamemodes_button_group])

        # Init One VS One Init Screen
        play_button = Button("Play", (200, 60), (window.get_rect().centerx, window.get_rect().centery + 80))
        vs_1_label = Label("1 vs 1", 70, (window.get_rect().centerx, window.get_rect().centery - 300))
        label_player_1 = Label("Player 1 Name: ", 20, (window.get_rect().centerx - 200, window.get_rect().centery - 100))
        label_player_2 = Label("Player 2 Name: ", 20, (window.get_rect().centerx - 200, window.get_rect().centery))
        player_1_name = TextField((window.get_rect().centerx, window.get_rect().centery - 100))
        player_2_name = TextField((window.get_rect().centerx, window.get_rect().centery))
        one_vs_one_button_group = pygame.sprite.Group()
        one_vs_one_button_group.add(play_button, vs_1_label, player_1_name, player_2_name, label_player_1, label_player_2)
        one_vs_one_init_screen = Screen([one_vs_one_button_group])

        clock = pygame.time.Clock()
        fps = 120

        # make a sign_list
        sign_list = []
        i = 0
        for sign in cycle(["Cross", "Circle"]):
            if i == 9:
               break
            sign_list.append(sign) 
            i += 1

        j = 0

        player_showfield.update(sign_list[j])
        while True:
            for event in pygame.event.get():
                #print(event)
                if event.type == pygame.QUIT:
                    return
                if event.type == BUTTON_CLICK and event.text == "Settings":
                    menu_screen.remove()
                    settings_screen.add()
                if event.type == BUTTON_CLICK and event.text == "Exit":
                    return
                if event.type == BUTTON_CLICK and event.text == "Back":
                    gamemodes_screen.remove()
                    settings_screen.remove()
                    menu_screen.add()
                if event.type == BUTTON_CLICK and event.text == "Start":
                    menu_screen.remove()
                    gamemodes_screen.add()
                if event.type == BUTTON_CLICK and event.text == "1 VS 1":
                    gamemodes_screen.remove()
                    one_vs_one_init_screen.add()
                if event.type == BUTTON_CLICK and event.text == "Play":
                    one_vs_one_init_screen.remove()
                    game_screen.add()
                    print(player_1_name.text)
                    print(player_2_name.text)
                for i in range(0, 9): 
                    if event.type == MATCHFIELD_CLICK and event.id == matchfield.hitbox_ids[i]:
                        matchfield.add_sign(event, j, sign_list, cross_group, circle_group)
                        matchfield.remove_hit_box(event.id)
                if event.type == MATCHFIELD_CLICK:
                    j += 1
                    if j <= 8:
                        player_showfield.update(sign_list[j])

                menu_screen.update(event)
                settings_screen.update(event)
                game_screen.update(event)
                gamemodes_screen.update(event)
                one_vs_one_init_screen.update(event)
            
            window.blit(background, (0, 0))

            menu_screen.draw(window)
            settings_screen.draw(window)
            game_screen.draw(window)
            gamemodes_screen.draw(window)
            one_vs_one_init_screen.draw(window)

            pygame.display.update()
            clock.tick(fps)
    finally:
        pygame.quit()


if __name__ == '__main__':
    main()