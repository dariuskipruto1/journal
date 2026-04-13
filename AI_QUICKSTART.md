# AI Quick Start Guide

## 5-Minute Setup

### Step 1: Install Ollama
```bash
# Download from https://ollama.ai
# Or use package manager:
# macOS: brew install ollama
# Linux: Visit https://ollama.ai
```

### Step 2: Pull a Model
```bash
ollama pull llama2
```

### Step 3: Start Ollama Server
```bash
ollama serve
# Runs at http://127.0.0.1:11434
```

### Step 4: Configure .env
```bash
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL=llama2
OLLAMA_TIMEOUT_SECONDS=30
```

### Step 5: Run App
```bash
python manage.py runserver
```

### Step 6: Test AI
Visit: http://localhost:8000/chatbot/health/

Should see:
```json
{
    "status": "healthy",
    "models": {
        "configured": "llama2",
        "available": ["llama2:latest"]
    }
}
```

---

## Using the AI Assistant

### In the App
1. Open journal entry list
2. Scroll to chatbot section
3. Type your question
4. Get AI-powered response

### Smart Keywords

#### Get Recommendations
```
"Suggest what I should work on"
"Give me advice on my tasks"
"What's my next priority?"
→ AI uses your journal context
```

#### Check Weather
```
"What's the weather?"
"Is it raining in London?"
"Weather in Tokyo today"
→ Real-time Open-Meteo data
```

#### Get Real-time Info
```
"What time is it?"
"Tell me today's date"
"Current time please"
→ Server local time
```

#### Mixed Request
```
"What should I do now? It's getting late and it looks cloudy."
→ Time + weather + recommendations
```

---

## Available Models

### Fast & Good (Recommended)
```bash
ollama pull llama2
# Pro: Fast, balanced quality
# Con: Smaller context
# Best for: General use, quick responses
```

### Latest & Best Quality
```bash
ollama pull llama3.2
# Pro: Newest, best reasoning
# Con: Slower (30-60 seconds)
# Best for: Complex questions
```

### Fast & Analytical
```bash
ollama pull mistral
# Pro: Very fast, good logic
# Con: Less conversational
# Best for: Analysis, math
```

### All at Once
```bash
ollama pull llama2 && \
ollama pull llama3.2 && \
ollama pull mistral
# Switch anytime in settings
```

---

## Common Questions

**Q: "AI is too slow"**
- Use `llama2` model (fastest)
- Check: `ollama list`
- Increase `OLLAMA_TIMEOUT_SECONDS` if needed

**Q: "Getting empty responses"**
- Check Ollama is running: `ollama serve`
- Check logs: `tail logs/journal.log`
- Restart Ollama

**Q: "Want to use different model"**
- Pull model: `ollama pull modelname`
- Update `.env`: `OLLAMA_MODEL=modelname`
- Restart app

**Q: "Can I use cloud-based LLM?"**
- Not yet, but architecture supports it
- Currently local-only for privacy

**Q: "How accurate is the AI?"**
- Good for suggestions and planning
- Your journal context makes it personal
- Always verify critical recommendations

---

## API Examples

### Test with curl

**Health Check**
```bash
curl http://localhost:8000/chatbot/health/
```

**Send Chat Message**
```bash
curl -X POST http://localhost:8000/chatbot/ \
  -H "Content-Type: application/json" \
  -H "Cookie: sessionid=YOUR_SESSION_ID" \
  -d '{"prompt": "What should I focus on?"}'
```

**Get Time & Weather**
```bash
curl "http://localhost:8000/chatbot/live/?location=Tokyo"
```

---

## Performance Tips

### Make AI Faster
1. Use `llama2` (fastest model)
2. Ask shorter questions
3. Avoid very long chat history
4. Check system RAM: `free -h` (Linux) or Activity Monitor (Mac)

### Make Responses Better
1. Be specific about what you want
2. Reference tasks by name
3. Mention you want "recommendations" or "advice"
4. Ask for specific format ("numbered steps", "checklist")

### Monitor Quality
```bash
# Watch logs in real-time
tail -f logs/journal.log | grep "ollama_chat"
```

---

## What Happens Behind the Scenes

1. **You type a message** → App receives prompt
2. **Smart detection** → App detects what you need (time? weather? recommendations?)
3. **Context building** → App loads your journal data (entries, tasks, priorities)
4. **API call** → App sends to Ollama with context
5. **Processing** → Model generates response
6. **Validation** → App checks response is valid
7. **Return** → Response sent to you

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Cannot connect to Ollama" | Run `ollama serve` |
| "Model not found" | Run `ollama pull llama2` |
| "Response is too slow" | Use faster model (`llama2`) |
| "Response is empty" | Check Ollama logs, increase timeout |
| "Out of memory" | Close other apps, use smaller model |
| "Health check returns 503" | Ollama server not running |

---

## Next Steps

1. ✅ **Install & Configure**: Complete 5-minute setup
2. ✅ **Test Health**: Visit `/chatbot/health/`
3. ✅ **Try Recommendations**: Ask AI "What should I work on?"
4. ✅ **Explore Features**: Try weather, time, task-specific help
5. ✅ **Monitor Logs**: Check `/logs/journal.log` for usage

---

## Learn More

- **Full AI Guide**: See `AI_INTEGRATION.md`
- **Technical Details**: See `AI_IMPROVEMENTS.md`
- **Project Docs**: See `README.md`

---

## Support

If having issues:
1. Check `/logs/journal.log` for errors
2. Run health check: `curl http://localhost:8000/chatbot/health/`
3. Verify Ollama: `ollama list` and `ollama serve` running
4. Review `AI_INTEGRATION.md` troubleshooting section
