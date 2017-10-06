default: run

deps:
	apt-get install youtube-dl
	apt-get install ffmpeg
	pip install telepot

run:
	python main.py

clean:
	rm *.mp3
