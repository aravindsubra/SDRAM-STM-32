# dram_ber_analysis.py
import os
import matplotlib.pyplot as plt

INPUT_DIR = r"D:\SAP\Dataset Yugal"
REFERENCE_FILE = os.path.join(INPUT_DIR, "Data_1.txt")
MEASURED_FILES = [
    os.path.join(INPUT_DIR, "Data_2.txt"),
    os.path.join(INPUT_DIR, "Data_3.txt"),
    os.path.join(INPUT_DIR, "Data_4.txt")
]
OUTPUT_FILE = os.path.join(INPUT_DIR, "BER_Analysis_Results.txt")
PLOT_FILE = os.path.join(INPUT_DIR, "BER_Analysis_Plot.png")

HEX_TO_BIN = {
    '0': '0000', '1': '0001', '2': '0010', '3': '0011',
    '4': '0100', '5': '0101', '6': '0110', '7': '0111',
    '8': '1000', '9': '1001', 'A': '1010', 'B': '1011',
    'C': '1100', 'D': '1101', 'E': '1110', 'F': '1111'
}

def calculate_ber(ref_path, meas_path):
    """Calculate BER while handling line length mismatches"""
    total_bits = 0
    error_bits = 0
    
    with open(ref_path, 'r') as f_ref, open(meas_path, 'r') as f_meas:
        for ref_line, meas_line in zip(f_ref, f_meas):
            ref_bytes = ref_line.strip().upper().split()
            meas_bytes = meas_line.strip().upper().split()
            
            # Handle line length mismatch
            min_len = min(len(ref_bytes), len(meas_bytes))
            
            for i in range(min_len):
                ref_bits = ''.join(HEX_TO_BIN.get(c, '0000') for c in ref_bytes[i])
                meas_bits = ''.join(HEX_TO_BIN.get(c, '0000') for c in meas_bytes[i])
                
                for rb, mb in zip(ref_bits, meas_bits):
                    total_bits += 1
                    if rb != mb:
                        error_bits += 1
                        
    return error_bits / total_bits if total_bits else 0

def main():
    results = []
    ber_values = []
    file_names = []
    
    for meas_file in MEASURED_FILES:
        try:
            ber = calculate_ber(REFERENCE_FILE, meas_file)
            results.append(f"{os.path.basename(meas_file)}: {ber:.4e}")
            ber_values.append(ber)
            file_names.append(os.path.basename(meas_file))
        except Exception as e:
            results.append(f"Error processing {os.path.basename(meas_file)}: {str(e)}")
    
    # Save results
    with open(OUTPUT_FILE, 'w') as f:
        f.write("Bit Error Rate Analysis Results\n")
        f.write("================================\n")
        f.write('\n'.join(results))
    
    # Generate plot
    plt.figure(figsize=(10, 6))
    plt.bar(file_names, ber_values, color=['blue', 'green', 'red'])
    plt.yscale('log')
    plt.ylabel('Bit Error Rate (log scale)')
    plt.title('BER Analysis for SDRAM Data Files')
    plt.grid(True, which='both', linestyle='--', alpha=0.7)
    plt.savefig(PLOT_FILE, dpi=300, bbox_inches='tight')
    
    print(f"Results saved to {OUTPUT_FILE}")
    print(f"Plot saved to {PLOT_FILE}")

if __name__ == "__main__":
    main()
