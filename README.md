# Lecture video indexer

## Dependencies

Python version: 3.8

 1. Make sure `tesseract` binary is installed system-wise
 2. Install pyhton packages -  `pip install -r requirements.txt`

## Run in Docker

```bash
make build

# Runs bash in the container with mounted video folder
make run

python3 src/cli.py -i video/test.mp4
```
