# SentimentLab — AI-Based Sentiment Analyzer

A full-stack sentiment analysis application built with **Python, Flask, Hugging Face Transformers, PyTorch, and MongoDB**. Analyze individual reviews or social posts, process CSV datasets in batches, and explore sentiment reports through a responsive web dashboard.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?logo=flask&logoColor=white)
![Transformers](https://img.shields.io/badge/Hugging%20Face-Transformers-FFD21E?logo=huggingface&logoColor=111111)
![MongoDB](https://img.shields.io/badge/MongoDB-7%2B-47A248?logo=mongodb&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

## Features

- **Three-class sentiment analysis:** predicts positive, neutral, or negative sentiment using a pretrained transformer model.
- **Confidence and probability scores:** displays the probability assigned to each sentiment class and the confidence of the winning prediction.
- **Signed sentiment score:** calculates a continuous score from `-100` (most negative) to `+100` (most positive).
- **Single-text analysis:** analyze product reviews, social media posts, feedback, and comments from the dashboard.
- **CSV batch processing:** analyze up to 100 non-empty text rows per upload and save each prediction to MongoDB.
- **Visual reports:** interactive charts show all-time sentiment distribution and daily volume over the last 7, 14, or 30 days.
- **Analysis history:** view recent saved text, predicted sentiment, confidence, sentiment score, and date.
- **REST API:** use the same analysis engine from scripts or other applications.
- **Lazy model initialization:** the model is downloaded and loaded only when the first analysis is requested.
- **CPU/GPU selection:** automatically uses CUDA when available, with CPU fallback; the device can also be configured explicitly.
- **Automated tests:** API tests use a deterministic fake model and `mongomock`, so they do not need a live MongoDB server or a model download.
- **Docker support:** run the Flask app and MongoDB together with Docker Compose.

## Tech stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| NLP / inference | Hugging Face Transformers, PyTorch |
| Pretrained model | `cardiffnlp/twitter-roberta-base-sentiment-latest` |
| Database | MongoDB, PyMongo |
| Frontend | HTML, CSS, JavaScript |
| Charts | Chart.js |
| Testing | pytest, mongomock |
| Containerization | Docker, Docker Compose |

## Project structure

```text
ai-sentiment-analyzer/
├── app/
│   ├── __init__.py                 # Flask application factory and configuration
│   ├── sentiment.py                # Lazy Hugging Face model loader and inference
│   ├── routes.py                   # Dashboard and REST API routes
│   ├── templates/
│   │   └── index.html              # Dashboard UI
│   └── static/
│       ├── css/style.css           # Responsive dashboard styles
│       ├── js/app.js               # Charts and frontend behavior
│       └── sample_reviews.csv      # Example dataset
├── tests/
│   └── test_api.py                 # API and persistence tests
├── .github/workflows/tests.yml     # GitHub Actions test workflow
├── .env.example                    # Environment variable template
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── LICENSE
├── README.md
├── requirements.txt
├── requirements-dev.txt
├── requirements-test.txt
├── requirements-deploy.txt
├── run.py                          # Local development entry point
└── wsgi.py                         # Production WSGI entry point
```

## How sentiment scoring works

The application uses the Cardiff NLP RoBERTa model, which returns probabilities for three classes:

- `negative`
- `neutral`
- `positive`

The class with the highest probability is returned as the predicted sentiment. The **confidence** is that winning class probability, shown as a percentage. Model input is tokenized with a 512-token maximum; longer input is truncated by the tokenizer.

The signed sentiment score is calculated as:

```text
sentiment_score = (positive_probability - negative_probability) × 100
```

Examples:

| Negative | Neutral | Positive | Predicted label | Sentiment score |
|---:|---:|---:|---|---:|
| 0.90 | 0.07 | 0.03 | Negative | -87 |
| 0.10 | 0.80 | 0.10 | Neutral | 0 |
| 0.05 | 0.10 | 0.85 | Positive | +80 |

The score is a convenient directional indicator, not a calibrated measure of customer satisfaction. A high confidence score does not guarantee that a prediction is correct.

## Requirements

- Python **3.10 or newer** (Python 3.11 recommended)
- MongoDB 7+ locally, MongoDB Atlas, or Docker
- Internet access for the first Hugging Face model download
- PyTorch-compatible hardware; a CPU is sufficient, while a supported NVIDIA GPU can accelerate inference

The pretrained model is several hundred megabytes. The first analysis may take longer while the model is downloaded and initialized. Later analyses reuse the in-memory model.

## Run locally (Windows PowerShell)

### 1. Clone the repository

```powershell
git clone https://github.com/YOUR_USERNAME/ai-sentiment-analyzer.git
cd ai-sentiment-analyzer
```

### 2. Create and activate a virtual environment

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

If PowerShell blocks activation, use a terminal where virtual-environment activation is permitted, or run the environment's Python directly with `.\.venv\Scripts\python.exe`.

### 3. Install dependencies

For a CPU-only Windows setup, install the CPU PyTorch wheel first:

```powershell
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
```

For a CUDA-enabled setup, install the PyTorch build compatible with your installed NVIDIA driver from the [official PyTorch installation selector](https://pytorch.org/get-started/locally/), then install the rest of the dependencies:

```powershell
pip install -r requirements.txt
```

### 4. Configure environment variables

```powershell
Copy-Item .env.example .env
```

The default `.env.example` values point to MongoDB on `127.0.0.1:27017`. Edit `.env` if you use MongoDB Atlas or another database host.

### 5. Start MongoDB

**Option A — Docker (recommended):**

```powershell
docker compose up -d mongodb
```

**Option B — Existing MongoDB installation:**

Start your local MongoDB service and leave `MONGO_URI` set to `mongodb://127.0.0.1:27017`.

### 6. Start the Flask application

```powershell
python run.py
```

Open **http://127.0.0.1:5000** in your browser. The model is loaded the first time you submit text, not when Flask starts.

## Run locally (macOS / Linux)

```bash
git clone https://github.com/YOUR_USERNAME/ai-sentiment-analyzer.git
cd ai-sentiment-analyzer
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
docker compose up -d mongodb
python run.py
```

Then visit `http://127.0.0.1:5000`.

## Run with Docker Compose

Docker Compose starts both the web application and MongoDB. The first image build installs PyTorch and Transformers, so it can be large. The first analysis also downloads the pretrained model into the container's Hugging Face cache.

```bash
docker compose up --build
```

Open `http://127.0.0.1:5000`.

Stop the containers:

```bash
docker compose down
```

Stop the containers and delete the MongoDB data volume (this permanently deletes stored analyses):

```bash
docker compose down -v
```

For persistent model caching across container recreation, add a dedicated volume mounted at the Hugging Face cache directory, such as `/root/.cache/huggingface`.

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `MONGO_URI` | `mongodb://127.0.0.1:27017` | MongoDB connection string |
| `MONGO_DB_NAME` | `sentiment_analyzer` | Database name |
| `MONGO_COLLECTION` | `analyses` | Collection used for saved predictions |
| `MODEL_NAME` | `cardiffnlp/twitter-roberta-base-sentiment-latest` | Hugging Face model ID or local model path |
| `MODEL_DEVICE` | `auto` | `auto`, `cpu`, or `cuda` |
| `SECRET_KEY` | development fallback | Flask secret key; set a unique value for deployment |
| `FLASK_DEBUG` | `false` | Set to `true` only for local development |

## REST API

All API responses are JSON. The application stores successful predictions in MongoDB.

### `GET /api/health`

Checks MongoDB connectivity and reports whether the sentiment model has been loaded.

Example:

```bash
curl http://127.0.0.1:5000/api/health
```

### `POST /api/analyze`

Analyze one text string.

Request:

```json
{
  "text": "The product quality is excellent and delivery was quick."
}
```

Example:

```bash
curl -X POST http://127.0.0.1:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"text":"The product quality is excellent and delivery was quick."}'
```

The response includes the prediction, probability for each class, confidence percentage, signed sentiment score, model name, timestamp, and MongoDB document ID.

### `POST /api/analyze/batch`

Analyze a JSON array of strings:

```json
{
  "texts": [
    "I absolutely love this product.",
    "The experience was terrible.",
    "It is an average product."
  ]
}
```

Or upload a CSV file as `multipart/form-data` using the field name `file`. The endpoint auto-detects a column named `text`, `review`, `content`, `message`, or `comment`; otherwise it uses the first column. You can explicitly choose a column by sending an optional `text_column` field.

Example:

```bash
curl -X POST http://127.0.0.1:5000/api/analyze/batch \
  -F "file=@app/static/sample_reviews.csv"
```

The batch endpoint accepts up to 100 non-empty rows per request. Empty rows are ignored.

### `GET /api/history`

Returns saved analyses, newest first.

```text
GET /api/history?limit=10&page=1
```

`limit` is clamped to 1–100. The response includes pagination metadata and each saved analysis.

### `GET /api/analytics`

Returns all-time sentiment totals and a daily timeline.

```text
GET /api/analytics?days=14
```

Supported timeline ranges are `7`, `14`, and `30` days. The distribution counts and average sentiment score cover all saved analyses; the timeline covers only the selected date range.

## Run tests

The test suite does not load the Hugging Face model. It injects a deterministic fake model and uses an in-memory MongoDB mock.

```bash
pip install -r requirements-test.txt
pytest -q
```

For full local development, including the real inference stack and test tools:

```bash
pip install -r requirements-dev.txt
pytest -q
```

A GitHub Actions workflow runs the lightweight test suite for pushes and pull requests.

## Important notes and limitations

- **Language:** the selected CardiffNLP model is intended for English. Predictions on other languages may be unreliable.
- **Domain:** the model is social-media-oriented. It can be useful for short posts and reviews, but specialized domains, sarcasm, mixed-language text, slang, and ambiguous statements can reduce accuracy.
- **Not a fact detector:** sentiment analysis estimates the tone expressed in text. It does not verify the truth of claims or explain why someone feels a certain way.
- **Privacy:** submitted text is stored in your configured MongoDB collection. Do not upload confidential or personally identifying content unless you have permission and an appropriate data-handling policy.
- **Production deployment:** the included Docker Compose file is a convenient local setup, not a hardened public deployment. Configure MongoDB authentication, network restrictions, TLS, a strong secret, request rate limits, access controls, monitoring, and backups before exposing the service publicly.
- **Model licensing:** review the model's own license and terms before redistributing model weights or using it commercially. The application code's MIT license does not replace the model's license.

## Model reference

- Model card: [cardiffnlp/twitter-roberta-base-sentiment-latest](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest)
- The model card documents the three labels as `0 = Negative`, `1 = Neutral`, and `2 = Positive`, and includes the Transformers pipeline usage example.
- Model paper: [TimeLMs: Diachronic Language Models from Twitter](https://arxiv.org/abs/2202.03829)

## License

This repository's application code is released under the [MIT License](LICENSE). The Hugging Face model has its own license and usage conditions; see its model card before using or redistributing it.

---

**Built as a portfolio-ready full-stack machine learning project.** Contributions, issues, and improvements are welcome.
