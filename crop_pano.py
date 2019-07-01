import sys
import subprocess

num_parts = 8

w = 3402
h = 3108

x = 0
y = 0

input_name = sys.argv[1]
extension_pos = input_name.rfind('.')  # Find the last '.' in the input image name

for ind in range(num_parts):
  output_name = input_name[0:extension_pos] + f'_{ind}' + input_name[extension_pos:len(input_name)]  # Add number to output file name
  cmd = f'convert -crop {w}x{h}+{x}+{y} {input_name} {output_name}'
  # print(cmd)
  subprocess.run(cmd, shell=True)
  x = x + w