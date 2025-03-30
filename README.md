# Korean Celebrity Ranker

A fun web application that helps you find your favorite Korean male celebrity through a series of choices.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Add celebrity images:
   - Place celebrity images in the `static/images` directory
   - Image filenames should match those referenced in `main.py`
   - Supported image formats: jpg, jpeg, png

3. Run the application:
```bash
python main.py
```

4. Open your browser and visit: http://127.0.0.1:8000

## How it Works

1. The application shows you two Korean celebrities
2. Click on your preferred celebrity
3. The selected celebrity will compete against a new random celebrity
4. This continues for 10 rounds
5. At the end, you'll see your most preferred celebrity!
