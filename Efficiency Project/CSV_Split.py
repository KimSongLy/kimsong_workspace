import os
import pandas as pd

def split_csv(input_file, output_dir, output_prefix, max_size_mb=50):
    """Splits a large CSV file into multiple files of approximately 50MB each."""

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # Create directory if it doesn't exist
    
    chunk_size = 100_000  # Adjust as needed
    file_index = 1
    output_file = os.path.join(output_dir, f"{output_prefix}_{file_index}.csv")

    with pd.read_csv(input_file, chunksize=chunk_size) as reader:
        for chunk in reader:
            if os.path.exists(output_file) and os.path.getsize(output_file) >= max_size_mb * 1024 * 1024:
                file_index += 1
                output_file = os.path.join(output_dir, f"{output_prefix}_{file_index}.csv")
            chunk.to_csv(output_file, mode='a', index=False, header=not os.path.exists(output_file))
   
    print(f"CSV split into {file_index} files in '{output_dir}'.")

# Path
input_file = r"[Path]"  # Change to your file path
output_dir =  r"[Path]"  # Change to your desired output folder
split_csv(input_file, output_dir, "split_part")
