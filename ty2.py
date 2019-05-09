#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2019/5/7 15:57:36

import cocos
import sys
import os
import pyglet
import time
import random
import json

class Highscore(object):
    
    def __init__(self):
        self.highscore_file = ''
        self.level = 'Normal'
        self.name = 'judy'

    def show_highscore(self):
        """load the record file and return _data

        """
        with open(self.highscore_file) as _file:
            try:
                _data = json.load(_file)
            except:
                print('open file failed')
            return _data


    def write_highscore(self, name, highscore):
        """write the name and highscore into the record file

        """
        with open(self.highscore_file) as _file:
            try:
                _data = json.load(_file)
            except:
                print('open file failed')

            data_normal = sorted(_data[0:5])
            data_hard = sorted(_data[5:])
            
            if self.level == 'Normal':
                _ = data_normal
            elif self.level == 'Hard':
                _ = data_hard
            else:
                print('wrong game level')
            #trim the name below 10 chars
            _ = _ + [[int(highscore), name[:10]]]
            # _  sorted
            _ = sorted(_)
            # _ trimed into 5 items)
            _ = _[:5]
            # combine the Normal top5 and the Hard top5
            if self.level == 'Normal':
                _data = _ + data_hard
            elif self.level == 'Hard':
                _data = data_normal + _


        with open(self.highscore_file, 'w') as _file:
            try:
                json.dump(_data, _file)
            except:
                print('write file failed')
        
    def refresh_highscore(self, normal_highscore_label, hard_highscore_label, *args):
        """show the TOP5 high score
        
        """
        _data = self.show_highscore()
        for _ in range(5):
            normal_highscore_label[_].element.text = _data[_][1] + ' ' * (10 - len(_data[_][1])) + str(_data[_][0] // 60) + ':' + str(_data[_][0] % 60) 
        for _ in range(5):
            hard_highscore_label[_].element.text = _data[5 + _][1] + ' ' * (10 - len(_data[5 + _][1])) + str(_data[5 + _][0] // 60) + ':' + str(_data[5 + _][0] % 60) 
        
        if len(args) > 0:
            if self.level == 'Normal':
                _data = _data[:5]
            elif self.level == 'Hard':
                _data = _data[5:]
            else:
                print('unknown game level')
                sys.exit()

            for _ in _data:
                if _[1] == self.name:
                    args[0].element.text = str(_[0] // 60) + ':' + str(_[0] % 60)
                    break


    def get_highscore(self):
        """return the fifth high score from the record file
            used to judge TOP5 or not
        """
        with open(self.highscore_file) as _file:
            try:
                _data = json.load(_file)
            except:
                print('open file failed')

            data_normal = sorted(_data[0:5])
            data_hard = sorted(_data[5:])
            if self.level == 'Normal':
                return data_normal[4][0]
            elif self.level == 'Hard':
                return data_hard[4][0]
            else:
                print('wrong game level')

class Main(cocos.layer.Layer):

    is_event_handler = True
    default_color = (0, 0, 0, 255)
    highlight_color = (200, 30, 30, 255)

    def __init__(self, highscore, max_len=20):

        super(Main, self).__init__()
        self.keys_pressed = set()
        self.input_text = ''
        self.prac_str = ''
        self.name_input_text = ''
        self.game_started = False
        self.highscore = highscore
        self.highscore.name ='crix'
        self.highscore.highscore_file = 'highscore.tp'

        self.max_len = max_len

        self.name_displayed = False
        self.menu_displayed = False
        self.main_displayed = False
        self.time_passed = 0
        self.schedule_interval(self.refresh_time, 1)

        self.Time_Label = cocos.text.Label('00:00',
            font_size = 16,
            font_name = 'Verdana', 
            bold = False, 
            color = self.default_color, 
            x = 165, y = 205)
        self.add(self.Time_Label)

        self.best_time_label = cocos.text.Label('99:59',
            font_size = 16,
            font_name = 'Verdana', 
            bold = False, 
            color = self.default_color, 
            x = 555, y = 205)
        self.add(self.best_time_label)

        self.level_label = cocos.text.Label(self.highscore.level,
            font_size = 20,
            font_name = 'Verdana', 
            bold = True, 
            color = Main.highlight_color, 
            x = 355, y = 240)
        self.add(self.level_label)

        self.image = pyglet.resource.image("bg.png")

        self.start_sprite = self.gen_anime_sprite('start.png', 2, 1, 0.5, True, 400, 280)
        self.add(self.start_sprite)
        #self.start_sprite.visible = False

        self.alpha_image = pyglet.image.ImageGrid(pyglet.resource.image('alpha.png'), 2, 27)   

        self.t2_anime = []
        self.t2_anime.append(self.alpha_image[26])
        self.t2_anime.append(self.alpha_image[53])
        self.t2_seq = pyglet.image.Animation.from_image_sequence(self.t2_anime, 0.5, True)
        self.t2_sprite = cocos.sprite.Sprite(self.t2_seq, position = (650, 400))
        self.add(self.t2_sprite)
        self.t2_sprite.scale = 1.5
        #self.t2_sprite.visible = False

        self.alpha_str = []
        for _ in range(self.max_len):
            self.alpha_str.append(cocos.sprite.Sprite(self.alpha_image[_], position = (0, 0)))
            self.add(self.alpha_str[_])
            #self.alpha_str[_].visible = False
        self.show_menu()
        self.game_status = 'menu'

        # initialise the highscore labels
        _data = self.highscore.show_highscore()
        self.normal_highscore_label = []
        self.hard_highscore_label = []

        for _ in range(5):
            #print('normal', _)
            self.normal_highscore_label.append(cocos.text.Label(_data[_][1] + ' ' * (10 - len(_data[_][1])) + str(_data[_][0] // 60) + ':' + str(_data[_][0] % 60), 
               font_size = 16, 
               font_name = 'Verdana', 
               bold = False, 
               color = Main.default_color, 
               x = 220, y = 110 - (_ * 25)))
            self.add(self.normal_highscore_label[_])

        for _ in range(5):
            #print('hard', _)
            self.hard_highscore_label.append(cocos.text.Label(_data[5 + _][1] + ' ' * (10 - len(_data[5 + _][1])) + str(_data[5 + _][0] // 60) + ':' + str(_data[5 + _][0] % 60), 
               font_size = 16, 
               font_name = 'Verdana', 
               bold = False, 
               color = Main.default_color, 
               x = 450, y = 110 - (_ * 25)))
            self.add(self.hard_highscore_label[_])
        

    def show_menu(self):

        self.game_started = False
        self.show_alpha('typingpractice', 100, 450)
        for _ in range(6):
            self.alpha_str[_].position = 280 + _ * 50, 500
            self.alpha_str[_].scale = random.randrange(8,20) / 10
            self.alpha_str[_].rotation = random.randrange(-30, 30)

        for _ in range(8):
            self.alpha_str[6 + _].position = 230 + _ * 50, 400 
            self.alpha_str[6 + _].scale = random.randrange(8,20) / 10
            self.alpha_str[6 + _].rotation = random.randrange(-30, 30)

        self.t2_sprite.visible = True
        self.start_sprite.visible = True
        self.menu_displayed = True
        self.level_label.visible = True
        self.game_status = 'menu'

    def show_or_hide(self, _bool, *arg):
        for _ in arg:
            if _bool:
                _.visible = True
            else:
                _.visible = False


    def hide_menu(self):
        for _ in range(14):
            self.show_or_hide(False, self.alpha_str[_])
        self.show_or_hide(False, self.t2_sprite, self.start_sprite)
        self.level_label.visible = False
        self.menu_displayed = False

    def gen_anime_sprite(self, img, grid_x, grid_y, delay, loop, pos_x, pos_y):

        _image = pyglet.resource.image(img)
        _anime = pyglet.image.ImageGrid(_image, grid_x, grid_y)
        _seq = pyglet.image.Animation.from_image_sequence(_anime, delay, loop)
        return cocos.sprite.Sprite(_seq, position = (pos_x, pos_y))
        
    def show_alpha(self, _str, pos_x=100, pos_y=400):
        if len(_str) > self.max_len:
            _str = _str[:max_len]
        print('show alpha:', _str)
        for _ in range(len(_str)):
            if _str[_] in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
                _str_index = ord(_str[_])
                if _str_index >= 97:
                    _str_index -= 97
                else:
                    _str_index -= 38
            else:
                _str_index = 26

            self.alpha_str[_].visible = True
            self.alpha_str[_].image = self.alpha_image[_str_index]
            self.alpha_str[_].position = pos_x + _ * 50, pos_y
            self.alpha_str[_].scale = random.randrange(8,20) / 10
            self.alpha_str[_].rotation = random.randrange(-30, 30)

    def show_main(self):
        
        if self.game_started:
            return 1
        else:
            self.game_started = True
            self.time_passed = 0
            # generate a string to be practiced
            _str = []
            if self.highscore.level == 'Normal':
                #print('Normal game started')
                for _ in range(self.max_len):
                    _str.append(chr(random.randint(97,122))) 
                random.shuffle(_str)
                _str = ''.join(_str)
            elif self.highscore.level == 'Hard':
                #print('Hard game started')
                for _ in range(26):
                    _str.append(chr(97 + _))
                    _str.append(chr(65 + _))
                random.shuffle(_str)
                _str = _str[:self.max_len]
                _str = ''.join(_str)
            else:
                print('unknown game level')
                sys.exit()
            self.prac_str = _str
            print('the _str is:', _str)
            self.show_alpha(_str, 100, 400)

        self.main_displayed = True
        self.game_status ='main'

        
        
    def hide_main(self):
        
        for _ in range(self.max_len):
            self.show_or_hide(False, self.alpha_str[_])
        self.main_displayed = False


    def show_highscore_name(self, _str):
        _str = _str[:6]
        for _ in range(14, self.max_len):
            self.alpha_str[_].visible = False
        for _ in range(len(_str)):
            _str_index = ord(_str[_])
            if _str_index >= 97:
                _str_index -= 97
            else:
                _str_index -= 38

            self.alpha_str[_ + 14].visible = True
            self.alpha_str[_ + 14].image = self.alpha_image[_str_index]
            self.alpha_str[_ + 14].position = 100 + _ * 50, 300
            #self.alpha_str[_ + 14].scale = random.randrange(8,20) / 10
            #self.alpha_str[_ + 14].rotation = random.randrange(-30, 30)
        

    def refresh_time(self, dt):
        if self.game_started:
            self.time_passed += dt
            #self.start_timer = 0
            self.Time_Label.element.text = str(int(self.time_passed // 60)) + ' : ' + str(int(self.time_passed % 60)) 
            self.highscore.refresh_highscore(self.normal_highscore_label, self.hard_highscore_label, self.best_time_label)

        if self.game_status == 'menu' and self.menu_displayed == False:
            self.show_menu()
            self.hide_main()
            return 1

        if self.game_status == 'main' and self.main_displayed == False:
            self.show_main()
            self.hide_menu()
            return 1

        if self.game_status == 'highscore' and self.name_displayed == False:
            self.show_highscore_name(self.highscore.name)
            return 1



    def on_key_press(self, key, modifiers):

        _str='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.keys_pressed.add(key)
        key_names = [pyglet.window.key.symbol_string(k) for k in self.keys_pressed]
        
        if self.game_status == 'main':
            if 'SPACE' in key_names:
                self.hide_main()
                self.show_menu()
            elif 'ENTER' in key_names and self.game_started == False:
                self.show_main()
            elif self.game_started:
                #print('main screen key pressed', key_names)
                if len(key_names) > 1 and ('LSHIFT' in key_names) and (key_names[1] in _str or key_names[0] in _str):
                    if key_names[0] in _str:
                        self.input_text = key_names[0]
                    else:
                        self.input_text = key_names[1]
                elif len(key_names) == 1 and (key_names[0] in _str):
                    self.input_text = key_names[0].lower()

                #print(self.input_text, self.prac_str)
                if len(self.prac_str) > 0:
                    if self.input_text == self.prac_str[0]:
                        self.alpha_str[self.max_len - len(self.prac_str)].image = self.alpha_image[26]
                        self.prac_str = self.prac_str[1:]
                        if len(self.prac_str) > 10:
                            for _ in range(self.max_len):
                                _pos_x, _pos_y = self.alpha_str[_].position
                                if _pos_x - 50 >=0:
                                    self.alpha_str[_].position = _pos_x - 50, _pos_y
                                else:
                                    self.alpha_str[_].position = 0, _pos_y
                        elif len(self.prac_str) == 0:
                            # typing complete
                            #print('bingo!')
                            if self.time_passed <= self.highscore.get_highscore():
                                self.highscore.game_time = self.time_passed
                                self.show_alpha('HIGHSCORE NAME')
                                self.name_input_text = self.highscore.name
                                #print('now game changes into ' + self.game.status + ' mode')
                                self.game_status = 'highscore'
                            else:
                                self.show_alpha('continue')
                                self.game_status = 'main'
                            self.game_started = False
                    else:
                        # wrong typing
                        action = cocos.actions.RotateBy(15, 0.03) + cocos.actions.RotateBy( -15, 0.03)
                        self.alpha_str[self.max_len - len(self.prac_str)].do(action)
        # <<highscore mode>>
        # do key events when the game is in 'highscore' mode
        elif self.game_status == 'highscore' and self.game_started == False:
            if 'SPACE' in key_names:
                self.hide_main()
                self.show_menu()
            elif 'ENTER' in key_names:
                # confirm the name when get high score
                #print('highscore mode enter pressed')
                self.highscore.write_highscore(self.highscore.name, self.highscore.game_time)
                self.highscore.refresh_highscore(self.normal_highscore_label, self.hard_highscore_label, self.best_time_label)
                #print('highscore name sprite invisible')
                for _ in range(0, self.max_len):
                    self.alpha_str[_].visible = False
                self.show_alpha('continue')
                #print('highscore mode changed into main mode')
                self.game_status = 'main'
               
                #self.show_main()
            elif 'BACKSPACE' in key_names:
                if len(self.name_input_text) > 0:
                    self.name_input_text = self.name_input_text[:len(self.name_input_text) - 1]
                self.highscore.name = self.name_input_text
                self.show_highscore_name(self.highscore.name)
            elif len(key_names) > 1 and ('LSHIFT' in key_names) and (key_names[1] in _str or key_names[0] in _str) and len(self.name_input_text) < 6:
                if key_names[0] in _str:
                    self.name_input_text += key_names[0]
                else:
                    self.name_input_text += key_names[1]
                self.highscore.name = self.name_input_text
                self.show_highscore_name(self.highscore.name)
            elif len(key_names) == 1 and (key_names[0] in _str) and len(self.name_input_text) < 6:
                self.name_input_text += key_names[0].lower()
                self.highscore.name = self.name_input_text
                self.show_highscore_name(self.highscore.name)
        # <<menu mode>>
        # do key events when game is in 'menu' mode
        elif self.game_status == 'menu':
            if 'ENTER' in key_names:
                self.hide_menu()
                self.show_main()
            elif 'LEFT' in key_names:
                if self.highscore.level != 'Normal':
                    self.highscore.level = 'Normal'
                    self.level_label.element.text = self.highscore.level
            elif 'RIGHT' in key_names:
                if self.highscore.level != 'Hard':
                    self.highscore.level = 'Hard'
                    self.level_label.element.text = self.highscore.level
        # <<unknown mode for future expansion>>
        else:
            print("unkown game status")
            sys.exit()

    def on_key_release(self, key, modifiers):

        if len(self.keys_pressed) > 0:
            self.keys_pressed.remove(key)
            self.input_text = ''

    def draw(self):

        self.image.blit(0,0)

if __name__ == '__main__':

    # change the working dir to the exe temp dir for the pyinstaller 
    if getattr(sys, 'frozen', False):
        os.chdir(sys._MEIPASS)

    cocos.director.director.init(width = 800, height = 600, caption = 'sprite test')

    my_highscore = Highscore()
    main_layer = Main(my_highscore)
    main_scene = cocos.scene.Scene(main_layer)
    #print ('game initialised')
    cocos.director.director.run(main_scene)

    #print('game end')

