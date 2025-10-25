# GrokSplit by DeMoD LLC

![GrokSplit](groksplit.svg)

GrokSplit is a lightweight, dependency-free Python toolset for splitting large text files into smaller, semantically coherent chunks optimized for processing with Grok, xAI's AI assistant. It includes scripts to split files, process chunks with Grok via xAI’s API (preserving overlaps for perfect alignment), and merge them back into a single file. Designed for Grok’s token limits (~256k for Grok-4, up to 2M for Fast variants), GrokSplit is ideal for researchers, developers, and users of xAI’s free-tier or API services who need to edit or analyze large texts.

## Features
- **Semantic Splitting**: Splits text at paragraph, line, sentence, or word boundaries to preserve context, avoiding mid-sentence cuts.
- **Configurable Chunking**: Supports chunk sizes in characters or estimated tokens (~4 chars/token), with defaults tuned for Grok (1M chars ~250k tokens).
- **Overlap Preservation**: Configurable overlap (default: 20k chars ~5k tokens) ensures continuity, with exact overlaps stored for perfect alignment during merging.
- **LLM Processing**: Processes only core (non-overlap) chunk portions with Grok, preserving overlaps to ensure seamless reassembly.
- **Merging Capability**: Reconstructs the original or modified file, deduplicating overlaps accurately.
- **No Dependencies**: Built with Python’s standard library, ensuring easy deployment.
- **Open Source**: Licensed under BSD 3-Clause for flexible use and modification.

## Installation
1. Clone or download the repository:
   ```bash
   git clone https://github.com/DeMoD-LLC/GrokSplit.git
   cd GrokSplit
   ```
2. Ensure Python 3.6+ is installed.
3. Use the scripts directly (`split_large_file.py`, `process_chunks.py`, `merge_parts.py`).

## Usage

### Splitting a File
Split a large text file into chunks for Grok:
```bash
python groksplit.py input.txt --chunk_size 1000000 --chunk_overlap 20000 --length_metric tokens --output_dir parts
```
- `input.txt`: Path to your text file.
- `--chunk_size`: Max size per chunk (default: 1M chars ~250k tokens).
- `--chunk_overlap`: Overlap between chunks (default: 20k chars ~5k tokens).
- `--length_metric`: Use 'chars' or 'tokens' (default: chars).
- `--output_dir`: Directory for output files and `manifest.json` (default: 'parts').

Output: Chunk files (`part_1.txt`, `part_2.txt`, etc.) and a `manifest.json` with overlap metadata.

### Processing Chunks with Grok
Process chunks using Grok’s API, preserving overlaps for alignment:
```bash
python process_chunks.py --input_dir parts --output_dir processed_parts --api_key YOUR_API_KEY --prompt_template "Summarize this text: {core}" --merge --output_file modified.txt
```
- `--input_dir`: Directory with split parts and `manifest.json` (default: 'parts').
- `--output_dir`: Directory for processed parts (default: 'processed_parts').
- `--api_key`: xAI API key (required; get from https://docs.x.ai/docs/overview).
- `--prompt_template`: Prompt with `{core}` placeholder (default: 'Rewrite this text for clarity: {core}').
- `--system_prompt`: System prompt (default: 'You are a helpful assistant.').
- `--max_tokens`: Max response tokens (default: 1000).
- `--temperature`: Generation temperature (default: 0.7).
- `--merge`: Merge processed chunks into a single file.
- `--output_file`: Path for merged file (default: `processed_<original_name>`).

Output: Processed chunks (`processed_part_1.txt`, etc.), a `processed_manifest.json`, and optionally a merged file.

**Note**: For free-tier Grok (no API), manually process core chunks (extracted via `manifest.json`’s `prefix_overlaps`) on grok.com and save outputs.

### Merging Chunks
Reconstruct the original or processed file:
```bash
python merge_parts.py --input_dir processed_parts --output_file original.txt
```
- `--input_dir`: Directory with parts and manifest (default: 'parts').
- `--output_file`: Path for reconstructed file (default: `reconstructed_<original_name>`).

Output: A single file with overlaps deduplicated.

### Example
Split a research paper, summarize with Grok, and merge:
```bash
python split_large_file.py paper.txt --chunk_size 200000 --chunk_overlap 10000 --length_metric tokens
python process_chunks.py --input_dir parts --output_dir processed --api_key YOUR_API_KEY --prompt_template "Summarize this text: {core}" --merge --output_file summarized_paper.txt
```
Or, merge manually:
```bash
python merge_parts.py --input_dir processed --output_file summarized_paper.txt
```

## License
Copyright (c) 2025 DeMoD LLC

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions, and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions, and the following disclaimer in the documentation and/or other materials provided with the distribution.
3. Neither the name of DeMoD LLC nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

## Contributing
Contributions are welcome! Please:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/awesome-feature`).
3. Commit changes (`git commit -m 'Add awesome feature'`).
4. Push to the branch (`git push origin feature/awesome-feature`).
5. Open a pull request.

Report issues or suggest features via GitHub Issues. For Grok-specific feedback, join discussions on X (@DeMoD_LLC).

## Support
- For Grok or xAI API questions, visit [xAI](https://x.ai) or [xAI API](https://x.ai/api).
- For script issues, open a GitHub issue or check community discussions on X (@DeMoD_LLC).
- Note: DeMoD LLC provides limited support; community contributions drive improvements.

## About DeMoD LLC
DeMoD LLC develops tools to enhance AI workflows, proudly contributing to xAI’s mission of accelerating human scientific discovery. Follow us on X (@DeMoD_LLC) for updates.
