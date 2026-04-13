# AI Assistant Integration Guide

## Overview

The Journal Desk application includes an advanced AI chatbot powered by Ollama, a local large language model (LLM) system. The AI assistant helps you reflect on journal entries, provides task recommendations, and offers contextual information like weather and real-time data.

## Features

### 1. **Smart Context Awareness**
The AI has access to your journal context:
- Total entries, tasks, and completion status
- Priority levels of pending tasks
- Overdue task alerts
- Recent journal activity
- Starred (important) entries

### 2. **Intelligent Prompt Detection**
The AI automatically detects what you need:
- **Recommendations**: Asks for task suggestions and insights
  - Keywords: "recommend", "suggest", "advice", "plan", "next step", "prioritize"
  - Returns: Numbered action steps based on your journal context
  
- **Real-time Context**: Current date/time information
  - Keywords: "today", "right now", "now", "time", "date", "current time"
  - Returns: Server local time with timezone
  
- **Weather Integration**: Current weather conditions
  - Keywords: "weather", "temperature", "forecast", "rain", "wind", "sunny", "cloud"
  - Returns: Real-time weather from Open-Meteo API

### 3. **Optimized Response Quality**
- **Temperature Control**: Lower temperature (0.6) for recommendations, normal (0.7) for general chat
- **Response Limits**: Capped at 500 tokens to ensure focused, concise responses
- **Validation**: Truncates responses > 5000 characters with proper ending
- **error Handling**: Graceful fallback to alternative models if configured model is unavailable

## System Requirements

### Ollama Setup

1. **Install Ollama**
   - Visit: https://ollama.ai
   - Download and install for your OS (macOS, Linux, Windows)

2. **Pull a Model**
   - Open terminal/command prompt
   - Run: `ollama pull llama2` (or other models)
   - Available models: llama2, llama3.2, mistral, neural-chat, qwen2.5

3. **Start Ollama Server**
   - Run: `ollama serve`
   - Default URL: http://127.0.0.1:11434
   - The server runs in the background on Linux/macOS

### Configuration

Set these environment variables in `.env`:

```
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL=llama2
OLLAMA_TIMEOUT_SECONDS=30
OLLAMA_FALLBACK_MODELS=llama2,llama3.2,mistral,qwen2.5
```

**OLLAMA_MODEL**: Your preferred model (must be pulled first)
**OLLAMA_TIMEOUT_SECONDS**: Max wait time for responses (default 30s)
**OLLAMA_FALLBACK_MODELS**: Fallback models if primary is unavailable

## API Endpoints

### 1. **Chat Endpoint** `POST /chatbot/`

Send a message to the AI assistant.

**Request:**
```json
{
    "prompt": "What should I prioritize next?",
    "history": [
        {"role": "user", "content": "How's my progress?"},
        {"role": "assistant", "content": "You have 3 overdue tasks..."}
    ],
    "model": "llama2",
    "weather_location": "Nairobi",
    "lat": -0.897150,
    "lon": 37.002800
}
```

**Parameters:**
- `prompt` (required): Your question or message
- `history`: Previous messages (last 12 messages kept)
- `model`: Override configured model (optional)
- `weather_location`: City for weather lookup (optional)
- `lat`, `lon`: Coordinates for weather (optional, overrides location)

**Response:**
```json
{
    "reply": "Based on your journal...",
    "model": "llama2",
    "realtime": {
        "local_datetime": "Monday, April 07, 2026 22:30:45",
        "timezone": "UTC",
        "iso": "2026-04-07T22:30:45+00:00"
    },
    "weather": {
        "location": "Nairobi, Kenya",
        "temperature_c": 24.5,
        "feels_like_c": 23.8,
        "weather": "Partly cloudy",
        "wind_kph": 12,
        "precip_mm": 0
    }
}
```

### 2. **Realtime Endpoint** `GET /chatbot/live/`

Get current time and weather without AI response.

**Query Parameters:**
- `location`: City name (e.g., "London")
- `lat`, `lon`: GPS coordinates

**Response:**
```json
{
    "realtime": {
        "local_datetime": "Monday, April 07, 2026 22:30:45",
        "timezone": "UTC"
    },
    "weather": {
        "location": "Nairobi, Kenya",
        "temperature_c": 24.5,
        "feels_like_c": 23.8,
        "weather": "Partly cloudy",
        "wind_kph": 12,
        "precip_mm": 0
    }
}
```

### 3. **Health Check** `GET /chatbot/health/`

Check Ollama connectivity and available models.

**Response:**
```json
{
    "status": "healthy",
    "ollama_url": "http://127.0.0.1:11434",
    "models": {
        "configured": "llama2",
        "available": ["llama2:latest", "llama3.2:latest", "mistral:latest"]
    },
    "errors": [],
    "warnings": []
}
```

**Status Values:**
- `healthy`: Ollama running with available models
- `no-models`: Ollama connected but no models pulled
- `unhealthy`: Cannot connect to Ollama

## Usage Examples

### Example 1: Get Task Recommendations
```
User: "What should I focus on today? Suggest a plan."
```
The AI detects keywords "suggest" and "plan", loads your journal context, and returns numbered recommendations prioritizing overdue tasks.

### Example 2: Ask About Weather
```
User: "What's the weather like in Tokyo today?"
```
The AI:
1. Detects "weather" keyword
2. Extracts location "Tokyo"
3. Fetches current weather from Open-Meteo API
4. Includes weather in response

### Example 3: Task-Specific Help
```
User: "How should I approach my quarterly review task?"
```
The AI:
1. Searches your journal for entries containing "quarterly review"
2. Extracts context about that task
3. Provides specific, actionable steps

### Example 4: Real-time + Recommendation
```
User: "What do I need to do right now? It's getting late."
```
The AI includes:
- Current time (from "right now")
- Task recommendations (from "what do I need")
- Urgency assessment based on task due times

## Model Selection

### Recommended Models

**llama2** (7B parameters)
- Pro: Fast, balanced quality, good for recommendations
- Con: Smaller context window
- Best for: General chat, quick responses

**llama3.2** (Latest)
- Pro: Newer, better reasoning, improved recommendations
- Con: Slower than llama2
- Best for: Complex reasoning, task planning

**mistral** (7B parameters)
- Pro: Fast, good math/logic, excellent docs
- Con: Less fine-tuned for journaling
- Best for: Analytical questions

**neural-chat** (7B parameters)
- Pro: Optimized for conversations
- Con: Less common, fewer resources
- Best for: Natural conversation flow

### Pull Multiple Models
```bash
ollama pull llama2
ollama pull llama3.2
ollama pull mistral
```

Switch at runtime or via API using the `model` parameter.

## Error Handling

### Common Issues

**"Could not connect to Ollama"**
- Check if Ollama server is running: `ollama serve`
- Verify OLLAMA_BASE_URL in .env
- Check firewall/network settings

**"Configured Ollama model was not found"**
- Pull the model: `ollama pull llama2`
- System will automatically try fallback models
- Check available models with `/chatbot/health/`

**"Weather lookup failed"**
- Non-critical error, gracefully falls back
- Uses last known location
- Check internet connection

**Empty Response**
- Model may be overloaded or unresponsive
- Try again with shorter prompt
- Check logs: `tail -f logs/journal.log`

**Timeout**
- Increase OLLAMA_TIMEOUT_SECONDS to 60+
- May indicate slow system or network
- Try simpler prompts first

## Performance Tuning

### Optimize Response Speed

1. **Choose faster models**
   - llama2 is fastest
   - neural-chat good alternative

2. **Increase timeouts if needed**
   ```
   OLLAMA_TIMEOUT_SECONDS=60
   ```

3. **Adjust temperature**
   - Lower = faster but more conservative
   - Higher = more creative but slower

4. **Limit history**
   - Default keeps 12 messages (optimized)
   - Reducing further speeds up processing

5. **Use shorter prompts**
   - Lengthy prompts take longer to process
   - Be specific and concise

### System Resources

- **RAM**: 8GB minimum (16GB+ recommended)
- **VRAM**: Not required (CPU only)
- **Storage**: 5-10GB per model
- **Network**: Not needed after model is pulled

## Logging

Check `/logs/journal.log` for AI activity:

```
INFO 2026-04-07 22:30:45 ollama_chat Ollama chat successful: user=jayden, model=llama2, prompt_len=156, response_len=287
INFO 2026-04-07 22:30:42 chatbot_health Chatbot health check successful: 3 models available
WARNING 2026-04-07 22:30:40 ollama_chat Response exceeded 5000 chars, truncating
ERROR 2026-04-07 22:30:38 ollama_chat Ollama returned empty response
```

## API Authentication

All AI endpoints require user authentication:
- User must be logged in
- Respects user's journal (only their entries used)
- Each query logged with username for debugging

## Best Practices

1. **Be Specific**
   - Good: "What priority should I give to the quarterly review task?"
   - Bad: "help"

2. **Reference Your Journal**
   - The AI knows your recent entries and tasks
   - Mention specific task names for better context

3. **Ask for Formats**
   - "Give me numbered steps"
   - "Format as a checklist"
   - "Keep it to 2-3 sentences"

4. **Use Real-time Context**
   - "What should I finish before 5 PM today?"
   - "Weather in my area - how should I plan?"

5. **For Recommendations**
   - Mention you want "advice", "suggestions", or a "plan"
   - AI will automatically add journal context
   - Prioritizes overdue items

## Advanced: Custom Models

To use a custom or different model:

1. Download from Ollama library or create custom
2. Pull using Ollama: `ollama pull yourmodel`
3. Set in `.env`: `OLLAMA_MODEL=yourmodel`
4. Restart application

## Troubleshooting Checklist

- [ ] Ollama is running: `ollama serve`
- [ ] Model is pulled: `ollama list`
- [ ] OLLAMA_BASE_URL is correct in .env
- [ ] Firewall allows localhost:11434
- [ ] Python logs show no errors: `tail -f logs/journal.log`
- [ ] Health check passes: `GET /chatbot/health/`
- [ ] User is logged in
- [ ] Prompt is not empty
- [ ] No network issues (for weather lookup)

## Future Improvements

Potential AI enhancements:
- [ ] Rag (Retrieval-Augmented Generation) with full journal search
- [ ] Multi-turn reasoning for complex tasks
- [ ] Task time estimates and scheduling
- [ ] Sentiment analysis of entries
- [ ] Custom model fine-tuning on user patterns
- [ ] Image-based weather icons
- [ ] Voice input/output
- [ ] Multi-language support

## Support

For issues:
1. Check `/logs/journal.log` for errors
2. Run health check: `curl http://localhost:8000/chatbot/health/`
3. Verify Ollama: `curl http://localhost:11434/api/tags`
4. Check system resources: `htop` (RAM/CPU)
5. Review this guide's troubleshooting section

## Resources

- Ollama: https://ollama.ai
- Available Models: https://ollama.ai/library
- Open-Meteo Weather API: https://open-meteo.com
- Django Logging: https://docs.djangoproject.com/en/6.0/topics/logging/
