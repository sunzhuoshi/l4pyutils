#
# splice images into one image(only one row supported by now)
#
from glob import glob
from PIL import Image
import os
import sys

def usage():
    print('splice_images.py [input images wildcard. e.g *.png] [output image path]')
    print('NOTE: only one row output supported')


def main(argv=sys.argv):
    if len(argv) < 3:
        usage()
        return 1

    input_images_wildcard = argv[1]
    output_image_path = argv[2]

    try:
        files = glob(input_images_wildcard)
        output_image_width = 0
        output_image_height = 0
        input_images = []
        for file in files:
            image = Image.open(file)
            input_images.append(image)
            output_image_width += image.width
            if output_image_height < image.height:
                output_image_height = image.height

        output_image = Image.new('RGBA', (output_image_width, output_image_height))
        offset_x = 0
        output_info_path, ext = os.path.splitext(output_image_path)
        output_info_path += '.txt'
        output_info_file = open(output_info_path, 'w')
        for image in input_images:
            output_image.paste(image, (offset_x, 0))
            output_info_file.write('{0} {1} {2} {3} {4}\n'.format(image.filename, offset_x, 0, image.width, image.height))
            offset_x += image.width
            image.close()
        output_image.save(output_image_path)
        output_image.close()
        print('done!')
    except:
        print('Error:', sys.exc_info())
        return 2

if __name__ == '__main__':
    main()