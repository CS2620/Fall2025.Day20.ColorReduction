from PIL import Image
import random

max_colors = 10
iterations = 2
file = "horse.jpg"

def distance(a, b):
    return sum(abs(x-y) for x, y in zip(a, b))

def closest(color, colors):
    return min(colors, key=lambda c: distance(color, c))

def random_color():
    return tuple(random.randint(0, 255) for _ in range(3))

image = Image.open(file)
raster = image.load()

palette = dict()

for y in range(image.height):
    for x in range(image.width):
        pixel = raster[x, y]
        if pixel not in palette:
            palette[pixel] = 0
        palette[pixel] += 1

# Now do the machine learning part
means = [random_color() for _ in range(max_colors)]

for _ in range(iterations):

    closest_colors_list = [[] for _ in range(len(means))]

    for color in palette.items():
        best_index = min(range(len(means)),
                         key=lambda i: distance(means[i], color[0]))
        closest_colors_list[best_index].append(color)

    for i, mean in enumerate(means):
        closest_colors = closest_colors_list[i]
        if not closest_colors:
            means[i] = random_color()
        else:
            sum_weights = sum(count for color, count in closest_colors)
            sum_colors = [sum(color[j]*count for color, count in closest_colors) for j in range(3)]
            means[i] = tuple(a//sum_weights for a in sum_colors)

for y in range(image.height):
    for x in range(image.width):
        pixel = raster[x, y]
        closest_color = closest(pixel, means)
        raster[x, y] = closest_color

image.save(f"color_reduction.png")
