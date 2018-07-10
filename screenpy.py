#!/usr/bin/env python3
"""
screenpy.py - a CLI wrapper around OSX's screencapture for easy screenshotting. I use it all the time for blogging
              technical tutorials that require a lot of screenshots:
              http://2015.padjo.org/tutorials/mapping/077-ok-schools-quakes/

Dependencies: Python 3.x and PIL

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

"""

from src.cli import main as cli_main


if __name__ == '__main__':
    cli_main()



