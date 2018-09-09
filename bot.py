import yt2mp3
import telepot
import sys
import threading

# CONSTANTS
IDLE_STATE = 0
WAITING_LINK = 1
QUERY_MP3 = 3
QUERY_MP4 = 4

class Bot:
    def __init__(self, api):
        self.bot = telepot.Bot(api)
        self.offset = 0
        self.help = '/help - displays this message\n/mp3 link - converts a video to an mp3\n/mp4 link - converts a video to an mp4'
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
            self.states[userId] = { 'state': IDLE_STATE }

        current_state = self.states[userId]['state']
        if query.startswith('/start') or query.startswith('/help'):
            self.bot.sendMessage(userId, self.help)
        elif current_state == IDLE_STATE:
            if query.startswith('/mp3') or query.startswith('/mp4'):
                thread = threading.Thread(target=self.idle_download,
                                          args=(userId, query))
                thread.start()
            else:
                self.bot.sendMessage(userId, 'what?')
        elif current_state == WAITING_LINK:
            thread = threading.Thread(target=self.waiting_download,
                                      args=(userId, self.states[userId]['query'], query))
            thread.start()

    def idle_download(self, userId, query):
        kind = QUERY_MP3 if query.startswith('/mp3') else QUERY_MP4
        try:
            link = query.split(' ')[1]
            self.waiting_download(userId, kind, link)
        except IndexError:
            self.bot.sendMessage(userId, 'what about the link?')
            self.states[userId] = {
                'state': WAITING_LINK,
                'query': kind
            }

    def waiting_download(self, userId, kind, link):
        self.bot.sendMessage(userId, 'now loading...')
        job = yt2mp3.download_mp3 if kind == QUERY_MP3 else yt2mp3.download_mp4
        package = job(link)
        # XXX What if the job fails?
        with open(package, 'rb') as fp:
            self.bot.sendDocument(userId, fp)
            self.states[userId] = { 'state': IDLE_STATE }

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
