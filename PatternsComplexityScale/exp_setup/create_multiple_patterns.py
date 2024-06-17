from PatternsComplexityScale.creating_patterns.creating_patterns import CreatingPatterns
from PIL import Image, ImageDraw, ImageFont
import argparse
import shutil
import os


def create_patterns(amount=5, complexity_level=6, scaling_factor=0.1, rows=500, columns=500, output_directory_path='patterns_uncovered'):
    # Check if the output directory exists and is not empty
    if os.path.exists(output_directory_path) and os.listdir(output_directory_path):
        print(f"Directory {output_directory_path} is not empty. Deleting all files.")
        # Delete all files in the output directory
        for filename in os.listdir(output_directory_path):
            file_path = os.path.join(output_directory_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

    if not os.path.exists(output_directory_path):
        os.makedirs(output_directory_path)

    counter_numbers = 0
    counter = 0

    for i in range(1, 2 * amount + 1):
        if i % 2 != 0:
            try:
                # Create the number image
                number_image = Image.new('RGB', (columns, rows), color='black')
                draw = ImageDraw.Draw(number_image)
                number_font_size = min(columns, rows) // 2

                try:
                    # Try to use a truetype font if available
                    font = ImageFont.truetype("DejaVuSans.ttf", number_font_size)
                except IOError as e:
                    print('Error:', str(e))
                    break

                text = str(counter_numbers + 1)
                text_width, text_height = draw.textsize(text, font=font)
                text_x = (columns - text_width) // 2
                text_y = (rows - text_height) // 2
                draw.text((text_x, text_y), text, fill='white', font=font)
                number_output_path = f'{output_directory_path}/image_{counter + 1}.png'
                number_image.save(number_output_path)
                print(f'Success: Number image generated and saved to {number_output_path}.')

                counter += 1
                counter_numbers += 1

            except Exception as e:
                print('Error:', str(e))
                break
        else:
            try:
                creating_patterns = CreatingPatterns(rows, columns, complexity_level, scaling_factor)
                rand_comb = creating_patterns.find_valid_combinations(complexity_level, scaling_factor, False)

                if not rand_comb:
                    print('Error', 'No valid combinations found.')
                    print(str(counter_numbers) + ' images have been generated for now.')
                    return

                # Create the pattern image
                lit_image = creating_patterns.create_lit_image(columns, rows)
                target_sum = round((len(lit_image) * len(lit_image[0])) / 3)
                unlit_areas = creating_patterns.generate_unlit_regions(rand_comb[0], rand_comb[1], lit_image, target_sum)
                filled_image = creating_patterns.fill_image(lit_image, unlit_areas)
                creating_patterns.print_matrix(filled_image)
                pattern_output_path = f'{output_directory_path}/image_{counter + 1}.png'
                creating_patterns.matrix_to_image(filled_image, pattern_output_path)
                print(f'Success: Pattern generated and saved to {pattern_output_path}.')

                counter += 1

            except Exception as e:
                print('Error:', str(e))
                break

    print(f'{int(counter / 2)} patterns have been generated.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate patterns and number images.')
    parser.add_argument('--amount', type=int, default=10, help='Number of patterns to generate.')
    parser.add_argument('--complexity_level', type=int, default=6, help='Complexity level of the patterns.')
    parser.add_argument('--scaling_factor', type=float, default=0.1, help='Scaling factor for the patterns.')
    parser.add_argument('--rows', type=int, default=500, help='Number of rows in the image.')
    parser.add_argument('--columns', type=int, default=500, help='Number of columns in the image.')
    parser.add_argument('--output_directory_path', type=str, default='patterns_uncovered', help='Directory to save the generated images.')

    args = parser.parse_args()

    create_patterns(
        amount=args.amount,
        complexity_level=args.complexity_level,
        scaling_factor=args.scaling_factor,
        rows=args.rows,
        columns=args.columns,
        output_directory_path=args.output_directory_path
    )
