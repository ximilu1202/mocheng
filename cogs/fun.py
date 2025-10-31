import random
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="gossip")
    async def gossip(self, ctx):
        """隨機講一句八卦"""
        gossips = [
            "你知道嗎？機器人其實也會偷懶。",
            "有人說今天的天氣會影響心情喔～",
            "別告訴別人，其實我最喜歡你！🤫",
            "聽說XX暗戀誰誰誰～",
            "今天老師忘記帶講義🤣",
            "隔壁伺服器又出大事了！"
        ]
        await ctx.send(random.choice(gossips))

    @commands.command(name="random")
    async def random_reply(self, ctx):
        """隨機回覆一句可愛的話"""
        replies = [
            "喵～(ฅ'ω'ฅ)",
            "你今天看起來特別棒呢！✨",
            "給你一個虛擬擁抱 🤗",
            "你好可愛喔！(⁎˃ᴗ˂⁎)",
            "今天也要加油呀！💪",
            "嘿嘿～我在這裡陪你～"
        ]
        await ctx.send(random.choice(replies))

    @commands.command(name="daily")
    async def daily(self, ctx):
        """每日一句金句"""
        quotes = [
            "成功的秘訣就是開始行動。",
            "再小的努力，乘以365都很驚人。",
            "不要害怕緩慢前進，只怕停滯不前。",
            "失敗是成功的母親。",
            "保持微笑，就會有奇蹟發生。",
            "每一天都值得被好好過。"
        ]
        await ctx.send(random.choice(quotes))

async def setup(bot):
    await bot.add_cog(Fun(bot))
