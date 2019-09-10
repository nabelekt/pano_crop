import sys
import subprocess
import math

input_name = sys.argv[1]
num_parts = int(sys.argv[2])
extension_pos = input_name.rfind('.')  # Find the last '.' in the input image name

x = 0
y = 0

h = int(subprocess.check_output(f'magick identify -format "%[fx:h]" "{input_name}"', shell=True))
w = int(subprocess.check_output(f'magick identify -format "%[fx:w]" "{input_name}"', shell=True))
w = math.floor(w/num_parts)

for ind in range(num_parts):
  output_name = input_name[0:extension_pos] + f'_{ind}' + input_name[extension_pos:len(input_name)]  # Add number to output file name
  cmd = f'convert -crop {w}x{h}+{x}+{y} {input_name} {output_name}'
  # print(cmd)
  subprocess.run(cmd, shell=True)
  x = x + w