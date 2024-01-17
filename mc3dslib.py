import os

def extract_bytes(filename, arg1, arg2):
    # Cracko298
    with open(filename, 'rb+') as file:
        try:
            file.seek(arg1)
            extracted_bytes = file.read(arg2 - arg1)
            return extracted_bytes
        
        except Exception as e:
            return f"Error extracting bytes: {e}"

def convert_bytes(bytestring,order=""):
    # Cracko298
    if not isinstance(bytestring, (bytes, bytearray)):
        return "Invalid input. Please provide a valid bytearray or bytes object."

    if order == "r" or order == "R":
        bytestring[::-1]

    elif order == "f" or order == "F" or order == "":
        pass

    else:
        return "Invlid Order Options."

    byte_data = int.from_bytes(bytestring)
    return byte_data

def extract_colors(image_path):
    # Cracko298
    tmp0 = image_path.replace('.3dst','')
    output_path = f"colors_{tmp0}.txt"

    existing_colors = set()

    try:
        with open(output_path, "r") as existing_file:
            existing_colors = {line.strip() for line in existing_file}
    except FileNotFoundError:
        pass
    
    with open(image_path, "rb") as image_file:
        image_file.seek(0x20)
        argb_data = image_file.read()
        
        rgb_hex_values = []
        for i in range(0, len(argb_data), 4):
            b, g, r, _ = argb_data[i:i+4]
            rgb_hex = "#{:02X}{:02X}{:02X}".format(r, g, b)
            
            if rgb_hex not in existing_colors:
                existing_colors.add(rgb_hex)
                rgb_hex_values.append(rgb_hex)

        with open(output_path, "a") as output_file:
            for hex_value in rgb_hex_values:
                output_file.write(hex_value + "\n")

def green_filter(rgb_bytes):
    red = rgb_bytes[0]
    green = rgb_bytes[1]
    blue = rgb_bytes[2]

    if red >= 0x10:
        red -= 0x10

    if blue >= 0x10:
        blue -= 0x10
    
    green = 0xB0

    green_filtered_rgb = bytearray([red, green, blue])
    return green_filtered_rgb

def greenify(image_path):
    # Cracko298
    with open(image_path, 'rb+') as file:
        while True:
            offset = file.tell()
            byte = file.read(1)

            if not byte:
                break

            if offset >= 0x20 and byte == b'\xFF':
                rgb_bytes = file.read(3)
                if len(rgb_bytes) == 3:
                    green_filtered_rgb = green_filter(rgb_bytes)
                    file.seek(-3, 1)
                    file.write(green_filtered_rgb)
    
    return f"Set Green Hue To: '{image_path}'."

def invert_color(rgb_bytes):
    inverted_rgb = bytearray([255 - byte for byte in rgb_bytes])
    return inverted_rgb

def invertclrs(image_path):
    # Cracko298
    with open(image_path, 'rb+') as file:
        while True:
            offset = file.tell()
            byte = file.read(1)

            if not byte:
                break

            if offset >= 0x20 and byte == b'\xFF':
                rgb_bytes = file.read(3)
                if len(rgb_bytes) == 3:
                    inverted_rgb = invert_color(rgb_bytes)
                    file.seek(-3, 1)
                    file.write(inverted_rgb)
    
    return f"Inverted Color of: '{image_path}'."

def red_filter(rgb_bytes):
    red = rgb_bytes[0]
    green = rgb_bytes[1]
    blue = rgb_bytes[2]

    if red >= 0x10:
        red -= 0x10

    blue = 0xA0

    if green >= 0x10:
        green -= 0x10

    red_filter_bytes = bytearray([red, green, blue])
    return red_filter_bytes

def redify(image_path):
    # Cracko298
    with open(image_path, 'rb+') as file:
        while True:
            offset = file.tell()
            byte = file.read(1)

            if not byte:
                break

            if offset >= 0x20 and byte == b'\xFF':
                rgb_bytes = file.read(3)
                if len(rgb_bytes) == 3:
                    red_filter_bytes = red_filter(rgb_bytes)
                    file.seek(-3, 1)
                    file.write(red_filter_bytes)
    
    print(f"Set Red Hue To: '{image_path}'.")

def orange_filter(rgb_bytes):
    red = rgb_bytes[0]
    green = rgb_bytes[1]
    blue = rgb_bytes[2]

    red = 0x10

    blue = 0xF0

    orange_filter_rgb = bytearray([red, green, blue])
    return orange_filter_rgb

def orangify(image_path):
    # Cracko298
    with open(image_path, 'rb+') as file:
        while True:
            offset = file.tell()
            byte = file.read(1)

            if not byte:
                break

            if offset >= 0x20 and byte == b'\xFF':
                rgb_bytes = file.read(3)
                if len(rgb_bytes) == 3:
                    orange_filter_rgb = orange_filter(rgb_bytes)
                    file.seek(-3, 1)
                    file.write(orange_filter_rgb)
    
    print(f"Set Orange/Yellow Hue To: '{image_path}'.")

def blue_filter(rgb_bytes):
    red = rgb_bytes[0]
    green = rgb_bytes[1]
    blue = rgb_bytes[2]

    red = 0xDF

    green = 0xFF

    blue_filter_rgb = bytearray([red, green, blue])
    return blue_filter_rgb

def bluify(image_path):
    # Cracko298
    with open(image_path, 'rb+') as file:
        while True:
            offset = file.tell()
            byte = file.read(1)

            if not byte:
                break

            if offset >= 0x20 and byte == b'\xFF':
                rgb_bytes = file.read(3)
                if len(rgb_bytes) == 3:
                    blue_filter_rgb = blue_filter(rgb_bytes)
                    file.seek(-3, 1)
                    file.write(blue_filter_rgb)
    
    print(f"Set Blue Hue To: '{image_path}'.")


def meta_grab(image_path):
    # Cracko298
    tempdata = image_path.replace('.3dst','')
    output_path = f"{tempdata}_metadata.txt"
    with open(image_path, 'rb') as f, open(output_path, 'a') as of:
        data0 = f.read(0x4)
        f.seek(0x4)
        data1 = f.read(0x01)
        f.seek(0xC)
        data2 = f.read(0x01)
        f.seek(0x10)
        data3 = f.read(0x01)
        f.seek(0x14)
        data4 = f.read(0x01)
        f.seek(0x18)
        data5 = f.read(0x01)

        int_data = int.from_bytes(data1)
        print(f"Texture Mode: {int_data}")
        of.write(f"Texture Mode: {int_data}\n")
        int_data = int.from_bytes(data2)
        print(f"Skin Width: {int_data}")
        of.write(f"Skin Width: {int_data}\n")
        int_data = int.from_bytes(data3)
        print(f"Skin Height: {int_data}")
        of.write(f"Skin Height: {int_data}\n")

        int_data = data0.decode("ascii")
        print(f"Header Name: {int_data}")
        of.write(f"Header Name: {int_data}\n")
        print(f'MIP Value: 1')
        of.write(f"MIP Value: 1\n")
        print("Img Format: RGBA8")
        of.write(f"Image Format: RGBA8\n")
        print("Bit Depth: 8")
        of.write(f"Bit Depth: 8\n")

        int_data = int.from_bytes(data4)
        print(f"Width Checksum: {int_data}")
        of.write(f"Width Checksum: {int_data}\n")
        int_data = int.from_bytes(data5)
        print(f"Height Checksum: {int_data}")
        of.write(f"Height Checksum: {int_data}\n")
        print(" ")
        return f"Saved MetaData As: '{output_path}'."

def mat2json(file_path):
    # Cracko298
    files = ["material", "material3DS", "images", "bak", "dat"]
    filestypes = ["*.material", "*.material3DS", "*.mat", "*.bak", "*.dat"]

    filename = os.path.basename(file_path)
    f0, f1 = filename.split('.')

    if f1 not in files:
        print(f"WARNING: If you proceed with this file, it may cause an error that could result in a Corrupted File.")
        print(f"File extensions that are allowed/expected are as follows: {files}.\n")
        print(f"Press the 'Enter Key' to close the Application.")
        print(f"Press the '0 Key' then press the 'Enter Key' to continue with the selected file.\n")
        exit(1)
    else:
        pass

    parts = filename.split('.')
    out_file = '.'.join(parts[:-1]) + ".json"

    with open(file_path, 'rb+') as f:
        with open(out_file, 'wb') as o:
            dats = f.read()
            data = dats[::-1]
            writable_d = data[::-1]

            o.write(writable_d)

def convert_options(file_path,output_file_path):
    # Cracko298 and Wolfyxon
    target_bytes = bytes([0xD8, 0x05, 0x20, 0x20, 0x6D, 0x70])
    with open(file_path, 'rb') as file:
        content = file.read()

        if content.startswith(target_bytes):
            modified_content = content.replace(b'\x20', b'\x00')

            with open(output_file_path, 'wb') as modified_file:
                modified_file.write(modified_content)
            print("Modification successful.")
        else:
            print("Target bytes not found, no modification needed.")

def reverse_four_bytes(data):
    reversed_four_bytes = data[:4][::-1]
    return reversed_four_bytes

def reverse_three_bytes(data):
    reversed_three_bytes = data[:3][::-1]
    reversed_three_bytes += data[3:4]
    return reversed_three_bytes

def extract_lines(image_path):
    # Cracko298
    if ".3dst" not in image_path:
        print('Error: Provided File is not a Valid .3dst Image.\n')
        exit(1)

    with open(image_path, 'rb') as file:
        header_data = file.read(0x20)
        out_path = image_path.replace(".3dst", "_firstline.3dst")
        print("1")
        file.seek(0x20, 1)

        with open(out_path, 'wb+') as f:
            f.write(header_data)
            for _ in range(8):
                data1 = file.read(0x08)
                print(data1)
                file.seek(0x08, 1)
                data2 = file.read(0x08)
                file.seek(0x28, 1)
                data3 = file.read(0x08)
                file.seek(0x08, 1)
                data4 = file.read(0x08)
                file.seek(0xA8, 1)
                f.write(data1)
                f.write(data2)
                f.write(data3)
                f.write(data4)

    with open(f"{image_path}_converted.r3dst",'wb+') as f:
        with open(out_path, 'rb') as file:
            file.seek(0x20, 1)
            for i in range(0x01, 0x41):
                data = file.read(0x04)
                data = reverse_four_bytes(data)
                data = reverse_three_bytes(data)

                f.write(data)
                file.seek(0x04 * i)

def extract_head(image_path, output_path):
    # Cracko298
    offset = 0x20
    with open(image_path,'rb') as f, open(output_path, 'wb+') as outpf:
        header = f.read(offset)
        f.seek(0x3020)
        data = f.read(0x4020-0x3020)

        outpf.write(header)
        outpf.seek(offset)
        outpf.write(data)
        exit(1)
