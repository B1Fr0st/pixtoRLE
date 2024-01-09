import numpy as np
from PIL import Image

def encode(string):
    encoded = ""
    #Create an array of tuples with the value and the number of times it appears in a row, then stringify it
    index = 0
    while index < len(string)-1:
        count = 1
        while string[index] == string[index+1]:
            count += 1
            index += 1
            if index == len(string) - 1:
                break
        encoded += "(" + string[index] + ")" + str(count)
        index += 1

    return encoded

def decode(encoded):
    decoded = ""
    for i in range(len(encoded)):
        if encoded[i] == "(":
            color = encoded[i+1]
            index = i+2
            while encoded[index] != ")":
                color += encoded[index]
                index += 1
            multiplier = ""
            while True:
                index += 1
                if index > len(encoded) - 1 or encoded[index] == "(":
                    break
                multiplier += encoded[index]
            decoded += color * int(multiplier)
    return decoded



image_height = 192

# Load image, find unique colours and convert to palette image
im = Image.open('art.png').convert('P')

# Convert to Numpy array of shape=(1152,1152) containing palette indices
na = np.array(im)

# Decimate image by factor of im.height/image_height (192)
factor = int(im.height / image_height)
di = na[::factor, ::factor]

palette = np.reshape(im.getpalette(),(-1,3)).tolist()

encoded = [encode("".join([str(x) for x in row])) for row in di]

inverted_colors = {}
for i in range(len(palette)):
    if palette[i] == [0,0,0]:
        continue
    inverted_colors[str(i)] = palette[i]

def save_image(image:list,path:str,inverted_colors:dict):
    print("Saving image...")
    image_height = len(image)
    image_width = len(decode(image[0]))
    test_image = Image.new(mode="RGB",size=(image_width,image_height))
    try:
        for i in range(image_height):
            for j in range(image_width):
                test_image.putpixel((j,i),tuple(inverted_colors[decode(image[i])[j]]))
    except Exception as e:
        print(e)
    finally:
        test_image.save(path)
def save_to_js(image:list,inverted_colors:dict,rows:int):
    """Saves the image to a js variable that can be used in the game."""
    with open("output.txt", "w") as file:
        template = """var scene = {
        art: %s,
        palette: %s,
        rowSize: %s
    };"""%(image,inverted_colors,rows)
        file.write(template)

save_image(encoded,"new_test.png",inverted_colors)
save_to_js(encoded,inverted_colors,len(encoded))