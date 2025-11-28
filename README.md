# LLM Analysis Quiz Solver

Automated quiz solver using LLMs for data sourcing, preparation, analysis, and visualization.

## Features

- Flask API endpoint to receive quiz tasks
- Headless browser (Playwright) for JavaScript-rendered pages
- LLM-powered quiz understanding and solution generation
- Support for multiple data formats (CSV, JSON, PDF, images)
- Automated answer submission with retry logic

## Setup

### Installation

```bash
pip install -r requirements.txt
playwright install chromium
```

### Configuration

Create a `.env` file:

```env
EMAIL=your-email@example.com
SECRET=your-secret-string
OPENAI_API_KEY=your-openai-key
PORT=8000
```

### Running Locally

```bash
python app.py
```

The server will start on `http://0.0.0.0:8000`

## API Endpoints

### POST /quiz

Receives quiz tasks and processes them automatically.

**Request:**
```json
{
  "email": "your-email@example.com",
  "secret": "your-secret",
  "url": "https://example.com/quiz-url"
}
```

**Response:**
- `200 OK` - Request accepted and processing
- `400 Bad Request` - Invalid JSON or missing fields
- `403 Forbidden` - Invalid secret

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

## Deployment

### Render

1. Push code to GitHub
2. Create new Web Service on Render
3. Connect your repository
4. Set environment variables (EMAIL, SECRET, OPENAI_API_KEY)
5. Deploy

### Railway

1. Push code to GitHub
2. Create new project on Railway
3. Deploy from GitHub
4. Add environment variables

### Heroku

```bash
heroku create your-app-name
heroku config:set EMAIL=your-email
heroku config:set SECRET=your-secret
heroku config:set OPENAI_API_KEY=your-key
git push heroku main
```

## Project Structure

```
.
├── app.py              # Flask API endpoint
├── quiz_solver.py      # Quiz solving logic
├── data_processor.py   # Data handling utilities
├── monitor.py          # Health monitoring script
├── requirements.txt    # Python dependencies
├── Procfile           # Heroku deployment
├── render.yaml        # Render deployment
└── runtime.txt        # Python version
```

## Monitoring

Monitor your deployed endpoint:

```bash
python monitor.py
```

## Architecture

See [DESIGN.md](DESIGN.md) for detailed architecture and design decisions.

## Prompts

See [prompts.md](prompts.md) for prompt engineering strategies.

## License

MIT License
