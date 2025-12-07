import os, json
from src.pipeline import run_text_pipeline, run_file_pipeline

def main():
    mode = os.getenv("MODE", "text")  # "text" or "file"
    algo = os.getenv("ALGO", "sha256")
    input_text = os.getenv("INPUT_TEXT", "Hello, Hashing Project!")
    input_file = os.getenv("INPUT_FILE", "/app/data/input/sample.txt")

    if mode == "text":
        out = run_text_pipeline(input_text, algo=algo)
    elif mode == "file":
        out = run_file_pipeline(input_file, algo=algo)
    else:
        raise ValueError("MODE must be 'text' or 'file'")

    out_path = "/app/data/output/hashes.json"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
