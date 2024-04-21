# portfolio

データ分析のポートフォリオです。

## 背景
　近年、コンピュータゲームを用いた認知機能のトレーニングが注目されている。認知機能の中でも、特に注意機能は患者の日常生活における判断や行動の正確性(安全性)を左右するため、その向上は生活の質の向上に直結すると考えられる。  
　具体的には、注意機能が向上することで転倒リスクが軽減できる。転倒が寝たきりに繋がるケースが多く、医療現場では対策が急務である。さらに、精神疾患の多くや高齢者は注意機能の低下および注意機能障害が顕著にみられるため、転倒に繋がりやすい。  
　ゲームが治療プログラムとして、注意機能の向上に寄与するか否かを明らかにすることで、今後の注意機能トレーニングのためのゲーム開発や治療手段の選定に貢献することを期待し本分析を実施した。

## 目的
　Pygameで自作したゲームを用いて、ゲーム実施前後の注意機能スコアを比較することにより、注意機能への効果があるか否かを検証することである。  
　さらに、得られたゲーム前後のスコアやその他の情報を利用し、機械学習モデル（回帰モデル）を構築し、新患者のスコアを予測することで治療前説明、患者の動機付け、治療効果の長期的な効果検証を行うことである。

## ディレクトリ構成
### ディレクトリ1：data_analysis
データを分析したノートブックやノートブック内で使用している画像ファイルが格納されている。
ーーーーーーーーーーーーーーーーーーーーーーーーーー
メインソースコード：cognitive function analysis
ーーーーーーーーーーーーーーーーーーーーーーーーーー
### ディレクトリ2：game_center
ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
メインソースコード：bird_bomb.py
ゲームのexe化ファイル：バード・ボム.exe(実行すればゲームスタート)
ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
◇◇◇ ゲームの説明（分析ノートブック内でも行っている） ◇◇◇
◆ゲームのコンセプト  
　本ゲームのコンセプトは「都会に住む猫が青い鳥のフンを避けるゲームでスコアを競う」というやや斬新でシンプルなものである。このようなコンセプトにした理由は以下の通り。  
①シンプルでわかりやすいゲームが高齢者への導入には必須である  
②ややクスッと笑えるようなコンセプトが対象者の興味を引き出しやすい  

◆メインメニューについて  
　以下に示す画像は本ゲームのメインメニュー画面である。高齢者でもわかりやすいシンプルなユーザーインターフェースにしている。  
　メインメニューを見てわかるように難易度を3段階設定している。かんたん・ふつう・むずかしいで対象者に合わせて「ゲームを楽しめる」ことを前提に調整可能になっている。  
　各モードの違いはゲーム画面で出現する「鳥のフンの落下速度」である。かんたんでは遅く容易に回避できるが、むずかしいでは速く回避困難なため、いかに減点されないかを競うことになる。  

◆ゲームのステージ画面について  
　ゲームのステージ画面では、残り時間と現在のスコアを表示できるようにしている。スコアが加算されるシステムとしては1秒経過する度に+10が加算され、フンとネコが衝突してしまうと-10がスコアに反映されてしまう。残り時間が0になると自動的にリザルト画面に推移する。  

◆リザルト画面について  
　リザルト画面はゲームの残り時間が0になると自動的に表示される。大きな文字サイズでプレイヤーごとに表示される。見学している人にも見えるようにすることで自然とコミュニケーションが生まれるように工夫している。

◆操作方法
＜プレイヤー1の操作＞  
左へ移動：J  
右へ移動：L  
＜プレイヤー2の操作＞  
左へ移動：A  
右へ移動：D  
＜その他のキー操作＞  
メインメニューに戻る：space  