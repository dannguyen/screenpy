import src.imagefoo as imgfoo

import argparse
from os import makedirs, unlink
from os.path import basename, dirname, expanduser, getsize, join, relpath, splitext
from time import sleep
from subprocess import call
from sys import stderr, stdout
from tempfile import NamedTemporaryFile


HTML_TEMPLATE = """<img src="{src}" alt="{alt}">"""
MKDOWN_TEMPLATE = """![image {alt}]({src})"""
RST_IMG_TEMPLATE = """\
.. image:: {src}
    :alt: {alt}"""
RST_FIG_TEMPLATE = """\
.. figure:: {src}
    :alt: {alt}

    {caption}"""

def _extract_format_name(path, format=None):
    if format:
        fmtstring = format.lower()
    else:  # or it is implicit in output_path's extension
        _ofmt = splitext(path)[1].split('.')[-1].lower()
        # by default, make it a PNG if there is no extension
        fmtstring = _ofmt if _ofmt else 'png'
    return fmtstring

def my_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("output_path", nargs=1, help="Path to save file to")


    parser.add_argument('--alt-text', '-a',
        type=str,
        help="alt text for image" )

    parser.add_argument('--best-quality', '-b',
        action= "store_true",
        help="Do least amount of image optimization/compression" )

    parser.add_argument('--format', '-f',
        help='Specify a format, such as jpg, png, gif' )

    parser.add_argument('--pause', '-p',
        default=2.5,
        help='Number of seconds to wait before taking the screenshot')

    parser.add_argument('--quality', '-q',
        help='Set a quality level from 0 to 100',
        default=imgfoo.QUALITY_FACTOR_DEFAULT)

#    parser.add_argument('--s3', '-s', help='Send to S3', action="store_true")

    return parser

def make_log(output_path, output_params, alt_text=None):
    loggy = {}
    _dashes = ''.join('-' for i in range(len(output_path)))
    loggy['output_path'] = output_path
    loggy['alt_text'] = alt_text if alt_text else basename(output_path)
    loggy['html'] = HTML_TEMPLATE.format(src=output_path, alt=loggy['alt_text'])
    loggy['md'] = MKDOWN_TEMPLATE.format(src=output_path, alt=loggy['alt_text'])
    loggy['rst-img'] = RST_IMG_TEMPLATE.format(src=output_path, alt=loggy['alt_text'])
    _caption = alt_text if alt_text else ''
    loggy['rst-fig'] = RST_FIG_TEMPLATE.format(src=output_path, alt=loggy['alt_text'], caption=_caption)
    loggy['message'] = '\n'.join(['Writing to:',
                      _dashes,
                      output_path,
                      loggy['html'],
                      loggy['md'],
                      loggy['rst-img'],
                      loggy['rst-fig'],
                      _dashes,
                      ])
    loggy['params'] = output_params
    return loggy



def screencapture_tempfile(image_format):
    """Screencapture to a temporary filename with a given file extension
    Returns: String, temporary filename, if screenshot taken
    """
    ## create a temp filename
    tfile = NamedTemporaryFile(suffix='.{}'.format(image_format), delete=False)
    tpath = tfile.name
    # yield to user control and take the screenshot
    call(["screencapture", "-i", "-o", "-r", "-t", image_format, tpath,])
    if getsize(tpath) == 0:
        raise RuntimeError("No screenshot was taken.")
    else:
        return tpath





def main():

    #######################
    # BEGIN ARGUMENT PARSING

    ### CLI
    parser = my_arg_parser()
    args = parser.parse_args()
    abs_output_path = expanduser(args.output_path[0])
    output_path = relpath(abs_output_path)
    alt_text = args.alt_text
    pause_sec = int(args.pause)

    ## choose a format; either it's explicitly set via --format
    _fmn = _extract_format_name(path=output_path, format=args.format)

    ## determine optimization level
    if args.best_quality:
        _qlevel = imgfoo.QUALITY_FACTOR_MAX
    elif args.quality and args.quality.isnumeric():
        _qlevel =  int(args.quality)
    else:
        _qlevel = imgfoo.QUALITY_FACTOR_DEFAULT
    output_params = imgfoo.get_image_output_params(format=_fmn,  quality_factor=_qlevel)


    # Save the file depending on output_format
    ##############

    ## Make the parent directories for the output_path
    ## TODO: MAke it not crash with relative dir
    abs_dir = dirname(abs_output_path)
    if abs_dir:
        makedirs(abs_dir, exist_ok = True)

    ## Might as well output information before we go to sleep...
    # We want to print markup and markdown to screen as quickly as possible
    loggy = make_log(output_path,  output_params, alt_text=alt_text)
    # Output HTMl to stdout, for pipeable reasons
    stderr.write(loggy['message'])
    ### Begin file-writing process
    stderr.write("\nPrepare for `screencapture` interaction in {} seconds...\n\n".format(pause_sec))
    sleep(pause_sec)
    ### Start the screencapture process
    tname = screencapture_tempfile(output_params['format'])
    # reopen the saved screenshot file
    meta = imgfoo.save_image(src=tname, dest=abs_output_path,
               format=output_params['format'],
#               color_mode=output_params['color_mode'],
               pillow_params=output_params['pillow_params'],)
    for k, v in meta.items():
        stderr.write("  {}: {}".format(k, v))
        stderr.write("\n")

    print(loggy['html'])

    # remove the temp screen grab file from memory
    unlink(tname)
