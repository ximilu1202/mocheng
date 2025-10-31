from discord.ext import commands
from deep_translator import GoogleTranslator
import discord

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def serverinfo(self, ctx):
        """查看伺服器資訊 📊"""
        guild = ctx.guild
        embed = discord.Embed(
            title=f"{guild.name} 的伺服器資訊",
            color=discord.Color.blue()
        )
        embed.add_field(name="👥 成員數", value=len(guild.members))
        embed.add_field(name="📅 建立時間", value=guild.created_at.strftime("%Y-%m-%d"))
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        await ctx.send(embed=embed)

    @commands.command()
    async def userinfo(self, ctx, member: discord.Member = None):
        """查看使用者資訊 🧍"""
        member = member or ctx.author
        embed = discord.Embed(
            title=f"{member.display_name} 的使用者資料",
            color=discord.Color.green()
        )
        embed.add_field(name="🪪 使用者名稱", value=str(member), inline=False)
        embed.add_field(name="📅 加入時間", value=member.joined_at.strftime("%Y-%m-%d"))
        embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
        await ctx.send(embed=embed)

    @commands.command(name="translate")
    async def translate(self, ctx, lang, *, text):
        """
        翻譯文字 🌐
        用法：
        !translate zh-tw Hello
        !translate en 你好
        !translate ja 我愛你
        支援語言：
        zh-tw（繁體）、zh-cn（簡體）、en（英文）、ja（日文）
        """
        lang = lang.lower()
        supported = ["zh-tw", "zh-cn", "en", "ja"]
        if lang not in supported:
            await ctx.send(f"⚠️ 不支援的語言代碼，請使用以下之一：{', '.join(supported)}")
            return

        try:
            result = GoogleTranslator(source='auto', target=lang).translate(text)
            embed = discord.Embed(
                title="🌍 翻譯結果",
                description=f"**{result}**",
                color=discord.Color.teal()
            )
            embed.set_footer(text=f"語言：{lang} ｜ 由 deep-translator 提供")
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"⚠️ 翻譯失敗：{e}")

async def setup(bot):
    await bot.add_cog(Info(bot))
