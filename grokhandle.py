import argparse
import json
import os
import sys
import urllib.request

def make_api_request(api_key, model, messages, max_tokens=1000, temperature=0.7):
    url = "https://api.x.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    body = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as response:
            resp_data = json.loads(response.read().decode("utf-8"))
            return resp_data["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        print(f"API Error: {e.code} - {e.reason}")
        print(e.read().decode("utf-8"))
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

def find_overlap(s1, s2, max_ov):
    min_len = min(len(s1), len(s2), max_ov)
    for k in range(min_len, 0, -1):
        if s1[-k:] == s2[:k]:
            return k
    return 0

def main():
    parser = argparse.ArgumentParser(description="Process split chunks with Grok API and optionally merge modified outputs.")
    parser.add_argument("--input_dir", default="parts", help="Directory with split parts and manifest.json (default: 'parts').")
    parser.add_argument("--output_dir", default="processed_parts", help="Directory to save processed parts (default: 'processed_parts').")
    parser.add_argument("--api_key", required=True, help="xAI API key (required; get from https://docs.x.ai/docs/overview).")
    parser.add_argument("--model", default="grok-4", help="Grok model to use (default: grok-4).")
    parser.add_argument("--prompt_template", default="Rewrite this text for clarity: {chunk}", help="Prompt template with {chunk} placeholder (default: 'Rewrite this text for clarity: {chunk}').")
    parser.add_argument("--system_prompt", default="You are a helpful assistant.", help="System prompt for the LLM (default: 'You are a helpful assistant.').")
    parser.add_argument("--max_tokens", type=int, default=1000, help="Max tokens for response (default: 1000).")
    parser.add_argument("--temperature", type=float, default=0.7, help="Temperature for generation (default: 0.7).")
    parser.add_argument("--merge", action="store_true", help="Merge processed chunks into a single file after processing.")
    parser.add_argument("--output_file", default=None, help="Path for merged file if --merge is set (default: based on manifest).")
    args = parser.parse_args()

    manifest_path = os.path.join(args.input_dir, "manifest.json")
    if not os.path.exists(manifest_path):
        print("Error: manifest.json not found.")
        sys.exit(1)
    
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    
    parts = manifest.get("parts", [])
    chunk_overlap = manifest.get("chunk_overlap", 0)
    original_name = manifest.get("original_file", "processed.txt")
    
    os.makedirs(args.output_dir, exist_ok=True)
    processed_parts = []
    for i, part in enumerate(parts, 1):
        part_path = os.path.join(args.input_dir, part)
        with open(part_path, "r", encoding="utf-8") as f:
            chunk = f.read()
        
        user_prompt = args.prompt_template.format(chunk=chunk)
        messages = [
            {"role": "system", "content": args.system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        print(f"Processing part {i}/{len(parts)}...")
        modified = make_api_request(args.api_key, args.model, messages, args.max_tokens, args.temperature)
        
        proc_part = f"processed_part_{i}.txt"
        proc_path = os.path.join(args.output_dir, proc_part)
        with open(proc_path, "w", encoding="utf-8") as f:
            f.write(modified)
        processed_parts.append(proc_part)
    
    proc_manifest = manifest.copy()
    proc_manifest["parts"] = processed_parts
    proc_manifest_path = os.path.join(args.output_dir, "processed_manifest.json")
    with open(proc_manifest_path, "w", encoding="utf-8") as f:
        json.dump(proc_manifest, f, indent=4)
    
    print(f"Processed {len(parts)} parts into '{args.output_dir}'. Processed manifest saved.")
    
    if args.merge:
        merged = ""
        for j, proc_part in enumerate(processed_parts):
            proc_path = os.path.join(args.output_dir, proc_part)
            with open(proc_path, "r", encoding="utf-8") as f:
                mod_chunk = f.read()
            if j == 0:
                merged += mod_chunk
            else:
                actual_ov = find_overlap(merged, mod_chunk, chunk_overlap)
                if actual_ov == 0 and chunk_overlap > 0:
                    print(f"Warning: No overlap found for {proc_part}; appending fully.")
                merged += mod_chunk[actual_ov:]
        
        output_file = args.output_file or os.path.join(args.output_dir, f"processed_{original_name}")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(merged)
        print(f"Merged file saved as '{output_file}'.")

if __name__ == "__main__":
    main()
