default: run

deps:
	apt-get install youtube-dl
	apt-get install ffmpeg
	pip install -r requirements

bot:
	python bot.py $(API)

run:
	python main.py

clean:
	rm *.mp3
