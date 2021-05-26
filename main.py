import pygame, sys
import gameplay

mainClock = pygame.time.Clock()

pygame.init()
pygame.display.set_caption("Tic Tac Toe")
screen = pygame.display.set_mode((1000, 600))

title_font = pygame.font.SysFont("Berlin Sans FB Demi", 72, True)
subtitle_font = pygame.font.SysFont("Berlin Sans FB Demi", 60, True)


# for making text box
def draw_text(text, font, color, surface, x, y):
    textObject = font.render(text, 1, color)
    textRect = textObject.get_rect()
    textRect.topleft = (x, y)
    surface.blit(textObject, textRect)


# for making text box with white border
def draw_rect_text(text, font, color, surface, bg_color, rect):
    pygame.draw.rect(surface, (255, 255, 255), rect)
    smaller_rect_for_border = (rect[0] + 5, rect[1] + 5, rect[2] - 10, rect[3] - 10)
    pygame.draw.rect(surface, bg_color, smaller_rect_for_border)
    textObject = font.render(text, 1, color)
    textRect = textObject.get_rect()
    textRect.midtop = ((rect[0] + rect[2] // 2), rect[1])
    surface.blit(textObject, textRect)


# the main menu loop
def main_menu():
    click = False
    while True:
        screen.fill((228, 101, 63))
        draw_text("Tic Tac Toe", title_font, (255, 255, 255), screen, 90, 80)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(510, 230, 360, 80)
        button_2 = pygame.Rect(510, 335, 360, 80)

        if button_1.collidepoint((mx, my)):
            if click:
                gameplay.vsComp(screen)

        if button_2.collidepoint((mx, my)):
            if click:
                gameplay.vsHuman(screen)

        click = False
        draw_rect_text("vs. Comp", subtitle_font, (255, 255, 255), screen, (228, 101, 63), button_1)
        draw_rect_text("vs. Human", subtitle_font, (255, 255, 255), screen, (228, 101, 63), button_2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)


if __name__ == '__main__':
    main_menu()
