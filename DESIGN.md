# Design Document

## Architecture Overview

The system consists of three main components:

1. **API Endpoint** (Flask) - Receives quiz tasks and validates requests
2. **Quiz Solver** - Orchestrates the quiz-solving process
3. **Data Processor** - Handles various data formats and operations

## Design Decisions

### 1. Flask for API Endpoint

**Why Flask?**
- Lightweight and simple for single-endpoint API
- Easy to deploy on various platforms
- Built-in JSON handling
- Good for synchronous request handling

**Alternatives considered:**
- FastAPI: More features than needed for this use case
- Django: Too heavy for a simple endpoint

### 2. Playwright for Browser Automation

**Why Playwright?**
- Handles JavaScript-rendered pages (required by quiz)
- Reliable headless browser automation
- Good Python support
- Can wait for network idle state

**Alternatives considered:**
- Selenium: Older, less reliable
- Requests + BeautifulSoup: Cannot handle JavaScript rendering

### 3. GPT-4 for Quiz Understanding

**Why GPT-4?**
- Strong reasoning capabilities for understanding varied quiz formats
- Can generate executable Python code
- Good at extracting structured information from text

**Strategy:**
- Two-step LLM approach:
  1. Understand question and create solution plan
  2. Generate executable code based on plan
- Low temperature (0.1) for consistent, deterministic outputs

### 4. Background Processing

**Current approach:**
- Immediate 200 response to avoid timeout
- Quiz solving happens asynchronously
- Logs track progress

**Why?**
- Quiz solving can take up to 3 minutes
- HTTP clients may timeout on long requests
- Allows server to handle multiple requests

### 5. Error Handling

**Strategy:**
- Validate secret before processing
- Return appropriate HTTP status codes (400, 403, 200)
- Retry logic for incorrect answers (within 3-minute window)
- Comprehensive logging for debugging

### 6. Data Processing

**Supported formats:**
- PDF (PyPDF2)
- CSV (pandas)
- JSON (native)
- Images (Pillow + base64 encoding)
- HTML (BeautifulSoup)

**Why these libraries?**
- Industry standard
- Well-documented
- Reliable

## Prompt Engineering

### System Prompt Strategy (Defense)

Goal: Prevent LLM from revealing the code word

Approach:
- Use absolute language ("never", "must")
- Explicitly mention confidentiality
- Address override attempts directly
- Keep simple to avoid loopholes

### User Prompt Strategy (Attack)

Goal: Make LLM reveal the code word

Approach:
- Direct instruction to ignore previous context
- Request specific output format
- Use authoritative language
- Minimize room for refusal

## Security Considerations

1. **Secret validation** - Prevents unauthorized access
2. **Input validation** - Checks for required fields
3. **Code execution safety** - Limited scope for exec()
4. **File system isolation** - Downloads go to specific directory
5. **Timeout limits** - 3-minute maximum per quiz chain

## Scalability

Current limitations:
- Single-threaded processing
- No queue system
- In-memory state

For production at scale:
- Add Celery for task queue
- Use Redis for state management
- Implement rate limiting
- Add monitoring and alerting

## Testing Strategy

1. **Unit tests** - Test individual components
2. **Integration tests** - Test full quiz flow
3. **Demo endpoint** - Validate against provided demo
4. **Manual testing** - Test various quiz types

## Deployment

Recommended platforms:
- Render (easy, free tier available)
- Railway (simple deployment)
- Heroku (established platform)

Requirements:
- HTTPS support (required by project)
- Environment variable support
- Python 3.11+
- Sufficient memory for Playwright

## Future Improvements

1. **Caching** - Cache LLM responses for similar questions
2. **Parallel processing** - Handle multiple quizzes simultaneously
3. **Better code generation** - Fine-tune prompts for more reliable code
4. **Vision API** - Use GPT-4 Vision for image-based questions
5. **Monitoring** - Add metrics and alerting
6. **Database** - Store quiz history and results
