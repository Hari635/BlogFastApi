web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
web: uvicorn app.main:app --host=0.0.0.0 --port=${PORT}