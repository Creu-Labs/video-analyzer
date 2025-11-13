# Video Analyzer

Extract frames from a video at fixed intervals and perform sequential visual analysis using OpenAI vision models. Each frame is analyzed with context from the previous 5 frames, allowing GPT to identify and describe only the changes between frames.

## Features
* Frame extraction at configurable time intervals with timestamp labeling
* Sequential vision analysis with sliding window context (last 5 frames)
* Task-driven analysis using custom task descriptions
* Automatic retry logic with exponential backoff for rate limiting
* JSON output with timestamps and frame metadata
* Organized output in `analysis/` directory

## Installation

To set up the environment, use the conda environment specified in `environment.yml`:

```bash
conda env create -f environment.yml
conda activate video-analyzer-env
```

This will install all required dependencies, including OpenCV and OpenAI libraries.

## Configuration

Create a `.env` file in the `src/video_analyzer/` directory with your OpenAI API key:

```bash
OPENAI_API_KEY=your-api-key-here
```

You can use `.example.env` as a template.

## Usage

Basic run with task:

```bash
python run_video_analyzer.py --video videos/sample.mp4 --interval 5 --task venipuncture.md
```

Custom system prompt:

```bash
python run_video_analyzer.py --video videos/sample.mp4 --interval 2 --system-prompt "You are an expert security analyst."
```

Different model:

```bash
python run_video_analyzer.py --video videos/sample.mp4 --interval 5 --task patient_bed_exit_alert.md --model gpt-4o
```

## Task Descriptions

Task descriptions are markdown files stored in the `tasks/` directory that provide specific instructions for what to analyze in the video. Examples:

- `tasks/venipuncture_procedure.md` - Medical procedure analysis checklist
- `tasks/patient_bed_exit_alert.md` - Patient bed exit monitoring
- `tasks/package_delivery_confirmation.md` - Package delivery confirmation
- `tasks/bottle_filling_check.md` - Bottle filling status verification
- `tasks/empty_shelf_detection.md` - Empty shelf detection in retail

## Output Structure

Analysis results are saved as JSON files in the `analysis/` directory with the naming format:
```
analysis_YYYYMMDD-HHMMSS_<video_name>_<task_name>.json
```

Each analysis file contains:

```jsonc
{
  "task": "Full task description text",
  "video": "sample.mp4",
  "frames": [
    {
      "index": 0,
      "path": "frames/frame_00m_00s.jpg",
      "raw_response_text": "Description of what changed in this frame",
      "timestamp": "00:00"
    },
    {
      "index": 1,
      "path": "frames/frame_00m_05s.jpg",
      "raw_response_text": "Description of changes from previous frame",
      "timestamp": "00:05"
    }
  ]
}
```

## How It Works

1. **Frame Extraction**: Extract frames every N seconds using OpenCV, saving them with timestamp-based filenames (e.g., `frame_01m_30s.jpg` for 1 minute 30 seconds)

2. **Sequential Analysis**: For each frame:
   - Send the **text analyses** from the previous 5 frames (or fewer if at the start)
   - Send the **current frame as an image**
   - GPT analyzes the new frame and describes only what has changed

3. **Context Window**: Uses a sliding window of the last 5 frame analyses to provide context, keeping API costs reasonable while maintaining continuity

4. **Rate Limit Handling**: Automatically retries up to 5 times with exponential backoff (2s, 4s, 8s, 16s) when hitting OpenAI rate limits

## Cost Considerations

Each frame triggers a separate API call. To control cost:
* Increase `--interval` to reduce frame count (e.g., 5 seconds instead of 1 second)
* Use `gpt-4o-mini` instead of `gpt-4o` (default is already `gpt-4o-mini`)
* Process shorter videos or specific segments
* The sliding window of 5 frames keeps context size manageable

## File Structure

```
.
├── analysis/              # Analysis output files (gitignored)
├── frames/                # Extracted video frames (gitignored)
├── tasks/                 # Task description markdown files
├── videos/                # Video files (gitignored)
├── src/
│   └── video_analyzer/
│       ├── analyzer.py    # Main VideoAnalyzer class
│       ├── cli.py         # Command-line interface
│       ├── extractor.py   # Frame extraction logic
│       └── llm_client.py  # OpenAI API client
├── environment.yml        # Conda environment specification
└── README.md
```

## Testing

Run unit tests (mocking OpenAI):

```bash
pytest -q
```

## Limitations

* Frames are analyzed sequentially (not in parallel) to maintain proper context flow
* Context window is limited to last 5 frames to balance cost and continuity
* Requires OpenAI API key and credits
* Video files and analysis outputs are excluded from git

## License

MIT
