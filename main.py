import yt2mp3

if __name__ == '__main__':
  videos = [ ]
  with open('videos.txt', 'r') as fp:
    for line in fp:
      videos.append(line.strip())
  for video in videos:
    yt2mp3.just_do_it(video)
