import os

def download_mp3(link):
  mp3 = '{0}.mp3'.format(get_code(link))
  cmd = 'youtube-dl -o {1} -f bestaudio {0}'.format(link, mp3)
  os.system(cmd)
  return mp3
  
def download_mp4(link):
  webm = download(link)
  mp4 = convert_to_mp4(webm)
  delete(webm)
  return mp4

def get_code(link):
  outlet = 'ytdl'
  try:
    outlet = link.split('=')[1]
  except IndexError:
    outlet = link.split('/')[-1]
  return outlet


def download(link):
  webm = '{0}.webm'.format(get_code(link))
  cmd = 'youtube-dl -o {1} -f webm {0}'.format(link, webm)
  os.system(cmd)
  return webm

def convert_to_mp3(webm):
  mp3 = webm.split('.')[0] + '.mp3'
  cmd = 'ffmpeg -i {0} -acodec libmp3lame -aq 4 {1}'.format(webm, mp3)
  print('#!' + cmd)
  os.system(cmd)
  return mp3

def convert_to_mp4(webm):
  mp4 = webm.split('.')[0] + '.mp4'
  cmd = 'ffmpeg -i {0} {1}'.format(webm, mp4)
  os.system(cmd)
  return mp4

def delete(webm):
  os.system('rm {0}'.format(webm))
