import argparse
import json
import os
import time
from .analyzer import VideoAnalyzer


def main():
    parser = argparse.ArgumentParser(description="Chained video frame analyzer using OpenAI vision models")
    parser.add_argument("--video", required=True, help="Path to video file")
    parser.add_argument("--interval", type=float, default=2.0, help="Interval between frames in seconds")
    parser.add_argument("--model", default="gpt-4o-mini", help="OpenAI vision-capable model name")
    parser.add_argument("--system-prompt", default="You are a meticulous observer describing changes across video frames.", help="System prompt to seed context")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of text summary")
    parser.add_argument("--task", help="Optional path to a task description file in the tasks/ directory")

    args = parser.parse_args()

    # Load task description if provided
    task_description = None
    if args.task:
        task_path = f"tasks/{args.task}"
        try:
            with open(task_path, "r") as task_file:
                task_description = task_file.read().strip()
        except FileNotFoundError:
            print(f"Error: Task file '{task_path}' not found.")
            return

    # Pass task description as part of the system prompt
    if task_description:
        args.system_prompt += f"\nTask: {task_description}"

    analyzer = VideoAnalyzer(model=args.model)
    results = analyzer.analyze_video(args.video, args.interval, system_prompt=args.system_prompt)

    # Generate timestamped filename for JSON output
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    task_name = os.path.basename(args.task).split('.')[0] if args.task else "default_task"
    
    # Create analysis directory if it doesn't exist
    os.makedirs("analysis", exist_ok=True)
    
    output_filename = f"analysis/analysis_{timestamp}_{os.path.basename(args.video).split('.')[0]}_{task_name}.json"

    # Prepare JSON output structure
    output_data = {
        "task": task_description,
        "video": os.path.basename(args.video),
        "frames": [r.__dict__ for r in results]
    }

    # Save JSON to file
    with open(output_filename, "w") as json_file:
        json.dump(output_data, json_file, indent=2)
    print(f"Analysis results saved to {output_filename}")

    if args.json:
        out = [r.__dict__ for r in results]
        print(json.dumps(out, indent=2))
    else:
        print("Sequential Frame Analysis:\n")
        for r in results:
            print(f"Frame {r.index} ({r.path}):\n{r.raw_response_text}\n")
        print("Overall Narrative:\n")
        if results:
            print("\n\n".join([r.raw_response_text for r in results]))

if __name__ == "__main__":
    main()
