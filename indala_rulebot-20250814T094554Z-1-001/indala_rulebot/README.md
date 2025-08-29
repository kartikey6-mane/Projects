# Indala Rule-Based Chatbot (FastAPI)

## Quick Start
1) Create and activate a virtual environment
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```
2) Install requirements
   ```bash
   pip install -r requirements.txt
   ```
3) Edit `data/faq_template.csv` (add your FAQs), then seed:
   ```bash
   python scripts/seed_db.py
   ```
4) Run the API
   ```bash
   uvicorn app.main:app --reload
   ```
5) Test at http://127.0.0.1:8000/docs

6) Floating widget:
   - Serve `static/widget/chatbot-widget.js`
   - In that file set `API_BASE` to your server URL
   - Add to your page before </body>:
     ```html
     <script src="chatbot-widget.js"></script>
     ```