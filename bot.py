import yt2mp3
import telepot
import sys

class Bot:
    def __init__(self, api):
        self.bot = telepot.Bot(api)
        self.offset = 0
        self.help = '/help - displays this message\n/download link - converts a video to mp3\n'

    def loop(self):
        updates = self.bot.getUpdates(self.offset)
        for update in updates:
            self.offset = updates[-1]['update_id'] + 1
            print(update)
            if 'message' in update:
                userId = update['message']['chat']['id']
                query = update['message']['text']
                if query.startswith('/start') or query.startswith('/help'):
                    self.bot.sendMessage(userId, self.help)
                elif query.startswith('/download'):
                    link = query.split(' ')[1]
                    # TODO Recover from this call if something happens
                    mp3 = yt2mp3.just_do_it(link)
                    with open('videos.txt', 'r') as fp:
                        self.bot.sendDocument(userId, fp)
                else:
                    self.bot.sendMessage(userId, 'wtf?')

if __name__ == '__main__':
    api = sys.argv[1]
    bot = Bot(api)
    print('---')
    while True:
        try:
            bot.loop()
        except KeyboardInterrupt:
            print("...")
            break
