# dram_retention_analyzer.py
import os
import matplotlib.pyplot as plt

DATA_DIR = r"D:\SAP\Dataset Yugal"
REFERENCE_FILE = os.path.join(DATA_DIR, "Data_1.txt")
MEASURED_FILES = [
    os.path.join(DATA_DIR, "Data_2.txt"),
    os.path.join(DATA_DIR, "Data_3.txt"),
    os.path.join(DATA_DIR, "Data_4.txt")
]
OUTPUT_FILE = os.path.join(DATA_DIR, "Retention_Analysis_Report_v2.txt")
PLOT_FILE = os.path.join(DATA_DIR, "Retention_Rate_Plot_v2.png")

def calculate_retention(ref_path, meas_path):
    """Calculate retention with mismatch logging"""
    retained = 0
    total = 0
    mismatch_samples = []
    
    with open(ref_path, 'r') as f_ref, open(meas_path, 'r') as f_meas:
        for line_num, (ref_line, meas_line) in enumerate(zip(f_ref, f_meas), 1):
            # Normalize lines and split into bytes
            ref_bytes = ref_line.strip().upper().split()
            meas_bytes = meas_line.strip().upper().split()
            
            # Handle line length mismatches
            min_len = min(len(ref_bytes), len(meas_bytes))
            if len(ref_bytes) != len(meas_bytes):
                print(f"Line {line_num}: Length mismatch ({len(ref_bytes)} vs {len(meas_bytes)})")
            
            # Compare individual bytes
            for idx in range(min_len):
                total += 1
                if ref_bytes[idx] == meas_bytes[idx]:
                    retained += 1
                else:
                    if len(mismatch_samples) < 5:  # Log first 5 mismatches
                        mismatch_samples.append(
                            f"Line {line_num}, Byte {idx+1}: "
                            f"Ref={ref_bytes[idx]} vs Meas={meas_bytes[idx]}"
                        )
    
    retention_rate = retained / total if total else 0
    return retention_rate, mismatch_samples

def generate_report(results):
    """Create detailed analysis report"""
    with open(OUTPUT_FILE, 'w') as f:
        f.write("DRAM Cell Retention Analysis Report\n")
        f.write("===================================\n")
        
        for file_path, retention, samples in results:
            f.write(f"\nFile: {os.path.basename(file_path)}\n")
            f.write(f"Retention Rate: {retention:.2%}\n")
            f.write("Sample Mismatches:\n")
            f.write('\n'.join(samples) + '\n')

def plot_retention(results):
    """Generate annotated retention plot"""
    labels = [os.path.basename(f[0]) for f in results]
    rates = [f[1] for f in results]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, rates, color=['#2ecc71', '#f1c40f', '#e74c3c'])
    plt.ylim(0, 1)
    plt.title("DRAM Cell Retention Analysis")
    plt.ylabel("Retention Rate")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height:.2%}', ha='center', va='bottom')
    
    plt.savefig(PLOT_FILE, dpi=300, bbox_inches='tight')
    plt.close()

def main():
    results = []
    
    for meas_file in MEASURED_FILES:
        print(f"\nAnalyzing {os.path.basename(meas_file)}...")
        try:
            retention_rate, mismatches = calculate_retention(REFERENCE_FILE, meas_file)
            results.append((meas_file, retention_rate, mismatches))
            print(f"Retention Rate: {retention_rate:.2%}")
        except Exception as e:
            print(f"Error: {str(e)}")
            results.append((meas_file, 0.0, [str(e)]))
    
    # Generate outputs
    generate_report(results)
    plot_retention(results)
    
    print(f"\nReport saved to: {OUTPUT_FILE}")
    print(f"Plot saved to: {PLOT_FILE}")

if __name__ == "__main__":
    main()
