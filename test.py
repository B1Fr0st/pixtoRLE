from PIL import Image
from numpy import asarray, array
from json import dumps
from os import remove

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



path = input("Path to image:")
img = Image.open(path)
img.verify()
img = Image.open(path)
#img = img.convert('RGB')
rows = int(input("Height of image:"))
pixel_size = int(img.height/rows) #Calculated by dividing the size of the image by the size given on pixilart
print(pixel_size)


data = asarray(img).tolist()

Canvas = asarray(data)

test_image = Image.fromarray(Canvas)
test_image.save("test.png")



#loop through each pixel and find all RGB values, then create a dict containing all RGB values corresponding to incrementing numbers
colors = {}
#convert lists to tuples so they can be used as keys in the dict
for i in range(len(data)):
    for j in range(len(data[i])):
        data[i][j] = tuple(data[i][j][0:3])


index = 0
for row in data:
    for pixel in row:
        if pixel not in colors.keys():
            colors[pixel] = str(index)
            index += 1
print(len(colors))
image = []
index = 0
for row_index in range(rows):
    pixel_row = data[row_index*pixel_size]
    row = ""
    for pixel in range(int(len(pixel_row)/pixel_size)):
        row += colors[pixel_row[pixel*pixel_size]]
    row = encode(row)
    image.append(row)
    index += 1
    print(f"Finished {index}/{rows} rows.",end="\r")


for row in data:
    row = ""
    for pixel in row:
        row += colors[pixel]
    row = encode(row)
    image.append(row)
    index += 1
    print(f"Finished {index}/{rows} rows.",end="\r")
    








inverted_colors = {}
for key in colors.keys():
    inverted_colors[colors[key]] = list(key)







with open("output.txt", "w") as file:
    template = """var scene = {
    art: %s,
    palette: %s,
    rowSize: %s
};"""%(image,inverted_colors,rows)
    file.write(template)

