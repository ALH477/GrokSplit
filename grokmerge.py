import os
import sys
import argparse
import json

def find_overlap(s1, s2, max_ov):
    min_len = min(len(s1), len(s2), max_ov)
    for k in range(min_len, 0, -1):
        if s1[-k:] == s2[:k]:
            return k
    return 0

def main():
    parser = argparse.ArgumentParser(description="Merge split chunks back into the original file, handling overlaps.")
    parser.add_argument("--input_dir", default="parts", help="Directory containing the split parts and manifest.json (default: 'parts').")
    parser.add_argument("--output_file", default=None, help="Path to the output reconstructed file (default: based on manifest's original_file).")
    args = parser.parse_args()
    
    manifest_path = os.path.join(args.input_dir, 'manifest.json')
    if not os.path.exists(manifest_path):
        print("Error: manifest.json not found in input_dir.")
        sys.exit(1)
    
    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
    
    parts = manifest.get('parts', [])
    if not parts:
        print("Error: No parts listed in manifest.json.")
        sys.exit(1)
    
    chunk_overlap = manifest.get('chunk_overlap', 0)
    original_name = manifest.get('original_file', 'reconstructed.txt')
    output_file = args.output_file or os.path.join(args.input_dir, f"reconstructed_{original_name}")
    
    merged = ''
    for i, part in enumerate(parts):
        part_path = os.path.join(args.input_dir, part)
        if not os.path.exists(part_path):
            print(f"Error: Missing part file {part_path}.")
            sys.exit(1)
        with open(part_path, 'r', encoding='utf-8') as f:
            chunk = f.read()
        if i == 0:
            merged += chunk
        else:
            actual_ov = find_overlap(merged, chunk, chunk_overlap)
            if actual_ov == 0 and chunk_overlap > 0:
                print(f"Warning: No overlap found for {part}; appending fully.")
            merged += chunk[actual_ov:]
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(merged)
    
    print(f"File reconstructed and saved as '{output_file}'.")

if __name__ == "__main__":
    main()
