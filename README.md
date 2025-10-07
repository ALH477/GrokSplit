# File Splitter for Grok

A Python script to split large text files into smaller, logical chunks optimized for processing with Grok (xAI's AI). It uses recursive splitting at semantic boundaries (paragraphs, lines, sentences, words) to preserve context, with configurable chunk sizes and overlap tailored for Grok's token limits (~256k for Grok-4, up to 2M for Fast variants).

## Features
- Splits text files at logical boundaries to avoid mid-sentence cuts.
- Supports chunk size in characters or estimated tokens (~4 chars/token).
- Configurable overlap to maintain context across chunks.
- No external dependencies; pure Python.
- Outputs chunks as individual files for easy processing with Grok.

## Usage
Run from the command line:
```bash
python groksplit.py input.txt --chunk_size 1000000 --chunk_overlap 20000 --length_metric tokens --output_dir parts
```
- `input.txt`: Path to your text file.
- `--chunk_size`: Max size per chunk (default: 1M chars ~250k tokens).
- `--chunk_overlap`: Overlap between chunks (default: 20k chars ~5k tokens).
- `--length_metric`: Use 'chars' or 'tokens' (default: chars).
- `--output_dir`: Directory for output files (default: 'parts').

Example: Split a large research paper and feed `part_1.txt`, `part_2.txt`, etc., to Grok via grok.com or xAI's API.

## Installation
1. Clone or download this repository.
2. Ensure Python 3.6+ is installed.
3. Run the script with your text file.

## License
Copyright (c) 2025 Asher LeRoy, DeMoD LLC

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

## Support
For Grok-related questions or xAI API access, visit [xAI](https://x.ai) or [xAI API](https://x.ai/api). For script issues, open a GitHub issue or check community discussions on X.
