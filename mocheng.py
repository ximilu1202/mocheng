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

bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=commands.DefaultHelpCommand(),
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
    # 常見錯誤處理範例
    if isinstance(error, commands.CommandNotFound):
        return  # 忽略未知指令
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("缺少參數。請檢查指令使用方式。")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("你沒有權限執行此指令。")
    else:
        logger.exception("Unhandled command error: %s", error)
        await ctx.send("執行指令時發生錯誤。")

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
