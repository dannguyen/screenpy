#!/usr/bin/env python3
"""
screenpy.py - a CLI wrapper around OSX's screencapture for easy screenshotting. I use it all the time for blogging
              technical tutorials that require a lot of screenshots:
              http://2015.padjo.org/tutorials/mapping/077-ok-schools-quakes/

Dependencies: Python 3.x, boto3 (for AWS S3 uploading), and PIL

Standard usage:

   $ screenpy /tmp/myimage.jpg

   Gives you 2 seconds to switch back to your desktop/application before `screencapture` is executed in interactive mode,
   allowing you to select/size a window for screenshotting. The resulting file is saved in the path, /tmp/myimage.jpg.

   The following is output to STDERR:

       Writing to: hello.jpg
        Format: jpeg
        optimize: True
        quality: 75
      ![image hello.jpg](/tmp/myimage.jpg)

  The following is output to STDOUT for easy copy-pasting:

      <img src="/tmp/myimage.jpg" alt="hello.jpg">

Integration with S3: If you aren't using a static site generator, sometimes you want a remote URL. Adjust the `S3`
global variables to your liking (e.g. S3_BUCKET and S3_DOMAIN), and then call screenpy as so:

      $ screenpy --s3 myonlinepicture.png
"""
from src.cli import main as cli_main


# http://stackoverflow.com/questions/89228/calling-an-external-command-in-python


if __name__ == '__main__':
    cli_main()



