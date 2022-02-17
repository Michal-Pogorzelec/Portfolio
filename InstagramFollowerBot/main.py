from InstagramFollower import InstaFollower


def main():
    bot = InstaFollower()
    bot.login()
    bot.find_followers()
    bot.quit()


if __name__ == '__main__':
    main()

