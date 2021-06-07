import pygame
from pygame import math
from pygame import mouse
import pygame.freetype

def draw_matchfield_lines(surface, width):
    # vertical lines
    for i in range(0, 3):
        pygame.draw.line(surface, (255, 255, 255), (width/3 * i, 0), (width/3 * i, width), width=5)
    pygame.draw.line(surface, (255, 255, 255), (width/3 * 3 - 1, 0), (width/3 * 3 - 1, width), width=5)

    # horizontal lines
    for i in range(0, 3):
        pygame.draw.line(surface, (255, 255, 255), (0, width/3 * i), (width,width/3 *i ), width=5)
    pygame.draw.line(surface, (255, 255, 255), (0, width/3*3-1), (width, width/3*3-1), width=5)


def calculate_matchfield_positions(rect, sign_width = 140):
    positions = []

    # row 1
    for i in range (1, 6, 2):
        vector = pygame.math.Vector2(rect.topleft) + (sign_width/1.6 * i, sign_width/1.6)
        positions.append(vector)

    # row 2
    for i in range (1, 6, 2):
        vector = pygame.math.Vector2(rect.topleft) + (sign_width/1.6 * i, sign_width*1.85)
        positions.append(vector)

    # row 3
    for i in range (1, 6, 2):
        vector = pygame.math.Vector2(rect.topleft) + (sign_width/1.6 * i, sign_width*3.1)
        positions.append(vector)

    return positions


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

    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.hover()
        else:
            self.unhover()
    
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


class Screen:
    def __init__(self, sprite_groups, sprite_lists, surfaces):
        pass

    def add(self):
        # add the screen to the main surface
        # -> add all sprites from the sprite_lists to the right sprite_groups
        # -> draw all sprite_groups
        pass

    def show(self):
        # draw all sprite_groups
        pass

    def remove():
        # empty() all sprite groups
        # draw/blit a black screen over the main surface
        pass


def main():
    pygame.init()
    try:
        screen_width = 720
        matchfield_width = screen_width - 200

        window = pygame.display.set_mode((screen_width, screen_width))
        pygame.display.set_caption("Clock")

        background = pygame.Surface((screen_width, screen_width))
        background_rect = background.get_rect(center=window.get_rect().center)
        matchfield = pygame.Surface((matchfield_width, matchfield_width))
        matchfield_rect = matchfield.get_rect(center=background_rect.center)
        draw_matchfield_lines(matchfield, matchfield_width)

        # Player Showfield
        player_showfield = PlayerShowField(50, (255, 255, 255), background)
        player_showfield_group = pygame.sprite.Group()
        player_showfield_group.add(player_showfield)

        cross_width = 140
        positions = calculate_matchfield_positions(matchfield_rect, cross_width)

        # Crosses
        cross_group = pygame.sprite.Group()

        # Mousebox
        mousebox_width = 10
        mousebox = Mousebox(mousebox_width)
        mousebox_group = pygame.sprite.Group()
        mousebox_group.add(mousebox)

        # Hitboxes
        hitbox = Hitbox(cross_width, positions[0])
        hitbox_group = pygame.sprite.Group()
        hitbox_group.add(hitbox)
        for position in positions:
            hitbox_group.add(Hitbox(cross_width, position))

        circle_group = pygame.sprite.Group()

        # testing
        player_x = True
        player_o = False

        # testing Button
        start_button = Button("Start", (200, 60), window.get_rect().center)
        button_group = pygame.sprite.Group()
        
        exit_button = Button("Exit", (200, 60), (window.get_rect().centerx, window.get_rect().centery + 80))
        exit_button.unclick()

        buttons = [start_button, exit_button]
        
        button_group.add(buttons)

        buttons = {}
        for button in button_group.sprites():
            buttons[button.text] = button
        
        clock = pygame.time.Clock()
        fps = 120
        game_screen = False
        menu_screen = True
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and game_screen:
                    hit_list = pygame.sprite.spritecollide(mousebox, hitbox_group, True)
                    if len(cross_group) < 9 and len(hit_list) > 0:
                        if player_x:
                            cross_group.add(Cross(cross_width, hit_list[0].pos))
                            player_x = False
                            player_o = True
                        elif player_o:
                            circle_group.add(Circle(140, 15, hit_list[0].pos))
                            player_x = True
                            player_o = False
                if event.type == pygame.MOUSEBUTTONDOWN and buttons["Start"].rect.collidepoint(event.pos):
                    buttons["Start"].click(10)
                if event.type == pygame.MOUSEBUTTONUP and buttons["Start"].rect.collidepoint(event.pos):
                    buttons["Start"].unclick()
                    game_screen = True
                    menu_screen = False
                if event.type == pygame.MOUSEBUTTONDOWN and buttons["Exit"].rect.collidepoint(event.pos):
                    buttons["Exit"].click(10)
                if event.type == pygame.MOUSEBUTTONUP and buttons["Exit"].rect.collidepoint(event.pos):
                    buttons["Exit"].unclick()
                    return

            window.blit(background, (0, 0))

            # show the screen
            if game_screen:
                show_game_screen(background, matchfield, matchfield_rect, player_showfield_group, cross_group, circle_group, window, mousebox)
            elif menu_screen:
                show_menuscreen(button_group, background)

            mousebox.update()

            pygame.display.update()
            clock.tick(fps)
    finally:
        pygame.quit()


if __name__ == '__main__':
    main()