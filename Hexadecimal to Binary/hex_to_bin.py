# hex_to_bin_converter.py
import os

INPUT_DIR = r"D:\SAP\Dataset Yugal"
INPUT_FILES = ["Data_1.txt", "Data_2.txt", "Data_3.txt", "Data_4.txt"]
HEX_TO_BIN = {
    '0': '0000', '1': '0001', '2': '0010', '3': '0011',
    '4': '0100', '5': '0101', '6': '0110', '7': '0111',
    '8': '1000', '9': '1001', 'A': '1010', 'B': '1011',
    'C': '1100', 'D': '1101', 'E': '1110', 'F': '1111'
}

def convert_hex_file(input_path, output_path):
    """Convert hexadecimal file to binary text file"""
    with open(input_path, 'r') as f_in, open(output_path, 'w') as f_out:
        for line in f_in:
            # Process each hexadecimal byte in the line
            bin_line = []
            for hex_byte in line.strip().split():
                # Convert each character in the hex byte to 4-bit binary
                bin_byte = ''.join(HEX_TO_BIN.get(char.upper(), '0000') 
                                 for char in hex_byte)
                bin_line.append(bin_byte)
            f_out.write(' '.join(bin_line) + '\n')

def main():
    # Create output directory if it doesn't exist
    os.makedirs(INPUT_DIR, exist_ok=True)
    
    # Process each input file
    for filename in INPUT_FILES:
        input_path = os.path.join(INPUT_DIR, filename)
        output_path = os.path.join(INPUT_DIR, f"hexa_{filename}")
        
        if os.path.exists(input_path):
            convert_hex_file(input_path, output_path)
            print(f"Converted: {filename} -> hexa_{filename}")
        else:
            print(f"File not found: {filename}")

if __name__ == "__main__":
    main()
