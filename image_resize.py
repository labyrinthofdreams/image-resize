"""
The MIT License (MIT)

Copyright (c) 2014 https://github.com/labyrinthofdreams

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import argparse
import functools
import glob
import math
import os
import multiprocessing as mp
from PIL import Image

def resize(width, height, new_width):
    return (new_width, int(round((float(height) / width) * new_width)))

def parse_args():
    parser = argparse.ArgumentParser(description='Parallel image resizing script')
    parser.add_argument('width', type=int, help='Resize to width')
    parser.add_argument('src', help='Load images from this directory')
    parser.add_argument('dst', help='Save resized images to this directory')
    parser.add_argument('--quality', default='95', type=int, help='JPEG image quality (1=worst, 95=best) (default=95)')
    parser.add_argument('--threads', type=int, help='Override the default number of threads')
    return parser.parse_args()

def resize_image(src_path, dst_path, to_width, img_quality):
    try:
        filename, ext = os.path.splitext(os.path.basename(src_path))
        im = Image.open(src_path)
        im = im.resize(resize(im.size[0], im.size[1], to_width), Image.ANTIALIAS)
        im.save(os.path.join(dst_path, filename) + '.jpg', 'JPEG', quality=img_quality)
    except Exception, e:
        print 'Error (resize):', str(e)

def main():
    try:
        args = parse_args()
        if not os.path.exists(args.src):
            raise Exception('Source directory does not exist')
        if not os.path.exists(args.dst):
            os.makedirs(args.dst)
        if os.path.normpath(args.src) == os.path.normpath(args.dst):
            raise Exception('Source and destination directories cannot be same')
        image_quality = int(args.quality)
        if image_quality < 1 or image_quality > 95:
            raise Exception('Invalid value for image quality (must be between 1 and 95)')
        image_iter = glob.iglob(os.path.join(args.src, '*'))
        pool = mp.Pool(processes=args.threads)
        pool.map(functools.partial(resize_image, dst_path=args.dst,
                                    to_width=args.width, img_quality=image_quality), image_iter)
    except Exception as e:
        print 'Error:', str(e)

if __name__ == '__main__':
    main()