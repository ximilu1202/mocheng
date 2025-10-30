import os
import logging
import asyncio
from discord.ext import commands
import discord
from dotenv import load_dotenv

# 載入 .env（本地開發）
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)
print("🔍 ENV PATH:", env_path)
print("🔍 Token loaded:", os.getenv("DISCORD_TOKEN"))
print("🔍 Command prefix:", os.getenv("COMMAND_PREFIX"))
print("ENV PATH:", env_path)
print("TOKEN:", os.getenv("DISCORD_TOKEN"))

TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("COMMAND_PREFIX", "!")

# 設定基礎日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("discord_bot")

intents = discord.Intents.default()
intents.message_content = True  # 如果要處理文字內容，需啟用
intents.members = True  # 若需要成員事件，保留
intents.presences = False       # 可選，不需要就關掉

bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None,
                   description="範例 Discord Bot")

# ---------- Events ----------
@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print(f"Bot 已上線：{bot.user} (ID: {bot.user.id})")
    # 註冊 sync app commands（slash）到伺服器（可視情況關掉）
    try:
        await bot.tree.sync()
        logger.info("Slash commands synced.")
    except Exception as e:
        logger.exception("Failed to sync slash commands: %s", e)

@bot.event
async def on_command_error(ctx, error):
    # 顯示詳細錯誤
    import traceback
    traceback_text = "".join(traceback.format_exception(type(error), error, error.__traceback__))
    await ctx.send(f"⚠️ 錯誤發生：```{traceback_text[:1900]}```")

# ---------- Basic commands ----------
@bot.command(name="ping")
async def ping(ctx):
    """簡單回應延遲"""
    latency = round(bot.latency * 1000)  # ms
    await ctx.send(f"Pong! 延遲：{latency} ms")

@bot.command(name="say")
@commands.has_permissions(manage_messages=True)
async def say(ctx, *, message: str):
    """讓機器人說指定的話（需要 manage_messages 權限）"""
    await ctx.message.delete()
    await ctx.send(message)

# ---------- Interactive Help Command ----------

from discord.ui import View, Select
import discord

class HelpSelectView(View):
    def __init__(self):
        super().__init__(timeout=60)  # 互動持續 60 秒

        # 建立選單項目
        self.select = Select(
            placeholder="請選擇想查看的指令分類 :point_down:",
            options=[
                discord.SelectOption(label="🧰 管理功能", description="踢人、封鎖、清理訊息", emoji="🧰"),
                discord.SelectOption(label="🎮 遊戲互動", description="猜數字、抽卡、擲骰子", emoji="🎮"),
                discord.SelectOption(label="💬 趣味對話", description="八卦、隨機回覆、每日一語", emoji="💬"),
                discord.SelectOption(label="📊 查詢功能", description="伺服器資訊、成員資料查詢", emoji="📊"),
            ]
        )
        self.select.callback = self.select_callback
        self.add_item(self.select)

    async def select_callback(self, interaction: discord.Interaction):
        """處理選單選擇事件"""
        choice = self.select.values[0]

        if "管理" in choice:
            embed = discord.Embed(
                title="🧰 管理功能",
                description=(
                    "`!kick <@使用者>`：踢出成員\n"
                    "`!ban <@使用者>`：封鎖成員\n"
                    "`!clear <數量>`：清理指定數量的訊息"
                ),
                color=discord.Color.orange()
            )

        elif "遊戲" in choice:
            embed = discord.Embed(
                title="🎮 遊戲互動",
                description=(
                    "`!guess`：猜數字遊戲\n"
                    "`!draw`：抽卡看看你的運氣！\n"
                    "`!dice`：擲骰子（1～6）"
                ),
                color=discord.Color.green()
            )

        elif "趣味" in choice:
            embed = discord.Embed(
                title="💬 趣味對話",
                description=(
                    "`!gossip`：隨機講一句八卦🤭\n"
                    "`!random`：隨機回覆一句可愛的話(⁎˃ᴗ˂⁎)\n"
                    "`!daily`：每日一句金句✨"
                ),
                color=discord.Color.purple()
            )

        elif "查詢" in choice:
            embed = discord.Embed(
                title="📊 查詢功能",
                description=(
                    "`!serverinfo`：查看伺服器資訊\n"
                    "`!userinfo <@使用者>`：查看成員資料\n"
                    "`!ping`：查看延遲"
                ),
                color=discord.Color.blurple()
            )

        else:
            embed = discord.Embed(title=":question: 無此分類", color=discord.Color.red())

        embed.set_footer(text="選單將於 60 秒後自動關閉 🕒")

        await interaction.response.edit_message(embed=embed, view=self)

    async def on_timeout(self):
        """超時後鎖定互動"""
        for child in self.children:
            child.disabled = True
        try:
            await self.message.edit(content="⏳ 選單已超時，請重新輸入 `!help` 以再次開啟。", view=self)
        except Exception:
            pass

@bot.command(name="help")
async def custom_help(ctx):
    """互動式說明選單"""
    view = HelpSelectView()
    embed = discord.Embed(
        title="📚 指令分類選單",
        description="請從下方選擇想查看的分類 👇",
        color=discord.Color.teal()
    )
    embed.set_footer(text="選單將於 60 秒後自動關閉 🕒")

    sent = await ctx.send(embed=embed, view=view)
    view.message = sent  # 儲存訊息給 timeout 時使用

# ---------- Cog 管理（僅限擁有者） ----------
@bot.command(name="load")
@commands.is_owner()
async def load_cog(ctx, cog: str):
    """載入 cog，參數是 module path，例如 cogs.example"""
    try:
        bot.load_extension(cog)
        await ctx.send(f"已載入 {cog}")
    except Exception as e:
        await ctx.send(f"載入失敗：{e}")

@bot.command(name="unload")
@commands.is_owner()
async def unload_cog(ctx, cog: str):
    try:
        bot.unload_extension(cog)
        await ctx.send(f"已卸載 {cog}")
    except Exception as e:
        await ctx.send(f"卸載失敗：{e}")

@bot.command(name="reload")
@commands.is_owner()
async def reload_cog(ctx, cog: str):
    try:
        bot.reload_extension(cog)
        await ctx.send(f"已重新載入 {cog}")
    except Exception as e:
        await ctx.send(f"重新載入失敗：{e}")

# ---------- 範例 Slash Command ----------
@bot.tree.command(name="hello", description="Say hello to the bot")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello, {interaction.user.mention} 👋")

# ---------- 自動載入 cogs 下的所有模組 ----------
if __name__ == "__main__":
    # 載入 cogs 目錄下的所有 python 檔（例如 cogs/example.py -> cogs.example）
    import glob
    for filepath in glob.glob("cogs/*.py"):
        module = filepath[:-3].replace("/", ".").replace("\\", ".")
        try:
            bot.load_extension(module)
            logger.info(f"Loaded cog: {module}")
        except Exception as e:
            logger.exception(f"Failed to load cog {module}: {e}")

    if not TOKEN:
        raise RuntimeError("DISCORD_TOKEN 環境變數未設定。請在 .env 或環境中設置。")
    bot.run(TOKEN)
