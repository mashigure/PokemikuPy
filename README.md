Pokemiku.py
=========

ポケットミクが音階を歌うPythonスクリプト

## 概要

ポケットミクまはたeVY1が音階を歌うPythonスクリプト（プログラム）です。
ポケットミクまたはeVY1シールドを接続したPCで実行することができます。
ゲームパッド/MIDIキーボードを接続すると、その入力で演奏することができます。
入力機器を接続しない場合でも、画面上の鍵盤をクリックすることで演奏することができます。

![画面のスクリーンショット](img/PokemikuPy.png)

[Raspberry Pi内臓ポケミク](http://mashigure.blog.jp/archives/9299520.html)で実行しているものの改良版であり、
基本的な使い方などは同じですので、どのようなものかはそちらも参考にしてください。


## 必要機器

* [ポケットミク](http://www.otonanokagaku.net/nsx39/)、
[eVY1シールド](https://www.switch-science.com/catalog/1490/)
 または 
[eVY1ボード](https://www.switch-science.com/catalog/1489/)

* ゲームパッドまたはMIDIキーボード（両方同時に使用可能）

※ 使用するゲームパッドはXInput対応のものまたは
[Buffalo製レトロ調USBゲームパッド](http://buffalo.jp/product/input/gamepad/bsgp801/)を
想定していますが、その他のゲームパッドでも動作します。ただし、キーコンフィグ（config.ini）の設定変更などが必要です。

※ MIDIキーボード使用の際は、ソースコード38行目のリストに使用するキーボード名を追加して下さい。


## 動作環境

下記がインストールされ、動作可能なPC上またはディスプレイを接続したRaspberry Pi上

* Python 2.4
* Pygame


### 確認済み環境
Windows 10 Pro および Rasbian Stretch(2017/11/29)　上にて動作を確認


## 実行方法

### 準備
* Pokemiku.pyおよびconfig.ini、imgフォルダ、songsフォルダとその中の全ファイルをダウンロードし、任意のフォルダに保存して下さい。
* Pokemiku.pyを保存したフォルダに、[IPAフォント Pゴシック](http://forest.watch.impress.co.jp/library/software/ipafont/)をダウンロードして保存して下さい。

### 実行
* Pokemiku.pyを実行して下さい。

## 操作方法

### ゲームパッド：演奏操作
ゲームパッド接続時のボタンの対応は画面上の設定で変更できます。
設定画面上のConfig1およびConfig2は、config.iniの修正でボタン割り当てを変更できます。
下記の説明はBuffalo製レトロ調USBゲームパッドの場合を想定しています。

* 十字キー（ジョイスティック） ↓： ド 
* 十字キー（ジョイスティック） ←： レ
* 十字キー（ジョイスティック） ↑： ミ
* 十字キー（ジョイスティック） →： ファ
* ボタン3(Y)：ソ
* ボタン1(B)：ラ
* ボタン0(A)：シ
* ボタン2(X)：ド
* ボタン4(L)：押している間半音上がる
* ボタン5(R)：押している間１オクターブ上がる


### ゲームパッド：演奏以外のボタン操作

* ボタン6(SELECT)単独: ボーカロイド（歌唱）モードのときビブラート、楽器モードのときサステイン(RLと同時押しでトランスポーズになるためSTARTを推奨)
* ボタン7(START)単独: ボーカロイド（歌唱）モードのときビブラート、楽器モードのときサステイン
* ボタン4(L)を押しながらボタン6(SELECT)： トランスポーズ-1（半音下げる）
* ボタン5(R)を押しながらボタン6(SELECT)： トランスポーズ+1（半音上げる）
* ボタン4(L)とボタン5(R)を押しながらボタン6(SELECT)： トランスポーズを元に戻す
* ボタン4(L)+ ボタン5(R) + ボタン6(SELECT) + ボタン7(START) 同時押し： ウィンドウを閉じる


### その他

* エスケープキー： ウィンドウを閉じる
* エンターキー： ボーカロイド（歌唱）モードのときビブラート、楽器モードのときサステイン


