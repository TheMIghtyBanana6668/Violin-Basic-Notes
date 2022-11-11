import jetson.inference
import jetson.utils

import argparse

$ video-viewer v4l2:///dev/video0                 # /dev/video0 can be replaced with /dev/video1, ect.
$ video-viewer /dev/video0                        # dropping the v4l2:// protocol prefix is fine
$ video-viewer /dev/video0 output.mp4             # save output stream to MP4 file (H.264 by default)
$ video-viewer /dev/video0 rtp://192.168.1.181:1234 

$ video-viewer --input-width=1920 --input-height=1080 --input-codec=h264 /dev/video0

$ sudo apt-get install v4l-utils
$ v4l2-ctl --device=/dev/video0 --list-formats-ext

import jetson.utils
import argparse
import sys

# parse command line
parser = argparse.ArgumentParser()
parser.add_argument("input_URI", type=str, help="URI of the input stream")
parser.add_argument("output_URI", type=str, default="", nargs='?', help="URI of the output stream")
opt = parser.parse_known_args()[0]

# create video sources & outputs
input = jetson.utils.videoSource(opt.input_URI, argv=sys.argv)
output = jetson.utils.videoOutput(opt.output_URI, argv=sys.argv)

# capture frames until user exits
while output.IsStreaming():
	image = input.Capture(format='rgb8')  // can also be format='rgba8', 'rgb32f', 'rgba32f'
	output.Render(image)
	output.SetStatus("Video Viewer | {:d}x{:d} | {:.1f} FPS".format(image.width, image.height, output.GetFrameRate()))
