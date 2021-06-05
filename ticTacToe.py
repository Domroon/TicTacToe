import pygame

def draw_background(background, screen_width):
    pygame.draw.line(background, (255, 255, 255), (screen_width/3, 0), (screen_width/3, screen_width))
    pygame.draw.line(background, (255, 255, 255), (screen_width/3*2, 0), (screen_width/3*2, screen_width))

    pygame.draw.line(background, (255, 255, 255), (0, screen_width/3), (screen_width, screen_width/3))
    pygame.draw.line(background, (255, 255, 255), (0, screen_width/3*2), (screen_width, screen_width/3*2))


def main():
    pygame.init()
    try:
        screen_width = 720

        window = pygame.display.set_mode((screen_width, screen_width))
        pygame.display.set_caption("Clock")

        background = pygame.Surface(window.get_size())
        draw_background(background, screen_width)
        
        clock = pygame.time.Clock()
        fps = 120
        while True:
            window.blit(background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return


            pygame.display.update()
            clock.tick(fps)
    finally:
        pygame.quit()


if __name__ == '__main__':
    main()