# GrokSplit by DeMoD LLC

GrokSplit is a lightweight, dependency-free Python toolset for splitting large text files into smaller, semantically coherent chunks optimized for processing with Grok, xAI's AI assistant. It supports recursive splitting at logical boundaries (paragraphs, lines, sentences, words) and includes a companion script to merge chunks back into the original file. Designed for Grok’s token limits (~256k for Grok-4, up to 2M for Fast variants), GrokSplit is ideal for researchers, developers, and users of xAI’s free-tier or API services.

## Features
- **Semantic Splitting**: Splits text at paragraph, line, sentence, or word boundaries to preserve context, avoiding mid-sentence cuts.
- **Configurable Chunking**: Supports chunk sizes in characters or estimated tokens (~4 chars/token), with defaults tuned for Grok (1M chars ~250k tokens).
- **Overlap Support**: Configurable overlap (default: 20k chars ~5k tokens) ensures continuity across chunks for coherent processing.
- **Merging Capability**: Reconstructs the original file from split parts using a `manifest.json`, deduplicating overlaps.
- **No Dependencies**: Built with Python’s standard library, ensuring easy deployment.
- **Open Source**: Licensed under BSD 3-Clause for flexible use and modification.

## Installation
1. Clone or download the repository:
   ```bash
   git clone https://github.com/DeMoD-LLC/GrokSplit.git
   cd GrokSplit
   ```
2. Ensure Python 3.6+ is installed.
3. Use the scripts directly (`split_large_file.py` and `merge_parts.py`).

## Usage

### Splitting a File
Split a large text file into chunks for Grok:
```bash
python split_large_file.py input.txt --chunk_size 1000000 --chunk_overlap 20000 --length_metric tokens --output_dir parts
```
- `input.txt`: Path to your text file.
- `--chunk_size`: Max size per chunk (default: 1M chars ~250k tokens).
- `--chunk_overlap`: Overlap between chunks (default: 20k chars ~5k tokens).
- `--length_metric`: Use 'chars' or 'tokens' (default: chars).
- `--output_dir`: Directory for output files and `manifest.json` (default: 'parts').

Output: Chunk files (`part_1.txt`, `part_2.txt`, etc.) and a `manifest.json` in the output directory.

### Merging Chunks
Reconstruct the original file:
```bash
python merge_parts.py --input_dir parts --output_file original.txt
```
- `--input_dir`: Directory with split parts and `manifest.json` (default: 'parts').
- `--output_file`: Path for the reconstructed file (default: `reconstructed_<original_name>`).

Output: A single file combining all parts, with overlaps deduplicated.

### Example
Split a large research paper and process with Grok:
```bash
python split_large_file.py paper.txt --chunk_size 200000 --chunk_overlap 10000 --length_metric tokens
```
Feed `parts/part_1.txt`, `parts/part_2.txt`, etc., to Grok via grok.com, x.com, or xAI’s API. Merge back:
```bash
python merge_parts.py --input_dir parts --output_file restored_paper.txt
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

Report issues or suggest features via GitHub Issues. For Grok-specific feedback, join discussions on X.

## Support
- For Grok-related questions or xAI API access, visit [xAI](https://x.ai) or [xAI API](https://x.ai/api).
- For script issues, open a GitHub issue or check community discussions on X (@DeMoD_LLC).
- Note: DeMoD LLC provides limited support; community contributions drive improvements.

## About DeMoD LLC
DeMoD LLC is a developer of tools to enhance AI workflows, proudly contributing to xAI’s mission of accelerating human scientific discovery. Follow us on X (@DeMoD_LLC) for updates.
