import os

def just_do_it(link):
    webm = download(link)
    mp3 = convert(webm)
    delete(webm)
    return mp3

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

def convert(webm):
  mp3 = webm.split('.')[0] + '.mp3'
  cmd = 'ffmpeg -i {0} -acodec libmp3lame -aq 4 {1}'.format(webm, mp3)
  os.system(cmd)
  return mp3

def delete(webm):
  os.system('rm {0}'.format(webm))
