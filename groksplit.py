import os
import re
import sys
import argparse

def estimate_tokens(text):
    # Rough token estimate: ~4 chars/token for English; adjust for accuracy if needed
    return len(text) // 4 + 1

def split_on_separator(text, separator, chunk_size, chunk_overlap, is_regex=False, length_function=len):
    if not separator:
        chunks = []
        step = chunk_size - chunk_overlap
        if step <= 0:
            step = chunk_size
        for i in range(0, length_function(text), step):
            chunks.append(text[i:i + chunk_size])
        return chunks
    
    if is_regex:
        # Use re.split with capture to keep separators
        splits = re.split(f"({separator})", text)
    else:
        parts = text.split(separator)
        splits = []
        for i, p in enumerate(parts):
            splits.append(p)
            if i < len(parts) - 1:
                splits.append(separator)
    
    chunks = []
    current = []
    total = 0
    for s in splits:
        s_len = length_function(s)
        if total + s_len > chunk_size and current:
            chunk = ''.join(current)
            chunks.append(chunk)
            # Trim from start for overlap: remove initial splits until under overlap
            while total > chunk_overlap:
                popped_len = length_function(current[0])
                total -= popped_len
                current.pop(0)
            # Start next chunk with remaining (overlap)
        current.append(s)
        total += s_len
    if current:
        chunks.append(''.join(current))
    return chunks

def recursive_split(text, separators, chunk_size, chunk_overlap, length_function=len):
    text_len = length_function(text)
    if text_len <= chunk_size:
        return [text]
    
    current_sep, is_regex = separators[0]
    big_chunks = split_on_separator(text, current_sep, chunk_size, chunk_overlap, is_regex, length_function)
    
    final = []
    for bc in big_chunks:
        bc_len = length_function(bc)
        if bc_len <= chunk_size:
            final.append(bc)
        elif bc_len > chunk_size:
            # Warn only if significantly over (e.g., indivisible part)
            if len(separators) == 1:
                print(f"Warning: Indivisible chunk of size {bc_len} > {chunk_size}")
            sub = recursive_split(bc, separators[1:], chunk_size, chunk_overlap, length_function)
            final.extend(sub)
    return final

def main():
    parser = argparse.ArgumentParser(description="Split a large text file into logical chunks optimized for Grok.")
    parser.add_argument("input_file", help="Path to the input file.")
    parser.add_argument("--chunk_size", type=int, default=1000000, help="Approximate maximum size of each chunk (default: 1000000 chars ~250k tokens for Grok-4).")
    parser.add_argument("--chunk_overlap", type=int, default=20000, help="Overlap size between chunks (default: 20000 chars ~5k tokens).")
    parser.add_argument("--length_metric", choices=['chars', 'tokens'], default='chars', help="Measure size in 'chars' or estimated 'tokens' (default: chars).")
    parser.add_argument("--output_dir", default="parts", help="Directory to save the output parts (default: 'parts').")
    args = parser.parse_args()
    
    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        print("Error: File may not be text or encoding issue. Assuming UTF-8.")
        sys.exit(1)
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    separators = [
        (r"\n{2,}", True),  # Paragraphs (multiple newlines)
        (r"\n+", True),     # Lines
        (r"(?<=[.!?])\s+", True),  # Sentences
        (r"\s+", True),     # Words
        ("", False)         # Characters
    ]
    
    length_func = len if args.length_metric == 'chars' else estimate_tokens
    chunks = recursive_split(content, separators, args.chunk_size, args.chunk_overlap, length_func)
    
    for i, chunk in enumerate(chunks, 1):
        output_file = os.path.join(args.output_dir, f'part_{i}.txt')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(chunk)
    
    print(f"File split into {len(chunks)} parts in '{args.output_dir}' directory.")

if __name__ == "__main__":
    main()
