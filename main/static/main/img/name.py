import os
import glob

current_script_path = os.path.dirname(os.path.abspath(__file__))

svg_files = glob.glob(os.path.join(current_script_path, "*.svg"))

files = [
    "cooler.svg",
    "cpu.svg",
    "hdd.svg",
    "motherboard.svg",
    "power_supply.svg",
    "ram.svg",
    "ssd.svg",
    "video_card.svg",
]

for svg_file in files:
    full_file_path = os.path.join(current_script_path, svg_file)
    file_name = os.path.basename(full_file_path)
    with open(full_file_path, "r") as f:
        lines = f.readlines()
    with open(os.path.join(current_script_path, "product.svg"), mode="+a") as f:
        for line in lines:
            f.write(line)
        f.write("\n")

# for svg_file in svg_files:
#     full_file_path = os.path.join(current_script_path, svg_file)

#     file_name = os.path.basename(full_file_path)

#     print(file_name)

#     with open(full_file_path, 'r') as f:
#         lines = f.readlines()

#     with open(full_file_path, 'w') as f:
#         for line in lines:
#             if not line.startswith(('<!', '<?', '<m')):
#                 if line.startswith('<svg'):
#                     filename = file_name
#                     filename_without_extension = os.path.splitext(filename)[0]
#                     f.write(f'{line[:-2]} id="{filename_without_extension}">\n')
#                 else:
#                     f.write(line)
