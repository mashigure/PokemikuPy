#! /usr/bin/env python
# coding: utf-8
# coding=utf-8
# -*- coding: utf-8 -*-
# vim: fileencoding=utf-8

import pygame
import pygame.midi
from pygame.locals import *
import os
import codecs
import time
import random
import ConfigParser


# 描画関連の定数
WINDOW_TITLE     = 'Poke miku'
BG_COLOUR        = (255, 255, 255)  # 背景色
WHITEKEY_COLOUR  = (192,192,192)    # 白鍵の表示色
PLAYING_COLOUR   = (0,255,160)      # 押されている（鳴らしている）Keyの表示色
NEXT_COLOUR      = (255,0,0)        # 次に押すKeyの表示色
LYRICS_COLOUR    = (0,180,120)      # 歌詞のフォントカラー
TEXT_COLOUR      = (32,94,32)       # 文字のフォントカラー

FONT_SIZE_TEXT   = 16
FONT_FILE        = 'ipagp.ttf'      # 使用する日本語TTFフォントファイル名
                                    # このプログラムと同じフォルダに入れる。
                                    # DL元 http://forest.watch.impress.co.jp/library/software/ipafont/

MODE_INST        = 0
MODE_SNGL        = 1
MODE_SONG        = 2

FPS = 30

# MIDIキーボードのリスト
KEYBOARDS = ["CH345","Keystation","Xkey"]

## eVY1用文字テーブル
evy1_ch = '''
a,i,M,e,o
k a,k\' i,k M,k e,k o
g a,g\' i,g M,g e,g o
k\' a,k\' M,k\' o
N\' a,g\' M,N\' o
s a,s i,s M,s e,s o
dz a,dz i,dz M,dz e,dz o
S a,S i,S M,S e,S o
dZ a,dZ i,dZ M,dZ e,dZ o
t a,t\' i,t M,t e,t o
d a,d i,d M,d e,d o
t\' M,d\' M
tS a,tS i,tS M,tS e,tS o
ts a,ts i,ts M,ts e,ts o
n a,J i,n M,n e,n o
J a,J M,J o
h a,C i,p\\ M,h e,h o
b a,b\' i,b M,b e,b o
p a,p\' i,p M,p e,p o
C a,C M,C o
b\' a,b\' M,b\' o
p\' a,p\' M,p\' o
p\\ a,p\\ i,p\\\' M,p\\ e,p\\ o
m a,m\' i,m M,m e,m o
m\' a,m\' M,m\' o
j a,j M,j o
4 a,4\' i,4 M,4 e,4 o
4\' a,4\' M,4\' o
w a,w i,w e,w o,N\\,m,N,J,n'''.strip().replace(',','\n').split('\n')

ch_tbl = u'''
あ,い,う,え,お
か,き,く,け,こ
が,ぎ,ぐ,げ,ご
きゃ,きゅ,きょ
ぎゃ,ぎゅ,ぎょ
さ,すぃ,す,せ,そ
ざ,ずぃ,ず,ぜ,ぞ
しゃ,し,しゅ,しぇ,しょ
じゃ,じ,じゅ,じぇ,じょ
た,てぃ,とぅ,て,と
だ,でぃ,どぅ,で,ど
てゅ,でゅ
ちゃ,ち,ちゅ,ちぇ,ちょ
つぁ,つぃ,つ,つぇ,つぉ
な,に,ぬ,ね,の
にゃ,にゅ,にょ
は,ひ,ふ,へ,ほ
ば,び,ぶ,べ,ぼ
ぱ,ぴ,ぷ,ぺ,ぽ
ひゃ,ひゅ,ひょ
びゃ,びゅ,びょ
ぴゃ,ぴゅ,ぴょ
ふぁ,ふぃ,ふゅ,ふぇ,ふぉ
ま,み,む,め,も
みゃ,みゅ,みょ
や,ゆ,よ
ら,り,る,れ,ろ
りゃ,りゅ,りょ
わ,うぃ,うぇ,うぉ,ん,ん,ん,ん,ん'''.strip().replace(',','\n').split('\n')

# 楽器一覧
inst_name = '''
Acostic Grand Piano,Bright Acostic Piano,Electric Grand Piano,Honky-Tonk Piano,Electric Piano 1,Electric Piano 2,Harpsicord,Clavi
Celesta,Glockenspiel,Music Box,Vibraphone,Marimba,Xylophone,Tubular Bells,Dulcimer
Drawber Organ,Percussive Organ,Rock Organ,Church Organ,Reed Organ,Accordion,Harmonica,Tango Accordion
Acostic Guitar (nylon),Acostic Guitar (steel),Electric Guitar (jazz),Electric Guitar (clean),Electric Guitar (muted),Overdriven Guitar,Distortion Guitar,Guitar Harmonics
Acosic Bass,Electric Bass (finger),Electric Bass (pick),Fretless Bass,Slap Bass 1,Slap Bass 2,Synth Bass 1,Synth Bass 2
Violin,Viola,Cello,Contrabass,Tremoro Strings,Pizzicato Strings,Orchestral Harp,Timpani
String Ensamble 1,String Ensamble 2,Synth Strings 1,Synth Strings 2,Choir Aahs,Voice Oohs,Synth Voice,Orchestra Hit
Trumpet,Trombone,Tuba,Muted Trumpet,French Horn,Brass Section,Synth Brass 1,Synth Brass 2
Soprano Sax,Alto Sax,Tenor Sax,Baritone Sax,Oboe,English Horn,Bassoon,Clarinet
Piccolo,Flute,Recorder,Pan Flute,Bottle Blow,Shakuhachi,Whistle,Ocarina
Square Lead,Sawtooth Lead,Caliope Lead,Chiff Lead,Charang Lead,Voice Lead,Fifth Lead,Bass + Lead
New age,Warm,Polysynth,Choir,Bowed,Metalic,Halo,Sweep
Rain,Soundtrack,Crystal,Atmosphere,Brightness,Goblins,Echoes,Sci-fi
Sitar,Banjo,Shamisen,Koto,Kalimba,Bagpipe,Fiddle,Shanai
Tinkle Bell,Agogo,Steel Drums,Woodblock,Taiko Drum,Melodic Tom,Synth Drum,Reverse Cymbal
Guitar Fret Noise,Breath Noise,Seashore,Bird Tweet,Telephone Ring,Helicopter,Applause,Gun Shot'''.strip().replace(',','\n').split('\n')

# Single歌声一覧
single_sound = [u"ドレミ（♯）",u"ドレミ（♭）",u"ラ",u"て",u"Random"]

# 設定管理クラス -------------------------------------------------------------------------------------
class ConfigMng(object):

    def __init__(self, conf_file):

        # 設定ファイルが見つからなかったときのデフォルト値を適当に設定
        self.conf_file      = conf_file
        self.screen_width   = 800
        self.screen_height  = 480
        self.is_screen_full = False
        self.isGamePadConf  = self.isGamepadConf(0)
        self.isGamePadConf2 = self.isGamepadConf(1)
        self.song_file_1    = ""
        self.song_file_2    = ""
        self.song_file_3    = ""
        self.song_file_4    = ""
        self.song_file_5    = ""
        self.song_file_6    = ""
        self.song_file_7    = ""
        self.song_file_8    = ""

        self.setGempadXInput()

        initfile = ConfigParser.SafeConfigParser()
        initfile.read(conf_file)

        if initfile.has_option('SCREEN','width'):
            self.screen_width = initfile.getint('SCREEN', 'width')

        if initfile.has_option('SCREEN','height'):
            self.screen_height = initfile.getint('SCREEN', 'height')

        if (initfile.has_option('SCREEN','full_screen')) and (initfile.get('SCREEN', 'full_screen') == 'True'):
            self.is_screen_full = True

        if initfile.has_option('SONG','file1'):
            self.song_file_1 = initfile.get('SONG', 'file1')

        if initfile.has_option('SONG','file2'):
            self.song_file_2 = initfile.get('SONG', 'file2')

        if initfile.has_option('SONG','file3'):
            self.song_file_3 = initfile.get('SONG', 'file3')

        if initfile.has_option('SONG','file4'):
            self.song_file_4 = initfile.get('SONG', 'file4')

        if initfile.has_option('SONG','file5'):
            self.song_file_5 = initfile.get('SONG', 'file5')

        if initfile.has_option('SONG','file6'):
            self.song_file_6 = initfile.get('SONG', 'file6')

        if initfile.has_option('SONG','file7'):
            self.song_file_7 = initfile.get('SONG', 'file7')

        if initfile.has_option('SONG','file8'):
            self.song_file_8 = initfile.get('SONG', 'file8')

        self.keyboard_top    = self.screen_height / 2
        self.white_height    = self.keyboard_top - 2
        self.black_height    = self.white_height / 2
        self.fontsize_lyrics = self.screen_height * 5 / 13
        self.fontsize_follow = self.screen_height * 2 / 13

    # ゲームパッドのコンフィグが存在するかどうかを確認する -----------------------------------------------
    def isGamepadConf(self, no=0):

        initfile = ConfigParser.SafeConfigParser()
        initfile.read(self.conf_file)

        if no == 0:
            if initfile.has_option('GAMEPAD','button_G') == False:
                return False

            if initfile.has_option('GAMEPAD','button_A') == False:
                return False

            if initfile.has_option('GAMEPAD','button_B') == False:
                return False

            if initfile.has_option('GAMEPAD','button_C') == False:
                return False

        else:
            if initfile.has_option('GAMEPAD2','button_G') == False:
                return False

            if initfile.has_option('GAMEPAD2','button_A') == False:
                return False

            if initfile.has_option('GAMEPAD2','button_B') == False:
                return False

            if initfile.has_option('GAMEPAD2','button_C') == False:
                return False

        return True

    # ゲームパッドのボタン配置をXInputに設定する -------------------------------------------------------
    def setGempadXInput(self):
        self.gamepad_g      = 2    # ソの音：スーファミで言うYボタン
        self.gamepad_a      = 0    # ラの音：スーファミで言うBボタン
        self.gamepad_b      = 1    # シの音：スーファミで言うAボタン
        self.gamepad_c      = 3    # ドの音：スーファミで言うXボタン
        self.gamepad_one_up = 4    # 半音UPボタン（L）
        self.gamepad_oct_up = 5    # オクターブUPボタン（R）
        self.gamepad_select = 6    # SELECTボタン
        self.gamepad_start  = 7    # STARTボタン
        self.selected_pad   = 0

    # ゲームパッドのボタン配置をBuffalo SNESに設定する -------------------------------------------------
    def setGempadSNES(self):
        self.gamepad_g      = 3    # ソの音：スーファミで言うYボタン
        self.gamepad_a      = 1    # ラの音：スーファミで言うBボタン
        self.gamepad_b      = 0    # シの音：スーファミで言うAボタン
        self.gamepad_c      = 2    # ドの音：スーファミで言うXボタン
        self.gamepad_one_up = 4    # 半音UPボタン（L）
        self.gamepad_oct_up = 5    # オクターブUPボタン（R）
        self.gamepad_select = 6    # SELECTボタン
        self.gamepad_start  = 7    # STARTボタン
        self.selected_pad   = 1

    # ゲームパッドのボタン配置をConfig.iniをもとに設定する ---------------------------------------------
    def setGempadByConf(self, no=0):

        initfile = ConfigParser.SafeConfigParser()
        initfile.read(self.conf_file)

        if no == 0:
            if initfile.has_option('GAMEPAD','button_G'):
                self.gamepad_g = initfile.getint('GAMEPAD', 'button_G')

            if initfile.has_option('GAMEPAD','button_A'):
                self.gamepad_a = initfile.getint('GAMEPAD', 'button_A')

            if initfile.has_option('GAMEPAD','button_B'):
                self.gamepad_b = initfile.getint('GAMEPAD', 'button_B')

            if initfile.has_option('GAMEPAD','button_C'):
                self.gamepad_c = initfile.getint('GAMEPAD', 'button_C')

            if initfile.has_option('GAMEPAD','one_up'):
                self.gamepad_one_up = initfile.getint('GAMEPAD', 'one_up')

            if initfile.has_option('GAMEPAD','oct_up'):
                self.gamepad_oct_up = initfile.getint('GAMEPAD', 'oct_up')

            if initfile.has_option('GAMEPAD','select'):
                self.gamepad_select = initfile.getint('GAMEPAD', 'select')

            if initfile.has_option('GAMEPAD','start'):
                self.gamepad_start = initfile.getint('GAMEPAD', 'start')

            self.selected_pad = 2

        else:
            if initfile.has_option('GAMEPAD2','button_G'):
                self.gamepad_g = initfile.getint('GAMEPAD2', 'button_G')

            if initfile.has_option('GAMEPAD2','button_A'):
                self.gamepad_a = initfile.getint('GAMEPAD2', 'button_A')

            if initfile.has_option('GAMEPAD2','button_B'):
                self.gamepad_b = initfile.getint('GAMEPAD2', 'button_B')

            if initfile.has_option('GAMEPAD2','button_C'):
                self.gamepad_c = initfile.getint('GAMEPAD2', 'button_C')

            if initfile.has_option('GAMEPAD2','one_up'):
                self.gamepad_one_up = initfile.getint('GAMEPAD2', 'one_up')

            if initfile.has_option('GAMEPAD2','oct_up'):
                self.gamepad_oct_up = initfile.getint('GAMEPAD2', 'oct_up')

            if initfile.has_option('GAMEPAD2','select'):
                self.gamepad_select = initfile.getint('GAMEPAD2', 'select')

            if initfile.has_option('GAMEPAD2','start'):
                self.gamepad_start = initfile.getint('GAMEPAD2', 'start')

            self.selected_pad = 3


# ボタンクラス ---------------------------------------------------------------------------------------
class Button(object):

    def __init__(self, x, y, width=36, height=36, file_name="", offset=0):
        
        self.x       = x
        self.y       = y
        self.width   = width
        self.height  = height
        self.offset  = 0
        self.isImage = False

        if file_name != "":
            self.isImage = True
            self.img     = pygame.image.load(file_name)
            self.offset  = offset


    # 引数の座標がボタンの範囲内かどうかを確認
    def check_within(self, x, y):

        if (x < self.x) or (y < self.y) or (self.x + self.width < x) or (self.y + self.height < y):
            return False

        return True


    # ボタンの表示
    def view(self, screen, active=False):
        
        if self.isImage:
            if active:
                screen.blit(self.img, (self.x, self.y), (self.width, self.offset, self.width, self.height))
            else:
                screen.blit(self.img, (self.x, self.y), (0, self.offset, self.width, self.height))
        else:
            if active:
                pygame.draw.rect(screen, (0,180,120), Rect(self.x, self.y, self.width, self.height))
            else:
                pygame.draw.rect(screen, (0,180,120), Rect(self.x, self.y, self.width, self.height), 2)


# 描画クラス -----------------------------------------------------------------------------------------
class PokemikuPyViewer:

    def __init__(self, conf_mng):

        self.song_title  = single_sound[0]
        self.disp_str    = u""
        self.follow_str  = u""
        self.playing_key = []
        self.transpose   = 0
        self.follow_key  = -1
        self.config      = conf_mng

        self.setLayout(0)

        self.close_button  = Button(self.config.screen_width- 45,  5,  36, 36, "img/menu.png", 0*36)
        self.restart_btn   = Button(self.config.screen_width- 90,  5,  36, 36, "img/menu.png", 1*36)
        self.config_button = Button( 10,  5,  36, 36, "img/menu.png", 2*36)
        self.ton_conf_btn  = Button( 55,  5,  36, 36, "img/menu.png", 3*36)
        self.select_inst   = Button( 10, 55, 110, 36, "img/select.png", 0*36)
        self.select_sngl   = Button(130, 55, 110, 36, "img/select.png", 1*36)
        self.select_song   = Button(250, 55, 110, 36, "img/select.png", 2*36)
        self.inst_typ0_btn = Button( 10,105,  50, 36, "img/InstType.png",  8*36)
        self.inst_typ1_btn = Button( 70,105,  50, 36, "img/InstType.png",  9*36)
        self.inst_typ2_btn = Button(130,105,  50, 36, "img/InstType.png", 10*36)
        self.inst_typ3_btn = Button(190,105,  50, 36, "img/InstType.png", 11*36)
        self.inst_typ4_btn = Button(250,105,  50, 36, "img/InstType.png", 12*36)
        self.inst_typ5_btn = Button(310,105,  50, 36, "img/InstType.png", 13*36)
        self.inst_typ6_btn = Button(370,105,  50, 36, "img/InstType.png", 14*36)
        self.inst_typ7_btn = Button(430,105,  50, 36, "img/InstType.png", 15*36)
        self.inst_typ8_btn = Button( 10,145,  50, 36, "img/InstType.png", 16*36)
        self.inst_typ9_btn = Button( 70,145,  50, 36, "img/InstType.png", 17*36)
        self.inst_typA_btn = Button(130,145,  50, 36, "img/InstType.png", 18*36)
        self.inst_typB_btn = Button(190,145,  50, 36, "img/InstType.png", 19*36)
        self.inst_typC_btn = Button(250,145,  50, 36, "img/InstType.png", 20*36)
        self.inst_typD_btn = Button(310,145,  50, 36, "img/InstType.png", 21*36)
        self.inst_typE_btn = Button(370,145,  50, 36, "img/InstType.png", 22*36)
        self.inst_typF_btn = Button(430,145,  50, 36, "img/InstType.png", 23*36)
        self.select_g0_btn = Button( 10,190,  50, 36, "img/InstType.png",  0*36)
        self.select_g1_btn = Button( 70,190,  50, 36, "img/InstType.png",  1*36)
        self.select_g2_btn = Button(130,190,  50, 36, "img/InstType.png",  2*36)
        self.select_g3_btn = Button(190,190,  50, 36, "img/InstType.png",  3*36)
        self.select_g4_btn = Button(250,190,  50, 36, "img/InstType.png",  4*36)
        self.select_g5_btn = Button(310,190,  50, 36, "img/InstType.png",  5*36)
        self.select_g6_btn = Button(370,190,  50, 36, "img/InstType.png",  6*36)
        self.select_g7_btn = Button(430,190,  50, 36, "img/InstType.png",  7*36)
        self.select_v0_btn = Button( 10,105,  50, 36, "img/InstType.png", 24*36)
        self.select_v1_btn = Button( 70,105,  50, 36, "img/InstType.png", 25*36)
        self.select_v2_btn = Button(130,105,  50, 36, "img/InstType.png", 26*36)
        self.select_v3_btn = Button(190,105,  50, 36, "img/InstType.png", 27*36)
        self.select_v4_btn = Button(250,105,  50, 36, "img/InstType.png", 28*36)
        self.song1_button  = Button( 10,105,  50, 36, "img/InstType.png",  0*36)
        self.song2_button  = Button( 70,105,  50, 36, "img/InstType.png",  1*36)
        self.song3_button  = Button(130,105,  50, 36, "img/InstType.png",  2*36)
        self.song4_button  = Button(190,105,  50, 36, "img/InstType.png",  3*36)
        self.song5_button  = Button(250,105,  50, 36, "img/InstType.png",  4*36)
        self.song6_button  = Button(310,105,  50, 36, "img/InstType.png",  5*36)
        self.song7_button  = Button(370,105,  50, 36, "img/InstType.png",  6*36)
        self.song8_button  = Button(430,105,  50, 36, "img/InstType.png",  7*36)
        self.set_Layout0   = Button( 10, 55, 110, 36, "img/select.png", 4*36)
        self.set_Layout1   = Button(130, 55, 110, 36, "img/select.png", 5*36)
        self.set_Layout2   = Button(250, 55, 110, 36, "img/select.png", 6*36)
        self.set_Layout3   = Button(370, 55, 110, 36, "img/select.png", 7*36)
        self.set_GamePad0  = Button( 10,105, 110, 36, "img/select.png", 8*36)
        self.set_GamePad1  = Button(130,105, 110, 36, "img/select.png", 9*36)
        self.set_GamePad2  = Button(250,105, 110, 36, "img/select.png",10*36)
        self.set_GamePad3  = Button(370,105, 110, 36, "img/select.png",11*36)
        self.mode      = MODE_SNGL
        self.selected  = 0
        self.isTonConf = False
        self.isConfig  = False


    # 表示する鍵盤数の設定 ----------------------------------------------------------------------------
    def setLayout(self, key_layout):

        self.key_layout = key_layout

        if key_layout == 0:
            self.black_keys = ( 1,3,  6,8,10,  13,15,   18,20,22,    )
            self.white_keys = (0,2,4,5,7,9,11,12,14,16,17,19,21,23,24)
            self.base_key  = 60 # 表示上左端の鍵盤のMIDIでの番号
        elif key_layout == 1:
            self.black_keys = ( 1,3,  6,8,10,  13,15,   18,20,22,   25,27,    )
            self.white_keys = (0,2,4,5,7,9,11,12,14,16,17,19,21,23,24,26,28,29)
            self.base_key  = 48 # 表示上左端の鍵盤のMIDIでの番号
        elif key_layout == 2:
            self.black_keys = ( 1,3,5,  8,10,  13,15,17,   20,22,   25,27,29     )
            self.white_keys = (0,2,4,6,7,9,11,12,14,16,18,19,21,23,24,26,28,30,31)
            self.base_key  = 53 # 表示上左端の鍵盤のMIDIでの番号
        else:
            self.black_keys = ( 1,3,  6,8,10,  13,15,   18,20,22,   25,27,   30,32,34     )
            self.white_keys = (0,2,4,5,7,9,11,12,14,16,17,19,21,23,24,26,28,29,31,33,35,36)
            self.base_key  = 48 # 表示上左端の鍵盤のMIDIでの番号

        self.white_width  = self.config.screen_width / len(self.white_keys)
        self.black_width  = self.white_width * 7.0 / 12.0
        keyboard_width    = self.white_width * len(self.white_keys)
        self.left_margin  = (self.config.screen_width-keyboard_width)/2 +1


    # 画面の初期化 -----------------------------------------------------------------------------------
    def initViewer(self, title_text, isConnectGamepad=False):

        self.isGamepad = isConnectGamepad

        # 画面を作る
        if self.config.is_screen_full:
            self.screen = pygame.display.set_mode((self.config.screen_width, self.config.screen_height), FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((self.config.screen_width, self.config.screen_height)) 

        pygame.display.set_caption(title_text) # タイトル
        pygame.display.flip() # 画面を反映

        self.sysfont_lyrics = pygame.font.Font(FONT_FILE, self.config.fontsize_lyrics)
        self.sysfont_follow = pygame.font.Font(FONT_FILE, self.config.fontsize_follow)
        self.sysfont_text   = pygame.font.Font(FONT_FILE, FONT_SIZE_TEXT)
		

    # 画面の描画 -------------------------------------------------------------------------------------
    def view(self):
    
        self.screen.fill(BG_COLOUR)   # 画面の初期化

        # 白鍵
        for i in range(len(self.white_keys)):

            if 0 < self.playing_key.count(self.white_keys[i]+self.base_key):
                pygame.draw.rect(self.screen,  PLAYING_COLOUR, Rect(self.left_margin + i*self.white_width , self.config.keyboard_top, self.white_width-2, self.config.white_height))
            else: 
                pygame.draw.rect(self.screen, WHITEKEY_COLOUR, Rect(self.left_margin + i*self.white_width , self.config.keyboard_top, self.white_width -2, self.config.white_height))

            if (self.mode == MODE_SONG) and (self.disp_str=="") and (self.white_keys[i]+self.base_key == self.follow_key):
                pygame.draw.ellipse(self.screen,  NEXT_COLOUR, Rect(self.left_margin + i*self.white_width , self.config.screen_height -self.white_width-4, self.white_width-2, self.white_width-2), 4)

        # 黒鍵の枠部分（空白）
        for i in self.black_keys:
            pygame.draw.rect(self.screen, BG_COLOUR, Rect(self.left_margin-2 + i*self.black_width, self.config.keyboard_top, self.black_width+2, self.config.black_height+2))

        # 黒鍵
        for i in self.black_keys:

            if 0 < self.playing_key.count(i+self.base_key):
                pygame.draw.rect(self.screen, PLAYING_COLOUR, Rect(self.left_margin + i*self.black_width, self.config.keyboard_top, self.black_width-2, self.config.black_height))
            else:
                pygame.draw.rect(self.screen, (0,0,0), Rect(self.left_margin + i*self.black_width, self.config.keyboard_top, self.black_width-2, self.config.black_height))

            if (self.mode == MODE_SONG) and (self.disp_str=="") and (i+self.base_key == self.follow_key):
                pygame.draw.ellipse(self.screen, NEXT_COLOUR, Rect(self.left_margin + i*self.black_width, self.config.keyboard_top+self.config.black_height-self.black_width-2, self.black_width-2, self.black_width-2), 4)
        
        if (self.isConfig == False) and (self.isTonConf == False):

            # 発声している歌詞を表示
            if self.mode != MODE_INST:
                lryc_img = self.sysfont_lyrics.render(self.disp_str, True, LYRICS_COLOUR)
                drow_x = (self.config.screen_width - lryc_img.get_width()) / 2
                self.screen.blit(lryc_img, (drow_x, 42))

            # 歌詞の続きを表示
            if self.mode == MODE_SONG:
                follow_img = self.sysfont_follow.render(self.follow_str, True, LYRICS_COLOUR)
                drow_x = self.config.screen_width / 2 + self.config.fontsize_lyrics
                drow_y = 42 + (self.config.fontsize_lyrics - self.config.fontsize_follow) / 2
                self.screen.blit(follow_img, (drow_x, drow_y))

            # トランスポーズ（キーのシフト情報）
            if self.transpose != 0:
                text_img = self.sysfont_text.render('transpose: ' + str(self.transpose) + ' ', True, TEXT_COLOUR)
                drow_x = (self.config.screen_width - text_img.get_width() - 8)
                drow_y = self.config.keyboard_top - 48
                self.screen.blit(text_img, (drow_x, drow_y))

        # ボタン類
        self.close_button.view(self.screen)
        self.restart_btn.view(self.screen)
        self.ton_conf_btn.view(self.screen, self.isTonConf)
        self.config_button.view(self.screen, self.isConfig)

        # 楽器名表示
        if self.mode == MODE_INST:
            text_img = self.sysfont_text.render(inst_name[self.selected], True, TEXT_COLOUR)
            drow_x = (self.config.screen_width - text_img.get_width() - 8)
            drow_y = self.config.keyboard_top - 24
            self.screen.blit(text_img, (drow_x, drow_y))

        # 曲名表示
        else:
            text_img = self.sysfont_text.render(self.song_title, True, TEXT_COLOUR)
            drow_x = (self.config.screen_width - text_img.get_width() - 8)
            drow_y = self.config.keyboard_top - 24
            self.screen.blit(text_img, (drow_x, drow_y))

        if self.isTonConf:
            self.select_inst.view(self.screen, self.mode==0)
            self.select_sngl.view(self.screen, self.mode==1)
            if self.config.song_file_1 != "":
                self.select_song.view(self.screen, self.mode==2)

            if self.mode == MODE_INST:
                self.inst_typ0_btn.view(self.screen, self.selected//8== 0)
                self.inst_typ1_btn.view(self.screen, self.selected//8== 1)
                self.inst_typ2_btn.view(self.screen, self.selected//8== 2)
                self.inst_typ3_btn.view(self.screen, self.selected//8== 3)
                self.inst_typ4_btn.view(self.screen, self.selected//8== 4)
                self.inst_typ5_btn.view(self.screen, self.selected//8== 5)
                self.inst_typ6_btn.view(self.screen, self.selected//8== 6)
                self.inst_typ7_btn.view(self.screen, self.selected//8== 7)
                self.inst_typ8_btn.view(self.screen, self.selected//8== 8)
                self.inst_typ9_btn.view(self.screen, self.selected//8== 9)
                self.inst_typA_btn.view(self.screen, self.selected//8==10)
                self.inst_typB_btn.view(self.screen, self.selected//8==11)
                self.inst_typC_btn.view(self.screen, self.selected//8==12)
                self.inst_typD_btn.view(self.screen, self.selected//8==13)
                self.inst_typE_btn.view(self.screen, self.selected//8==14)
                self.inst_typF_btn.view(self.screen, self.selected//8==15)
                self.select_g0_btn.view(self.screen, self.selected%8==0)
                self.select_g1_btn.view(self.screen, self.selected%8==1)
                self.select_g2_btn.view(self.screen, self.selected%8==2)
                self.select_g3_btn.view(self.screen, self.selected%8==3)
                self.select_g4_btn.view(self.screen, self.selected%8==4)
                self.select_g5_btn.view(self.screen, self.selected%8==5)
                self.select_g6_btn.view(self.screen, self.selected%8==6)
                self.select_g7_btn.view(self.screen, self.selected%8==7)

            elif self.mode == MODE_SNGL:
                self.select_v0_btn.view(self.screen, self.selected==0)
                self.select_v1_btn.view(self.screen, self.selected==1)
                self.select_v2_btn.view(self.screen, self.selected==2)
                self.select_v3_btn.view(self.screen, self.selected==3)
                self.select_v4_btn.view(self.screen, self.selected==4)

            elif self.mode == MODE_SONG:
                if self.config.song_file_1 != "":
                    self.song1_button.view(self.screen, self.selected==0)
                if self.config.song_file_2 != "":
                    self.song2_button.view(self.screen, self.selected==1)
                if self.config.song_file_3 != "":
                    self.song3_button.view(self.screen, self.selected==2)
                if self.config.song_file_4 != "":
                    self.song4_button.view(self.screen, self.selected==3)
                if self.config.song_file_5 != "":
                    self.song5_button.view(self.screen, self.selected==4)
                if self.config.song_file_6 != "":
                    self.song6_button.view(self.screen, self.selected==5)
                if self.config.song_file_7 != "":
                    self.song7_button.view(self.screen, self.selected==6)
                if self.config.song_file_8 != "":
                    self.song8_button.view(self.screen, self.selected==7)

        if self.isConfig:
            self.set_Layout0.view(self.screen, self.key_layout==0)
            self.set_Layout1.view(self.screen, self.key_layout==1)
            self.set_Layout2.view(self.screen, self.key_layout==2)
            self.set_Layout3.view(self.screen, self.key_layout==3)

            if self.isGamepad:
                self.set_GamePad0.view(self.screen, self.config.selected_pad==0)
                self.set_GamePad1.view(self.screen, self.config.selected_pad==1)

                if self.config.isGamePadConf:
                    self.set_GamePad2.view(self.screen, self.config.selected_pad==2)

                if self.config.isGamePadConf2:
                    self.set_GamePad3.view(self.screen, self.config.selected_pad==3)

        # display Surface全体を更新して画面に描写
        pygame.display.flip()


    # 座標から音階を算出 ------------------------------------------------------------------------------
    def calcTonleiter(self, x, y):

        if y < self.config.keyboard_top:
            return -1

        if y < self.config.keyboard_top + self.config.black_height:
            for i in self.black_keys:
                if self.left_margin + i*self.black_width <= x and x <= self.left_margin + (i+1)*self.black_width -2:
                    return i + self.base_key

        if y < self.config.keyboard_top + self.config.white_height:
            for i in range(len(self.white_keys)):
                if self.left_margin + i*self.white_width <= x and x <= self.left_margin + (i+1)*self.white_width -2:
                    return self.white_keys[i] + self.base_key

        return -1


    # キーの表示をON状態に ----------------------------------------------------------------------------
    def KeyOn(self, key_no, str=""):

        if self.mode != MODE_INST:
            self.playing_key = []

        if self.playing_key.count(key_no) == 0:
            self.playing_key.append(key_no)

        self.disp_str = str

    # キーをOFFに ------------------------------------------------------------------------------------
    def KeyOff(self, key_no):

        while 0 < self.playing_key.count(key_no):
            self.playing_key.remove(key_no)

        if len(self.playing_key) == 0:
            self.disp_str = u""


# ゲームパッドのボタン状態を管理する変数群 -------------------------------------------------------------
class GamePad:

    def __init__(self):
		
		self.down   = False
		self.left   = False
		self.up     = False
		self.right  = False
		self.y      = False
		self.b      = False
		self.a      = False
		self.x      = False
		self.start  = False
		self.select = False
		self.oct_up = False
		self.one_up = False
		self.oct_dn = False
		self.one_dn = False


# ポケミク 演奏クラス ---------------------------------------------------------------------------------
class PokemikuPy:

    def __init__(self):

        self.sent_note_down  = 0
        self.sent_note_left  = 0
        self.sent_note_up    = 0
        self.sent_note_right = 0
        self.sent_note_y     = 0
        self.sent_note_b     = 0
        self.sent_note_a     = 0
        self.sent_note_x     = 0

        self.transpose       = 0
        self.velosity        = 127
        self.song_data       = []
        self.song_text       = []
        self.song_keys       = []
        self.song_deco       = []
        self.song_itr        = 0

        self.connect_gamepad = False
        self.connect_midiin  = False

        self.config = ConfigMng('./config.ini')
        self.viewer = PokemikuPyViewer(self.config)
            

    # Game Padの初期化 -------------------------------------------------------------------------------
    def init_gamepad(self):

        pygame.joystick.init()
        
        try:
            self.g_pad = pygame.joystick.Joystick(0) # create a joystick instance
            self.g_pad.init() # init instance
            print 'Gamepad Name: ' + self.g_pad.get_name()
            print 'Button Num  : ' + str(self.g_pad.get_numbuttons())
            return True

        except pygame.error:
            print 'Gamepad is not found.'

        return False


    # 出力先となるeVY1モジュール・ポケミクを探して接続する -----------------------------------------------
    def connectMidiOut(self):
        
        self.flag_pokemiku = False
    
        for i in range(pygame.midi.get_count()):
            interf, name, input, output, opened = pygame.midi.get_device_info(i)
            
            if output and name.startswith('eVY1'):
                self.midiout = pygame.midi.Output(i)
                return True
            
            if output and name.startswith('NSX-39'):
                self.midiout = pygame.midi.Output(i)
                self.flag_pokemiku = True
                return True

        print 'NSX-39/eVY1 is not found.'
        return False
                

    # 入力元となる鍵盤などを探して接続する --------------------------------------------------------------
    def connectMidiIn(self):
    
        for i in range(pygame.midi.get_count()):
            interf, name, input, output, opened = pygame.midi.get_device_info(i)

            for keyboard_name in KEYBOARDS:

                if input and name.startswith(keyboard_name):
                    self.midiin = pygame.midi.Input(i)
                    return True

        print 'MIDI Keyboard is not found.'
        return False
        

    # MIDIの初期化 -----------------------------------------------------------------------------------
    def init_midi(self):

        pygame.midi.init()
        self.midiout = pygame.midi.Output(pygame.midi.get_default_output_id())

        if self.connectMidiOut() == False:
            return False

        self.connect_midiin = self.connectMidiIn()

        # メインボリューム 
        pygame.midi.Output.write_short(self.midiout, 0xb0, 0x07, 0x7f)
        pygame.midi.Output.write_short(self.midiout, 0xb1, 0x07, 0x7f)

        return True
        

    # 音を鳴らす処理 ---------------------------------------------------------------------------------
    def sendNoteOn(self, key_no, velocity=0x7f):

        if self.viewer.mode == MODE_SNGL:
            if self.viewer.selected == 0:
                l_no_list = (50, 50, 114, 114, 101, 95, 95, 25, 25, 111, 111, 32)
                l_list    = (u"ド", u"♯ド", u"レ", u"♯レ", u"ミ", u"ファ", u"♯ファ", u"ソ", u"♯ソ", u"ラ", u"♯ラ", u"シ")
                lyric_no  = l_no_list[key_no % 12]
                lyric     = l_list[key_no % 12]
            elif self.viewer.selected == 1:
                l_no_list = (50, 114, 114, 101, 101, 95, 25, 25, 111, 111, 32, 32)
                l_list    = (u"ド", u"♭レ", u"レ", u"♭ミ", u"ミ", u"ファ", u"♭ソ", u"ソ", u"♭ラ", u"ラ", u"♭シ", u"シ")
                lyric_no  = l_no_list[key_no % 12]
                lyric     = l_list[key_no % 12]
            elif self.viewer.selected == 2:
                lyric_no  = 111
                lyric     = u"ラ"
            elif self.viewer.selected == 3:
                lyric_no  = 44
                lyric     = u"て"
            else:
                lyric_no  = random.randint(0,122)
                lyric     = ch_tbl[lyric_no]
        
            self.set_lyric(self.midiout, lyric_no)
            pygame.time.delay(6)
            pygame.midi.Output.write_short(self.midiout, 0x90, key_no, velocity)
            self.viewer.KeyOn(key_no, lyric)

        elif self.viewer.mode == MODE_SONG:
        
            lyric_no = self.song_data[self.song_itr]
            lyric    = self.song_text[self.song_itr]

            self.set_lyric(self.midiout, lyric_no)
            pygame.time.delay(6)
            pygame.midi.Output.write_short(self.midiout, 0x90, key_no, velocity)
            self.viewer.KeyOn(key_no, lyric)

            self.song_itr = ( self.song_itr + 1 ) % len(self.song_data)

            self.viewer.follow_str = self.song_text[self.song_itr]
            self.viewer.follow_key = self.song_keys[self.song_itr]
            if self.song_itr + 1 < len(self.song_data):
                self.viewer.follow_str += self.song_text[self.song_itr+1]
            if self.song_itr + 2 < len(self.song_data):
                self.viewer.follow_str += self.song_text[self.song_itr+2]

        else:
            pygame.midi.Output.write_short(self.midiout, 0x91, key_no, velocity)
            self.viewer.KeyOn(key_no)


    # 音を止める処理 ---------------------------------------------------------------------------------
    def sendNoteOff(self, key_no):

        if self.viewer.mode != MODE_INST:
            if (self.viewer.mode == MODE_SONG) and (self.song_deco[self.song_itr] == "+"):
                self.sendNoteOn(key_no, 0x3f)

            elif (self.viewer.mode == MODE_SONG) and (1 <= self.song_itr) and (self.song_deco[self.song_itr-1] == "-"):
                # ノートオフしない
                pass

            else:
                pygame.midi.Output.write_short(self.midiout, 0x80, key_no, 0)
                self.viewer.KeyOff(key_no)
        else:
            pygame.midi.Output.write_short(self.midiout, 0x81, key_no, 0)
            self.viewer.KeyOff(key_no)



    # 歌詞を設定するメッセージを送信する ---------------------------------------------------------------
    def set_lyric(self, output, ch):
        
        output.write_sys_ex( 0, '\xF0\x43\x79\x09\x00\x50\x10' + evy1_ch[ch] + '\x00\xF7')      # for eVY1 

        if self.flag_pokemiku:
            output.write_sys_ex( 0, [0xF0, 0x43, 0x79, 0x09, 0x11, 0x0A, 0x00, ch, 0xF7])       # for NSX-39


    # MIDIキーボードからの入力を処理して演奏する---------------------------------------------------------
    def play_midi_keyboard(self):

        if self.connect_midiin == False: return
    
        if self.midiin.poll():
            for e in self.midiin.read(1000):
                data, timestamp = e

                if data[0] & 0xf0 == 0x90 or data[0] & 0xf0 == 0x80:
                    transposed = data[1] + self.transpose
                    if transposed <0: transposed = 0
                    if 127 < transposed: transposed = 127
                else:
                    transposed = data[1]
                
                if data[0] == 0x90 and 0 < data[2]: # Note On

                    self.sendNoteOn(transposed, data[2])
    
                elif (data[0] == 0x90 and data[2] == 0) or (data[0] == 0x80): # Note Off
                
                    self.sendNoteOff(transposed)
                
                # 受信した Note ON/OFF 以外の信号はそのまま送信する
                else:
                    if self.viewer.mode != MODE_INST:
                        pygame.midi.Output.write_short(self.midiout, data[0], data[1], data[2])  # 入力をそのまま出力する
                    else:
                        pygame.midi.Output.write_short(self.midiout, data[0]+1, data[1], data[2])  # 入力をch2からそのまま出力する


	# STARTとSELECTボタンによる特殊操作 ---------------------------------------------------------------
    def pushStartSelect(self, current, last):

        # SELECT の処理        
        if (current.select == True) and (last.select == False):

            # START + SELECT -> All sound OFF 
            if current.start == True:
                pygame.midi.Output.write_short(self.midiout, 0xB0, 120, 0)
                pygame.midi.Output.write_short(self.midiout, 0xB1, 120, 0)

            # R + L + SELECT -> Transpose = 0
            elif (current.oct_up == True) and (current.one_up == True):
                if 0 != self.transpose:
                    self.transpose = 0
                    pygame.midi.Output.write_short(self.midiout, 0xB0, 123, 0)
                    pygame.midi.Output.write_short(self.midiout, 0xB1, 123, 0)
                    self.viewer.playing_key = []

            # L + SELECT -> Transpose -1
            elif current.one_up == True:
                if -24 < self.transpose:
                    self.transpose -= 1
                    pygame.midi.Output.write_short(self.midiout, 0xB0, 123, 0)
                    pygame.midi.Output.write_short(self.midiout, 0xB1, 123, 0)
                    self.viewer.playing_key = []

            # R + SELECT -> Transpose +1
            elif current.oct_up == True:
                if self.transpose < 24:
                    self.transpose += 1
                    pygame.midi.Output.write_short(self.midiout, 0xB0, 123, 0)
                    pygame.midi.Output.write_short(self.midiout, 0xB1, 123, 0)
                    self.viewer.playing_key = []

            # SELECT単独でVibrato
            else:
                pygame.midi.Output.write_short(self.midiout, 0xb0, 0x01, 0x7f) # Vibrato ON
                pygame.midi.Output.write_short(self.midiout, 0xb1, 0x40, 0x7F) # Sustain ON

            last.select = True
        
        # START の処理        
        if (current.start == True) and (last.start == False):

            # START + SELECT = All sound OFF    
            if current.select == True:
                pygame.midi.Output.write_short(self.midiout, 0xB0, 120, 0)
                pygame.midi.Output.write_short(self.midiout, 0xB1, 120, 0)

            # START単独でVibrato
            else:
                pygame.midi.Output.write_short(self.midiout, 0xb0, 0x01, 0x7f) # Vibrato ON
                pygame.midi.Output.write_short(self.midiout, 0xb1, 0x40, 0x7F) # Sustain ON

            last.start = True
        
        if (current.select == False) and (last.select == True):
            last.select = False
            pygame.midi.Output.write_short(self.midiout, 0xb0, 0x01, 0x00) # Vibrato OFF
            pygame.midi.Output.write_short(self.midiout, 0xb1, 0x40, 0x00) # Sustain OFF
        
        if (current.start == False) and (last.start == True):
            last.start = False
            pygame.midi.Output.write_short(self.midiout, 0xb0, 0x01, 0x00) # Vibrato OFF
            pygame.midi.Output.write_short(self.midiout, 0xb1, 0x40, 0x00) # Sustain OFF


	# ボタン状態の差（変化）を元に音を鳴らす ------------------------------------------------------------
    def play_midi_gamepad(self, current, last):

        shift = self.transpose

        # 演奏用の各ボタンの処理        
        if current.one_up == True: shift += 1
        if current.oct_up == True: shift += 12
        if current.one_dn == True: shift -= 1
        if current.oct_dn == True: shift -= 12

        if (current.down == True) and (last.down == False):
            self.sent_note_down = 60 + shift
            self.sendNoteOn(self.sent_note_down)
            last.down = True
        
        if (current.left == True) and (last.left == False):
            self.sent_note_left = 62 + shift
            self.sendNoteOn(self.sent_note_left)
            last.left = True
        
        if (current.up == True) and (last.up == False):
            self.sent_note_up = 64 + shift
            self.sendNoteOn(self.sent_note_up)
            last.up = True
        
        if (current.right == True) and (last.right == False):
            self.sent_note_right = 65 + shift
            self.sendNoteOn(self.sent_note_right)
            last.right = True
        
        if (current.y == True) and (last.y == False):
            self.sent_note_y = 67 + shift
            self.sendNoteOn(self.sent_note_y)
            last.y = True
        
        if (current.b == True) and (last.b == False):
            self.sent_note_b = 69 + shift
            self.sendNoteOn(self.sent_note_b)
            last.b = True

        if (current.a == True) and (last.a == False):
            self.sent_note_a = 71 + shift
            self.sendNoteOn(self.sent_note_a)
            last.a = True
        
        if (current.x == True) and (last.x == False):
            self.sent_note_x = 72 + shift
            self.sendNoteOn(self.sent_note_x)
            last.x = True

        if (current.down == False) and (last.down == True):
            self.sendNoteOff(self.sent_note_down)
            last.down = False
            self.sent_note_down = 0
        
        if (current.left == False) and (last.left == True):
            self.sendNoteOff(self.sent_note_left)
            last.left = False
            self.sent_note_left = 0
        
        if (current.up == False) and (last.up == True):
            self.sendNoteOff(self.sent_note_up)
            last.up = False
            self.sent_note_up = 0
        
        if (current.right == False) and (last.right == True):
            self.sendNoteOff(self.sent_note_right)
            last.right = False
            self.sent_note_right = 0
        
        if (current.y == False) and (last.y == True):
            self.sendNoteOff(self.sent_note_y)
            last.y = False
            self.sent_note_y = 0
        
        if (current.b == False) and (last.b == True):
            self.sendNoteOff(self.sent_note_b)
            last.b = False
            self.sent_note_b = 0
        
        if (current.a == False) and (last.a == True):
            self.sendNoteOff(self.sent_note_a)
            last.a = False
            self.sent_note_a = 0
        
        if (current.x == False) and (last.x == True):
            self.sendNoteOff(self.sent_note_x)
            last.x = False
            self.sent_note_x = 0


	# マウス左ボタン押下時に音を鳴らす -----------------------------------------------------------------
    def play_midi_mouse_on(self, x, y):

        key_no = self.viewer.calcTonleiter(x,y)

        if 0 <= key_no:
            self.sendNoteOn(key_no)


	# マウス左ボタン開放時に音を消す -------------------------------------------------------------------
    def play_midi_mouse_off(self, x, y):

        key_no  = self.viewer.calcTonleiter(x,y)

        if (0 <= key_no) and (0 < self.viewer.playing_key.count(key_no)):
            self.sendNoteOff(key_no)


	# マウス左ボタンが押されたまま移動したときに音を変化させる --------------------------------------------
    def play_midi_mouse_move(self, new_x, new_y, old_x, old_y):

        new_key_no  = self.viewer.calcTonleiter(new_x, new_y)
        old_key_no  = self.viewer.calcTonleiter(old_x, old_y)

        if new_key_no != old_key_no:

            if (0 <= old_key_no) and (0 < self.viewer.playing_key.count(old_key_no)):            
                self.sendNoteOff(old_key_no)

            if 0 <= new_key_no:
                self.sendNoteOn(new_key_no)


	# マウス左ボタン押下時に音色等の設定を変更する ------------------------------------------------------
    def change_program_mouse_on(self, x, y):

        if self.viewer.ton_conf_btn.check_within(x,y):
            if self.viewer.isTonConf:
                self.viewer.isTonConf = False
            else:
                self.viewer.isTonConf = True
                self.viewer.isConfig  = False

        if self.viewer.config_button.check_within(x,y):
            if self.viewer.isConfig:
                self.viewer.isConfig = False
            else:
                self.viewer.isConfig  = True
                self.viewer.isTonConf = False

        if self.viewer.isTonConf:
            # 演奏モード
            if self.viewer.select_inst.check_within(x,y):
                self.viewer.mode = 0
                self.viewer.selected = 0
                pygame.midi.Output.write_short(self.midiout, 0xc1, 0x00)

            elif self.viewer.select_sngl.check_within(x,y):
                self.viewer.mode = 1
                self.viewer.selected = 0
                self.viewer.song_title = single_sound[0]

            elif (self.viewer.config.song_file_1 != "") and (self.viewer.select_song.check_within(x,y)) and (self.readSongFile(self.config.song_file_1)):
                self.viewer.mode = 2
                self.viewer.selected = 0                

            # 楽器設定
            if self.viewer.mode == MODE_INST:
                if self.viewer.inst_typ0_btn.check_within(x,y):
                    self.viewer.selected =  0*8 + (self.viewer.selected % 8)
                    pygame.midi.Output.write_short(self.midiout, 0xc1, self.viewer.selected)

                elif self.viewer.inst_typ1_btn.check_within(x,y):
                    self.viewer.selected =  1*8 + (self.viewer.selected % 8)
                    pygame.midi.Output.write_short(self.midiout, 0xc1, self.viewer.selected)

                elif self.viewer.inst_typ2_btn.check_within(x,y):
                    self.viewer.selected =  2*8 + (self.viewer.selected % 8)
                    pygame.midi.Output.write_short(self.midiout, 0xc1, self.viewer.selected)

                elif self.viewer.inst_typ3_btn.check_within(x,y):
                    self.viewer.selected =  3*8 + (self.viewer.selected % 8)
                    pygame.midi.Output.write_short(self.midiout, 0xc1, self.viewer.selected)

                elif self.viewer.inst_typ4_btn.check_within(x,y):
                    self.viewer.selected =  4*8 + (self.viewer.selected % 8)
                    pygame.midi.Output.write_short(self.midiout, 0xc1, self.viewer.selected)

                elif self.viewer.inst_typ5_btn.check_within(x,y):
                    self.viewer.selected =  5*8 + (self.viewer.selected % 8)
                    pygame.midi.Output.write_short(self.midiout, 0xc1, self.viewer.selected)

                elif self.viewer.inst_typ6_btn.check_within(x,y):
                    self.viewer.selected =  6*8 + (self.viewer.selected % 8)
                    pygame.midi.Output.write_short(self.midiout, 0xc1, self.viewer.selected)

                elif self.viewer.inst_typ7_btn.check_within(x,y):
                    self.viewer.selected =  7*8 + (self.viewer.selected % 8)
                    pygame.midi.Output.write_short(self.midiout, 0xc1, self.viewer.selected)

                elif self.viewer.inst_typ8_btn.check_within(x,y):
                    self.viewer.selected =  8*8 + (self.viewer.selected % 8)
                    pygame.midi.Output.write_short(self.midiout, 0xc1, self.viewer.selected)

                elif self.viewer.inst_typ9_btn.check_within(x,y):
                    self.viewer.selected =  9*8 + (self.viewer.selected % 8)
                    pygame.midi.Output.write_short(self.midiout, 0xc1, self.viewer.selected)

                elif self.viewer.inst_typA_btn.check_within(x,y):
                    self.viewer.selected = 10*8 + (self.viewer.selected % 8)
                    pygame.midi.Output.write_short(self.midiout, 0xc1, self.viewer.selected)

                elif self.viewer.inst_typB_btn.check_within(x,y):
                    self.viewer.selected = 11*8 + (self.viewer.selected % 8)
                    pygame.midi.Output.write_short(self.midiout, 0xc1, self.viewer.selected)

                elif self.viewer.inst_typC_btn.check_within(x,y):
                    self.viewer.selected = 12*8 + (self.viewer.selected % 8)
                    pygame.midi.Output.write_short(self.midiout, 0xc1, self.viewer.selected)

                elif self.viewer.inst_typD_btn.check_within(x,y):
                    self.viewer.selected = 13*8 + (self.viewer.selected % 8)
                    pygame.midi.Output.write_short(self.midiout, 0xc1, self.viewer.selected)

                elif self.viewer.inst_typE_btn.check_within(x,y):
                    self.viewer.selected = 14*8 + (self.viewer.selected % 8)
                    pygame.midi.Output.write_short(self.midiout, 0xc1, self.viewer.selected)

                elif self.viewer.inst_typF_btn.check_within(x,y):
                    self.viewer.selected = 15*8 + (self.viewer.selected % 8)
                    pygame.midi.Output.write_short(self.midiout, 0xc1, self.viewer.selected)

                elif self.viewer.select_g0_btn.check_within(x,y):
                    self.viewer.selected =  0 + 8*(self.viewer.selected // 8)
                    pygame.midi.Output.write_short(self.midiout, 0xc1, self.viewer.selected)

                elif self.viewer.select_g1_btn.check_within(x,y):
                    self.viewer.selected =  1 + 8*(self.viewer.selected // 8)
                    pygame.midi.Output.write_short(self.midiout, 0xc1, self.viewer.selected)

                elif self.viewer.select_g2_btn.check_within(x,y):
                    self.viewer.selected =  2 + 8*(self.viewer.selected // 8)
                    pygame.midi.Output.write_short(self.midiout, 0xc1, self.viewer.selected)

                elif self.viewer.select_g3_btn.check_within(x,y):
                    self.viewer.selected =  3 + 8*(self.viewer.selected // 8)
                    pygame.midi.Output.write_short(self.midiout, 0xc1, self.viewer.selected)

                elif self.viewer.select_g4_btn.check_within(x,y):
                    self.viewer.selected =  4 + 8*(self.viewer.selected // 8)
                    pygame.midi.Output.write_short(self.midiout, 0xc1, self.viewer.selected)

                elif self.viewer.select_g5_btn.check_within(x,y):
                    self.viewer.selected =  5 + 8*(self.viewer.selected // 8)
                    pygame.midi.Output.write_short(self.midiout, 0xc1, self.viewer.selected)

                elif self.viewer.select_g6_btn.check_within(x,y):
                    self.viewer.selected =  6 + 8*(self.viewer.selected // 8)
                    pygame.midi.Output.write_short(self.midiout, 0xc1, self.viewer.selected)

                elif self.viewer.select_g7_btn.check_within(x,y):
                    self.viewer.selected =  7 + 8*(self.viewer.selected // 8)
                    pygame.midi.Output.write_short(self.midiout, 0xc1, self.viewer.selected)

            # 歌う音設定
            elif self.viewer.mode == MODE_SNGL:
                if self.viewer.select_v0_btn.check_within(x,y):
                    self.viewer.selected = 0
                    self.viewer.song_title = single_sound[0]

                elif self.viewer.select_v1_btn.check_within(x,y):
                    self.viewer.selected = 1
                    self.viewer.song_title = single_sound[1]

                elif self.viewer.select_v2_btn.check_within(x,y):
                    self.viewer.selected = 2
                    self.viewer.song_title = single_sound[2]

                elif self.viewer.select_v3_btn.check_within(x,y):
                    self.viewer.selected = 3
                    self.viewer.song_title = single_sound[3]

                elif self.viewer.select_v4_btn.check_within(x,y):
                    self.viewer.selected = 4
                    self.viewer.song_title = single_sound[4]

            # 歌の設定
            elif self.viewer.mode == MODE_SONG:
                if (self.config.song_file_1 != "") and (self.viewer.song1_button.check_within(x,y)) and (self.readSongFile(self.config.song_file_1)):
                    self.viewer.selected = 0

                elif (self.config.song_file_2 != "") and (self.viewer.song2_button.check_within(x,y)) and (self.readSongFile(self.config.song_file_2)):
                    self.viewer.selected = 1

                elif (self.config.song_file_3 != "") and (self.viewer.song3_button.check_within(x,y)) and (self.readSongFile(self.config.song_file_3)):
                    self.viewer.selected = 2

                elif (self.config.song_file_4 != "") and (self.viewer.song4_button.check_within(x,y)) and (self.readSongFile(self.config.song_file_4)):
                    self.viewer.selected = 3

                elif (self.config.song_file_5 != "") and (self.viewer.song5_button.check_within(x,y)) and (self.readSongFile(self.config.song_file_5)):
                    self.viewer.selected = 4

                elif (self.config.song_file_6 != "") and (self.viewer.song6_button.check_within(x,y)) and (self.readSongFile(self.config.song_file_6)):
                    self.viewer.selected = 5

                elif (self.config.song_file_7 != "") and (self.viewer.song7_button.check_within(x,y)) and (self.readSongFile(self.config.song_file_7)):
                    self.viewer.selected = 6

                elif (self.config.song_file_8 != "") and (self.viewer.song8_button.check_within(x,y)) and (self.readSongFile(self.config.song_file_8)):
                    self.viewer.selected = 7

        if self.viewer.isConfig:
            # キーレイアウト
            if self.viewer.set_Layout0.check_within(x,y):
                self.viewer.setLayout(0)

            elif self.viewer.set_Layout1.check_within(x,y):
                self.viewer.setLayout(1)

            elif self.viewer.set_Layout2.check_within(x,y):
                self.viewer.setLayout(2)

            elif self.viewer.set_Layout3.check_within(x,y):
                self.viewer.setLayout(3)

            # Game Pad ボタン設定
            if self.connect_gamepad:
                if self.viewer.set_GamePad0.check_within(x,y):
                    self.config.setGempadXInput()

                elif self.viewer.set_GamePad1.check_within(x,y):
                    self.config.setGempadSNES()

                elif (self.config.isGamePadConf) and (self.viewer.set_GamePad2.check_within(x,y)):
                    self.config.setGempadByConf(0)

                elif (self.config.isGamePadConf2) and (self.viewer.set_GamePad3.check_within(x,y)):
                    self.config.setGempadByConf(1)


    # 歌詞情報を保存したCSVファイルを読み込んでリスト化 ---------------------------------------------------
    def readSongFile(self, file_name):
        
        if os.path.exists(file_name) == False:
            return False

        self.song_data = []
        self.song_text = []
        self.song_keys = []
        self.song_deco = []
        self.song_itr  = 0

        self.viewer.song_title = ""
    
        self.fin = codecs.open(file_name, encoding='utf_8_sig')

        while True:
            read_next = self.fin.readline()

            if read_next == "":
                self.fin.close()
                self.viewer.follow_str = ""
                if 0 < len(self.song_data):
                    self.viewer.follow_str += self.song_text[0]
                    self.viewer.follow_key =  self.song_keys[0]
                if 1 < len(self.song_data):
                    self.viewer.follow_str += self.song_text[1]
                if 2 < len(self.song_data):
                    self.viewer.follow_str += self.song_text[2]
                return True

            data = read_next.replace("\n","").split(",")

            if self.viewer.song_title == "":
                self.viewer.song_title = data[0]
            else:
                self.song_text.append(data[0])
                self.song_data.append(int(data[1]))
                if data[2] == "":
                    self.song_keys.append(-1)
                else:
                    self.song_keys.append(int(data[2]))
                self.song_deco.append(data[3])


    # メインループを実行する関数 （関数を抜けたあとも再実行する場合にTrueを返す）----------------------------
    def loopMain(self):
        
        btn = GamePad()
        last_btn = GamePad()
        mouse_x = 0
        mouse_y = 0
        last_x  = 0
        last_y  = 0
        is_mouse_on = False

        self.viewer.initViewer(WINDOW_TITLE, self.connect_gamepad)        

        clock = pygame.time.Clock()
        clock.tick(FPS)

        # メインループ
        while 1:

            # キーボード・マウス・ゲームパッドからの入力を処理
            for e in pygame.event.get(): # イベントチェック
                if e.type == QUIT: # Closeされた
                    return False

                if (e.type == KEYDOWN) and (e.key  == K_ESCAPE): # ESCが押された
                    return False

                if (e.type == KEYDOWN) and (e.key  == K_RETURN): # ENTERが押された
                    pygame.midi.Output.write_short(self.midiout, 0xb0, 0x01, 0x7f) # Vibrato ON
                    pygame.midi.Output.write_short(self.midiout, 0xb1, 0x40, 0x7f) # Sustain ON

                if (e.type == KEYUP) and (e.key  == K_RETURN):   # ENTERが離された
                    pygame.midi.Output.write_short(self.midiout, 0xb0, 0x01, 0x00) # Vibrato OFF
                    pygame.midi.Output.write_short(self.midiout, 0xb1, 0x40, 0x00) # Sustain OFF

                # マウス関連のイベントチェック
                if (e.type is MOUSEBUTTONDOWN) and (e.button == 1):
                    mouse_x, mouse_y = e.pos
                    self.play_midi_mouse_on(mouse_x, mouse_y)
                    self.change_program_mouse_on(mouse_x, mouse_y)
                    is_mouse_on = True

                    if self.viewer.close_button.check_within(mouse_x, mouse_y):
                        return False

                    if self.viewer.restart_btn.check_within(mouse_x, mouse_y):
                        return True

                elif (e.type is MOUSEBUTTONUP) and (e.button == 1):
                    self.play_midi_mouse_off(mouse_x, mouse_y)
                    is_mouse_on = False

                elif (e.type is MOUSEMOTION) and (is_mouse_on == True):
                    last_x = mouse_x
                    last_y = mouse_y
                    mouse_x, mouse_y = e.pos
                    self.play_midi_mouse_move(mouse_x, mouse_y, last_x, last_y)


                # Joystick関連のイベントチェック
                if e.type == pygame.locals.JOYAXISMOTION:
                    x , y = self.g_pad.get_axis(0), self.g_pad.get_axis(1)
                    if (0.5 < y):
                        btn.down = True
                        btn.up   = False
                    elif (y < -0.5):
                        btn.down = False
                        btn.up   = True
                    else:
                        btn.down = False
                        btn.up   = False

                    if (0.5 < x):
                        btn.left  = False
                        btn.right = True
                    elif (x < -0.5):
                        btn.left  = True
                        btn.right = False
                    else:
                        btn.left  = False
                        btn.right = False

                    if 2 < self.g_pad.get_numaxes():
                        z = self.g_pad.get_axis(2)
                        if z < -0.2:
                            btn.oct_dn = True
                            btn.one_dn = False
                        elif 0.2 < z:
                            btn.oct_dn = False
                            btn.one_dn = True
                            pass
                        else:
                            btn.oct_dn = False
                            btn.one_dn = False

                elif e.type == pygame.locals.JOYHATMOTION:
                    hat_x, hat_y = self.g_pad.get_hat(0)
                    if hat_x == -1:
                        btn.left  = True
                        btn.right = False
                    elif hat_x == 1:
                        btn.left  = False
                        btn.right = True
                    else:
                        btn.left  = False
                        btn.right = False

                    if hat_y == -1:
                        btn.up   = False
                        btn.down = True
                    elif hat_y == 1:
                        btn.up   = True
                        btn.down = False
                    else:
                        btn.up   = False
                        btn.down = False

                elif e.type == pygame.locals.JOYBUTTONDOWN:
                    if   (e.button==self.config.gamepad_b     ): btn.a = True
                    elif (e.button==self.config.gamepad_a     ): btn.b = True
                    elif (e.button==self.config.gamepad_c     ): btn.x = True
                    elif (e.button==self.config.gamepad_g     ): btn.y = True
                    elif (e.button==self.config.gamepad_one_up): btn.one_up = True
                    elif (e.button==self.config.gamepad_oct_up): btn.oct_up = True
                    elif (e.button==self.config.gamepad_select): btn.select = True
                    elif (e.button==self.config.gamepad_start ): btn.start  = True
                    else: pass
                
                elif e.type == pygame.locals.JOYBUTTONUP:
                    if   (e.button==self.config.gamepad_b     ): btn.a = False
                    elif (e.button==self.config.gamepad_a     ): btn.b = False
                    elif (e.button==self.config.gamepad_c     ): btn.x = False
                    elif (e.button==self.config.gamepad_g     ): btn.y = False
                    elif (e.button==self.config.gamepad_one_up): btn.one_up = False
                    elif (e.button==self.config.gamepad_oct_up): btn.oct_up = False
                    elif (e.button==self.config.gamepad_select): btn.select = False
                    elif (e.button==self.config.gamepad_start ): btn.start  = False
                    else: pass

            # メインループ脱出コマンド START + SELECT + L + R
            if btn.start and btn.select and btn.one_up and btn.oct_up:
                return False

            # 音を鳴らす処理
            self.pushStartSelect(btn, last_btn)
            self.play_midi_gamepad(btn, last_btn)
            self.play_midi_keyboard()

            # 表示
            self.viewer.transpose = self.transpose
            self.viewer.view()

            clock.tick(FPS)


    # 実行 -------------------------------------------------------------------------------------------
    def play(self):

        ret_value = False

        if self.init_midi():
            self.connect_gamepad = self.init_gamepad()
            ret_value =  self.loopMain()

            pygame.midi.Output.write_short(self.midiout, 0xB0, 120, 0)     # CH1 All sound OFF 
            pygame.midi.Output.write_short(self.midiout, 0xB1, 120, 0)     # CH2 All sound OFF 
            pygame.midi.Output.write_short(self.midiout, 0xb0, 0x01, 0x00) # Vibrato OFF
            pygame.midi.Output.write_short(self.midiout, 0xb1, 0x40, 0x00) # Sustain OFF

        return ret_value


# メイン ---------------------------------------------------------------------------------------------
if  __name__ == '__main__':
    try:
        loop = True
        pygame.init()
        while loop:
            loop = PokemikuPy().play()
        pygame.quit()
    finally:
        pass

