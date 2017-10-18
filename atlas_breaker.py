# Atlas Breaker
# a simple tool to extract sprites in atlas
# sunzhuoshi@gmail.com
from PIL import Image
import csv
import sys
import os.path
import getopt


def usage():
    print('atlas_breaker.py [-c csv | -w width -h height [-p prefix]] atlas outdir')
    print(' -c csv\tcsv file path')
    print(' -w width -h height \t width and height of single image')
    print(' -p prefix of output file when -w -h used')
    print(' atlas\tatlas image path')
    print(' outdir\toutput directory')

def main(argv=sys.argv):
    csv_path = None
    output_width = None
    output_height = None
    output_file_prefix = 'output_'

    try:
        opts, args = getopt.getopt(argv[1:], 'c:w:h:p:')
        for o, a in opts:
            if '-c' == o:
                csv_path = a
            elif '-w' == o:
                output_width = int(a)
            elif '-h' == o:
                output_height = int(a)
            elif '-p' == o:
                output_file_prefix = a
    except getopt.GetoptError as err:
        print(err)  # will print something like "option -a not recognized"
        usage()
        return 1

    if csv_path is None and ((output_width is None) or (output_height is None)):
        usage()
        return 1

    atlas_image_path = args[0]
    output_dir = args[1]

    try:
        atlas_image = Image.open(atlas_image_path)
        tmp, ext = os.path.splitext(atlas_image_path)
        if csv_path:
            with open(csv_path) as csv_file:
                reader = csv.reader(csv_file, delimiter=' ')
                for csv_line in reader:
                    output_file_name = csv_line[0]
                    width = int(csv_line[1])
                    height = int(csv_line[2])
                    x = int(float(csv_line[3]) * atlas_image.width)
                    y = int(float(csv_line[4]) * atlas_image.height)
                    box = [x, y, x + width, y + height]
                    output_image = atlas_image.crop(box)
                    output_image.save(output_dir + os.path.sep + output_file_name + ext)
        else:
            output_index = 0
            start_x = 0
            start_y = 0
            while (start_x < atlas_image.width) and (start_y < atlas_image.height):
                output_file_name = output_file_prefix + str(output_index)
                x = start_x
                y = start_y
                box = [x, y, x + output_width, y + output_height]
                output_image = atlas_image.crop(box)
                output_image.save(output_dir + os.path.sep + output_file_name + ext)
                output_index += 1
                start_x += output_width
                if start_x >= atlas_image.width:
                    start_y += output_height
                    start_x = 0
        return 0
    except:
        print('Error:', sys.exc_info())
        return 2


if __name__ == "__main__":
    main()
