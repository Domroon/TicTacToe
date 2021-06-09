import pygame
from pygame import math
from pygame import mouse
from pygame import sprite
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION
import pygame.freetype
from itertools import cycle


BUTTON_CLICK = pygame.event.custom_type()
MATCHFIELD_CLICK = pygame.event.custom_type()


def show_game_screen(background, matchfield, matchfield_rect, player_showfield_group, cross_group, circle_group, window, mousebox):
    background.blit(matchfield, matchfield.get_rect(center=matchfield_rect.center))
            
    player_showfield_group.update(1)
    player_showfield_group.draw(window)

    cross_group.draw(window)
    circle_group.draw(window)


def show_menuscreen(button_group, surface):
    surface.fill((0, 0, 0))
    button_group.update()
    button_group.draw(surface)


def check_menu_screen_actions(event, menu_screen, menu_screen_2):
    if event.type == MOUSEBUTTONDOWN:
        for sprite_list in menu_screen.sprite_lists:
            for sprite in sprite_list:
                if type(sprite).__name__ == "Button":
                    if sprite.text == "Start" and sprite.rect.collidepoint(pygame.mouse.get_pos()):
                        sprite.click(10)
                    elif sprite.text == "Settings" and sprite.rect.collidepoint(pygame.mouse.get_pos()):
                        sprite.click(10)
                    elif sprite.text == "Exit" and sprite.rect.collidepoint(pygame.mouse.get_pos()):
                        sprite.click(10)

    if event.type == MOUSEBUTTONUP:
        for sprite_list in menu_screen.sprite_lists:
            for sprite in sprite_list:
                if type(sprite).__name__ == "Button":
                    if sprite.text == "Start" and sprite.rect.collidepoint(pygame.mouse.get_pos()):
                        print("Start clicked")
                        sprite.unclick()
                    elif sprite.text == "Settings" and sprite.rect.collidepoint(pygame.mouse.get_pos()):
                        menu_screen.remove()
                        menu_screen_2.add()
                        sprite.unclick()
                    elif sprite.text == "Exit" and sprite.rect.collidepoint(pygame.mouse.get_pos()):
                        pygame.quit()
                        exit()


def check_menu_screen_2_actions(event, menu_screen, menu_screen_2):
    if event.type == MOUSEBUTTONDOWN:
        for sprite_list in menu_screen_2.sprite_lists:
            for sprite in sprite_list:
                if type(sprite).__name__ == "Button":
                    if sprite.text == "Back" and sprite.rect.collidepoint(pygame.mouse.get_pos()):
                        sprite.click(10)

    if event.type == MOUSEBUTTONUP:
        for sprite_list in menu_screen_2.sprite_lists:
            for sprite in sprite_list:
                if type(sprite).__name__ == "Button":
                    if sprite.text == "Back" and sprite.rect.collidepoint(pygame.mouse.get_pos()):
                        print("Back clicked")
                        sprite.unclick()
                        menu_screen_2.remove()
                        menu_screen.add()


class PlayerShowField(pygame.sprite.Sprite):
    def __init__(self, size, color, surface):
        super().__init__()
        self.color = color
        self.surface = surface
        self.font = pygame.freetype.Font(None, size)
        self.image, self.rect = self.font.render("Test", (255, 255, 255))
        self.rect = self.image.get_rect(midbottom=surface.get_rect().midbottom)

    def show_player_1(self):
        self.image, self.rect = self.font.render("Player 1", self.color)
        self.rect = self.image.get_rect(midbottom=self.surface.get_rect().midbottom)

    def show_player_2(self):
        self.image, self.rect = self.font.render("Player 2", self.color)
        self.rect = self.image.get_rect(midbottom=self.surface.get_rect().midbottom)

    def update(self, player):
        if player == 1:
            self.show_player_1()
        elif player == 2:
            self.show_player_2()


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
    def __init__(self, diameter, pos, color=(255, 255, 255), thickness=5):
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
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=pos)

    def update(self, event):
        if event.type == MOUSEBUTTONDOWN and self.rect.collidepoint(pygame.mouse.get_pos()):
            #print(id(self))
            matchfield_click_event = pygame.event.Event(MATCHFIELD_CLICK, id=id(self), rect=self.rect)
            pygame.event.post(matchfield_click_event)


class Mousebox(pygame.sprite.Sprite):
    def __init__(self, width):
        super().__init__()
        self.image = pygame.Surface((width, width))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(center=pygame.mouse.get_pos())

    def update(self):
        self.rect = self.image.get_rect(center=pygame.mouse.get_pos())


class Button(pygame.sprite.Sprite):
    def __init__(self, text, size, pos, color=(50, 50, 50), width = 10):
        super().__init__()
        self.text = text
        self.size = size
        self.pos = pos
        self.color = color
        self.image = pygame.Surface(self.size)
        self.image.fill((self.color))
        self.width = width

        self.rect = self.image.get_rect(center=pos)

        self.middle_rectangle = pygame.Surface((self.size[0] - self.width, self.size[1] - self.width))
        
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


class Matchfield(pygame.sprite.Sprite):
    def __init__(self, width, surface, sign_width=140):
        super().__init__()
        self.width = width
        self.image = pygame.Surface((width, width))
        self.image.fill((50, 50, 50))
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


class Screen:
    def __init__(self, sprite_groups):
        # sprite_lists attribute not necessary?!
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
        #self.sprite_lists = sprite_lists
        #self.active = False
        #implement a menu class for that?
        self.buttons = {}

    def add(self):
        # add all sprites from the sprite_lists to the right sprite_group
        i = 0
        for sprite_group in self.sprite_groups:
            sprite_group.add(self.sprite_lists[i])
            i += 1
        #self.active = True

        # implement a menu class for that?
        #for button in self.sprite_groups[0]:
            #self.buttons[button.text] = button

    def draw(self, surface):
        # draw all sprite_groups to the given surface
        # and update all groups
        for sprite_group in self.sprite_groups:
            sprite_group.draw(surface)

    def update(self, event):
        for sprite_group in self.sprite_groups:
            sprite_group.update(event)

    def remove(self):
        # empty() all sprite groups
        # draw/blit a black screen over the given surface
        for sprite_group in self.sprite_groups:
            sprite_group.empty()
            #sprite_group.clear(surface, background)
        #self.active = False

    
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

        mousebox_width = 10
        mousebox = Mousebox(mousebox_width)
        mousebox_group = pygame.sprite.Group()
        mousebox_group.add(mousebox)

        matchfield_group = pygame.sprite.Group()
        matchfield_group.add(matchfield)

        game_screen = Screen([matchfield_group, matchfield.hitbox_group, cross_group, circle_group])

        # Init Menu Screen
        start_button = Button("Start", (200, 60), window.get_rect().center)
        settings_button = Button("Settings", (200, 60), (window.get_rect().centerx, window.get_rect().centery + 80))
        exit_button = Button("Exit", (200, 60), (window.get_rect().centerx, window.get_rect().centery + 240))
        menu_buttons = [start_button, exit_button, settings_button]

        button_group = pygame.sprite.Group()
        button_group.add(menu_buttons)

        cross = Cross(140, (window.get_rect().centerx, window.get_rect().centery - 140))
        sign_sprites = [cross]
        sign_sprites_group = pygame.sprite.Group()
        sign_sprites_group.add(sign_sprites)

        menu_screen = Screen([button_group, sign_sprites_group])
        menu_screen.add()

        # Init Settings Screen
        back_button = Button("Back", (200, 60), (window.get_rect().centerx, window.get_rect().centery + 160))
        settings_button_group = pygame.sprite.Group()
        settings_button_group.add(back_button)
        settings_screen = Screen([settings_button_group])

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

        i = 0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == BUTTON_CLICK and event.text == "Settings":
                    menu_screen.remove()
                    settings_screen.add()
                if event.type == BUTTON_CLICK and event.text == "Exit":
                    return
                if event.type == BUTTON_CLICK and event.text == "Back":
                    settings_screen.remove()
                    menu_screen.add()
                if event.type == BUTTON_CLICK and event.text == "Start":
                    menu_screen.remove()
                    game_screen.add()
                if event.type == MATCHFIELD_CLICK and event.id == matchfield.hitbox_ids[0]:
                    print("Field 1 clicked")
                    if sign_list[i] == "Cross":
                        cross_group.add(Cross(140, event.rect.center, color=(255, 0, 0)))
                    elif sign_list[i] == "Circle":
                        circle_group.add(Circle())
                if event.type == MATCHFIELD_CLICK and event.id == matchfield.hitbox_ids[1]:
                    print("Field 2 clicked")
                    if sign_list[i] == "Cross":
                        cross_group.add(Cross(140, event.rect.center, color=(255, 0, 0)))
                    elif sign_list[i] == "Circle":
                        circle_group.add(Circle(140, event.rect.center, color=(255, 0, 0)))
                if event.type == MATCHFIELD_CLICK and event.id == matchfield.hitbox_ids[2]:
                    print("Field 3 clicked")
                    if sign_list[i] == "Cross":
                        cross_group.add(Cross(140, event.rect.center, color=(255, 0, 0)))
                    elif sign_list[i] == "Circle":
                        circle_group.add(Circle(140, event.rect.center, color=(255, 0, 0)))
                if event.type == MATCHFIELD_CLICK and event.id == matchfield.hitbox_ids[3]:
                    print("Field 4 clicked")
                    if sign_list[i] == "Cross":
                        cross_group.add(Cross(140, event.rect.center, color=(255, 0, 0)))
                    elif sign_list[i] == "Circle":
                        circle_group.add(Circle(140, event.rect.center, color=(255, 0, 0)))
                if event.type == MATCHFIELD_CLICK and event.id == matchfield.hitbox_ids[4]:
                    print("Field 5 clicked")
                    if sign_list[i] == "Cross":
                        cross_group.add(Cross(140, event.rect.center, color=(255, 0, 0)))
                    elif sign_list[i] == "Circle":
                        circle_group.add(Circle(140, event.rect.center, color=(255, 0, 0)))
                if event.type == MATCHFIELD_CLICK and event.id == matchfield.hitbox_ids[5]:
                    print("Field 6 clicked")
                    if sign_list[i] == "Cross":
                        cross_group.add(Cross(140, event.rect.center, color=(255, 0, 0)))
                    elif sign_list[i] == "Circle":
                        circle_group.add(Circle(140, event.rect.center, color=(255, 0, 0)))
                if event.type == MATCHFIELD_CLICK and event.id == matchfield.hitbox_ids[6]:
                    print("Field 7 clicked")
                    if sign_list[i] == "Cross":
                        cross_group.add(Cross(140, event.rect.center, color=(255, 0, 0)))
                    elif sign_list[i] == "Circle":
                        circle_group.add(Circle(140, event.rect.center, color=(255, 0, 0)))
                if event.type == MATCHFIELD_CLICK and event.id == matchfield.hitbox_ids[7]:
                    print("Field 8 clicked")
                    if sign_list[i] == "Cross":
                        cross_group.add(Cross(140, event.rect.center, color=(255, 0, 0)))
                    elif sign_list[i] == "Circle":
                        circle_group.add(Circle(140, event.rect.center, color=(255, 0, 0)))
                if event.type == MATCHFIELD_CLICK and event.id == matchfield.hitbox_ids[8]:
                    print("Field 9 clicked")
                    if sign_list[i] == "Cross":
                        cross_group.add(Cross(140, event.rect.center, color=(255, 0, 0)))
                    elif sign_list[i] == "Circle":
                        circle_group.add(Circle(140, event.rect.center, color=(255, 0, 0)))
                if event.type == MATCHFIELD_CLICK:
                    i += 1

                menu_screen.update(event)
                settings_screen.update(event)
                game_screen.update(event)
            
            window.blit(background, (0, 0))

            menu_screen.draw(window)
            settings_screen.draw(window)
            game_screen.draw(window)

            mousebox.update()

            pygame.display.update()
            clock.tick(fps)
    finally:
        pygame.quit()


if __name__ == '__main__':
    main()