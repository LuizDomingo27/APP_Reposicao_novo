import sys
from pathlib import Path

# Ensure project root is in sys.path for test discovery and IDE language servers
ROOT_DIR = str(Path(__file__).resolve().parent.parent)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
