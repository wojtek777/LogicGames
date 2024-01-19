import sys
import pygame
import settings as sets
import quests
import time


# Abstract Factory design pattern - superior Sprite class won't manage Sprite objects anymore,
# from now Button factory class takes over restructuring types of objects that serve as
# buttons displayed on the screen - other interactive sprites will be specified in other components
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
pyclock.tick(sets.Settings.get_frequency())
# screen.fill((50, 160, 90))
about_font = pygame.font.Font('Graphics/BigSpace.ttf', 60)
music_font = pygame.font.Font('Graphics/BigSpace.ttf', 50)
exit_game_font = pygame.font.Font('Graphics/Over.otf', 70)
game_over_font = pygame.font.Font('Graphics/Over.otf', 100)
music_on_text = music_font.render(
    'ON',
    True,
    'red'
)
music_off_text = music_font.render(
    'OFF',
    True,
    'red'
)
about_text = about_font.render(
    'Logic Games v0.1 - created to provide',
    True,
    'gray44'
)
about_text2 = about_font.render(
    'some basic training in math and logic games',
    True,
    'gray44'
)
exit_game_text = exit_game_font.render(
    'Exit Game?',
    True,
    'gray44'
)
you_won_text = exit_game_font.render(
    'You Won!',
    True,
    'gray44'
)
game_over_text = game_over_font.render(
    'GAME OVER',
    True,
    'orange'
)

screen.fill('cyan3')
game_music = pygame.mixer.Sound('Sounds/music_game.mp3')
game_music.play(loops=-1)
game_music.set_volume(0.7)
###
# Flyweight design pattern - buttons objects are flyweights kept and shared
# through this sprite group to allow to easy manage sprites on the screen,
# each object is small and needs to be effectively managed to avoid game lagging,
# also allows to easily compose more buttons added in the future
buttons = pygame.sprite.Group()
play_static_button = Button('Graphics/play_static.png', (520, 300))
options_static_button = Button('Graphics/options_static.png', (520, 400))
about_static_button = Button('Graphics/about_static.png', (520, 500))
exit_static_button = Button('Graphics/exit_static.png', (520, 600))
music_static_button = Button('Graphics/music_static.png', (520, 500))
yes_static_button = Button('Graphics/yes_static.png', (340, 400))
no_static_button = Button('Graphics/no_static.png', (580, 400))
play_pressed_button = Button('Graphics/play_pressed.png', (520, 300))
options_pressed_button = Button('Graphics/options_pressed.png', (520, 400))
about_pressed_button = Button('Graphics/about_pressed.png', (520, 500))
exit_pressed_button = Button('Graphics/exit_pressed.png', (520, 600))
music_pressed_button = Button('Graphics/music_pressed.png', (520, 500))
yes_pressed_button = Button('Graphics/yes_pressed.png', (340, 400))
no_pressed_button = Button('Graphics/no_pressed.png', (580, 400))
menu_buttons = (
    (play_pressed_button, play_static_button),
    (options_pressed_button, options_static_button),
    (about_pressed_button, about_static_button),
    (exit_pressed_button, exit_static_button)
)
settings_buttons = (
    (music_pressed_button, music_static_button),
    (exit_pressed_button, exit_static_button),
)
level_buttons = (
    (yes_pressed_button, yes_static_button),
    (no_pressed_button, no_static_button)
)
level_set = {yes_pressed_button, no_static_button}
settings_set = {music_pressed_button, exit_static_button}
menu_set = {play_pressed_button, options_static_button, about_static_button, exit_static_button}
buttons.add(*menu_set)
selected_button, level_index = 0, 0
basic_quests = quests.Quests()

# print(basic_quests.riddles)

active_level = {
    'menu': 1,
    'settings': 0,
    'about': 0,
    'level': 0,
    'exit_game_dialog': 0,
    'game_over': 0
    }


def display_menu():
    buttons.draw(screen)


def return_to_menu():
    """
    reverses buttons textures on the display to these
    present in main menu
    """
    active_level.update({
        'menu': 1,
        'settings': 0,
        'about': 0,
        'level': 0,
        'exit_game_dialog': 0,
        'game_over': 0
    })
    buttons.empty()
    buttons.add(*menu_set)


def enter_game_over():
    """
    "init and display the game over visual screen
    """
    screen.fill('purple')
    screen.blit(game_over_text, (400, 100))
    pygame.display.update()
    active_level.update({
        'menu': 0,
        'settings': 0,
        'about': 0,
        'level': 0,
        'exit_game_dialog': 0,
        'game_over': 1
    })
    buttons.empty()
    time.sleep(2.2)


while True:
    pygame.display.update()
    if sets.Settings.get_music_setting():
        game_music.set_volume(0.7)
    else:
        game_music.set_volume(0)
    screen.fill('cyan3')
    if active_level['level']:
        screen.fill('yellow')
        if level_index > basic_quests.last_riddle:
            screen.blit(you_won_text, (400, 100))
            time.sleep(3)
            return_to_menu()
            selected_button = 0
        else:
            quiz_text = exit_game_font.render(
                basic_quests.riddles[level_index][0],
                True,
                'gray44'
            )
            screen.blit(quiz_text, (360, 100))
    elif active_level['exit_game_dialog']:
        screen.fill('yellow2')
        screen.blit(exit_game_text, (400, 100))
    elif active_level['game_over']:
        print('Game Over')
        return_to_menu()
        selected_button = 0
    elif active_level['about']:
        screen.blit(about_text, (100, 60))
        screen.blit(about_text2, (100, 100))
    elif active_level['settings']:
        if sets.Settings.get_music_setting():
            screen.blit(music_on_text, (780, 420))
        else:
            screen.blit(music_off_text, (780, 420))

    display_menu()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.KEYDOWN and active_level['about']:
            if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                return_to_menu()
                selected_button = 0
        elif event.type == pygame.KEYDOWN and active_level['menu']:
            if event.key == pygame.K_DOWN:
                buttons.remove(menu_buttons[selected_button][0])
                buttons.add(menu_buttons[selected_button][1])
                selected_button += 1
                selected_button %= 4
                buttons.add(menu_buttons[selected_button][0])
                buttons.remove(menu_buttons[selected_button][1])
            if event.key == pygame.K_UP:
                buttons.remove(menu_buttons[selected_button][0])
                buttons.add(menu_buttons[selected_button][1])
                selected_button += 3
                selected_button %= 4
                buttons.add(menu_buttons[selected_button][0])
                buttons.remove(menu_buttons[selected_button][1])
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if selected_button == 0:
                    active_level.update({'menu': 0, 'level': 1})
                    buttons.empty()
                    buttons.add(*level_set)
                elif selected_button == 3:
                    pygame.quit()
                    sys.exit(0)
                elif selected_button == 1:
                    active_level.update({'menu': 0, 'settings': 1})
                    buttons.empty()
                    buttons.add(*settings_set)
                elif selected_button == 2:
                    active_level.update({'menu': 0, 'about': 1})
                    buttons.empty()
                    buttons.add(exit_pressed_button)
                selected_button = 0
        elif event.type == pygame.KEYDOWN and active_level['settings']:
            if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                buttons.remove(settings_buttons[selected_button][0])
                buttons.add(settings_buttons[selected_button][1])
                selected_button += 1
                selected_button %= 2
                buttons.add(settings_buttons[selected_button][0])
                buttons.remove(settings_buttons[selected_button][1])
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if selected_button == 1:
                    return_to_menu()
                    selected_button = 0
                else:
                    sets.Settings.change_music_setting()
            elif event.key == pygame.K_ESCAPE:
                return_to_menu()
                selected_button = 0
        elif event.type == pygame.KEYDOWN and active_level['level']:
            if event.key == pygame.K_ESCAPE:
                active_level.update({'exit_game_dialog': 1, 'level': 0})
                selected_button = 0
            elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                buttons.remove(level_buttons[selected_button][0])
                buttons.add(level_buttons[selected_button][1])
                selected_button += 1
                selected_button %= 2
                buttons.add(level_buttons[selected_button][0])
                buttons.remove(level_buttons[selected_button][1])
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if selected_button == basic_quests.riddles[level_index][1]:
                    enter_game_over()
                else:
                    level_index += 1
                    selected_button = 0
                    buttons.empty()
                    buttons.add(*level_set)
                    print('next level')
        elif event.type == pygame.KEYDOWN and active_level['exit_game_dialog']:
            if event.key == pygame.K_ESCAPE:
                buttons.empty()
                buttons.add(*level_set)
                active_level.update({'exit_game_dialog': 0, 'level': 1})
                selected_button = 0
            elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                buttons.remove(level_buttons[selected_button][0])
                buttons.add(level_buttons[selected_button][1])
                selected_button += 1
                selected_button %= 2
                buttons.add(level_buttons[selected_button][0])
                buttons.remove(level_buttons[selected_button][1])
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if selected_button == 0:
                    return_to_menu()
                else:
                    buttons.empty()
                    buttons.add(*level_set)
                    active_level.update({'exit_game_dialog': 0, 'level': 1})
                    selected_button = 0


