import time
from TwitterBot import InternetSpeedTwitterBot

bot = InternetSpeedTwitterBot()
current_speed = bot.get_internet_speed()
time.sleep(2)
print(bot.down, bot.up)
bot.log_into_tt()

bot.quit()

