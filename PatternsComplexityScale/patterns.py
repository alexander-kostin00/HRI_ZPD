# All three patterns have the same number of lit and unlit pixels, only their configuration changes

pattern_easy = [[1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1]
                ]

pattern_complex = [[1, 1, 1, 1, 1, 1],
                   [1, 0, 1, 1, 1, 1],
                   [1, 1, 1, 0, 0, 1],
                   [1, 0, 1, 0, 0, 1],
                   [1, 0, 1, 0, 0, 1],
                   [1, 1, 1, 1, 1, 1],
                   [1, 0, 1, 0, 0, 1],
                   [1, 1, 1, 1, 1, 1]
                   ]

pattern_middle = [[1, 1, 1, 1, 1, 1],
                  [1, 0, 0, 0, 0, 1],
                  [1, 1, 1, 1, 1, 1],
                  [1, 0, 0, 0, 0, 1],
                  [1, 1, 1, 1, 1, 1],
                  [1, 0, 0, 0, 0, 1],
                  [1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1]
                  ]


from PIL import Image

def matrix_to_image(matrix, filename):
    image = Image.new('1', (len(matrix[0]), len(matrix)))

    pixels = image.load()

    for i in range(image.size[1]):
        for j in range(image.size[0]):
            pixels[j, i] = 0 if matrix[i][j] == 1 else 1

    image.save(filename)


matrix_to_image(pattern_easy, 'pattern_easy.png')
matrix_to_image(pattern_complex, 'pattern_complex.png')
matrix_to_image(pattern_middle, 'pattern_middle.png')