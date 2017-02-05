# python script to download youtube video and split it into frames

import sys
import getopt
import re
import os
import subprocess

# make metadata file for frames
def export_metadata(data):
  print 'TODO'

#def run_process(cmd):
#  p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#  return iter(p.stdout.readline, b'')

def main(argv):
  input_url = '' 
  output_fps = '1/10'

  try:
    opts, args = getopt.getopt(argv, "hi:f:", ["input=", "fps="])
  except getopt.GetoptError:
    print 'start.py -i <youtube-video> -f <output-fps>'
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print 'start.py -i <youtube-video> -f <output-fps>'
      sys.exit()
    elif opt in ('-i', '--input'):
      input_url = arg
    elif opt in ('-f', '--fps'):
      output_fps = arg

  if input_url == '':
    print 'Must specify input video url using -i <youtube-video>'
    sys.exit()

  print 'Input url:', input_url
  print 'Output fps:', output_fps

  video_id = ""

  match = re.search(r'((?<=(v|V)/)|(?<=be/)|(?<=(\?|\&)v=)|(?<=embed/))([\w-]+)', input_url)
  if match:
    video_id = match.group(0)
  else:
    print 'Invalid youtube url.'
    sys.exit()

  os.mkdir(video_id)
  os.system('youtube-dl {} -o \'{}/video.%(ext)s\''.format(input_url, video_id, video_id))

  frame_data = {}

  os.mkdir('{}/frames'.format(video_id))
  cmd = 'ffmpeg -i {}/video.mp4 -vf fps={} -f image2 {}/frames/%03d.jpg'.format(video_id, output_fps, video_id)
  os.system(cmd)

  #for line in run_process(cmd):
  #  print (line)


if __name__ == "__main__":
  main(sys.argv[1:])


