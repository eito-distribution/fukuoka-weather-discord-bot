# ==== 必要なモジュールのインポート ====
import discord                     # DiscordのAPIを扱うdiscord.pyライブラリ(Discord Botを制作するために必須です。)
from discord.ext import commands   # コマンド拡張機能を利用するためのモジュール(スラッシュコマンドを実装するのに使います。)
import requests                    # Webからデータを取得するためのHTTPクライアントライブラリ(天気情報を持ってくるのに使います。)

# ==== ボットの基本設定 ====
TOKEN = "あなたのDisocrd Tokenを入力しましょう！"  # Discord Botのトークン文字列（⚠️‼️ここのコードは絶対に他人に教えてはいけません‼️⚠️）

# ボットオブジェクトの作成。コマンドプレフィックス（先頭記号）は "/" に設定します。
# intents はBotが受け取るイベントの種類を指定するもの。基本的な権限のみ有効化（既定のIntents.default()）します。
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)

# ==== スラッシュコマンド（ハイブリッドコマンド）の定義 ====
@bot.hybrid_command(name="tenki", description="福岡県の天気予報を表示します")  #name="Botに天気を聞くコマンドを入力します。" description="コマンドの説明を入力します。"
async def weather(ctx):
    """
    福岡の天気予報を取得して返すコマンド。
    このコマンドは '/' プレフィックスでも '/weather' スラッシュコマンドでも実行できます。
    """
    # 気象庁の天気予報API（JSONデータ）から福岡県の予報を取得します。
    # 福岡県のエリアコードは 400000 です:contentReference[oaicite:0]{index=0}。
    url = "https://www.jma.go.jp/bosai/forecast/data/forecast/400000.json"
    response = requests.get(url)        # APIにHTTPリクエストを送信
    data = response.json()             # 返ってきたJSONデータをPythonの辞書型に変換:contentReference[oaicite:1]{index=1}
    # JSON構造から、天気予報の文章を抽出します。
    # data[0]["timeSeries"][0]["areas"][0]["weathers"][0] に今日の天気文章が入っています。
    weather_text = data[0]["timeSeries"][0]["areas"][0]["weathers"][0]
    weather_text = weather_text.replace('　', '')  # 全角スペースが含まれる場合があるので除去
    # メッセージの組み立てと送信
    message = f"福岡県の今日の天気は: {weather_text} です。"
    await ctx.send(message)  # 天気予報メッセージを送信

# ==== ボット起動時のイベントハンドラ ====
@bot.event
async def on_ready():
    """
    Botが起動してDiscordに接続されたときに1度だけ実行される処理。
    """
    print(f"Botログイン完了: {bot.user}")  # 開発用にコンソールにログイン情報を表示
    # スラッシュコマンドをDiscordに同期（登録）します。
    try:
        synced = await bot.tree.sync()
        print(f"スラッシュコマンド同期完了（{len(synced)}個のコマンド）")
    except Exception as e:
        print(f"コマンド同期時にエラー: {e}")

# ==== Botの起動 ====
bot.run(TOKEN)
