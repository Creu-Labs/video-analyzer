import os
import types
from src.video_analyzer.analyzer import VideoAnalyzer, FrameAnalysisResult

class DummyVisionClient:
    def __init__(self, *args, **kwargs):
        pass
    def analyze_frames(self, frame_paths, system_prompt=None):
        results = []
        cumulative = ""
        for i, p in enumerate(frame_paths):
            raw = f"Dummy description for {os.path.basename(p)}"
            cumulative += f"\nFrame {i}: {raw}" if cumulative else f"Frame {i}: {raw}"
            results.append({
                "index": i,
                "path": p,
                "raw_response_text": raw,
                "cumulative_summary": cumulative,
            })
        return results

# Monkeypatch VisionClient inside analyzer module
from src.video_analyzer import analyzer as analyzer_mod  # noqa: F401

# Provide a dummy extractor that avoids OpenCV for test
from src.video_analyzer import extractor as extractor_mod

def dummy_extract(video_path, interval_seconds, output_dir="frames"):
    return [f"{output_dir}/frame_{i:05d}.jpg" for i in range(3)]

extractor_mod.extract_frames = dummy_extract  # Override globally for test


def test_chained_summary():
    va = VideoAnalyzer(model="dummy-model", client_cls=DummyVisionClient)
    results = va.analyze_video("fake.mp4", 1.0)
    assert len(results) == 3
    assert isinstance(results[0], FrameAnalysisResult)
    assert "Frame 2" in results[-1].cumulative_summary
    # Ensure cumulative grows
    assert results[0].cumulative_summary != results[-1].cumulative_summary
