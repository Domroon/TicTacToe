import pygame
from pygame import math
from pygame import mouse
import pygame.freetype

def draw_matchfield_lines(surface, width):
    # vertical lines
    for i in range(0, 3):
        pygame.draw.line(surface, (255, 255, 255), (width/3 * i, 0), (width/3 * i, width))
    pygame.draw.line(surface, (255, 255, 255), (width/3 * 3 - 1, 0), (width/3 * 3 - 1, width))

    # horizontal lines
    for i in range(0, 3):
        pygame.draw.line(surface, (255, 255, 255), (0, width/3 * i), (width,width/3 *i ))
    pygame.draw.line(surface, (255, 255, 255), (0, width/3*3-1), (width, width/3*3-1))


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
    def __init__(self, width, pos):
        super().__init__()
        self.image = pygame.Surface((width, width), pygame.SRCALPHA)

        # line 1
        self.line_1 = pygame.Surface((15,180), pygame.SRCALPHA)
        self.line_1.fill((255, 0, 0))
        self.line_1 = pygame.transform.rotozoom(self.line_1, 45, 1)
        self.line_1_rect = self.line_1.get_rect(center=self.image.get_rect().center)
        self.image.blit(self.line_1, (0, 0))

        # line 2
        self.line_2 = pygame.Surface((15,180), pygame.SRCALPHA)
        self.line_2.fill((255, 0, 0))
        self.line_2 = pygame.transform.rotozoom(self.line_2, 135, 1)
        self.image.blit(self.line_2, (0, 0))

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
        matchfield.fill((50, 50, 50))
        matchtfield_rect = matchfield.get_rect(center=background_rect.center)
        draw_matchfield_lines(matchfield, matchfield_width)

        # Player Showfield
        player_showfield = PlayerShowField(50, (255, 255, 255), background)
        player_showfield_group = pygame.sprite.Group()
        player_showfield_group.add(player_showfield)

        # Cross Test
        cross_width = 140
        positions = calculate_matchfield_positions(matchtfield_rect, cross_width)
        #cross = Cross(cross_width, positions[8])
        cross_group = pygame.sprite.Group()
        #cross_group.add(cross)

        # Mousebox Test
        mousebox_width = 10
        mousebox = Mousebox(mousebox_width)
        mousebox_group = pygame.sprite.Group()
        mousebox_group.add(mousebox)

        # Hitbox Test
        hitbox = Hitbox(cross_width, positions[0])
        hitbox_group = pygame.sprite.Group()
        hitbox_group.add(hitbox)
        for position in positions:
            hitbox_group.add(Hitbox(cross_width, position))
        
        clock = pygame.time.Clock()
        fps = 120
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            window.blit(background, (0, 0))
            background.blit(matchfield, matchfield.get_rect(center=matchtfield_rect.center))
            
            player_showfield_group.update(2)
            player_showfield_group.draw(window)

            # Hitbox Test
            hitbox_group.draw(window)

            # Cross Test
            cross_group.draw(window)

            # Mousebox Test
            mousebox.update()
            mousebox_group.draw(window)

            left_btn, middle_btn, right_btn = pygame.mouse.get_pressed()
            hit_list = pygame.sprite.spritecollide(mousebox, hitbox_group, False)
            if len(hit_list) >= 1 and left_btn:
                cross_group.add(Cross(cross_width, hit_list[0].pos))
                hitbox_group.remove(hit_list[0])

            pygame.display.update()
            clock.tick(fps)
    finally:
        pygame.quit()


if __name__ == '__main__':
    main()