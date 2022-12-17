"""
project group:
Nidish Chandra Birudaraju
Anuradha Gude
Chaitanya Meda
Vanitha Sannaobappa
"""

from time import sleep
from random import randrange
from typing import Any, List

import pygame
import pygame_menu
from pygame_menu.examples import create_example_window
from dataclasses import dataclass, field

from constants import WINDOW_HEIGHT, WINDOW_WIDTH
from levels.level1 import Level
from resources.dimension import Dimensions

DIFFICULTY = ['EASY']
DIMS=[3]
ROWS=[3]
COLUMNS=[3]
PLAYERS=[2]
FPS = 60


@dataclass
class Scores:
    
    difficulty: str = ""
    max: int = 0 
    min: int = 0
    attempt: int = 0


@dataclass
class Game:

    menu_states: List[str] = field(init=False)
    screen: pygame.Surface = field(init=False)
    play_menu: Any = field(init=False)
    stats: List[Scores] =  field(init=False)
    is_running: bool = True
    is_paused: bool = True
    display_caption_prefix: str = "Lost in Woods"

    play_image = pygame_menu.baseimage.BaseImage(
            image_path="./assets/play-board.png",
            drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY,
            #offset=(0,0)
    )


    # global game theme
    game_theme = pygame_menu.themes.Theme(
            background_color=play_image,
            title_font_color=(0,0,0),
            title_background_color=(46,45,136,0),
            widget_font = pygame_menu.font.FONT_8BIT,
            widget_font_size=30,
            widget_font_color=(27,0,47),
            widget_padding=15)

    selected_menu_state: str = 'main'

    auto_play: bool = False
    selected_level: str = 'EASY'

    # set background surface
    def background(self):
        global surface
        surface.fill((0,0,0))

    # set diificulty level[Easy/Medium/Hard]
    def set_difficulty(self,value, difficulty):
        self.selected_level=difficulty
        DIFFICULTY[0] = difficulty

    # set game row and columns[2-9]
    def set_rows(self,value, row):
        ROWS[0] = row

    def set_columns(self,value, col):
        COLUMNS[0] = col

    # set game dimensions[1-3]
    def change_dims(self,value, col):
        DIMS[0] = col
    
    # set game player[2-4]
    def set_players(self,value, players):
        PLAYERS[0] = players

    # set score
    def set_score(self, index, score):
            self.stats[index].attempt +=1
            self.stats[index].min = min(score, self.stats[index].min) if self.stats[index].min !=0 else score
            self.stats[index].max = max(score, self.stats[index].max) if self.stats[index].max !=0 else score

            try:
                with open(f'./scores/score{index}.txt','w') as file:
                    file.write(f"{self.stats[index].attempt}\n")
                    file.write(f"{self.stats[index].min}\n")
                    file.write(f"{self.stats[index].max}\n")
            except: 
                print("File not found")


    def game_play(self, difficulty, font, test = False):
        """:
        Main game function.
        :param difficulty: Difficulty of the game
        :param font: Pygame font
        :param test: Test method, if ``True`` only one loop is allowed
        """
        assert isinstance(difficulty, list)
        difficulty = difficulty[0]
        assert isinstance(difficulty, str)

        # Define globals
        global main_menu
        global clock


        if difficulty == 'EASY':
            level = Level(autoplay=False,dimensions= Dimensions(COLUMNS[0],ROWS[0]),number_of_players= PLAYERS[0])
            score = level.start(clock)
        elif difficulty == 'MEDIUM':
            level = Level(autoplay=False,dimensions= Dimensions(COLUMNS[0],ROWS[0]),number_of_players= PLAYERS[0])
            score = level.start(clock)
        elif difficulty == 'HARD':
            level = Level(autoplay=False,dimensions= Dimensions(COLUMNS[0],ROWS[0]),number_of_players= PLAYERS[0])
            score = level.start(clock)
        else:
            raise ValueError(f'unknown difficulty {difficulty}')
        f_esc = font.render('Game Ended', True, (255, 255, 255))

        if self.selected_level == "EASY":
            self.set_score(0,score)
        if self.selected_level == "MEDIUM":
            self.set_score(1,score)
        if self.selected_level == "HARD":
            self.set_score(2,score)

        bg_color = (0,0,0)
        self.game_window()
        # Reset main menu and disable
        # You also can set another menu, like a 'pause menu', or just use the same
        # main_menu as the menu that will check all your input.

        self.game_theme = pygame_menu.themes.THEME_DEFAULT.copy()
        main_menu = pygame_menu.Menu(
            height=WINDOW_HEIGHT * 0.8,
            theme=self.game_theme,
            title='Main Menu',
            width=WINDOW_WIDTH * 0.8
        )
        main_menu.add.button('Play', self.play_menu)

        main_menu.add.selector('Difficulty ',
                            [('Easy', 'EASY'),
                                ('Medium', 'MEDIUM'),
                                ('Hard', 'HARD')],
                            onchange=self.set_difficulty,
                            selector_id='select_difficulty')
        main_menu.add.button('Quit', pygame_menu.events.EXIT)

        main_menu.enable()

        while True:
            clock.tick(60)
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    exit()
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        main_menu.enable()
                        return
                        
            if main_menu.is_enabled():
                main_menu.update(events)

            surface.fill(bg_color)

            surface.blit(f_esc, (int((WINDOW_WIDTH - f_esc.get_width()) / 2),
                                int(WINDOW_HEIGHT / 2 + f_esc.get_height())))
            pygame.display.flip()


    def game_window(self):

        self.play_menu = pygame_menu.Menu(
            height=WINDOW_HEIGHT * 0.8,
            title='',
            width=WINDOW_WIDTH * 0.8,
            theme= self.game_theme
        )
        play_submenu = pygame_menu.Menu(
            height=WINDOW_HEIGHT * 0.8,
            theme=self.game_theme,
            title='Scores',
            width=WINDOW_WIDTH * 0.8
        )


        for stat in self.stats:
                min = stat.min
                max = stat.max
                attempt = stat.attempt
                play_submenu.add.label(f'Difficulty Level: {stat.difficulty} | Played : {attempt}') 
                play_submenu.add.label(f'Difficulty Level: {stat.difficulty} | Highest: {min}')
                play_submenu.add.label(f'Difficulty Level: {stat.difficulty} | Lowest : {max}')   
        play_submenu.add.button('Back to menu', pygame_menu.events.RESET)

        self.play_menu.add.selector('Rows: ',
                    [('2',2),('3',3),('4',4),('5',5),('6',6),('7',7),('8',8),('9',9)],
                    onchange=self.set_rows,
                    selector_id='select_row')
        self.play_menu.add.selector('Columns: ',
                        [('2',2),('3',3),('4',4),('5',5),('6',6),('7',7),('8',8),('9',9)],                      
                    onchange=self.set_columns,
                    selector_id='select_cols')
        self.play_menu.add.selector('Players: ',
                        [('2',2),('3',3),('4',4)],
                    onchange=self.set_players,
                    selector_id='select_players')
        self.play_menu.add.button('Scores', play_submenu)
        self.play_menu.add.button('Start',
                         self.game_play,
                         DIFFICULTY,
                            pygame.font.Font(pygame_menu.font.FONT_FRANCHISE, 30))
        self.play_menu.add.button('Back to menu', pygame_menu.events.BACK)



    def main_window(self):

        global clock
        global main_menu
        global surface

        surface = create_example_window('Lost in the Woods', (WINDOW_WIDTH,WINDOW_HEIGHT))
        clock = pygame.time.Clock()


        self.game_window()

        main_menu = pygame_menu.Menu(
            height=WINDOW_HEIGHT * 0.8,
            theme=self.game_theme,
            title='',
            width=WINDOW_WIDTH * 0.8
        )
                    
        self.game_theme.widget_font_size = 19
        

        main_menu.add.selector('Difficulty ',
                            [('Easy', 'EASY'),
                                ('Medium', 'MEDIUM'),
                                ('Hard', 'HARD')],
                            onchange=self.set_difficulty,
                            selector_id='select_difficulty',
                            font_size=25, border_width=1,)
        main_menu.add.button('Play', self.play_menu, font_color=(0,0,0), font_size=30, border_width=1,)
        main_menu.add.button('Exit', pygame_menu.events.EXIT, font_color=(0,0,0), font_size=35, border_width=1,)

    def get_score(self):
        score0 = [0 for i in range(3)]
        score1 = [0 for i in range(3)]
        score2 = [0 for i in range(3)]
        try:
            with open('./scores/score0.txt') as f:
                lines = f.readlines()
                for k,v in enumerate(lines):
                    score0[k] = round(float(v.strip()))
            with open('./scores/score1.txt') as f:
                lines = f.readlines()
                for k,v in enumerate(lines):
                    score1[k] = round(float(v.strip()))
            with open('./scores/score2.txt') as f:
                lines = f.readlines()
                for k,v in enumerate(lines):
                    score2[k] = round(float(v.strip()))
        except FileNotFoundError:
            print("File not found")
    
        self.stats = [ 
            Scores('EASY',score0[0],score0[1],score0[2]),
            Scores('MEDIUM',score1[0],score1[1],score1[2]),
            Scores('HARD',score2[0],score2[1],score2[2]),
        ]



    def start(self):
        pygame.init()
        pygame.mixer.init()
        self.get_score()
        self.main_window()
        pygame.mixer.music.load('./assets/audio.mp3')
        pygame.mixer.music.play(loops=0)
      
        while True:

            # Tick
            clock.tick(FPS)

            # Paint background
            self.background()

            # Application events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()

            # Main menu
            if main_menu.is_enabled():
                main_menu.mainloop(surface, self.background, disable_loop=False, fps_limit=FPS)

            # Flip surface
            pygame.display.flip()

## start the game
if __name__ == "__main__":
    game = Game()
    game.start()