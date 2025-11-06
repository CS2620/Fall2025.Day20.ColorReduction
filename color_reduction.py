from PIL import Image
import random
import math

def l1_difference(a, b):
    return sum(abs(x-y) for x,y in zip(a,b))

def l2_difference(a,b):
    return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2+(a[2]-b[2])**2)

def linf_difference(a,b):
    return max(abs(a[0]-b[0]), abs(a[1]-b[1]), abs(a[2]-b[2]))

def closest_color(color, color_list):
    return min(color_list, key=lambda option: linf_difference(color, option))

def random_color():
    return tuple(random.randint(0, 255) for _ in range(3))


image = Image.open("sky.jpg")
raster = image.load()

color_count = dict()

for y in range(image.height):
    for x in range(image.width):
        pixel = raster[x,y]
        if pixel not in color_count:
            color_count[pixel] = 0
        color_count[pixel]+=1
        
print(len(color_count.items()))

sorted_color_count = sorted(color_count.items(), key=lambda item:item[1], reverse=True)

# palette = list(map(lambda item: item[0], sorted_color_count))
# palette = palette[:10]


# k-means algorithm
k=10
iterations = 5
palette = [random_color() for _ in range(k)]

for i in range(iterations):
    closest_color_list = [[] for _ in range(k)]

    for color_count in sorted_color_count:
        closest_palette_color = closest_color(color_count[0], palette)
        closest_index = palette.index(closest_palette_color)
        closest_color_list[closest_index].append(color_count)
        
    for j in range(k):
        closest_list = closest_color_list[j]
        if len(closest_list) == 0:
            palette[j] = random_color()
        else:
            sums = [0,0,0]
            sum_weights = 0
            for color, count in closest_list:
                sums = [a+b*count for a,b in zip(sums, color)]
                sum_weights += count
            palette[j] = tuple(a//sum_weights for a in sums)

image.save("original.png")
for y in range(image.height):
    for x in range(image.width):
        pixel = raster[x,y]
        
        raster[x,y] = closest_color(pixel, palette)
        
image.save("color_reduced.png")
    
