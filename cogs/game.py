import random
from discord.ext import commands

class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="dice")
    async def dice(self, ctx):
        """擲骰子 🎲"""
        await ctx.send(f"🎲 你擲出了 **{random.randint(1, 6)}** 點！")

    @commands.command(name="draw")
    async def draw(self, ctx):
        """抽卡系統 🃏"""
        cards = ["SSR 🌟", "SR 💎", "R ⭐", "N 😐"]
        await ctx.send(f"🃏 你抽到了：**{random.choice(cards)}**！")

    @commands.command(name="guess")
    async def guess(self, ctx):
        """猜數字遊戲（1～10）🎯"""
        num = random.randint(1, 10)
        await ctx.send("我想了一個 **1～10** 的數字，來猜猜看吧！（15 秒內回答）")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await self.bot.wait_for("message", check=check, timeout=15)
            if not msg.content.isdigit():
                await ctx.send("❗ 請輸入數字喔～")
                return

            guess = int(msg.content)
            if guess == num:
                await ctx.send("🎉 恭喜答對！")
            else:
                await ctx.send(f"😅 錯了，是 **{num}**！")
        except Exception:
            await ctx.send("⏰ 超時囉！")

async def setup(bot):
    await bot.add_cog(Game(bot))



class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="choose")
    async def choose(self, ctx, *options):
        """從多個選項中隨機挑選一個"""
        if not options:
            await ctx.send("請提供幾個選項，例如：`!choose 蘋果 香蕉 葡萄` 🍎🍌🍇")
            return
        choice = random.choice(options)
        await ctx.send(f"🎲 我選擇…… **{choice}**！")

    @commands.command(name="fortune")
    async def fortune(self, ctx, *, question=None):
        """隨機抽籤運勢"""
        fortunes = [
            "🌟 大吉：萬事如意，今日適合行動！",
            "✨ 中吉：運勢不錯，保持好心情！",
            "😊 小吉：小有收穫，注意細節。",
            "🍀 吉：一切平穩，穩中求勝。",
            "😐 凶：小心謹慎，避免衝動。",
            "⚡ 小凶：可能有小挫折，別氣餒！",
            "💀 大凶：建議低調行事。",
            "🌌 特殊指引：命運之線正被改寫……"
        ]
        result = random.choices(
            fortunes,
            weights=[15, 20, 20, 15, 10, 8, 6, 1],
            k=1
        )[0]
        if question:
            await ctx.send(f"🔮 你問：「{question}」\n結果是：{result}")
        else:
            await ctx.send(f"🔮 你的今日運勢是：{result}")

async def setup(bot):
    await bot.add_cog(Game(bot))
