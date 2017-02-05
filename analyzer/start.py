#script to download youtube video and split it into frames

import sys
import getopt
import re
import os
import subprocess
import shutil
import race

def main(argv):
  input_url = '' 
  output_fps = '1/10'

  try:
    opts, args = getopt.getopt(argv, "hi:f:", ["input=", "fps="])
  except getopt.GetoptError:
    print('start.py -i <youtube-video> -f <output-fps>')
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print('start.py -i <youtube-video> -f <output-fps>')
      sys.exit()
    elif opt in ('-i', '--input'):
      input_url = arg
    elif opt in ('-f', '--fps'):
      output_fps = arg

  if input_url == '':
    print('Must specify input video url using -i <youtube-video>')
    sys.exit()

  print('Input url:', input_url)
  print('Output fps:', output_fps)

  video_id = ""
  match = re.search(r'((?<=(v|V)/)|(?<=be/)|(?<=(\?|\&)v=)|(?<=embed/))([\w-]+)', input_url)
  
  if match:
    video_id = match.group(0)
  else:
    print('Invalid youtube url.')
    sys.exit()

  frames_path = '{}/frames'.format(video_id)

  if not os.path.exists(video_id):
    os.mkdir(video_id)
    os.system('youtube-dl {} -o \'{}/video.%(ext)s\''.format(input_url, video_id, video_id))

    os.mkdir(frames_path)
    cmd = 'ffmpeg -i {}/video.* -vf fps={} -f image2 {}/frames/%03d.jpg 2>&1'.format(video_id, output_fps, video_id)
    os.system(cmd)

  num_frames = len([f for f in os.listdir(frames_path)
                if os.path.isfile(os.path.join(frames_path, f))])

  race.analyze(num_frames, frames_path)
 

if __name__ == "__main__":
  main(sys.argv[1:])
