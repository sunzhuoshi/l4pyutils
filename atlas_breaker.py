# Atlas Breaker
# a simple tool to extract sprites in atlas
# sunzhuoshi@gmail.com
from PIL import Image
import csv
import sys
import os.path


def main(argv=sys.argv):
    if len(argv) < 4:
        usage()
        return 1
    atlas_image_path = argv[1]
    csv_path = argv[2]
    output_dir = argv[3]

    try:
        atlas_image = Image.open(atlas_image_path)
        tmp, ext = os.path.splitext(atlas_image_path)
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
        return 0
    except:
        print("Error:", sys.exc_info()[0])
        return 1


def usage():
    print('atlas_breaker.py [atlas image path] [csv image path] [output directory]')

if __name__ == "__main__":
    main()
