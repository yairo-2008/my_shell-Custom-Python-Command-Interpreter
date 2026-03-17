import sys
import os


def create_bin_file_example():
    with open("example.bin", "wb") as f:
        f.write(b"Hello World!\n")
        f.write(bytes([0, 1, 2, 255]))
        f.write(b"Python HexDump")

def hexdump(file_path):
    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    try:
        offset = 0
        size = os.path.getsize(file_path)
        with open(file_path, "rb") as f:
            while size > 0:
                chunk = f.read(16)
                if not chunk:
                    break
                hex_bytes = ""
                ascii_txt = ""
                for b in chunk:
                    hex_bytes += f"{b:02X} "
                    ascii_txt += chr(b) if 32 <= b < 127 else "."
                print(f"{offset}  {hex_bytes:<48}  {ascii_txt}")
                offset += len(chunk)
                size -= len(chunk)
    except Exception as e:
        print(f"Error reading file: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(sys.argv)
        print('error arguments')
        sys.exit(1)
    hexdump(sys.argv[1])