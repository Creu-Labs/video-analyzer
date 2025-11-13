import os
import logging
from dataclasses import dataclass
from typing import List, Dict, Any
from .extractor import extract_frames
from .llm_client import VisionClient

@dataclass
class FrameAnalysisResult:
    index: int
    path: str
    raw_response_text: str
    timestamp: str  # Timestamp of the frame in the video

class VideoAnalyzer:
    def __init__(self, model: str = "gpt-4o-mini", client_cls=VisionClient):
        self.model = model
        self._client_cls = client_cls

    def analyze_video(self, video_path: str, interval_seconds: float, system_prompt: str | None = None, task: str | None = None) -> List[FrameAnalysisResult]:
        # Append task to system prompt if provided
        if task:
            system_prompt = (system_prompt or "") + f"\nTask: {task}"

        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
        logging.info("Starting video analysis")

        frame_paths = extract_frames(video_path, interval_seconds)
        logging.info(f"Extracted {len(frame_paths)} frames from video")

        client = self._client_cls(model=self.model)
        results: List[FrameAnalysisResult] = []
        all_frame_results: List[Dict[str, Any]] = []  # Track all results for context

        # Analyze all frames - client handles context internally
        for idx, path in enumerate(frame_paths):
            logging.info(f"Analyzing frame {idx + 1}/{len(frame_paths)}: {path}")
            # Extract timestamp from the frame filename (e.g., "frame_06m_05s.jpg" -> "06:05")
            filename = os.path.basename(path)
            parts = filename.replace(".jpg", "").split("_")
            if len(parts) >= 3:
                minutes = parts[-2].replace("m", "")
                seconds = parts[-1].replace("s", "")
                timestamp = f"{minutes}:{seconds}"
            else:
                timestamp = "00:00"
            
            # Pass previous results as context
            frame_results = client.analyze_frames([path], system_prompt=system_prompt, previous_results=all_frame_results)
            frame_result = frame_results[-1]  # Get the last (newly added) result
            frame_result["timestamp"] = timestamp
            frame_result["index"] = idx  # Set the correct index
            all_frame_results = frame_results  # Update with all results including new one
            results.append(FrameAnalysisResult(**frame_result))

        logging.info("Video analysis completed")
        return results

    @staticmethod
    def summarize_changes(results: List[FrameAnalysisResult]) -> str:
        # Simple extraction of per-frame delta sentences (could be improved with NLP post-processing)
        lines = []
        for r in results:
            lines.append(f"Frame {r.index}: {r.raw_response_text}")
        return "\n".join(lines)
