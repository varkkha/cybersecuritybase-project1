# Cyber Security Base - Project I

## Installation instructions

1. Clone the repository and move to the root folder
```bash
git clone git@github.com:varkkha/cybersecuritybase-project1.git
cd cybersecuritybase-project1
```

2. Set up a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run migrations. Make sure you're in the src-folder.
```bash
cd app
python manage.py migrate
```
5. Start the development server
```bash
python manage.py runserver
```
Visit http://localhost:8000 in your browser.