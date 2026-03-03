# police-bot
import discord
from discord.ext import commands
from discord.ui import Button, View
import os

# 1. 基礎設定
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# 2. 遊戲邏輯 View (負責處理按鈕與情境轉換)
class PoliceGame(View):
    def __init__(self):
        super().__init__(timeout=300)

    # 畫面更新工具
    async def update_screen(self, interaction, title, desc, buttons, color=0x1e90ff):
        embed = discord.Embed(title=title, description=desc, color=color)
        embed.set_footer(text="👮 台灣警察模擬器 - 正在執行深夜攔檢勤務")
        
        self.clear_items()
        for btn in buttons:
            self.add_item(btn)
        
        await interaction.response.edit_message(embed=embed, view=self)

    # --- 第一關：攔停 ---
    @discord.ui.button(label="要求下車受檢", style=discord.ButtonStyle.primary)
    async def step_1(self, interaction: discord.Interaction, button: Button):
        title = "🔍 盤查中：對方神情緊張"
        desc = "司機是一名刺青男子，下車時右手一直插在口袋，車內散發出濃厚的香水味。\n\n**你的判斷是？**"
        
        btn_a = Button(label="查詢 M-Police 證件", style=discord.ButtonStyle.secondary)
        btn_a.callback = self.step_2_id
        
        btn_b = Button(label="要求搜身檢查口袋", style=discord.ButtonStyle.danger)
        btn_b.callback = self.step_2_search
        
        await self.update_screen(interaction, title, desc, [btn_a, btn_b])

    # --- 第二關：分支 A (查證件) ---
    async def step_2_id(self, interaction):
        title = "📟 M-Police：查獲前科"
        desc = "系統顯示：該員為「毒品、槍砲」治安顧慮人口！\n此時男子突然轉身想衝回駕駛座！\n\n**緊急狀況！**"
        
        btn_win = Button(label="立刻壓制並呼叫支援", style=discord.ButtonStyle.danger)
        btn_win.callback = self.end_hero
        
        await self.update_screen(interaction, title, desc, [btn_win])

    # --- 第二關：分支 B (強制搜身) ---
    async def step_2_search(self, interaction):
        title = "⚖️ 執法爭議"
        desc = "男子咆哮：『警察了不起喔！我有犯法嗎？為什麼搜我口袋？』\n群眾開始圍觀並錄影。\n\n**你要如何回應？**"
        
        btn_retry = Button(label="冷靜解釋法規理由", style=discord.ButtonStyle.secondary)
        btn_retry.callback = self.step_1 # 回到第一關
        
        btn_fail = Button(label="強行搜查", style=discord.ButtonStyle.danger)
        btn_fail.callback = self.end_complaint
        
        await self.update_screen(interaction, title, desc, [btn_retry, btn_fail])

    # --- 結局 ---
    async def end_hero(self, interaction):
        await self.update_screen(interaction, "🏆 結局：大功一件", "你在男子拿槍前將其壓制，並於副駕駛座搜出改造手槍一把！", [], color=0xffd700)

    async def end_complaint(self, interaction):
        await self.update_screen(interaction, "❌ 結局：程序瑕疵", "你因違反程序強行搜查，雖然搜出違禁品，但被投訴違法，面臨行政處分。", [], color=0xff0000)

# 3. 啟動指令
@bot.command()
async def start(ctx):
    view = PoliceGame()
    embed = discord.Embed(
        title="🚨 深夜攔檢勤務",
        description="凌晨 02:00，你在路口攔下一輛蛇行的黑車。\n\n**學弟，準備好開始盤查了嗎？**",
        color=0x0055ff
    )
    await ctx.send(embed=embed, view=view)

# 4. 讀取 Token 並運行
token = os.environ.get('DISCORD_TOKEN')
if token:
    bot.run(token)
else:
    print("錯誤：找不到 DISCORD_TOKEN 環境變數！")
