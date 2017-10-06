import yt2mp3
import telepot
import sys

class Bot:
    def __init__(self, api):
        self.bot = telepot.Bot(api)
        self.offset = 0

    def loop(self):
        updates = self.bot.getUpdates(self.offset)
        for update in updates:
            self.offset = updates[-1]['update_id'] + 1
            print(update)
            if 'message' in update:
                userId = update['message']['chat']['id']
                query = update['message']['text']
                response = self.generateResponse(query)
                self.bot.sendMessage(userId, response)

    def generateResponse(self, query):
        # TODO Generate answer
        answer = 'not implemented yet'
        return answer

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
