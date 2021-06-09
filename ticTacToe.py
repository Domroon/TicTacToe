import pygame
from pygame import math
from pygame import mouse
from pygame import sprite
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP
import pygame.freetype


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
    def __init__(self, diameter, thickness, pos, color=(255, 255, 255)):
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
            matchfield_click_event = pygame.event.Event(MATCHFIELD_CLICK, id=id(self))
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
            self.click(10)
            #print(f"{self.text} DOWN")
        if event.type == MOUSEBUTTONUP and self.rect.collidepoint(pygame.mouse.get_pos()) and event.button == 1:
            self.unclick()
            button_click_event = pygame.event.Event(BUTTON_CLICK, text=self.text)
            pygame.event.post(button_click_event)
            #print(f"{self.text} UP")
    
    def click(self, offset):
        self.image = pygame.transform.scale(self.image, (self.size[0] + offset, self.size[1] + offset))
        self.middle_rectangle = pygame.transform.scale(self.middle_rectangle, (self.size[0] - self.width + offset, self.size[1] - self.width + offset))
        self.font = pygame.freetype.Font(None, 40 + offset)
        self.text_surface_rect.center = (self.middle_rectangle.get_rect().centerx - offset, self.middle_rectangle.get_rect().centery)

    def unclick(self):
        self.image = pygame.transform.scale(self.image, (self.size[0], self.size[1]))
        self.middle_rectangle = pygame.transform.scale(self.middle_rectangle, (self.size[0] - self.width, self.size[1] - self.width))
        self.font = pygame.freetype.Font(None, 40)
        self.text_surface_rect.center = self.middle_rectangle.get_rect().center


class Matchfield(pygame.sprite.Sprite):
    def __init__(self, width, surface):
        super().__init__()
        self.width = width
        self.image = pygame.Surface((width, width))
        self.image.fill((50, 50, 50))
        self.rect = self.image.get_rect(center = surface.get_rect().center)
        self.postitions = self.calculate_matchfield_positions()
        self.draw_matchfield_lines(5)

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

    def calculate_matchfield_positions(self, sign_width = 140):
        positions = []

        # row 1
        for i in range (1, 6, 2):
            vector = pygame.math.Vector2(self.rect.topleft) + (sign_width/1.6 * i, sign_width/1.6)
            positions.append(vector)

        # row 2
        for i in range (1, 6, 2):
            vector = pygame.math.Vector2(self.rect.topleft) + (sign_width/1.6 * i, sign_width*1.85)
            positions.append(vector)

        # row 3
        for i in range (1, 6, 2):
            vector = pygame.math.Vector2(self.rect.topleft) + (sign_width/1.6 * i, sign_width*3.1)
            positions.append(vector)

        return positions


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

        # Init Game Screen
        matchfield = Matchfield(matchfield_width, background)
        
        #background_rect = background.get_rect(center=window.get_rect().center)
        #matchfield = pygame.Surface((matchfield_width, matchfield_width))
        #matchfield_rect = matchfield.get_rect(center=background_rect.center)
        #draw_matchfield_lines(matchfield, matchfield_width)

        player_showfield = PlayerShowField(50, (255, 255, 255), window)
        player_showfield_group = pygame.sprite.Group()
        player_showfield_group.add(player_showfield)

        cross_width = 140
        positions = matchfield.postitions

        cross_group = pygame.sprite.Group()

        mousebox_width = 10
        mousebox = Mousebox(mousebox_width)
        mousebox_group = pygame.sprite.Group()
        mousebox_group.add(mousebox)

        hitbox = Hitbox(cross_width, positions[0])
        hitbox_group = pygame.sprite.Group()
        for position in positions:
            hitbox_group.add(Hitbox(cross_width, position))

        print(hitbox_group)

        circle_group = pygame.sprite.Group()

        player_x = True
        player_o = False

        matchfield_group = pygame.sprite.Group()
        matchfield_group.add(matchfield)

        game_screen = Screen([matchfield_group, hitbox_group])
        #game_screen.add()

        # Init Menu Screen
        start_button = Button("Start", (200, 60), window.get_rect().center)
        button_group = pygame.sprite.Group()

        settings_button = Button("Settings", (200, 60), (window.get_rect().centerx, window.get_rect().centery + 80))
        
        exit_button = Button("Exit", (200, 60), (window.get_rect().centerx, window.get_rect().centery + 240))

        menu_buttons = [start_button, exit_button, settings_button]

        button_group.add(menu_buttons)

        cross = Cross(140, (window.get_rect().centerx, window.get_rect().centery - 140))
        test_sprites = [cross]
        test_sprites_group = pygame.sprite.Group()
        test_sprites_group.add(test_sprites)

        menu_screen = Screen([button_group, test_sprites_group])
        menu_screen.add()

        # Init Settings Screen
        back_button = Button("Back", (200, 60), (window.get_rect().centerx, window.get_rect().centery + 160))
        settings_button_group = pygame.sprite.Group()
        settings_button_group.add(back_button)
        settings_screen = Screen([settings_button_group])

        clock = pygame.time.Clock()
        fps = 120
        while True:
            for event in pygame.event.get():
                print(event)
                if event.type == pygame.QUIT:
                    return
                #if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    #hit_list = pygame.sprite.spritecollide(mousebox, hitbox_group, True)
                    #if len(cross_group) < 9 and len(hit_list) > 0:
                        #if player_x:
                            #cross_group.add(Cross(cross_width, hit_list[0].pos))
                            #player_x = False
                            #player_o = True
                        #elif player_o:
                            #circle_group.add(Circle(140, 15, hit_list[0].pos))
                            #player_x = True
                            #player_o = False
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