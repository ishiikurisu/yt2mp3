import yt2mp3
import telepot
import sys
import threading

IDLE_STATE = 0
WAITING_LINK = 1
WAITING_LINK_FOR_VIDEO = 2

class Bot:
    def __init__(self, api):
        self.bot = telepot.Bot(api)
        self.offset = 0
        self.help = '/help - displays this message\n/download link - converts a video to mp3\n'
        self.states = { }

    def loop(self):
        updates = self.bot.getUpdates(self.offset)
        for update in updates:
            self.offset = updates[-1]['update_id'] + 1
            print(update)
            if 'message' in update:
                self.answer(update)


    def answer(self, update):
        userId = update['message']['chat']['id']
        query = update['message']['text']

        if userId not in self.states:
            self.states[userId] = IDLE_STATE

        current_state = self.states[userId]
        if query.startswith('/start') or query.startswith('/help'):
            self.bot.sendMessage(userId, self.help)
        elif current_state == IDLE_STATE:
            if query.startswith('/download'):
                thread = threading.Thread(target=self.idle_download,
                                          args=(userId, query))
                thread.start()
            elif query.startswith('/video'):
                thread = threading.Thread(target=self.idle_download_mp4,
                                          args=(userId, query))
                thread.start()
            else:
                self.bot.sendMessage(userId, 'what?')
        elif current_state == WAITING_LINK:
            thread = threading.Thread(target=self.waiting_download,
                                      args=(userId, query))
            thread.start()
        elif current_state == WAITING_LINK_FOR_VIDEO:
            thread = threading.Thread(target=self.waiting_video_link,
                                      args=(userId, query))
            thread.start()

    def idle_download(self, userId, query):
        try:
            link = query.split(' ')[1]
            self.bot.sendMessage(userId, 'now loading...')
            mp3 = yt2mp3.download_mp3(link)
            with open(mp3, 'rb') as fp:
                self.bot.sendDocument(userId, fp)
        except IndexError:
            self.bot.sendMessage(userId, 'what about the link?')
            self.states[userId] = WAITING_LINK

    def idle_download_mp4(self, userId, query):
        try:
            link = query.split(' ')[1]
            self.bot.sendMessage(userId, 'now loading...')
            mp4 = yt2mp3.download_mp4(link)
            with open(mp4, 'rb') as fp:
                self.bot.sendDocument(userId, fp)
        except IndexError:
            self.bot.sendMessage(userId, 'what about the link?')
            self.states[userId] = WAITING_LINK_FOR_VIDEO

    def waiting_download(self, userId, query):
        self.bot.sendMessage(userId, 'now loading...')
        mp3 = yt2mp3.download_mp3(query)
        with open(mp3, 'rb') as fp:
            self.bot.sendDocument(userId, fp)
            self.states[userId] = IDLE_STATE

    def waiting_video_link(self, userId, query):
        self.bot.sendMessage(userId, 'now loading...')
        mp4 = yt2mp3.download_mp4(query)
        with open(mp4, 'rb') as fp:
            self.bot.sendDocument(userId, fp)
            self.states[userId] = IDLE_STATE

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
