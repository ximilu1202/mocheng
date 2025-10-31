import os
import sys
import logging
import asyncio
import discord
import sys
sys.dont_write_bytecode = True
from discord.ext import commands
from dotenv import load_dotenv

# === 確保能找到 cogs 資料夾 ===
sys.path.append(os.path.dirname(__file__))

# === 載入環境變數 ===
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("COMMAND_PREFIX", "!")

# === 基本設定 ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("discord_bot")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None,
                   description="範例 Discord Bot")

# === 機器人啟動事件 ===
@bot.event
async def on_ready():
    logger.info(f"✅ 已登入為 {bot.user} (ID: {bot.user.id})")
    print(f"Bot 已上線：{bot.user}")

# === 錯誤處理 ===
@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"⚠️ 發生錯誤：```{error}```")

# === Ping 範例 ===
@bot.command(name="ping")
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"Pong! 延遲：{latency} ms")

# === 自訂互動式 Help 選單 ===
from discord.ui import View, Select

class HelpSelectView(View):
    def __init__(self):
        super().__init__(timeout=60)
        self.select = Select(
            placeholder="請選擇指令分類👇",
            options=[
                discord.SelectOption(label="🧰 管理功能", description="踢人、封鎖、清理訊息"),
                discord.SelectOption(label="🎮 遊戲互動", description="猜數字、抽卡、擲骰子"),
                discord.SelectOption(label="💬 趣味對話", description="八卦、隨機回覆、每日一語"),
                discord.SelectOption(label="📊 查詢功能", description="伺服器資訊、成員資料查詢"),
            ]
        )
        self.select.callback = self.select_callback
        self.add_item(self.select)

    async def select_callback(self, interaction: discord.Interaction):
        choice = self.select.values[0]

        if "管理" in choice:
            embed = discord.Embed(
                title="🧰 管理功能",
                description=(
                    "**!kick**　踢出成員\n"
                    "**!ban**　封鎖成員\n"
                    "**!clear**　清理指定數量訊息"
                ),
                color=discord.Color.orange()
            )
        elif "遊戲" in choice:
            embed = discord.Embed(
                title="🎮 遊戲互動",
                description=(
                    "**!guess**　猜數字遊戲\n"
                    "**!draw**　抽卡看看你的運氣\n"
                    "**!dice**　擲骰子（1～6）\n"
                    "**!choose**　隨機選擇一個選項"
                ),
                color=discord.Color.green()
            )
        elif "趣味" in choice:
            embed = discord.Embed(
                title="💬 趣味對話",
                description=(
                    "**!gossip**　隨機講一句八卦\n"
                    "**!random**　隨機回覆一句可愛的話\n"
                    "**!daily**　每日一句金句\n"
                    "**!fortune**　占卜你的運勢"
                ),
                color=discord.Color.purple()
            )
        elif "查詢" in choice:
            embed = discord.Embed(
                title="📊 查詢功能",
                description=(
                    "**!serverinfo**　查看伺服器資訊\n"
                    "**!userinfo**　查看使用者資料\n"
                    "**!ping**　查看延遲\n"
                    "**!translate**　文字翻譯（中、英、日、繁簡）"
                ),
                color=discord.Color.blurple()
            )
        else:
            embed = discord.Embed(title="❓ 無此分類", color=discord.Color.red())

        await interaction.response.edit_message(embed=embed, view=self)

@bot.command(name="help")
async def custom_help(ctx):
    view = HelpSelectView()
    embed = discord.Embed(
        title="📚 指令選單",
        description="請從下方選擇想查看的分類 👇",
        color=discord.Color.teal()
    )
    embed.set_footer(text="此選單將於 60 秒後自動關閉 🕒")
    msg = await ctx.send(embed=embed, view=view)
    view.message = msg

# === 載入所有 Cogs（✅ 絕對路徑版本） ===
async def load_extensions():
    cog_path = os.path.join(os.path.dirname(__file__), "cogs")
    for filename in os.listdir(cog_path):
        if filename.endswith(".py"):
            module_name = f"cogs.{filename[:-3]}"
            try:
                await bot.load_extension(module_name)
                print(f"✅ 已載入 {filename}")
            except Exception as e:
                print(f"⚠️ 載入 {filename} 失敗：{e}")


# === 主程式入口 ===
async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
