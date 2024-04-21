#BIRD_BOMB

#1.準備
import pygame as pg,sys
import random
import time
pg.init()
clock = pg.time.Clock()
width = 1366
height = 768
screen = pg.display.set_mode((width,height)) #ノートPCでフルサイズ
pg.display.set_caption("BIRD BOMB") #ゲームタイトル
##時間管理
### ゲーム開始時のタイムスタンプ
game_start_time = time.time()
### ゲームの制限時間（秒）XX
game_duration = 121
def update_timer():
    """タイマーを更新して残り時間を計算する"""
    current_time = time.time()
    elapsed_time = current_time - game_start_time
    remaining_time = max(game_duration - elapsed_time, 0)
    return remaining_time
def draw_timer(remaining_time):
    """ 画面にタイマーを中央上部に表示する """
    font = pg.font.Font("07鉄瓶ゴシック.otf", 50)
    timer_text = font.render(f"残り時間 {int(remaining_time)}", True, pg.Color("white"))
    text_rect = timer_text.get_rect(center=(width / 2, 40))  # 画面の幅の中央、上から10ピクセルの位置
    screen.blit(timer_text, text_rect)
def check_game_over(remaining_time):
    """ ゲーム終了条件をチェックする """
    if remaining_time <= 0:
        page_jump(4)  # ゲーム終了時にリザルト画面に移動
        music_played = False
##メインメニュー(page0)で使う画像
main_logo = pg.image.load("image_birdbomb/logo.png")
main_logo = pg.transform.scale(main_logo,(600,600))
image_width, image_height = main_logo.get_size()
center_x = (1300 - image_width) // 2
center_y = 0
##背景データ
bg01 = pg.image.load("image_birdbomb/bg01.png")
bg02 = pg.image.load("image_birdbomb/bg02.png")
##ブロックデータ
block_img = pg.image.load("image_birdbomb/block.png")
block_img = pg.transform.scale(block_img,(100,100))
block_x = 0
block_y = 668
block_width = 100
block_height = 100
blocks = []
for v in range(15): #15個のblock
    block_rect = pg.Rect(block_x, block_y, block_width, block_height)
    blocks.append(block_rect)
    block_x += 100 #100pxずつずらす
##ネコデータ
cat_left = pg.image.load("image_birdbomb/cat.png")
cat_left = pg.transform.scale(cat_left,(100,100))
cat_right = pg.transform.flip(cat_left,True,False)
cat_rect1 = pg.Rect(340,570,100,100)  #p1のネコは左側の中央
cat_rect2 = pg.Rect(1023,570,100,100) #p2のネコは右側の中央
##プレイヤーのキー入力と変数
vx1 = 0
vy1 = 0
leftFlag1 = True
vx2 = 0
vy2 = 0
leftFlag2 = True
# キーが押されているかどうかを管理する変数
left_key_pressed = False
right_key_pressed = False
left_key_pressed2 = False  # プレイヤー2の左キー入力
right_key_pressed2 = False  # プレイヤー2の右キー入力
##フンデータ
shit_img = pg.image.load("image_birdbomb/shit.png")
shit_img = pg.transform.scale(shit_img,(50,50))
shits = [] #mainmenu
for i in range(60): #60個のフン
    shit = pg.Rect(random.randint(0,768),10*i,15,15)
    shit.w = random.randint(2,5) #フンの落下読度
    shits.append(shit)
#easyのフン設定
shits_easy = []
for e in range(10000): #500個のフン
    sx = random.randint(-100,1400) #余裕を持たせて画面外にも落下させる
    sy = -100 * e #縦に200ずつ
    shits_easy.append(pg.Rect(sx,sy,50,50))
#normalのフン設定
shits_normal = []
for n in range(10000): #500個のフン
    sx = random.randint(-100,1400) #余裕を持たせて画面外にも落下させる
    sy = -75 * n #縦に200ずつ
    shits_normal.append(pg.Rect(sx,sy,50,50))
#hardのフン設定
shits_hard = []
for h in range(10000): #フン
    sx = random.randint(-100,1400) #余裕を持たせて画面外にも落下させる
    sy = -50 * h #縦に200ずつ
    shits_hard.append(pg.Rect(sx,sy,70,70))

##ボタンデータ
btn_width = 300
btn_height = 100
btn_num = 3
btn_between = 100
btn_names = ["image_birdbomb/easy.png","image_birdbomb/normal.png","image_birdbomb/hard.png"]
btn_images = [pg.image.load(filename) for filename in btn_names]
btn_images = [pg.transform.scale(pg.image.load(filename), (btn_width, btn_height)) for filename in btn_names]
##壁データ x,y,w,h
walls1 = [pg.Rect(0,0,680,1),      #上
          pg.Rect(0,0,1,768),      #左
          pg.Rect(677,0,1,768)]    #右
          #pg.Rect(0,668,680,1)]    #下
walls2 = [pg.Rect(686,0,680,1),    #上
          pg.Rect(683,0,1,768),    #左
          pg.Rect(1364,0,1,768)]   #右
          #pg.Rect(686,668,680,1)]  #下

##メインループで使う変数
pushFlag = False
page = 0
score1 = 0  # プレイヤー1のスコア
score2 = 0  # プレイヤー2のスコア
music_played = False
last_score_update = 0  # スコアを最後に更新した時刻
##音楽の初期設定
MUSIC_END_EVENT = pg.USEREVENT + 1
pg.mixer.music.set_endevent(MUSIC_END_EVENT)
##メインメニュー
def mainmenu():
    global page, music_played
    #music_played = False
    if not music_played:
        pg.mixer.music.stop()
        #pg.mixer.init()
        pg.mixer.music.load("sound_birdbomb/main.wav")
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.play()
        music_played = True
    # 画面をNAVY色で塗りつぶす
    screen.fill(pg.Color("NAVY"))
    key = pg.key.get_pressed()
    ###フンの処理
    for shit in shits:
        shit.y += shit.w
        screen.blit(shit_img,shit)
        if shit.y > 768:
            shit.x = random.randint(0,1366)
            shit.y = 0 #フンは一番上に戻る
            
    ###ロゴの処理
    screen.blit(main_logo,(center_x,center_y))
    ###ボタンの処理
    total_button_width = btn_num * btn_width + (btn_num - 1) * btn_between
    start_x = (screen.get_width() - total_button_width) // 2  # 画面の両端に100pxのスペースを持たせる
    for i in range(btn_num):
        btn_x = start_x + i * (btn_width + btn_between)
        btn_y = 650
        screen.blit(btn_images[i], (btn_x, btn_y))
        #キーボードで数字の1, 2, 3が押されたときの処理
        if key[pg.K_1] and i == 0:
            page_jump(i + 1)  # ボタンに対応するページ番号を渡す
        elif key[pg.K_2] and i == 1:
            page_jump(i + 1)  # ボタンに対応するページ番号を渡す
        elif key[pg.K_3] and i == 2:
            page_jump(i + 1)  # ボタンに対応するページ番号を渡す

        
##ページジャンプ関数
def page_jump(newpage):
    global page, pushFlag, music_played
        #if music_played:
    pg.mixer.music.stop()
    music_played = False
    screen.fill(pg.Color("BLACK"))
    pg.mixer.Sound("sound_birdbomb/pi.mp3").play()
    page = newpage
    pushFlag = True
##中間壁の描画
def center_wall():
    # ラインを描画するためのコード
    line_color = pg.Color("WHITE")
    line_start = (width // 2 - 3, 0)  # 幅が6pxなので中央から3px左にスタート
    line_end = (width // 2 - 3, height)  # 幅が6pxなので中央から3px左にエンド
    pg.draw.line(screen, line_color, line_start, line_end, 6)
##猫の描画関数
def draw_cats():
    # プレイヤー1の猫の描画
    screen.blit(cat_left if leftFlag1 else cat_right, cat_rect1) 
    # プレイヤー2の猫の描画
    screen.blit(cat_left if leftFlag2 else cat_right, cat_rect2)
#スコア描画
def draw_scores():
    """ 両プレイヤーのスコアを画面に表示する """
    font = pg.font.Font("07鉄瓶ゴシック.otf", 50)  # スコアのフォントサイズ
    # プレイヤー1のスコア
    score_text1 = font.render(f"Player1 スコア{score1}", True, pg.Color("white"))
    screen.blit(score_text1, (10, 15))  # 左上に表示
    # プレイヤー2のスコア
    score_text2 = font.render(f"Player2 スコア{score2}", True, pg.Color("white"))
    screen.blit(score_text2, (880,15))  # 右上に表示
# プレイヤー1の猫の描画
cat_rect1.x += vx1
if leftFlag1:
    screen.blit(cat_left, cat_rect1)
else:
    screen.blit(cat_right, cat_rect1)
# プレイヤー2の猫の描画
cat_rect2.x += vx2
if leftFlag2:
    screen.blit(cat_left, cat_rect2)
else:
    screen.blit(cat_right, cat_rect2)

##壁の描画関数
def wall_cat():
    global vx1, vy1, vx2, vy2
    # プレイヤー1の猫の位置を更新
    cat_rect1.x += vx1
    cat_rect1.y += vy1
    # 壁との衝突判定
    collision_index = cat_rect1.collidelist(walls1)
    if collision_index != -1:
        wall = walls1[collision_index]
        if vx1 > 0:  # 右に移動中
            cat_rect1.right = wall.left
        elif vx1 < 0:  # 左に移動中
            cat_rect1.left = wall.right
        if vy1 > 0:  # 下に移動中
            cat_rect1.bottom = wall.top
        elif vy1 < 0:  # 上に移動中
            cat_rect1.top = wall.bottom
    # プレイヤー2の猫の位置を更新
    cat_rect2.x += vx2
    cat_rect2.y += vy2
    # 壁との衝突判定
    collision_index = cat_rect2.collidelist(walls2)
    if collision_index != -1:
        wall = walls2[collision_index]
        if vx2 > 0:  # 右に移動中
            cat_rect2.right = wall.left
        elif vx2 < 0:  # 左に移動中
            cat_rect2.left = wall.right
        if vy2 > 0:  # 下に移動中
            cat_rect2.bottom = wall.top
        elif vy2 < 0:  # 上に移動中
            cat_rect2.top = wall.bottom
    ###壁の描画
    wall_color = pg.Color("white")  # 壁の色
    for wall in walls1:
        pg.draw.rect(screen, wall_color, wall)
    for wall in walls2:
        pg.draw.rect(screen, wall_color, wall)


##gameresult
def gameresult():
    global page, music_played, score1, score2  # score1とscore2をグローバルに指定
    screen.fill(pg.Color("BLACK"))  # 背景を黒で塗りつぶす
    ##music
    if not music_played:
        pg.mixer.music.stop()
        pg.mixer.music.load("sound_birdbomb/result.mp3")
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.play(-1)
        music_played = True
    ##リザルトデータ
    result_img = pg.image.load("image_birdbomb/result.png")
    result_img = pg.transform.scale(result_img,(width,height))
    screen.blit(result_img, (0, 0))
    # プレイヤー1のスコアを表示
    font = pg.font.Font("07鉄瓶ゴシック.otf", 250)
    score_text1 = font.render(f" {score1}", True, pg.Color("white"))
    screen.blit(score_text1, (-50, 450))
    # プレイヤー2のスコアを表示
    score_text2 = font.render(f" {score2}", True, pg.Color("white"))
    screen.blit(score_text2, (650, 450))
    #mainmenuへ戻る
    result_main = pg.image.load("image_birdbomb/main_menu.png")  # main_menu.png のファイルパスを正しく指定してください
    result_main = pg.transform.scale(result_main, (250, 100))
    screen.blit(result_main, (10, 5))
    

#猫とフンの衝突
def shits_cat_coll(shits_list):
    global score1, score2
    for shit in shits_list:
        if shit.colliderect(cat_rect1):
            score1 -= 10
            shit.x = random.randint(0, 1366)
            shit.y = -200  # フンは一番上に戻る
            pg.mixer.Sound("sound_birdbomb/shit_cat.mp3").play()
        elif shit.colliderect(cat_rect2):
            score2 -= 10
            shit.x = random.randint(0, 1366)
            shit.y = -200
            pg.mixer.Sound("sound_birdbomb/shit_cat.mp3").play()

##各モード
def easy():
    global page, score1, score2, time, music_played, game_start_time, last_score_update
    # 最初にゲームモードに入った時のみ、次のコードを実行
    if page == 1 and not music_played:
        game_start_time = time.time()  # ゲーム開始時刻をリセット
        last_score_update = game_start_time  # スコア更新時刻をリセット
        score1 = 0  # スコアをリセット
        score2 = 0  # スコアをリセット
        #pg.mixer.music.stop()
        pg.mixer.music.load("sound_birdbomb/easy.mp3")
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.play(-1)
        music_played = True

    ###背景
    screen.fill(pg.Color("BLACK"))
    screen.blit(bg01,(0,0))
    screen.blit(bg02,(683,0))
    ###ブロックの処理
    for block in blocks:
        screen.blit(block_img,block)
    ###中央壁と上左右
    center_wall()
    wall_cat()
    ###猫の描画
    draw_cats()
    ###猫の位置更新
    cat_rect1.x += vx1
    cat_rect1.y += vy1
    cat_rect2.x += vx2
    cat_rect2.y += vy2
    #easyのフン処理
    for shits_e in shits_easy:
        shits_e.y += 6 #落下速度
        screen.blit(shit_img,shits_e)
    ###フンと猫の処理
    shits_cat_coll(shits_easy)
    # タイマーの更新と描画
    remaining_time = update_timer()
    draw_timer(remaining_time)
    if check_game_over(remaining_time):
        page = 4
        music_played = False

    # スコアの自動加算
    current_time = time.time()
    if current_time - last_score_update >= 1:
        score1 += 10
        score2 += 10
        last_score_update = current_time  # 最後のスコア更新時刻を更新
    # スコアの表示
    draw_scores()

def normal():
    global page, score1, score2, time, music_played, game_start_time, last_score_update
    # 最初にゲームモードに入った時のみ、次のコードを実行
    if page == 2 and not music_played:
        game_start_time = time.time()  # ゲーム開始時刻をリセット
        last_score_update = game_start_time  # スコア更新時刻をリセット
        score1 = 0  # スコアをリセット
        score2 = 0  # スコアをリセット
        #pg.mixer.music.stop()
        pg.mixer.music.load("sound_birdbomb/normal.mp3")
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.play(-1)
        music_played = True
    ###背景
    screen.fill(pg.Color("BLACK"))
    screen.blit(bg01,(0,0))
    screen.blit(bg02,(683,0))
    ###ブロックの処理
    for block in blocks:
        screen.blit(block_img,block)
    ###中央壁と上左右
    center_wall()
    wall_cat()
    ###猫の描画
    draw_cats()
    ###猫の位置更新
    cat_rect1.x += vx1
    cat_rect1.y += vy1
    cat_rect2.x += vx2
    cat_rect2.y += vy2
    #normalのフン処理
    for shits_n in shits_normal:
        shits_n.y += 8 #落下速度
        screen.blit(shit_img,shits_n)
    ###フンと猫の処理
    shits_cat_coll(shits_normal)
    # タイマーの更新と描画
    remaining_time = update_timer()
    draw_timer(remaining_time)
    if check_game_over(remaining_time):
        page = 4
        music_played = False

    # スコアの自動加算
    current_time = time.time()
    if current_time - last_score_update >= 1:
        score1 += 10
        score2 += 10
        last_score_update = current_time  # 最後のスコア更新時刻を更新
    # スコアの表示
    draw_scores()
    
def hard():
    global page, score1, score2, time, music_played, game_start_time, last_score_update
    # 最初にゲームモードに入った時のみ、次のコードを実行
    if page == 3 and not music_played:
        game_start_time = time.time()  # ゲーム開始時刻をリセット
        last_score_update = game_start_time  # スコア更新時刻をリセット
        score1 = 0  # スコアをリセット
        score2 = 0  # スコアをリセット
        #pg.mixer.music.stop()
        pg.mixer.music.load("sound_birdbomb/hard.mp3")
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.play(-1)
        music_played = True
    ###背景
    screen.fill(pg.Color("BLACK"))
    screen.blit(bg01,(0,0))
    screen.blit(bg02,(683,0))
    ###ブロックの処理
    for block in blocks:
        screen.blit(block_img,block)
    ###中央壁と上左右
    center_wall()
    wall_cat()
    ###猫の描画
    draw_cats()
    ###猫の位置更新
    cat_rect1.x += vx1
    cat_rect1.y += vy1
    cat_rect2.x += vx2
    cat_rect2.y += vy2
    #easyのフン処理
    for shits_h in shits_hard:
        shits_h.y += 10 #落下速度
        screen.blit(shit_img,shits_h)
    ###フンと猫の処理
    shits_cat_coll(shits_hard)
    # タイマーの更新と描画
    remaining_time = update_timer()
    draw_timer(remaining_time)
    if check_game_over(remaining_time):
        page = 4
        music_played = False

    # スコアの自動加算
    current_time = time.time()
    if current_time - last_score_update >= 1:
        score1 += 10
        score2 += 10
        last_score_update = current_time  # 最後のスコア更新時刻を更新
    # スコアの表示
    draw_scores()
    
#2.メインループ
while True:
    if page == 0:
        mainmenu()
    elif page == 1:
        easy()
    elif page == 2:
        normal()
    elif page == 3:
        hard()
    elif page == 4:
        gameresult()
    ###keyイベント:
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_l:
                right_key_pressed = True
            elif event.key == pg.K_j:
                left_key_pressed = True
            elif event.key == pg.K_d:
                right_key_pressed2 = True
            elif event.key == pg.K_a:
                left_key_pressed2 = True
            elif event.key == pg.K_SPACE:
                if page in [1, 2, 3]:  # ゲームのページの場合のみ
                    page_jump(0)  # mainmenuに戻る
                    #page = 0  # メインメニューに戻る
                    #music_played = False  # 音楽フラグをリセット
                    #continue  # 他のキーイベント処理をスキップ
                if page == 4:  # リザルト画面のページ番号に応じて条件を設定
                    page = 0  # メインメニューページに戻る
                    music_played = False  # 音楽フラグをリセット
        elif event.type == pg.KEYUP:
            if event.key == pg.K_l:
                right_key_pressed = False
            elif event.key == pg.K_j:
                left_key_pressed = False
            elif event.key == pg.K_d:
                right_key_pressed2 = False
            elif event.key == pg.K_a:
                left_key_pressed2 = False
        ###音楽ループイベント
        elif event.type == MUSIC_END_EVENT and music_played:
            # 音楽が再生終了したら再度再生する
            if page == 0:
                pg.mixer.music.load("sound_birdbomb/main.wav")
            elif page == 1:
                pg.mixer.music.load("sound_birdbomb/easy.mp3")
            elif page == 2:
                pg.mixer.music.load("sound_birdbomb/normal.mp3")
            elif page == 3:
                pg.mixer.music.load("sound_birdbomb/hard.mp3")
            pg.mixer.music.play(-1)
            #music_played = False
        #終了イベント
        elif event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        # 猫の速度を設定
        # プレイヤーの猫の速度を設定
        if right_key_pressed:
            vx1 = 5
            leftFlag1 = False
        elif left_key_pressed:
            vx1 = -5
            leftFlag1 = True
        else:
            vx1 = 0

        if right_key_pressed2:
            vx2 = 5
            leftFlag2 = False
        elif left_key_pressed2:
            vx2 = -5
            leftFlag2 = True
        else:
            vx2 = 0

        # プレイヤーの猫の新しい位置を計算
        new_x1 = cat_rect1.x + vx1
        new_y1 = cat_rect1.y + vy1
        new_x2 = cat_rect2.x + vx2
        new_y2 = cat_rect2.y + vy2

        # 仮のRectを作成して衝突判定
        temp_rect1 = pg.Rect(new_x1, new_y1, cat_rect1.width, cat_rect1.height)
        temp_rect2 = pg.Rect(new_x2, new_y2, cat_rect2.width, cat_rect2.height)

        # 壁と猫の衝突判定
        if temp_rect1.collidelist(walls1) == -1 and temp_rect1.collidelist(walls2) == -1:
            cat_rect1.x = new_x1
            cat_rect1.y = new_y1
        if temp_rect2.collidelist(walls1) == -1 and temp_rect2.collidelist(walls2) == -1:
            cat_rect2.x = new_x2
            cat_rect2.y = new_y2

    # フレームレートの制御
    clock.tick(30)
            
    #更新
    pg.display.update()



