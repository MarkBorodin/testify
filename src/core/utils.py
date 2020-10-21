from PIL import Image


def resize_image(image, size=(300, 300), fixed_size=300):
    original_image = Image.open(image)
    width, height = original_image.size

    if width > fixed_size or height > fixed_size:
        if width == height:
            resized_image = original_image.resize(size)
            return resized_image.save(image.file.name)
        else:
            if width > height:
                new_width = fixed_size
                new_height = int(new_width * height / width)
            else:
                new_height = fixed_size
                new_width = int(new_height * width / height)
            resized_image = original_image.resize((new_width, new_height), Image.ANTIALIAS)
            return resized_image.save(image.file.name)
