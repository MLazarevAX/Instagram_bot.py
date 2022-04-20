from Instagram_bot.Inst_Bot_Class import InstagramBot
from DataUser import login, password

def main():
    my_bot = InstagramBot(login, password)
    my_bot.login_acc()
    my_bot.download_userpage_content('https://www.instagram.com/juliette/')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

