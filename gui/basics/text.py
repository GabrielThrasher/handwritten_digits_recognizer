import pygame as pg


# Function for simplifying displaying text on the screen
def display_text(screen, size, message, RGB, position, alignment="top_left",
                 style=[]):
    pg.font.init()
    font = pg.font.SysFont("Arial", size)

    if "bold" in style:
        font.set_bold(True)
    if "underline" in style:
        font.set_underline(True)
    if "italic" in style:
        font.set_italic(True)

    text = font.render(message, True, RGB)
    text_rect = text.get_rect()

    if alignment == "top_left":
        text_rect.topleft = position
    elif alignment == "center":
        text_rect.center = position

    screen.blit(text, text_rect)

    return text_rect
