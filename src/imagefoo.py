from datetime import datetime
from PIL import Image
from pathlib import Path

APPROVED_FORMAT_ALIASES = ['bmp', 'jpg', 'jpeg', 'gif', 'png', 'tiff', ]
QUALITY_FACTOR_DEFAULT = 75 # out of 100
QUALITY_FACTOR_MAX = 100
QUALITY_FACTOR_MIN = 0
QUALITY_FACTOR_RANGE = range(QUALITY_FACTOR_MIN, QUALITY_FACTOR_MAX + 1)

BMP_FORMAT = 'bmp'
GIF_FORMAT = 'gif'
JPEG_FORMAT = 'jpeg'
# Pillow spec says 95 is highest
# http://pillow.readthedocs.io/en/latest/handbook/image-file-formats.html#jpeg
JPEG_QUALITY_MAX = 95
PNG_FORMAT = 'png'
PNG_COMPRESS_LEVEL_MAX = 9
TIFF_FORMAT = 'tiff'
TIFF_DEFAULT_COMPRESSION = 'tiff_lzw'

################ HELPER FUNCTIONS
def get_canonical_format_name(ofmt):
    o = ofmt.lower().strip()
    # "jpg" must be "JPEG"
    if o == "jpg" or o == 'jpeg':
        return JPEG_FORMAT
    elif o == 'gif':
        return GIF_FORMAT
    elif o == 'png':
        return PNG_FORMAT
    elif o == 'tiff':
        return TIFF_FORMAT
    elif o == 'bmp':
        return BMP_FORMAT
    else:
        oopsmsg = "Image output format or file extension was: %s\n It must be: %s" % (ofmt, ', '.join(APPROVED_FORMAT_ALIASES))
        raise IOError(oopsmsg)


def get_pillow_save_params(format, quality_factor):
    """
    format is a str, e.g. 'png', 'jpg', 'gif', 'tiff'

    quality_factor is a number, from 0 to 100, 0 being worst quality + highest compression, and
        100 being minimal compression

    returns a dict meant to be keyword args for PIL.Image.save()
    http://pillow.readthedocs.io/en/latest/reference/Image.html#PIL.Image.Image.save
    """
    args = {}
    if format is PNG_FORMAT:
        # http://pillow.readthedocs.io/en/latest/handbook/image-file-formats.html#png
        args['compress_level'] = PNG_COMPRESS_LEVEL_MAX - round((quality_factor / 100) * 9)
    elif format is JPEG_FORMAT:
        # http://pillow.readthedocs.io/en/latest/handbook/image-file-formats.html#jpeg
        args['optimize'] = quality_factor < QUALITY_FACTOR_MAX
        args['quality'] = round((quality_factor / 100) *  JPEG_QUALITY_MAX)
    elif format is GIF_FORMAT:
        # http://pillow.readthedocs.io/en/latest/handbook/image-file-formats
        args['optimize'] = quality_factor < QUALITY_FACTOR_MAX # optimize always, unless quality explicitly set to 100%
    elif format is TIFF_FORMAT:
        args['compression'] = TIFF_DEFAULT_COMPRESSION if quality_factor < QUALITY_FACTOR_MAX else 'raw'
    elif format is BMP_FORMAT:
        pass
    return args



def get_image_output_params(format, quality_factor):
    d = {}
    d['format'] = get_canonical_format_name(format)
#    d['color_mode'] = 'RGB' if d['format'] == JPEG_FORMAT else 'RGBA'
    if not quality_factor or quality_factor is 'default':
        d['quality_factor'] = QUALITY_FACTOR_DEFAULT
    elif quality_factor == 'best':
        d['quality_factor'] = QUALITY_FACTOR_MAX
    elif quality_factor == 'worst':
        d['quality_factor'] = QUALITY_FACTOR_MIN
    else:
        _q = int(quality_factor)
        if _q in QUALITY_FACTOR_RANGE:
            d['quality_factor'] = _q
        else:
            raise IOError('Quality factor/number needs to be from 0 to 100, not {}'.format(quality_factor))
    d['pillow_params'] = get_pillow_save_params(format=d['format'], quality_factor=d['quality_factor'])
    return d


def save_image(src, dest, format, pillow_params):
    srcpath = Path(src)
    destpath = Path(dest)
#   color_mode is basically dictated by cli.screencapture_tempfile()
#    img = Image.open(srcpath).convert(color_mode)
    img = Image.open(srcpath)
    img.info = {} # delete all image meta data
    img.info['screenshot-timestamp'] = datetime.now().isoformat()
    img.save(destpath, format, exif=bytes(), **pillow_params)

    d = {}
    d['pillow_params'] = pillow_params
    d['dest_path'] = destpath
    d['image_format'] = format
    d['bytesize'] = destpath.stat().st_size
    d['byte_shrinkage'] = round(100 - 100 * d['bytesize'] / srcpath.stat().st_size, 2)
    d['width'] = img.width
    d['height'] = img.height
    d['timestamp'] = img.info['screenshot-timestamp']
    return d











