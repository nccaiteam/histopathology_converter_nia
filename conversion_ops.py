import os
from PIL import Image
from os.path import join
import math
import gc
from xml_to_np_test import create_mask_from_xml
import numpy as np
import cv2
try:
    if __file__[-2:] == 'py':
        package_dir_pth = join(os.path.dirname(os.path.abspath(__file__)))
    else:
        package_dir_pth = ''
        for i, sub_dir_path in enumerate(os.path.dirname(os.path.abspath(__file__)).split(os.sep)):
            if i == len(os.path.dirname(os.path.abspath(__file__)).split(os.sep)) - 2:
                break
            if i == 0:
                package_dir_pth = sub_dir_path + os.sep
            package_dir_pth = join(package_dir_pth, sub_dir_path)

    print("resulting package dir path: " + package_dir_pth)
    print("package file name: " + __file__)
    print("package directory path: " + os.path.dirname(os.path.abspath(__file__)))
    print("openslide path: " + join(package_dir_pth, "openslide-win64-20171122\\openslide-win64-20171122\\bin\\" + ";"))
    os.environ['PATH'] = join(package_dir_pth, "openslide-win64-20171122\\openslide-win64-20171122\\bin\\" + ";") + os.environ['PATH']
    import openslide as ops
    Image.MAX_IMAGE_PIXELS = None
except:
    print("Exception occurred while tracking python file/exe file.")

def patch_extraction_label_tissue_coords(image, height_and_width, overlap, stripped_file_name, target_dir):
    """ Extract patch from the cropped image in the size of (height_and_width, height_and_width).

    Args:
        image (PIL.Image): image to be splitted
        height_and_width (int): length of both height and width to be splitted to
        overlap (int): overlapping length.
        mask (bool): boolean value for patching mask or rgb image. (1 or 3 channel).

    Returns:
        List<PIL.Image>: List of extracted patch images

    Example:
        > > > patch_extraction(cropped_image, 1024, 512)
        List<PIL.Image>
    """
    returning_image_patches = []
    print("Image type: " + str(type(image)))

    crrnt_img_width, crrnt_img_height = image.size

    index = 0
    if (crrnt_img_height <= height_and_width) and (crrnt_img_width <= height_and_width):
        returning_image_patches.append(image)
        return returning_image_patches
    elif crrnt_img_height <= height_and_width:
        w_iteration = int(math.ceil((crrnt_img_width-overlap)/(height_and_width-overlap)))
        top, bottom = 0, crrnt_img_height
        for i in range(w_iteration):
            if i == (w_iteration-1):
                left, right = crrnt_img_width-height_and_width, crrnt_img_width
            else:
                left = ((height_and_width-overlap)*i)
                right = left + height_and_width
            if right > crrnt_img_width:
                print("Current Width is " + str(crrnt_img_width) + " but it exceeded with " + str(right))

            image.crop((left, top, right, bottom)).save(join(target_dir, stripped_file_name + '_' + str(index) + '.png'))
            index += 1
            gc.collect()
    elif crrnt_img_width <= height_and_width:
        h_iteration = int(math.ceil((crrnt_img_height-overlap)/(height_and_width-overlap)))
        left, right = 0, crrnt_img_width
        for j in range(h_iteration):
            if j == (h_iteration - 1):
                top, bottom = crrnt_img_height - height_and_width, crrnt_img_height
            else:
                top = ((height_and_width - overlap) * j)
                bottom = top + height_and_width
            if bottom > crrnt_img_height:
                print("Current Height is " + str(crrnt_img_height) + " but it exceeded with " + str(bottom))
            image.crop((left, top, right, bottom)).save(join(target_dir, stripped_file_name + '_' + str(index) + '.png'))
            index += 1
            gc.collect()
    else:
        w_iteration = int(math.ceil((crrnt_img_width-overlap)/(height_and_width-overlap)))
        h_iteration = int(math.ceil((crrnt_img_height-overlap)/(height_and_width-overlap)))
        for i in range(w_iteration):
            if i == (w_iteration-1):
                left, right = crrnt_img_width-height_and_width, crrnt_img_width
            else:
                left = ((height_and_width-overlap)*i)
                right = left + height_and_width
            for j in range(h_iteration):
                if j == (h_iteration - 1):
                    top, bottom = crrnt_img_height - height_and_width, crrnt_img_height
                else:
                    top = ((height_and_width - overlap) * j)
                    bottom = top + height_and_width
                if right > crrnt_img_width:
                    print("Current Width is " + str(crrnt_img_width) + " but it exceeded with " + str(right))
                if bottom > crrnt_img_height:
                    print("Current Height is " + str(crrnt_img_height) + " but it exceeded with " + str(bottom))
                image.crop((left, top, right, bottom)).save(join(target_dir, stripped_file_name + '_' + str(index) + '.png'))
                index += 1
                gc.collect()

    print("Image patches Length: " + str(len(returning_image_patches)))
    return returning_image_patches

def patch_extraction_label_tissue_coords_xml(image, height_and_width, overlap, stripped_file_name, target_dir, xml_dir, max_dim):
    """ Extract patch from the cropped image in the size of (height_and_width, height_and_width).

    Args:
        image (PIL.Image): image to be splitted
        height_and_width (int): length of both height and width to be splitted to
        overlap (int): overlapping length.
        mask (bool): boolean value for patching mask or rgb image. (1 or 3 channel).

    Returns:
        List<PIL.Image>: List of extracted patch images

    Example:
        > > > patch_extraction(cropped_image, 1024, 512)
        List<PIL.Image>
    """
    returning_image_patches = []
    print("Image type: " + str(type(image)))

    crrnt_img_width, crrnt_img_height = image.size
    class_name_list, class_mask_list = create_mask_from_xml(xml_dir, max_dim, False)

    mask = class_mask_list[0]

    index = 0

    if (crrnt_img_height <= height_and_width) and (crrnt_img_width <= height_and_width):
        returning_image_patches.append(image)
        return returning_image_patches
    elif crrnt_img_height <= height_and_width:
        w_iteration = int(math.ceil((crrnt_img_width - overlap) / (height_and_width - overlap)))
        top, bottom = 0, crrnt_img_height
        for i in range(w_iteration):
            if i == (w_iteration - 1):
                left, right = crrnt_img_width - height_and_width, crrnt_img_width
            else:
                left = ((height_and_width - overlap) * i)
                right = left + height_and_width
            if right > crrnt_img_width:
                print("Current Width is " + str(crrnt_img_width) + " but it exceeded with " + str(right))

            mask_patch = np.asarray(mask.crop((left, top, right, bottom)))
            cal_sum = np.zeros((height_and_width, height_and_width))
            cal_sum[mask_patch > 0] = 1
            base_number = height_and_width * height_and_width * 0.2
            if np.sum(cal_sum) > base_number:
                image.crop((left, top, right, bottom)).save(
                    join(target_dir, stripped_file_name + '_' + str(index) + '.png'))
                index += 1
                gc.collect()
            else:
                continue
    elif crrnt_img_width <= height_and_width:
        h_iteration = int(math.ceil((crrnt_img_height - overlap) / (height_and_width - overlap)))
        left, right = 0, crrnt_img_width
        for j in range(h_iteration):
            if j == (h_iteration - 1):
                top, bottom = crrnt_img_height - height_and_width, crrnt_img_height
            else:
                top = ((height_and_width - overlap) * j)
                bottom = top + height_and_width
            if bottom > crrnt_img_height:
                print("Current Height is " + str(crrnt_img_height) + " but it exceeded with " + str(bottom))
            mask_patch = np.asarray(mask.crop((left, top, right, bottom)))
            cal_sum = np.zeros((height_and_width, height_and_width))
            cal_sum[mask_patch > 0] = 1
            base_number = height_and_width * height_and_width * 0.2
            if np.sum(cal_sum) > base_number:
                image.crop((left, top, right, bottom)).save(
                    join(target_dir, stripped_file_name + '_' + str(index) + '.png'))
                index += 1
                gc.collect()
    else:
        w_iteration = int(math.ceil((crrnt_img_width - overlap) / (height_and_width - overlap)))
        h_iteration = int(math.ceil((crrnt_img_height - overlap) / (height_and_width - overlap)))
        for i in range(w_iteration):
            if i == (w_iteration - 1):
                left, right = crrnt_img_width - height_and_width, crrnt_img_width
            else:
                left = ((height_and_width - overlap) * i)
                right = left + height_and_width
            for j in range(h_iteration):
                if j == (h_iteration - 1):
                    top, bottom = crrnt_img_height - height_and_width, crrnt_img_height
                else:
                    top = ((height_and_width - overlap) * j)
                    bottom = top + height_and_width
                if right > crrnt_img_width:
                    print("Current Width is " + str(crrnt_img_width) + " but it exceeded with " + str(right))
                if bottom > crrnt_img_height:
                    print("Current Height is " + str(crrnt_img_height) + " but it exceeded with " + str(bottom))
                mask_patch = np.asarray(mask.crop((left, top, right, bottom)))
                cal_sum = np.zeros((height_and_width, height_and_width))
                cal_sum[mask_patch > 0] = 1
                base_number = height_and_width * height_and_width * 0.2
                if np.sum(cal_sum) > base_number:
                    image.crop((left, top, right, bottom)).save(
                        join(target_dir, stripped_file_name + '_' + str(index) + '.png'))
                    index += 1
                    gc.collect()

    print("Image patches Length: " + str(len(returning_image_patches)))
    return returning_image_patches

def conversion_main(file_path, conversion_type, parameter, target_dir, ROI , xml_dir = ''):
    file_name = file_path.split('/')[-1]
    file_name = file_name.split(os.sep)[-1]
    stripped_file_name = ''
    for i, name_comp in enumerate(file_name.split('.')):
        if i == (len(file_name.split('.'))-1):
            break
        stripped_file_name += name_comp

    try:
        ops_image = ops.open_slide(file_path)
    except:
        raise Exception("Exception occurred while opening WSI file.")
    if ROI == False:
        if conversion_type == "absolute":
            result_images = [abs_resizing_image(ops_image, parameter)]
            for i, ri in enumerate(result_images):
                ri.save(join(target_dir, stripped_file_name + '_' + str(i) + '.png'))
        elif conversion_type == "ratio":
            result_images = [rate_resizing_image(ops_image, parameter)]
            for i, ri in enumerate(result_images):
                ri.save(join(target_dir, stripped_file_name + '_' + str(i) + '.png'))
        elif conversion_type == "patch":
            patch_extract(ops_image, parameter, stripped_file_name, target_dir)
        else:
            raise Exception("Unexpected conversion type. Please report this matter.")
    elif ROI == True:
        if conversion_type == "absolute":
            result_images = abs_resizing_image_xml(ops_image, parameter, xml_dir)
            for i, ri in enumerate(result_images):
                ri.save(join(target_dir, stripped_file_name + '_' + str(i) + '.png'))
        elif conversion_type == "ratio":
            result_images = rate_resizing_image_xml(ops_image, parameter, xml_dir)
            for i, ri in enumerate(result_images):
                ri.save(join(target_dir, stripped_file_name + '_' + str(i) + '.png'))
        elif conversion_type == "patch":
            patch_extract_xml(ops_image, parameter, stripped_file_name, target_dir, xml_dir)
        else:
            raise Exception("Unexpected conversion type. Please report this matter.")
    print("Process All done...")

def patch_extract(ops_image, parameter, stripped_file_name, target_dir):
    max_dim = ops_image.dimensions
    print("max_dim: " + str(max_dim))
    image = ops_image.read_region((0, 0), 0, max_dim)
    print("original size of " + str(image.size))
    return patch_extraction_label_tissue_coords(image, int(parameter[0]), int(parameter[1]),
                                                stripped_file_name, target_dir)

def patch_extract_xml(ops_image, parameter, stripped_file_name, target_dir, xml_dir):
    max_dim = ops_image.dimensions
    print("max_dim: " + str(max_dim))
    image = ops_image.read_region((0, 0), 0, max_dim)
    print("original size of " + str(image.size))
    return patch_extraction_label_tissue_coords_xml(image, int(parameter[0]), int(parameter[1]),
                                                stripped_file_name, target_dir, xml_dir, max_dim)

def abs_resizing_image(ops_img, resize_shape):
    level_dims = ops_img.level_dimensions
    print("level dims: " + str(level_dims))
    best_level, best_dims = -1, (1000000000, 1000000000)
    for i, ld in enumerate(level_dims):
        if (int(resize_shape[0]) < ld[0]) and (int(resize_shape[1]) < ld[1]):
            best_dims = ld
            best_level = i
        else:
            break
    print("best_level: " + str(best_level))
    print("best dims: " + str(best_dims))
    try:
        print("Finding optimal size for resize begins")
        image = ops_img.read_region((0, 0), best_level, best_dims)
        print("Optimal size found as size of " + str(image.size))
    except ops.OpenSlideError as e:
        print("OpenSlideError has been found. Fetching original size.")
        image = ops_img.read_region((0, 0), 0, ops_img.dimensions)
        print("OpenSlideError has been found, hence the original size of " + str(image.size))
    print("Resizing image begins")
    resized_image = image.resize((int(resize_shape[0]), int(resize_shape[1])))
    print("Image resize has been success. Result size: " + str(resized_image.size))
    return resized_image

def abs_resizing_image_xml(ops_img, resize_shape, xml_dir):
    level_dims = ops_img.level_dimensions
    max_dim = ops_img.dimensions
    print("level dims: " + str(level_dims))
    best_level, best_dims, best_ds_factor = -1, (1000000000, 1000000000), -1
    for i, ld in enumerate(level_dims):
        if (int(resize_shape[0]) < ld[0]) and (int(resize_shape[1]) < ld[1]):
            best_dims = ld
            best_level = i
            best_ds_factor = ops_img.level_downsamples[i]
        else:
            break
    print("best_level: " + str(best_level))
    print("best dims: " + str(best_dims))
    class_name_list, class_mask_list = create_mask_from_xml(xml_dir, max_dim, False)
    mask = class_mask_list[0]
    rect = crop_out_coordinates(mask)
    resized_image_list = []
    for i, (x, y, w, h) in enumerate(rect):
        try:
            print("Finding optimal size for resize begins")
            image = ops_img.read_region((x, y), best_level, (math.floor(w/best_ds_factor), math.floor(h/best_ds_factor)))
            print("Optimal size found as size of " + str(image.size))
        except ops.OpenSlideError as e:
            print("OpenSlideError has been found. Fetching original size.")
            image = ops_img.read_region((x, y), 0, (w, h))
            print("OpenSlideError has been found, hence the original size of " + str(image.size))
        print("Resizing image begins")
        resized_image = image.resize((int(resize_shape[0]), int(resize_shape[1])))
        resized_image_list.append(resized_image)
        print("Image resize has been success. Result size: " + str(resized_image.size))
    return resized_image_list

def rate_resizing_image(ops_image, resize_ratio):
    resize_ratio = float(resize_ratio)
    print("resize_ratio: " + str(resize_ratio))
    max_dim = ops_image.dimensions
    print("max_dim: " + str(max_dim))

    width, height = int(math.ceil(max_dim[0]//resize_ratio)), int(math.ceil(max_dim[1]//resize_ratio))
    print("(width, height): " + str((width, height)))

    return abs_resizing_image(ops_image, (width, height))

def rate_resizing_image_xml(ops_image, resize_ratio, xml_dir):
    resize_ratio = float(resize_ratio)
    print("resize_ratio: " + str(resize_ratio))
    max_dim = ops_image.dimensions
    print("max_dim: " + str(max_dim))

    width, height = int(math.ceil(max_dim[0]//resize_ratio)), int(math.ceil(max_dim[1]//resize_ratio))
    print("(width, height): " + str((width, height)))

    return abs_resizing_image_xml(ops_image, (width, height), xml_dir)


def crop_out_coordinates(image):

    """ Takes a lower resolution level of the Whole-slide Image (WSI). Uses color filtering, clahe, and dilation to find
    contour of tissue existence. Then goes through two filtering of small regions and one merging of the overlapping
    area. Returns the resulting coordinates of the rectangles (tissue lying images)
    Args:
        image (PIL.Image): lowest resolution level of WSI.
    Returns:
        list<(int, int, int, int)>: all merged and large enough rectangle's coordinates list will be returned.
    Example:
        > > > crop_out_coordinates(low_wsi)
        [(0, 0, 350, 350), (2000,2000,4000,4000)]
    """

    tissue_mask = np.asarray(image)

    cnts, _= cv2.findContours(tissue_mask.astype(np.uint8), 0, 2)
    large_cnts = [cnt for cnt in cnts if cv2.contourArea(cnt) >= 1500]
    rect = [cv2.boundingRect(cnt) for cnt in large_cnts]
    rect = merge_overlapping_areas(rect)
    # Once again, filter out the small images.
    if len(rect) != 0:
        small_threshold = max([w * h for x, y, w, h in rect]) / 6
        rect = [(x, y, w, h) for x, y, w, h in rect if (w * h) > small_threshold]
    return rect


def merge_overlapping_areas(rect_lst):
    """ Takes list of coordinates of rectangles, checks if there is any overlapping regions.
    If there are overlapping regions, merge them, else pass.

    Args:
        rect_lst (list<(int, int, int, int)>): List of rectangle coordinates

    Returns:
        list<(int, int, int, int)>: all overlapping rectangles are merged and the 'straightened' list will be returned.

    Example:
        > > > merge_overlapping_areas([(0, 0, 350, 350), (100, 100, 200, 200), (2000,2000,4000,4000)])
        [(0, 0, 350, 350), (2000,2000,4000,4000)]
    """
    any_rect_merged = True
    # When there is any change in the rectangle list, start over the loop process.
    while any_rect_merged:
        any_rect_merged = False
        for i, (x1, y1, w1, h1) in enumerate(rect_lst):
            for j, (x2, y2, w2, h2) in enumerate(rect_lst[1:]):
                if i-1 == j:
                    continue
                # Compare the tuples and see if there is any overlapping areas.
                # If the two subject rectangles overlap, remove both of the corresponding coordinates and append the
                # bigger coordinates which results from merging them.
                if rect_intersects((x1, y1, w1, h1), (x2, y2, w2, h2), 100):
                    any_rect_merged = True
                    rect_lst.remove((x1, y1, w1, h1))
                    rect_lst.remove((x2, y2, w2, h2))
                    # In terms of x-axis
                    if x1 < x2:
                        x = x1
                    else:
                        x = x2
                    if (x1 + w1) > (x2 + w2):
                        w = (x1 + w1) - x
                    else:
                        w = (x2 + w2) - x
                    # In terms of y-axis
                    if y1 < y2:
                        y = y1
                    else:
                        y = y2
                    if (y1 + h1) > (y2 + h2):
                        h = (y1 + h1) - y
                    else:
                        h = (y2 + h2) - y
                    rect_lst.append((x, y, w, h))
                    break
            if any_rect_merged:
                break
    return rect_lst


def rect_intersects(rect1, rect2, flexible_space):

    """ Function to see if the two input rectangle coordinates overlap.
    Since the tissues can be considered as one portion even without overlapping,
    flexible_space is considered to give a slight boundary to each rectangle.

    Args:
        rect1 ((int, int, int, int)): tuple coordinates for the 1st rectangle each represents left, upper, right, lower
        rect2 ((int, int, int, int)): tuple coordinates for the 2nd rectangle each represents left, upper, right, lower
        flexible_space (int): extra length to each coordinate as a border

    Returns:
        Bool: True if there is an overlapping area,
              False if there is none.

    Example:
        > > > rect_intersects((0, 0, 350, 350), (100, 100, 200, 200), 100)
        True
    """
    x1, y1, w1, h1 = rect1[0]-flexible_space, rect1[1]-flexible_space, rect1[2]+flexible_space, rect1[3]+flexible_space
    x2, y2, w2, h2 = rect2[0]-flexible_space, rect2[1]-flexible_space, rect2[2]+flexible_space, rect2[3]+flexible_space

    if ((x1 <= x2) and ((x1+w1) >= x2)) and ((y1 <= y2) and ((y1+h1) >= y2)):
        return True
    elif ((x1+w1) >= (x2+w2)) and (x1 <= (x2+w2)) and (y1 <= y2) and ((y1+h1) >= y2):
        return True
    elif (x1 <= x2) and ((x1+w1) >= x2) and ((y1+h1) >= (y2+h2)) and ((y2+h2) >= y1):
        return True
    elif (x1 <= (x2 + w2)) and ((x2+w2) <= (x1+w1)) and (y1 <= (y2+h2)) and ((y2+h2) <= (y1+h1)):
        return True
    elif (x1 <= x2) and (x2 <= (x1+w1)) and ((x2+w2) <= (x1+w1))  and (y1 <= y2) and (y2 <= (y2+h2)) and ((y2+h2) <= (y1+h1)):
        return True
    elif (x2 <= x1) and (x1 <= (x2+w2)) and ((x1+w1) <= (x2+w2)) and (y2 <= y1) and (y1 <= (y1+h1)) and ((y1+h1) <= (y2+h2)):
        return True
    elif ((x1 <= x2 < (x2+w2) <= (x1+w1)) and (y2 <= y1 <= (y2+h2))) or ((x2 <= x1 <= (x1+w1) <= (x2+w2)) and (y1 <= y2 <= (y1+h1))):
        return True
    elif ((x1 <= x2 <= (x1+w1) <= (x2 + w2)) and (y1 <= y2 <= (y2+h2) <= (y1+h1))) or ((x2 <= x1 <= (x2+w2) <= (x1 + w1)) and (y2 <= y1 <= (y1+h1) <= (y2+h2))):
        return True
    elif (x1 <= x2 <= (x2+w2) <= (x1+w1) and (y1 <= y2 <= (y1+h1) <= (y2+h2))) or (x2 <= x1 <= (x1+w1) <= (x2+w2) and (y2 <= y1 <= (y2+h2) <= (y1+h1))):
        return True
    elif ((x2 <= x1 <= (x2+w2) <= (x1+w1)) and (y1 <= y2 <= (y2+h2) <= (y1+h1))) or ((x1 <= x2 <= (x1+w1) <= (x2+w2)) and (y2 <= y1 <= (y1+h1) <= (y2+h2))):
        return True
    else:
        return False

