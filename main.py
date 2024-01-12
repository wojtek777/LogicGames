import sys
import pygame
import settings


class Button(pygame.sprite.Sprite):
    def __init__(self, path: str, bottom_left_pos):
        super().__init__()
        image_orig = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(image_orig, tuple(z * 1.5 for z in image_orig.get_size()))
        self.rect = self.image.get_rect(bottomleft=bottom_left_pos)

    def update(self, *args, **kwargs):
        pass

    def destroy(self):
        self.kill()


# game init
pygame.init()
resolution = (1200, 800)
screen = pygame.display.set_mode(resolution)
pygame.display.set_caption('Logic Games v0.1')
pyclock = pygame.time.Clock()
pyclock.tick(60)
# screen.fill((50, 160, 90))
about_font = pygame.font.Font('Graphics/BigSpace.ttf', 50)
about_text = about_font.render(
    'Logic Games v0.1 - created to provide',
    True,
    'gray'
)
about_text2 = about_font.render(
    'some basic training in math and logic games',
    True,
    'gray'
)
screen.fill('cyan3')
game_music = pygame.mixer.Sound('Sounds/music_game.mp3')
game_music.play(loops=-1)
game_music.set_volume(0.7)
buttons = pygame.sprite.Group()
play_static_button = Button('Graphics/play_static.png', (520, 300))
options_static_button = Button('Graphics/options_static.png', (520, 400))
about_static_button = Button('Graphics/about_static.png', (520, 500))
exit_static_button = Button('Graphics/exit_static.png', (520, 600))
play_pressed_button = Button('Graphics/play_pressed.png', (520, 300))
options_pressed_button = Button('Graphics/options_pressed.png', (520, 400))
about_pressed_button = Button('Graphics/about_pressed.png', (520, 500))
exit_pressed_button = Button('Graphics/exit_pressed.png', (520, 600))
menu_buttons = (
    (play_pressed_button, play_static_button),
    (options_pressed_button, options_static_button),
    (about_pressed_button, about_static_button),
    (exit_pressed_button, exit_static_button)
)
settings_buttons = {}
menu_set = {play_pressed_button, options_static_button, about_static_button, exit_static_button}
buttons.add(*menu_set)
selected_button = 0


def display_menu():
    buttons.draw(screen)


active_level = {
    'menu': 1,
    'settings': 0,
    'about': 0,
    'level1': 0,
    'level2': 0,
    'level3': 0,
    'level4': 0,
    'level5': 0
    }


while True:
    pygame.display.update()
    screen.fill('cyan3')
    if active_level['menu'] == 1:
        display_menu()
    elif active_level['about'] == 1:
        buttons.empty()
        buttons.add(exit_pressed_button)
        screen.blit(about_text, (160, 60))
        screen.blit(about_text2, (160, 100))
        display_menu()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.KEYDOWN and active_level['about'] == 1:
            if event.key == pygame.K_RETURN:
                buttons.empty()
                screen.fill('cyan3')
                buttons.add(*menu_set)
                active_level.update({'menu': 1, 'about': 0})
                selected_button = 0
        elif event.type == pygame.KEYDOWN and active_level['menu'] == 1:
            if event.key == pygame.K_DOWN:
                screen.fill('cyan3')
                buttons.remove(menu_buttons[selected_button][0])
                buttons.add(menu_buttons[selected_button][1])
                selected_button += 1
                selected_button %= 4
                buttons.add(menu_buttons[selected_button][0])
                buttons.remove(menu_buttons[selected_button][1])
            if event.key == pygame.K_UP:
                screen.fill('cyan3')
                menu_buttons[selected_button][0].destroy()
                buttons.remove(menu_buttons[selected_button][0])
                buttons.add(menu_buttons[selected_button][1])
                selected_button += 3
                selected_button %= 4
                buttons.add(menu_buttons[selected_button][0])
                menu_buttons[selected_button][1].destroy()
                buttons.remove(menu_buttons[selected_button][1])
            if event.key == pygame.K_RETURN:
                if selected_button == 3:
                    pygame.quit()
                    sys.exit(0)
                elif selected_button == 2:
                    active_level.update({'menu': 0, 'about': 1})
                    buttons.add(exit_pressed_button)
            # buttons.empty()
