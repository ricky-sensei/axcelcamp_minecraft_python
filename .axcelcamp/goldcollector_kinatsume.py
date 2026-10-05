"""
goldcollector_kinatsume.py （元ファイル: goldcollector.py）

【このプログラムの機能】
金ブロックを全部ふむはやさをきそう競争ゲーム

1. あそびかた
   - スーパーフラットのワールドであそんでね
   - あしもとにひろがる金ブロックをふんでみよう
   - 全部ふんだら、タイムが表示されるよ!

2. しくみ
   - 金ブロックを置き終わった時点から時間を計りはじめる。
   - 0.01秒ごとにプレイヤーの足元のブロックを調べる。
   - 足元が金ブロックなら、丸石（COBBLESTONE）に置きかえ、
     プレイヤーを5マス上に持ち上げ（取れた合図）、残りの数を1減らす。



【アレンジしてみよう】
   - あつめるブロックの数: mokuhyou = 10 の数字をかえる
   - ばらまくはんい: hani_x = 10 と hani_z = 10 の数字をかえる
   - 置くブロックのしゅるい: block_syurui = block.GOLD_BLOCK の GOLD_BLOCK をかえる
   - 取ったあとのブロック: block.COBBLESTONE（コードのとちゅうに書いてある）
   - 取ったときにとび上がる高さ: 5（コードのとちゅうに書いてある）

【注意】
   - 金ブロックは「実行したときの足元の高さ」にだけ置かれる。でこぼこした
     地形では地面にうまったり空中に浮いたりするので、平らな場所で実行する。
   - 全部取るまでプログラムは終わらない。
   - はんいのマスの数より mokuhyou が大きいと、ブロックを置ききれないので、
     エラーのメッセージを出して終わる。
"""

#
# Code by Alexander Pruss and under the MIT license
#

# 先生向け：親フォルダにある Minecraft 用ライブラリを読み込む準備。
import sys
from pathlib import Path
import collections
from collections.abc import Iterable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# 古い mcpi が使う名前を補い、Python 3.10 以降でも動くようにする。
if not hasattr(collections, "Iterable"):
    collections.Iterable = Iterable

from mine import *
from random import *
from time import *

mc = Minecraft()


def nihongo_chat(message):
    """先生向け：日本語 Windows の RaspberryJamMod に合わせて送信する。"""
    # この環境の MOD は UTF-8 ではなく CP932 でチャットを受け取る。
    # 別の環境では、その MOD の受信文字コードに合わせる。
    message = str(message).replace("\r", " ").replace("\n", " ")
    command = f"chat.post({message})\n"
    data = command.encode("cp932")
    mc.conn.drain()
    mc.conn.lastSent = command
    mc.conn.socket.sendall(data)


pos = mc.player.getTilePos()

nokori_block_kazu = 0

hani_x = 10 # xほうこうのはんい
hani_z = 10 # zほうこうのはんい

block_syurui = block.GOLD_BLOCK  # ブロックのしゅるいをきめるよ! GOLD_BLOCK=金ブロック

mokuhyou = 10

# はんいのマスのかずより mokuhyou がおおきいと、ブロックをおききれない
masu_no_kazu = (hani_x * 2 + 1) * (hani_z * 2 + 1)
if mokuhyou > masu_no_kazu:
    nihongo_chat("エラーだよ!はんいのおおきさと ブロックのかずを 考えてみよう!")
    sys.exit()

while nokori_block_kazu < mokuhyou:
    x = pos.x + randint(-1 * hani_x, hani_x)
    z = pos.z + randint(-1 * hani_z, hani_z)
    if mc.getBlock(x,pos.y-1,z) != block_syurui.id:
        mc.setBlock(x,pos.y-1,z,block_syurui)
        nokori_block_kazu = nokori_block_kazu + 1

startTime = time()
while nokori_block_kazu > 0:
    pos = mc.player.getTilePos()
    if mc.getBlock(pos.x,pos.y - 1,pos.z) == block_syurui.id:
        mc.setBlock(pos.x,pos.y - 1,pos.z,block.COBBLESTONE)
        mc.player.setPos(pos.x,pos.y + 5, pos.z)
        nokori_block_kazu = nokori_block_kazu - 1
    sleep(0.01)

nihongo_chat(f"{mokuhyou} 個あつめるのに {round(time()-startTime, 1)} 秒かかったよ!")
