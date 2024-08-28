import os, json, hashlib, shutil, zipfile, struct
from pathlib import Path
from PIL import Image

class make_mcworld_struct:
    # Cracko298
    def make_dirs(self):
        os.makedirs("mcworld_files", exist_ok=True)
        os.makedirs(os.path.join("mcworld_files", "db"), exist_ok=True)
        os.makedirs(os.path.join("mcworld_files", "resource_packs"), exist_ok=True)
        os.makedirs(os.path.join("mcworld_files", "behavior_packs"), exist_ok=True)

        open(os.path.join("mcworld_files", "behavior_packs", "#KEEP_FOLDER"), "wb+")
        open(os.path.join("mcworld_files", "resource_packs", "#KEEP_FOLDER"), "wb+")

class MC3DSBlangException(Exception):
    def __init__(self, message):
        super().__init__(message)

class BlangFile:
    # STBUniverse (STBrian)
    def __init__(self):
        return

    def open(self, path: str = None):
        if path == None:
            raise MC3DSBlangException("path is empty")
        if type(path) is not str:
            raise MC3DSBlangException("path must be a 'str'")

        self.filename = Path(path).stem

        with open(path, "rb") as f:
            file_content = list(f.read())

        # Obtener longitud
        long = []
        for i in range(0, 4):
            long.append(file_content[i])
        long = int.from_bytes(bytearray(long), "little")

        # Obtener los elementos del indice
        idx = 4
        data = []
        for i in range(0, long):
            join = []
            for j in range(0, 4):
                join.append(file_content[idx])
                idx += 1
            data.append(join)
            idx += 4

        # Longitud de los textos
        textlong = []
        for i in range(idx, idx + 4):
            textlong.append(file_content[i])
        textlong = int.from_bytes(bytearray(textlong), "little")

        # Obtener los textos
        idx += 4
        texts = []
        for i in range(0, long):
            join = []
            while file_content[idx] != 0:
                join.append(file_content[idx])
                idx += 1
            texts.append(bytearray(join).decode("utf-8"))
            idx += 1

        self.data = data
        self.texts = texts
        return self

    def getData(self):
        return self.data

    def getTexts(self):
        return self.texts

    def replace(self, text: str, newtext: str):
        if type(text) is not str:
            raise MC3DSBlangException("text must be a 'str'")
        if type(newtext) is not str:
            raise MC3DSBlangException("newtext must be a 'str'")

        if text in self.texts:
            if newtext != "":
                self.texts[self.texts.index(text)] = newtext
            else:
                self.texts[self.texts.index(text)] = " "
        return

    def export(self, path: str):
        if type(path) is not str:
            raise MC3DSBlangException("path must be a 'str'")

        long = len(self.data)
        indexLong = list(long.to_bytes(4, "little"))

        indexData = []
        textData = []
        for i in range(0, long):
            # Copiar los primeros datos del elemento
            indexData.extend(self.data[i])

            # Posición de texto
            indexData.extend(list(len(textData).to_bytes(4, "little")))

            # Agregar texto
            textData.extend(list(self.texts[i].encode("utf-8")))

            # Separador/terminador
            textData.append(0)

        textsLong = list(len(textData).to_bytes(4, "little"))

        # Junta todo en una sola lista
        self.exportData = []
        self.exportData.extend(indexLong)
        self.exportData.extend(indexData)
        self.exportData.extend(textsLong)
        self.exportData.extend(textData)

        self.exportData = bytearray(self.exportData)

        with open(os.path.join(path, f"{self.filename}.blang"), "wb") as f:
            f.write(self.exportData)
        return

    def toJson(self, path: str):
        long = len(self.data)
        dataDictionary = {}
        for i in range(0, long):
            item = self.data[i]
            identifier = []
            for j in range(0, 4):
                identifier.append(item[j])
            identifier = bytearray(identifier)
            identifier = int.from_bytes(identifier, "little")
            identifier = str(identifier)

            dataDictionary[identifier] = {}
            dataDictionary[identifier]["order"] = i + 1
            dataDictionary[identifier]["text"] = self.texts[i]

        outFile = open(os.path.join(path, f"{self.filename}.json"), "w", encoding="utf-8")
        json.dump(dataDictionary, outFile, indent=4, ensure_ascii=False)
        outFile.close()
        return

    def fromJson(self, path: str):
        if type(path) is not str:
            raise MC3DSBlangException("path must be a 'str'")

        data = []
        texts = []

        with open(path, "r", encoding="utf-8") as jsonData:
            dataDictionary = json.load(jsonData)

        self.filename = Path(path).stem

        idx = 1
        while idx <= len(dataDictionary):
            for key in dataDictionary:
                if dataDictionary[key]["order"] == idx:
                    data.append(list(int(key).to_bytes(4, "little")))
                    texts.append(dataDictionary[key]["text"])
                    idx += 1
                    break

        self.data = data
        self.texts = texts
        return self

def extract_bytes(filename, arg1, arg2):
    # Cracko298
    with open(filename, "rb+") as file:
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
    with open(image_path, "rb+") as file:
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
    with open(image_path, "rb+") as file:
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
    with open(image_path, "rb+") as file:
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
    with open(image_path, "rb+") as file:
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
    with open(image_path, "rb+") as file:
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
    with open(image_path, "rb") as f, open(output_path, 'a') as of:
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

    with open(file_path, "rb+") as f:
        with open(out_file, "wb") as o:
            dats = f.read()
            data = dats[::-1]
            writable_d = data[::-1]

            o.write(writable_d)

def convert_options(file_path,output_file_path):
    # Cracko298 and Wolfyxon
    target_bytes = bytes([0xD8, 0x05, 0x20, 0x20, 0x6D, 0x70])
    with open(file_path, "rb") as file:
        content = file.read()

        if content.startswith(target_bytes):
            modified_content = content.replace(b'\x20', b'\x00')

            with open(output_file_path, "wb") as modified_file:
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

def create_r3dst(image_path):
    with open(f"{image_path}_converted.r3dst", "wb+") as f:
        with open(image_path, "rb") as file:
            file.seek(0x20, 1)
            for i in range(0x01, 0x4001):
                data = file.read(0x04)
                data = reverse_four_bytes(data)
                data = reverse_three_bytes(data)

                f.write(data)
                file.seek(0x04 * i)

def extract_head(image_path, output_path):
    offset = 0x20
    with open(image_path, "rb") as f, open(output_path, "wb+") as outpf:
        header = f.read(offset)
        f.seek(0x3020)
        data = f.read(0x4020-0x3020)

        outpf.write(header)
        outpf.seek(offset)
        outpf.write(data)
        exit(1)

def revert_options(file_path,output_file_path):
    # Cracko298 and Wolfyxon
    target_bytes = bytes([0xD8, 0x05, 0x00, 0x00, 0x6D, 0x70])
    with open(file_path, "rb") as file:
        content = file.read()

        if content.startswith(target_bytes):
            modified_content = content.replace(b'\x00', b'\x20')

            with open(output_file_path, "wb") as modified_file:
                modified_file.write(modified_content)
            print("Modification successful.")
        else:
            print("Target bytes not found, no modification needed.")

def image_convert(image_path):
    # Cracko298
    def extract_blocks(img):
        block_size = 0x100
        total_size = 0x4000
        offset = 0x20

        with open(img, "rb") as f:
            header = f.read(offset)

            for i in range(1, total_size // block_size + 1):
                with open(os.path.join("out", f"out_{i}.3dst"), "wb") as o:
                    o.write(header)
                    blocks = f.read(block_size)
                    o.write(blocks)

    def extract_lines(start_offset, output_folder):
        block_size = 0x100
        total_size = 0x4000
        for i in range(1, total_size // block_size + 1):
            with open("out", f"out_{i}.3dst", "rb+") as f:
                f.seek(start_offset)
                one = f.read(0x08)
                f.seek(start_offset + 0x10)
                two = f.read(0x08)
                f.seek(start_offset + 0x40)
                three = f.read(0x08)
                f.seek(start_offset + 0x50)
                four = f.read(0x08)

                with open(os.path.join("out", "lines", f"{output_folder}_out_{i}.3dst"), "wb+") as o:
                    o.write(one)
                    o.write(two)
                    o.write(three)
                    o.write(four)

    def sort_and_concatenate_binary_files(input_directory, output_directory):
        files_dict = {}

        for filename in os.listdir(input_directory):
            if filename.endswith(".3dst"):
                last_number = int(filename.split('_')[-1].split('.')[0])

                files_dict.setdefault(last_number, []).append(filename)

        os.makedirs(output_directory, exist_ok=True)

        for last_number in sorted(files_dict.keys()):
            with open(os.path.join(output_directory, f"compiled_lines_{last_number}.3dst"), "wb") as output_file:
                for filename in sorted(files_dict[last_number]):
                    input_file_path = os.path.join(input_directory, filename)
                    with open(input_file_path, "rb") as input_file:
                        output_file.write(input_file.read())


    os.makedirs("out", exist_ok=True)
    os.makedirs(os.path.join("out", "lines"), exist_ok=True)
    os.makedirs(os.path.join("out", "compiled_lines"), exist_ok=True)

    extract_blocks(image_path)
    extract_lines(0x20, "1")
    extract_lines(0x28, "2")
    extract_lines(0x40, "3")
    extract_lines(0x48, "4")
    extract_lines(0xA0, "5")
    extract_lines(0xA8, "6")
    extract_lines(0xC0, "7")
    extract_lines(0xC8, "8")
    sort_and_concatenate_binary_files(os.path.join("out", "lines"), os.path.join("out", "compiled_lines"))

def copy_lines(filename, line_number, mode=1):
    # YT-Toaster
    line_number -= 1
    try:
        with open(filename, "rb") as file:
            lines = file.readlines()

            if 0 <= line_number < len(lines):
                if mode == 0:
                    lines_to_copy = lines[line_number:]
                elif mode == 1:
                    lines_to_copy = [lines[line_number]]
                elif mode == 2:
                    lines_to_copy = [lines[line_number]]
                elif mode == 3:
                    line = lines[line_number]
                    hash_value = hashlib.sha256(line).hexdigest()
                    return f"SHA256 Hash of Line {line_number + 1}: {hash_value}"

                new_filename = f"{filename}_copied.bin"
                with open(new_filename, "wb") as new_file:
                    for line_to_copy in lines_to_copy:
                        new_file.write(line_to_copy)

                return f"Text(s) copied to {new_filename}"
            else:
                return "Invalid line number"

    except FileNotFoundError:
        return f"File '{filename}' not found"

def console2bedrock_cdb(folder_path, truncate_offset=0x84):
    # Cracko298
    make_mcworld_struct.make_dirs(make_mcworld_struct)

    file_prefix = "slt"
    output_file_name = "000001.ldb"

    def extract_number(file_name):
        try:
            return int(file_name[len(file_prefix):file_name.index(".cdb")])
        except ValueError:
            return 0

    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    filtered_files = [(file, extract_number(file)) for file in files if file.startswith(file_prefix)]

    if filtered_files:
        max_file = max(filtered_files, key=lambda x: x[1])
        max_file_name, max_file_number = max_file

        with open(os.path.join(folder_path, max_file_name), "rb+") as file:
            file_content = file.read()
            file.seek(truncate_offset)
            truncated_content = file.read()

            with open(os.path.join("mcworld_files", "db", output_file_name), "wb") as new_file:
                new_file.write(truncated_content)

        return f"Converted most Recent Slot to: '{output_file_name}'."
    else:
        return "No files found with the specified format."

def console2bedrock_vdb(folder_path):
    # Cracko298
    make_mcworld_struct.make_dirs(make_mcworld_struct)

    offset=0x8014
    file_prefix="slt"
    output_file_name="000002.log"

    if not os.path.exists(folder_path):
        return f"Error: '{folder_path}' is not a valid path."

    def extract_number(file_name):
        try:
            return int(file_name[len(file_prefix):file_name.index(".vdb")])
        except ValueError:
            return 0

    vdb_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.startswith(file_prefix)]

    if vdb_files:
        filtered_files = [(file, extract_number(file)) for file in vdb_files]
        max_file = max(filtered_files, key=lambda x: x[1])
        max_file_name, max_file_number = max_file

        with open(os.path.join(folder_path, max_file_name), "rb") as file:
            content_at_offset = file.read()
            file.seek(offset)
            check_file = file.read(0x01)

            with open(os.path.join("mcworld_files", "db", output_file_name), "wb") as new_file:
                new_file.write(content_at_offset)

        return f"Converted most recent VDB file to: '{output_file_name}'."
    else:
        return "No VDB files found with the specified format."

def console2bedrock_meta(level_dat=0, level_dat_old=0, levelname_txt=0, world_icon=None):
    # Cracko298
    make_mcworld_struct.make_dirs(make_mcworld_struct)
    checksum = 0x00

    if world_icon == None:
        checksum += 0x7A

    shutil.copy2(level_dat, "mcworld_files")
    shutil.copy2(level_dat_old, "mcworld_files")
    shutil.copy2(levelname_txt, "mcworld_files")

    if checksum >= 0x50:
        pass
    else:
        shutil.copy2(world_icon, "mcworld_files")

def convert_lockage(file_path):
    # Cracko298
    make_mcworld_struct.make_dirs(make_mcworld_struct)
    with open(file_path, "rb+") as f0:
        lockage_data = f0.read()

    with open(os.path.join("mcworld_files", "db", "MANIFEST-000001"), "wb+") as f1:
        f1.write(lockage_data)

    with open(os.path.join("mcworld_files", "db", "CURRENT"), "w+") as f2:
        f2.write("MANIFEST-000001\n")

    f3 = open(os.path.join("mcworld_files", "db", "LOCK"), "wb+")
    f4 = open(os.path.join("mcworld_files", "db", "LOG"), "wb+")
    f3.close()
    f4.close()

def zip_convert_contents(folder_path):
    # Cracko298
    zip_name = os.path.basename(folder_path)

    with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk("mcworld_files"):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), "mcworld_files"))

    zip_name = zip_name.replace(".zip", "")

    os.rename(zip_name, f"{zip_name}_Converted.mcworld")

def convert_save(folder_path, world_icon_path=None):
    # YT-Toaster & Cracko298
    make_mcworld_struct.make_dirs(make_mcworld_struct)

    toast0 = os.path.exists(os.path.join(folder_path, "db", "vdb"))
    toast1 = os.path.exists(os.path.join(folder_path, "db", "cdb"))

    if toast0 == True and toast1 == True:
        print("Valid Path Recieved.")
    else:
        return f"Path Recieved is Not Valid 3DS World Save.\n\nPath Provided: '{folder_path}'."

    console2bedrock_cdb(os.path.join(folder_path, "db", "cdb"))
    console2bedrock_vdb(os.path.join(folder_path, "db", "vdb"))

    chk0, chk1, chk2 = (".png", ".jpeg", ".jpg")

    if chk0 in folder_path or chk1 in folder_path or chk2 in folder_path:
        png_check = True
    else:
        png_check = False

    if world_icon_path == None:
        console2bedrock_meta(os.path.join(folder_path, "level.dat"), os.path.join(folder_path, "level.dat_old"), os.path.join(folder_path, "levelname.txt"))
    elif world_icon_path and png_check == True:
        console2bedrock_meta(os.path.join(folder_path, "level.dat"), os.path.join(folder_path, "level.dat_old"), os.path.join(folder_path, "levelname.txt"), world_icon_path)

    convert_lockage(os.path.join(folder_path, "db", "vdb", "newindex.vdb"))
    zip_convert_contents(folder_path)

def get_png_demesions(png_path: str):
    with Image.open(png_path) as image:
        width,height = image.size
        return width, height

def get_3dst_demensions(etc2_path: str):
    with open(etc2_path, "rb+") as of:
        of.seek(0x0C)
        width_b = of.read(0x04)
        of.seek(0x10)
        height_b = of.read(0x04)

        width = int.from_bytes(width_b, byteorder='little')
        height = int.from_bytes(height_b, byteorder='little')
        of.close()
        return width, height

def convert_2_img(etc2_file_path: str,show_flag=False):
    outname = os.path.basename(etc2_file_path)
    extension = os.path.splitext(etc2_file_path)[1]
    outname = outname.replace(extension,'.png')

    width, height = get_3dst_demensions(etc2_file_path)

    with open(etc2_file_path, "rb") as f:
        f.seek(0x20)
        etc2_data = f.read()

    image = Image.new('RGBA', (width, height))
    block_size = 8
    offset = 0
    for y in range(0, height, block_size):
        for x in range(0, width, block_size):
            for block_y in range(block_size):
                for block_x in range(block_size):
                    if offset + 4 <= len(etc2_data):
                        a, b, g, r = struct.unpack_from('BBBB', etc2_data, offset)
                        if a == 0:
                            r,g,b = 0,0,0
                        image.putpixel((x + block_x, y + block_y), (r, g, b, a))
                        offset += 4

    if show_flag == True:
        image.show()

    image.save(outname)
    return image

def convert_2_etc2(png_file_path: str):
    outname = os.path.basename(png_file_path)
    extension = os.path.splitext(png_file_path)[1]
    outname = outname.replace(extension,'.3dst')

    width,height = get_png_demesions(png_file_path)
    w = width.to_bytes(4, byteorder='little')
    h = height.to_bytes(4, byteorder='little')

    with Image.open(png_file_path) as image:
        if image.mode != 'RGBA':
            image = image.convert('RGBA')

        width, height = image.size
        etc2_data = bytearray()
        for y in range(0, height, 8):
            for x in range(0, width, 8):
                block_data = b''
                for block_y in range(8):
                    for block_x in range(8):
                        pixel = image.getpixel((x + block_x, y + block_y))
                        r, g, b, a = pixel
                        block_data += struct.pack('BBBB', a, b, g, r)

                etc2_data += block_data

        with open(outname, "wb+") as f:
            f.write(b'3DST\x03\x00\x00\x00\x00\x00\x00\x00'),f.write(w),f.write(h),f.write(w),f.write(h),f.write(b'\x01\x00\x00\x00')
            f.write(etc2_data)

        return bytes(etc2_data)
