import pygame
import pygame.freetype

def draw_matchfield(surface, width):
    # vertical lines
    for i in range(0, 3):
        pygame.draw.line(surface, (255, 255, 255), (width/3 * i, 0), (width/3 * i, width))
    pygame.draw.line(surface, (255, 255, 255), (width/3 * 3 - 1, 0), (width/3 * 3 - 1, width))

    # horizontal lines
    for i in range(0, 3):
        pygame.draw.line(surface, (255, 255, 255), (0, width/3 * i), (width,width/3 *i ))
    pygame.draw.line(surface, (255, 255, 255), (0, width/3*3-1), (width, width/3*3-1))


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


def main():
    pygame.init()
    try:
        screen_width = 720
        matchfield_width = screen_width - 200

        window = pygame.display.set_mode((screen_width, screen_width))
        pygame.display.set_caption("Clock")

        background = pygame.Surface((screen_width, screen_width))
        matchfield = pygame.Surface((matchfield_width, matchfield_width))
        draw_matchfield(matchfield, matchfield_width)

        # Player Showfield
        player_showfield = PlayerShowField(50, (255, 255, 255), background)
        player_showfield_group = pygame.sprite.Group()
        player_showfield_group.add(player_showfield)
        
        clock = pygame.time.Clock()
        fps = 120
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            window.blit(background, (0, 0))
            background.blit(matchfield, matchfield.get_rect(center=background.get_rect().center))
            
            player_showfield_group.update(2)
            player_showfield_group.draw(background)

            pygame.display.update()
            clock.tick(fps)
    finally:
        pygame.quit()


if __name__ == '__main__':
    main()