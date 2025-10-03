# bdpt
The Big Data Parse Theory

## Chat Bot Application

A simple chat bot application built with Streamlit and Google Gemini API.

### Setup

1. Install dependencies:
```bash
uv sync
```

2. Create `.env` file from example:
```bash
cp .env.example .env
```

3. Add your Gemini API key to `.env`:
```
GEMINI_API_KEY=your_actual_api_key
```

Get your API key from: https://makersuite.google.com/app/apikey

### Run

```bash
streamlit run app.py
```

### Features

- Interactive chat interface
- Message history preservation
- Clear chat history button
- Powered by Gemini 1.5 Flash model
