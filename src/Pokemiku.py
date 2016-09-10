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


# 描画関連の定数
WINDOW_TITLE     = 'Game Pad x Poke miku'
SCREEN_WIDTH     = 640
SCREEN_HEIGHT    = 480

KEYBOARD_TOP     = SCREEN_HEIGHT / 2
WHITE_HEIGHT     = KEYBOARD_TOP - 20
BLACK_HEIGHT     = WHITE_HEIGHT / 2

FLG_FULL_SCREEN  = False

BG_COLOUR        = (255, 255, 255)  # 背景色
WHITEKEY_COLOUR  = (192,192,192)    # 白鍵の表示色
PLAYING_COLOUR   = (0,255,160)      # 押されている（鳴らしている）Keyの表示色
LYRICS_COLOUR    = (0,180,120)      # 歌詞のフォントカラー

FONT_SIZE_LYRICS = SCREEN_HEIGHT * 5 / 13
FONT_SIZE_TEXT   = 16
FONT_FILE        = 'ipagp.ttf'      # 使用する日本語TTFフォントファイル名
                                    # このプログラムと同じフォルダに入れる。
                                    # DL元 http://forest.watch.impress.co.jp/library/software/ipafont/

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



# 表示関連 -------------------------------------------------------------------------------------------
class PokemikuPyViewer:

    def __init__(self):

        self.disp_str    = u""
        self.playing_key = []
        self.transpose   = 0

        self.black_keys = ( 1,3,5,  8,10,  13,15,17,   20,22,   25,27,29     )
        self.white_keys = (0,2,4,6,7,9,11,12,14,16,18,19,21,23,24,26,28,30,31)


        self.white_width  = SCREEN_WIDTH / len(self.white_keys)
        self.black_width  = self.white_width * 7.0 / 12.0
        keyboard_width    = self.white_width * len(self.white_keys)
        self.left_margin  = (SCREEN_WIDTH-keyboard_width)/2

        self.base_key  = 53 # 表示上左端の鍵盤のMIDIでの番号


    # 画面の初期化 -----------------------------------------------------------------------------------
    def initViewer(self, width, height, title_text, full_screen=False):

        self.width  = width
        self.height = height

        pygame.mouse.set_visible(False)

        # 画面を作る
        if full_screen == True:
            self.screen = pygame.display.set_mode( (width, height), FULLSCREEN )
        else:
            self.screen = pygame.display.set_mode( (width, height) ) 

        pygame.display.set_caption(title_text) # タイトル
        pygame.display.flip() # 画面を反映

        self.sysfont_lyrics = pygame.font.Font(FONT_FILE, FONT_SIZE_LYRICS)
        self.sysfont_text = pygame.font.Font(FONT_FILE, FONT_SIZE_TEXT)
		

    # 画面の描画-- -----------------------------------------------------------------------------------
    def view(self):
    
        self.screen.fill(BG_COLOUR)   # 画面の初期化


        # 白鍵
        for i in range(len(self.white_keys)):

            if 0 < self.playing_key.count(self.white_keys[i]+self.base_key):
                pygame.draw.rect(self.screen,  PLAYING_COLOUR, Rect(self.left_margin + i*self.white_width , KEYBOARD_TOP, self.white_width-2, WHITE_HEIGHT))
            else: 
                pygame.draw.rect(self.screen, WHITEKEY_COLOUR, Rect(self.left_margin + i*self.white_width , KEYBOARD_TOP, self.white_width -2, WHITE_HEIGHT))

        # 黒鍵の枠部分（空白）
        for i in self.black_keys:
            pygame.draw.rect(self.screen, BG_COLOUR, Rect(self.left_margin-2 + i*self.black_width, KEYBOARD_TOP, self.black_width+2, BLACK_HEIGHT+2))

        # 黒鍵
        for i in self.black_keys:

            if self.playing_key.count(i+self.base_key):
                pygame.draw.rect(self.screen, PLAYING_COLOUR, Rect(self.left_margin + i*self.black_width, KEYBOARD_TOP, self.black_width-2, BLACK_HEIGHT))

            else:
                pygame.draw.rect(self.screen, (0,0,0), Rect(self.left_margin + i*self.black_width, KEYBOARD_TOP, self.black_width-2, BLACK_HEIGHT))
        
        lryc_img = self.sysfont_lyrics.render(self.disp_str, True, LYRICS_COLOUR)
        drow_x = (self.width - lryc_img.get_width()) / 2
        self.screen.blit(lryc_img, (drow_x, 10))

        text_img = self.sysfont_text.render('transpose: ' + str(self.transpose) + ' ', True, (0,0,0))
        drow_x = (self.width - text_img.get_width())
        drow_y = (self.height - text_img.get_height())
        self.screen.blit(text_img, (drow_x, drow_y))

        
        # display Surface全体を更新して画面に描写
        pygame.display.flip()



# ゲームパッドのボタン状態を管理する変数群 ----------------------------------------------------------------
class Buttons:

    def __init__(self):
		
		self.down  = False
		self.left  = False
		self.up    = False
		self.right = False
		self.y     = False
		self.b     = False
		self.a     = False
		self.x     = False
		self.r     = False
		self.l     = False
		self.start = False
		self.select= False


# ゲームパッド x ポケミク 演奏クラス ----------------------------------------------------------------------
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

        self.voice_velosity  = 127
        self.square_velosity = 64

        self.connect_gamepad = False
        self.connect_midiin  = False

        self.viewer = PokemikuPyViewer()
            

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

        

    # 出力先となるeVY1モジュール・ポケミクを探して接続する --------------------------------------------------
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
                

    # 入力元となる鍵盤などを探して接続する ----------------------------------------------------------------
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

        # メインボリューム (ch:0)
        pygame.midi.Output.write_short(self.midiout, 0xb0, 0x07, 0x7f)

        # プログラムチェンジ
        pygame.midi.Output.write_short(self.midiout, 0xc1, 0x50)

        return True
                

    # 歌詞を設定するメッセージを送信する ------------------------------------------------------------------
    def set_lyric(self, output, ch):
        
        output.write_sys_ex( 0, '\xF0\x43\x79\x09\x00\x50\x10' + evy1_ch[ch] + '\x00\xF7')      # for eVY1 

        if self.flag_pokemiku:
            output.write_sys_ex( 0, [0xF0, 0x43, 0x79, 0x09, 0x11, 0x0A, 0x00, ch, 0xF7])       # for NSX-39


    # MIDIキーボードからの入力を処理して演奏する-----------------------------------------------------------
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
                
                if data[0] == 0x90 and data[2] > 0: # Note On
                    
                    if data[1] % 12 == 0:
                        self.set_lyric(self.midiout, 0x32)
                        self.viewer.disp_str = u"ド"
                    
                    if data[1] % 12 == 1:
                        self.set_lyric(self.midiout, 0x32)
                        self.viewer.disp_str = u"ド"
                    
                    elif data[1] % 12 == 2:
                        self.set_lyric(self.midiout, 0x72)
                        self.viewer.disp_str = u"レ"
                    
                    elif data[1] % 12 == 3:
                        self.set_lyric(self.midiout, 0x72)
                        self.viewer.disp_str = u"レ"

                    elif data[1] % 12 == 4:
                        self.set_lyric(self.midiout, 0x65)
                        self.viewer.disp_str = u"ミ"

                    elif data[1] % 12 == 5:
                        self.set_lyric(self.midiout, 0x5f)
                        self.viewer.disp_str = u"ファ"

                    elif data[1] % 12 == 6:
                        self.set_lyric(self.midiout, 0x5f)
                        self.viewer.disp_str = u"ファ"

                    elif data[1] % 12 == 7:
                        self.set_lyric(self.midiout, 0x19)
                        self.viewer.disp_str = u"ソ"

                    elif data[1] % 12 == 8:
                        self.set_lyric(self.midiout, 0x19)
                        self.viewer.disp_str = u"ソ"

                    elif data[1] % 12 == 9:
                        self.set_lyric(self.midiout, 0x6f)
                        self.viewer.disp_str = u"ラ"

                    elif data[1] % 12 == 10:
                        self.set_lyric(self.midiout, 0x6f)
                        self.viewer.disp_str = u"ラ"

                    elif data[1] % 12 == 11:
                        self.set_lyric(self.midiout, 0x20)
                        self.viewer.disp_str = u"シ"
                
                    pygame.midi.Output.write_short(self.midiout, data[0]+2, transposed, data[2])  # 入力をch3からも出力する
                        
                    pygame.time.delay(6)
                    self.viewer.playing_key.append(transposed)
    
                if (data[0] == 0x90 and data[2] == 0) or (data[0] == 0x80): # Note Off
                
                    pygame.midi.Output.write_short(self.midiout, data[0]+2, transposed, data[2])  # 入力をch3からも出力する
                    
                    if 0 < self.viewer.playing_key.count(transposed):
                        self.viewer.playing_key.remove(transposed)

                    if len(self.viewer.playing_key) == 0: self.viewer.disp_str = u""
                
                if self.voice_velosity != 0 or data[0] != 0x90:
                    pygame.midi.Output.write_short(self.midiout, data[0], transposed, data[2])  # 入力をそのまま出力する


	# ボタンによるNote ONの処理 ------------------------------------------------------------------------
    def note_on_by_button(self, tone, lyric_no, display_str):

        delay_time = 6

        self.set_lyric(self.midiout, lyric_no)
        pygame.midi.Output.write_short(self.midiout, 0x91, tone, self.square_velosity)
        pygame.time.delay(delay_time)
        pygame.midi.Output.write_short(self.midiout, 0x90, tone, self.voice_velosity)
        self.viewer.playing_key.append(tone)
        self.viewer.disp_str = display_str


	# ボタンによるNote OFFの処理 ------------------------------------------------------------------------
    def note_off_by_button(self, tone):
        pygame.midi.Output.write_short(self.midiout, 0x81, tone, 0)
        pygame.midi.Output.write_short(self.midiout, 0x80, tone, 0)

        if 0 < self.viewer.playing_key.count(tone):
            self.viewer.playing_key.remove(tone)

        if len(self.viewer.playing_key) == 0: self.viewer.disp_str = u""


	# STARTとSELECTボタンによる特殊操作 -----------------------------------------------------------------
    def pushStartSelect(self, current, last):

        # SELECT の処理        
        if(current.select == True and last.select == False ):

            # START + SELECT -> All sound OFF 
            if current.start == True:
                pygame.midi.Output.write_short(self.midiout, 0xB0, 120, 0)
                pygame.midi.Output.write_short(self.midiout, 0xB1, 120, 0)

            # R + L + SELECT -> Transpose = 0
            elif current.r == True and current.l == True:
                if 0 != self.transpose:
                    self.transpose = 0
                    pygame.midi.Output.write_short(self.midiout, 0xB0, 123, 0)
                    pygame.midi.Output.write_short(self.midiout, 0xB1, 123, 0)
                    self.viewer.playing_key = []

            # L + SELECT -> Transpose -1
            elif current.l == True:
                if -24 < self.transpose:
                    self.transpose -= 1
                    pygame.midi.Output.write_short(self.midiout, 0xB0, 123, 0)
                    pygame.midi.Output.write_short(self.midiout, 0xB1, 123, 0)
                    self.viewer.playing_key = []

            # R + SELECT -> Transpose +1
            elif current.r == True:
                if self.transpose < 24:
                    self.transpose += 1
                    pygame.midi.Output.write_short(self.midiout, 0xB0, 123, 0)
                    pygame.midi.Output.write_short(self.midiout, 0xB1, 123, 0)
                    self.viewer.playing_key = []

            last.select = True
        
        # START の処理        
        if(current.start == True and last.start == False ):

            # START + SELECT = All sound OFF    
            if current.select == True:
                pygame.midi.Output.write_short(self.midiout, 0xB0, 120, 0)
                pygame.midi.Output.write_short(self.midiout, 0xB1, 120, 0)

            # Vocaloid On <-> Off
            else:
              if self.voice_velosity == 0:
                  self.square_velosity = 64
                  self.voice_velosity  = 127

              else:
                  self.square_velosity = 127
                  self.voice_velosity  = 0

            last.start = True
        
        if(current.select == False and last.select == True ):
            last.select = False
        
        if(current.start == False and last.start == True ):
            last.start = False


	# ボタン状態の差（変化）を元に音を鳴らす --------------------------------------------------------------
    def play_midi_gamepad(self, current, last):

        shift = self.transpose


        # 演奏用の各ボタンの処理        
        if( current.l == True ): shift += 1
        if( current.r == True ): shift += 12

        if(current.down == True and last.down == False ):
            self.sent_note_down = 60 + shift
            self.note_on_by_button(self.sent_note_down,50,u"ド")
            last.down = True
        
        if(current.left == True and last.left == False ):
            self.sent_note_left = 62 + shift
            self.note_on_by_button(self.sent_note_left,114,u"レ")
            last.left = True
        
        if(current.up == True and last.up == False ):
            self.sent_note_up = 64 + shift
            self.note_on_by_button(self.sent_note_up,101,u"ミ")
            last.up = True
        
        if(current.right == True and last.right == False ):
            self.sent_note_right = 65 + shift
            self.note_on_by_button(self.sent_note_right,95,u"ファ")
            last.right = True
        
        if(current.y == True and last.y == False ):
            self.sent_note_y = 67 + shift
            self.note_on_by_button(self.sent_note_y,25,u"ソ")
            last.y = True
        
        if(current.b == True and last.b == False ):
            self.sent_note_b = 69 + shift
            self.note_on_by_button(self.sent_note_b,111,u"ラ")
            last.b = True

        if(current.a == True and last.a == False ):
            self.sent_note_a = 71 + shift
            self.note_on_by_button(self.sent_note_a,32,u"シ")
            last.a = True
        
        if(current.x == True and last.x == False ):
            self.sent_note_x = 72 + shift
            self.note_on_by_button(self.sent_note_x,50,u"ド")
            last.x = True

        if(current.down == False and last.down == True ):
            self.note_off_by_button(self.sent_note_down)
            last.down = False
            self.sent_note_down = 0
        
        if(current.left == False and last.left == True ):
            self.note_off_by_button(self.sent_note_left)
            last.left = False
            self.sent_note_left = 0
        
        if(current.up == False and last.up == True ):
            self.note_off_by_button(self.sent_note_up)
            last.up = False
            self.sent_note_up = 0
        
        if(current.right == False and last.right == True ):
            self.note_off_by_button(self.sent_note_right)
            last.right = False
            self.sent_note_right = 0
        
        if(current.y == False and last.y == True ):
            self.note_off_by_button(self.sent_note_y)
            last.y = False
            self.sent_note_y = 0
        
        if(current.b == False and last.b == True ):
            self.note_off_by_button(self.sent_note_b)
            last.b = False
            self.sent_note_b = 0
        
        if(current.a == False and last.a == True ):
            self.note_off_by_button(self.sent_note_a)
            last.a = False
            self.sent_note_a = 0
        
        if(current.x == False and last.x == True ):
            self.note_off_by_button(self.sent_note_x)
            last.x = False
            self.sent_note_x = 0


    # メインループを実行する関数 ------------------------------------------------------------------------
    def loopMain(self):
        
        btn = Buttons()
        last_btn = Buttons()

        self.viewer.initViewer(SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_TITLE, FLG_FULL_SCREEN)        

        clock = pygame.time.Clock()
        clock.tick(FPS)

        sysfont_lyrics = pygame.font.Font(FONT_FILE, FONT_SIZE_LYRICS)
        sysfont_text = pygame.font.Font(FONT_FILE, FONT_SIZE_TEXT)
    

        # メインループ
        while 1:

            # キーボード・ジョイスティックからの入力を処理
            for e in pygame.event.get(): # イベントチェック
                if e.type == QUIT: # 終了が押された？
                    return
                if (e.type == KEYDOWN and
                    e.key  == K_ESCAPE): # ESCが押された？
                    return

                # Joystick関連のイベントチェック
                if e.type == pygame.locals.JOYAXISMOTION: # 7
                    x , y = self.g_pad.get_axis(0), self.g_pad.get_axis(1)
                    if( 0.5 < y ):
                        btn.down = True
                        btn.up = False
                    elif( y < -0.5 ):
                        btn.down = False
                        btn.up = True
                    else:
                        btn.down = False
                        btn.up = False
                        
                    if( 0.5 < x ):
                        btn.left = False
                        btn.right = True
                    elif( x < -0.5 ):
                        btn.left = True
                        btn.right = False
                    else:
                        btn.left = False
                        btn.right = False

                elif e.type == pygame.locals.JOYBALLMOTION: # 8
                    print 'ball motion'
                elif e.type == pygame.locals.JOYHATMOTION: # 9
                    print 'hat motion'

                elif e.type == pygame.locals.JOYBUTTONDOWN: # 10
                    if(  e.button==0): btn.a = True
                    elif(e.button==1): btn.b = True
                    elif(e.button==2): btn.x = True
                    elif(e.button==3): btn.y = True
                    elif(e.button==4): btn.l = True
                    elif(e.button==5): btn.r = True
                    elif(e.button==6): btn.select = True
                    elif(e.button==7): btn.start  = True
                    else: print str(e.button)+'番目のボタンが押された'
                        
                                   
                elif e.type == pygame.locals.JOYBUTTONUP: # 11
                    if(  e.button==0): btn.a = False
                    elif(e.button==1): btn.b = False
                    elif(e.button==2): btn.x = False
                    elif(e.button==3): btn.y = False
                    elif(e.button==4): btn.l = False
                    elif(e.button==5): btn.r = False
                    elif(e.button==6): btn.select = False
                    elif(e.button==7): btn.start  = False
                    else: print str(e.button)+'番目のボタンが離された'

            # メインループ脱出コマンド START + SELECT + L + R
            if btn.start and btn.select and btn.l and btn.r:
                return

            # 音を鳴らす処理
            self.pushStartSelect(btn, last_btn)
            self.play_midi_gamepad( btn, last_btn )
            self.play_midi_keyboard()

            # 表示
            self.viewer.transpose = self.transpose
            self.viewer.view();

            clock.tick(FPS)


    # 実行 -------------------------------------------------------------------------------------------
    def play(self):
        
        pygame.init()
        
        if self.init_midi():

            self.connect_gamepad = self.init_gamepad()

            if self.connect_gamepad or self.connect_midiin:
                self.loopMain()

        pygame.quit()




# メイン ---------------------------------------------------------------------------------------------
if  __name__ == '__main__':
    try:
        PokemikuPy().play()
    finally:
        pass


