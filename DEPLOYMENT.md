# Deployment Checklist

## For Replit Deployment

### Prerequisites
- [x] `.replit` file created (already in repo)
- [x] `requirements.txt` updated with FastAPI and Uvicorn
- [x] `web_server.py` created and tested locally
- [x] `web/index.html` created with playground UI
- [x] Code pushed to GitHub

### Steps to Deploy

1. **Push to GitHub** (if not already done):
   ```bash
   git add -A
   git commit -m "Add web playground (FastAPI + Frontend)"
   git push origin main
   ```

2. **Deploy to Replit**:
   - Go to https://replit.com
   - Click "Create" → "Import from GitHub"
   - Paste your GitHub repo URL
   - Click "Import"
   - Wait 1-2 minutes for installation
   - Click "Run"
   - Copy the live URL from top-right

3. **Test the Playground**:
   - Click "Hello World" example
   - Click "Run Code"
   - See "Sannu Duniya" in output
   - Try modifying code

4. **Share the Link**:
   - Copy the Replit URL
   - Share on:
     - GitHub repo README
     - Reddit r/learnprogramming
     - Twitter/X
     - Dev.to

### What Replit Provides

- ✅ Free hosting (sleeping after 1 hour inactivity, wakes on request)
- ✅ Automatic HTTPS
- ✅ Always-on URL
- ✅ Python 3.10+ pre-installed
- ✅ Easy collaboration (share link)

### Troubleshooting

If server won't start:
1. Check `requirements.txt` has `fastapi` and `uvicorn`
2. Check `web_server.py` exists and is valid Python
3. Check `.replit` has `run = "python web_server.py"`
4. View logs in Replit console

### Future Improvements

- [ ] Add more tutorials/lessons
- [ ] Deploy feedback form to gather user requests
- [ ] Add syntax highlighting in editor
- [ ] Cache examples for offline use
- [ ] Add dark/light mode toggle
