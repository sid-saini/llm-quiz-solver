# Render Deployment - Step by Step

## Step 1: Sign Up / Login

1. Go to: **https://render.com**
2. Click **"Get Started"** or **"Sign In"**
3. Choose **"Sign in with GitHub"**
4. Authorize Render to access your GitHub account

## Step 2: Create New Web Service

1. Once logged in, click the **"New +"** button (top right)
2. Select **"Web Service"** from the dropdown

## Step 3: Connect Repository

1. You'll see a list of your GitHub repositories
2. Find **"llm-quiz-solver"** in the list
3. Click **"Connect"** next to it

   **If you don't see it:**
   - Click "Configure account" 
   - Grant Render access to the repository
   - Go back and click "Connect"

## Step 4: Configure Service

Fill in these settings:

### Basic Settings:
- **Name**: `llm-quiz-solver` (or any name you prefer)
- **Region**: Choose closest to you (e.g., Singapore, Oregon)
- **Branch**: `main`
- **Root Directory**: Leave blank
- **Runtime**: `Python 3`

### Build & Deploy:
- **Build Command**: 
  ```
  pip install -r requirements.txt && playwright install chromium
  ```

- **Start Command**:
  ```
  python app.py
  ```

### Instance Type:
- Select **"Free"** (should be selected by default)

## Step 5: Add Environment Variables

Scroll down to **"Environment Variables"** section and click **"Add Environment Variable"**

Add these 4 variables one by one:

1. **Key**: `EMAIL`  
   **Value**: `23f2003951@ds.study.iitm.ac.in`

2. **Key**: `SECRET`  
   **Value**: `data-science`

3. **Key**: `OPENAI_API_KEY`  
   **Value**: `your-actual-openai-api-key` (get from https://platform.openai.com/api-keys)

4. **Key**: `PORT`  
   **Value**: `10000`

## Step 6: Deploy

1. Scroll to the bottom
2. Click **"Create Web Service"**
3. Wait for deployment (5-10 minutes)

You'll see logs showing:
- Installing dependencies
- Installing Playwright
- Starting the server

## Step 7: Get Your URL

Once deployed, you'll see:
- **Status**: "Live" (green dot)
- **URL**: `https://llm-quiz-solver-xxxx.onrender.com`

Copy this URL - you'll need it for the Google Form!

## Step 8: Test Your Deployment

### Test 1: Health Check
Open in browser or use curl:
```
https://your-app-name.onrender.com/health
```

Should return: `{"status":"ok"}`

### Test 2: Quiz Endpoint
```bash
curl -X POST https://your-app-name.onrender.com/quiz \
  -H "Content-Type: application/json" \
  -d '{"email":"23f2003951@ds.study.iitm.ac.in","secret":"data-science","url":"https://tds-llm-analysis.s-anand.net/demo"}'
```

Should return: `{"status":"processing","url":"..."}`

## Troubleshooting

### Build Failed
- Check the logs in Render dashboard
- Make sure all files are pushed to GitHub
- Verify requirements.txt is correct

### Service Won't Start
- Check environment variables are set correctly
- Look at the logs for error messages
- Make sure PORT is set to 10000

### 500 Error
- Check application logs
- Verify OpenAI API key is valid
- Make sure you have OpenAI credits

## Monitoring

### View Logs:
1. Go to your service dashboard
2. Click **"Logs"** tab
3. Watch real-time logs during quiz time

### Restart Service:
1. Go to service dashboard
2. Click **"Manual Deploy"** → **"Clear build cache & deploy"**

## Important Notes

- **Free tier sleeps after 15 minutes of inactivity**
- **First request after sleep takes 30-60 seconds to wake up**
- **Keep the service active during quiz time (Nov 29, 3-4 PM IST)**
- **You can ping the health endpoint every 10 minutes to keep it awake**

## Your Deployment URL

Once deployed, your endpoint will be:
```
https://your-app-name.onrender.com/quiz
```

Use this URL in the Google Form submission!

## Next Step

After successful deployment, fill out the Google Form with:
- Your deployment URL
- GitHub repository URL
- System and user prompts

See `SUBMISSION_INFO.md` for complete form details.
