# Korean Celebrity Ranker

A fun web application that helps you find your favorite Korean male celebrity through a series of choices.

## Local Development Setup

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

4. Open your browser and visit: http://localhost:8080

## Docker Setup

1. Build the Docker image:
```bash
docker build -t korean-celeb-ranker .
```

2. Run the container:
```bash
docker run -p 8080:8080 korean-celeb-ranker
```

## Google Cloud Deployment

1. Install the Google Cloud SDK and initialize it:
```bash
gcloud init
```

2. Set your project ID:
```bash
gcloud config set project YOUR_PROJECT_ID
```

3. Build and push the container to Google Container Registry:
```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/korean-celeb-ranker
```

4. Deploy to Google App Engine:
```bash
gcloud app deploy
```

5. View your application:
```bash
gcloud app browse
```

## How it Works

1. The application shows you two Korean celebrities
2. Click on your preferred celebrity (❤️ for selected, 😭 for not selected)
3. The selected celebrity will compete against a new random celebrity
4. This continues for 25 rounds or until there's only one celebrity left
5. At the end, you'll see your most preferred celebrity!

## Features

- Tournament-style selection process
- Animated reactions when selecting celebrities
- Responsive design
- Docker containerization
- Google Cloud deployment ready
