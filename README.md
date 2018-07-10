# screenpy - wrapper around MacOS screencapture utility

When writing documentation and guides, I take a lot of screenshots with [MacOS/BSD's `screencapture` command-line utility](http://www.mitchchn.me/2014/os-x-terminal/) that I need to later refer to using some kind of markup, usually in HTML or Markdown format.

This **screenpy.py** script I've made (which I symlink to a system path as just `screenpy`) is used like this:


```sh
$ screenpy ./myfiles/images/some-screenshot.png
```

What it does:

- Gives me a few seconds to get my computer screen ready to take as creenshot.
- Runs `screencapture` with the following arguments:

    - `i`: Capture screen in interactive mode (hit **Spacebar** to toggle between mouse-selection and window-selection)
    - `o`: Do not capture window shadow if in window-selection mode
    - `r`: Do not include screenshot meta data
- Optimizes the saved image and saves it to `./myfiles/images/some-screenshot.png`
- Outputs easy-to-copy-and-paste markup for my blog/guide/docs, e.g. 

    ```
    myfiles/images/some-screenshot.jpg
<img src="myfiles/images/some-screenshot.jpg" alt="some-screenshot.jpg">
![image some-screenshot.jpg](myfiles/images/some-screenshot.jpg)
.. image:: myfiles/images/some-screenshot.jpg
    :alt: some-screenshot.jpg
.. figure:: myfiles/images/some-screenshot.jpg
    :alt: some-screenshot.jpg
    ```


## More info

The `--help` docs:

```
usage: screenpy [-h] [--alt-text ALT_TEXT] [--best-quality] [--format FORMAT]
                [--pause PAUSE] [--quality QUALITY]
                output_path

positional arguments:
  output_path           Path to save file to

optional arguments:
  -h, --help            show this help message and exit
  --alt-text ALT_TEXT, -a ALT_TEXT
                        alt text for image
  --best-quality, -b    Do least amount of image optimization/compression
  --format FORMAT, -f FORMAT
                        Specify a format, such as jpg, png, gif
  --pause PAUSE, -p PAUSE
                        Number of seconds to wait before taking the screenshot
  --quality QUALITY, -q QUALITY
                        Set a quality level from 0 to 100
```
