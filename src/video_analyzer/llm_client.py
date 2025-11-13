import base64
import os
import importlib
from typing import List, Dict, Any
import logging
import time
import openai

class VisionClient:
    """Wrapper around OpenAI Vision model for chained frame analysis."""

    def __init__(self, model: str = "gpt-4o-mini", api_key: str | None = None):
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise EnvironmentError("OPENAI_API_KEY not set")
        # Lazy import to allow tests to bypass dependency via injection
        openai_mod = importlib.import_module("openai")
        OpenAI = getattr(openai_mod, "OpenAI")
        self.client = OpenAI(api_key=api_key)
        self.model = model

    @staticmethod
    def encode_image_to_base64(path: str) -> str:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    def analyze_frames(self, frame_paths: List[str], system_prompt: str | None = None, previous_results: List[Dict[str, Any]] | None = None) -> List[Dict[str, Any]]:
        """Sequentially analyze frames with context from previous frames.

        Args:
            frame_paths: List of paths to frame images
            system_prompt: Optional system prompt to guide analysis
            previous_results: Previous frame analysis results for context

        Returns list of dicts with keys: index, path, raw_response_text.
        """
        results: List[Dict[str, Any]] = previous_results.copy() if previous_results else []
        max_context_frames = 5  # Number of previous frame analyses to include as context
        
        for idx, path in enumerate(frame_paths):
            b64 = self.encode_image_to_base64(path)
            
            # Build messages for this frame
            messages: List[Dict[str, Any]] = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            # Build user content with context from previous analyses
            user_content = []
            
            # Get the previous frame analyses (up to 5) based on current results length
            current_frame_index = len(results)  # This is the actual frame index
            context_start = max(0, current_frame_index - max_context_frames)
            previous_analyses = results[context_start:current_frame_index]
            
            if previous_analyses:
                # Add text context from previous frames
                context_text = "Here are the analyses from the previous frames:\n\n"
                for prev in previous_analyses:
                    context_text += f"Frame {prev['index']}: {prev['raw_response_text']}\n\n"
                
                user_content.append({
                    "type": "text",
                    "text": context_text + "Now analyze this NEW frame and describe what has changed or what is new compared to the previous frames:"
                })
            else:
                user_content.append({
                    "type": "text",
                    "text": "This is the first frame. Analyze it and describe what you observe:"
                })
            
            # Add the current frame to analyze
            user_content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{b64}"
                }
            })
            
            messages.append({"role": "user", "content": user_content})

            # Retry logic with backoff
            for attempt in range(5):  # Retry logic with up to 5 attempts
                try:
                    # Use chat.completions API
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=messages,
                    )
                    break  # Exit loop if successful
                except openai.RateLimitError as e:  # Fixing the error reference
                    if attempt < 5:  # Retry up to 5 times
                        backoff_time = (2 ** attempt)  # Exponential backoff: 2s, 4s, 8s, 16s
                        logging.warning(f"Rate limit reached. Retrying in {backoff_time} seconds...")
                        time.sleep(backoff_time)
                    else:
                        logging.error("Exceeded maximum retry attempts due to rate limiting.")
                        raise e
            
            # Extract text from standard chat completion response
            raw_text = response.choices[0].message.content.strip()

            results.append({
                "index": idx,
                "path": path,
                "raw_response_text": raw_text,
            })
            
        return results
