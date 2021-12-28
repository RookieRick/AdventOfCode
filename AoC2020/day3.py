from AoC2020.inputs import get_input


if __name__ == "__main__":
    input = get_input(3)

    width = len(input[0])
    height = len(input)

    tree_product = 1

    for delta_x, delta_y in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
        trees = 0
        x = 0
        for y in range(delta_y, height, delta_y):
            x = (x + delta_x) % width
            if input[y][x] == '#':
                trees += 1

        print(f"{trees} trees for {delta_x}, {delta_y}")
        tree_product *= trees

    print(f"gt: {tree_product}")
    print("fin.")
