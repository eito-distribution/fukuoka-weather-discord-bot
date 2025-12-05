import discord
from discord.ext import commands
import requests

# ===== ここは授業のときに各PCで書き換える =====
TOKEN = "YOUR_BOT_TOKEN_HERE"      # 自分のBotトークンに差し替え
GUILD_ID = 123456789012345678      # Botを使うDiscordサーバーのID
# =============================================

# Discordの権限設定（Intents）
intents = discord.Intents.default()
intents.message_content = True  # メッセージ内容を扱うときに必要

# Bot本体（!から始まるコマンド & スラッシュコマンドを扱う）
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    """Bot起動時に1度だけ呼ばれる"""
    print(f"ログインしました: {bot.user}")

    # スラッシュコマンドをDiscordに登録（同期）
    try:
        guild = discord.Object(id=GUILD_ID)
        synced = await bot.tree.sync(guild=guild)
        print(f"{len(synced)} 個のスラッシュコマンドを同期しました")
    except Exception as e:
        print(f"スラッシュコマンド同期エラー: {e}")

# ハイブリッドコマンド
# → /tenki でも !tenki でも呼び出せる
@bot.hybrid_command(name="tenki", description="福岡のきょうの天気を表示します")
async def tenki(ctx: commands.Context):
    """福岡の天気予報を取得して返信するコマンド"""
    # 気象庁API（福岡県: 400000）の天気予報JSON
    jma_url = "https://www.jma.go.jp/bosai/forecast/data/forecast/400000.json"

    try:
        res = requests.get(jma_url, timeout=5)
        res.raise_for_status()
        data = res.json()

        # data[0]: 府県予報区
        # timeSeries[0]: 天気・風・波など
        # areas[0]: 福岡地方
        # weathers[0]: きょうの天気の文章
        weather_text = data[0]["timeSeries"][0]["areas"][0]["weathers"][0]
        weather_text = weather_text.replace("　", "")  # 全角スペースを削除

        await ctx.send(f"福岡の天気: {weather_text}")
    except Exception as e:
        print(f"天気取得エラー: {e}")
        await ctx.send("天気情報の取得に失敗しました…あとでやり直してみてください。")

# プログラムを実行するときの入り口
if __name__ == "__main__":
    if TOKEN == "YOUR_BOT_TOKEN_HERE":
        raise RuntimeError("main.py の TOKEN を自分のBotトークンに書き換えてください。")
    bot.run(TOKEN)
