from PIL import Image
import numpy


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




def load_image(path:str,image_height:int) -> (list, int):
    """Loads an image from a given path and returns an array of the image's pixels and the number of actual rows in the image."""
    print("Loading image...")
    img = Image.open(path)
    img.verify()
    img = Image.open(path)
    #img = img.convert('RGB')
    data = numpy.array(img)
    data = [[tuple(pixel) for pixel in row] for row in data]
    return data, int(img.height/image_height) #Calculated by dividing the size of the image by the size given on pixilart



def downscale(data:list,pixel_size:int) -> list:
    """Because the image is actually oversized and contains extra pixels we don't need, downscaling it provides a massive performance boost."""
    print("Downscaling image...")
    new_data = []
    for i in range(len(data)):
        if i%pixel_size == 0:
            new_row = []
            for j in range(len(data[i])):
                if j%pixel_size == 0:
                    new_row.append(data[i][j])
            new_data.append(new_row)
    return new_data





def find_colors(data:list) -> dict:
    print("Finding colors...")
    colors = {}
    index = 0
    for row in data:
        for pixel in row:
            if pixel not in colors.keys():
                colors[pixel] = str(index)
                index += 1
    return colors

def encode_row(row:list,colors:dict) -> str:
    rle = ""
    for i in range(len(row)):
        rle += colors[row[i]]
    return encode(rle)

def encode_image(data:list,colors:dict) -> list:
    print("Encoding image...")
    image = []
    for row in data:
        image.append(encode_row(row,colors))
    return image


def invert_colors(colors:dict):
    print("Inverting colors...")
    """Needed to invert the colors because the way the image is encoded, the key is the background color, which is not what we want."""
    inverted_colors = {}
    for key in colors.keys():
        inverted_colors[colors[key]] = list(key)
    return inverted_colors



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

def main():
    #hardcoded, change to inputs
    path = "art.png"
    image_height = 192

    data, pixel_size = load_image(path,image_height)#load image
    data = downscale(data,pixel_size)#downscale image
    colors = find_colors(data)#find colors
    image = encode_image(data,colors)#encode image using encode()
    inverted_colors = invert_colors(colors)#swap keys and values in colors
    save_image(image,"result.png",inverted_colors)#save a test image.
    save_to_js(image,inverted_colors,len(image))#saves to output.txt



if __name__ == "__main__":
    main()