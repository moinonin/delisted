install:
	apt install firefox xorg
test:
	MOZ_HEADLESS=1 python main.py
run:
	MOZ_HEADLESS=1 gunicorn -k uvicorn.workers.UvicornWorker main:app --reload
