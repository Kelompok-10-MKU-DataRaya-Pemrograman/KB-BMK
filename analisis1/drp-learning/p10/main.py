from functools import reduce


data = [[1, 2], [3, 4]]

# ekivalen lambda x: sum(x):
def x(n):
    return sum(n)


if __name__ == '__main__':
    # map: memproses masing-masing block
    result = map(lambda x: sum(x), data)

    # reduce: mengolah hasil dari masing-masing block menjadi satu nilai
    result2 = reduce(lambda x, y: x+y, result)
    print(result2)
