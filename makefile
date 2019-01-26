default: run

deps:
	apt-get install youtube-dl
	apt-get install ffmpeg
	pip install -r requirements

bot:
	python3 bot.py $(API)

run:
	python3 main.py

clean:
	rm *.mp3
	rm *.mp4
