from AoC2019.inputs import day8_raw

image_size = len(day8_raw)
width = 25
height = 6
layer_size = width * height

def print_image(image):
    for row in image:
        row_string = ""
        print(row_string.join(row).replace('0', ' '))


print(f"image size={image_size}, layer_size={layer_size}")

# no bounds-checking for now. ;)
#part 1:
layers = [day8_raw[start:start+layer_size] for start in range(0, image_size, layer_size)]
segments_with_zero_counts = [(segment, segment.count('0')) for segment in layers]
sorted_segments = sorted(segments_with_zero_counts, key=lambda x: x[1])
target_layer = sorted_segments[0][0]
print(target_layer.count('1') * target_layer.count('2'))

image = [['2'] * width for height in range(0, height)]

print_image(image)
print('-----------------------------')

for layer in layers:
    layer_rows = [layer[start:start+width] for start in range(0, layer_size, width)]
    for col in range(0, width):
        for row in range(0, height):
            if image[row][col] == '2' and layer_rows[row][col] < '2':
                image[row][col] = layer_rows[row][col]
    print_image(image)
    print('-----------------------------')



