FROM python:3.9-slim

WORKDIR /app

RUN python3 -c "import urllib.request, zipfile, os; urllib.request.urlretrieve('https://github.com/v2fly/v2ray-core/releases/download/v5.48.0/v2ray-linux-64.zip', '/tmp/v2ray.zip'); zipfile.ZipFile('/tmp/v2ray.zip').extractall('/tmp/v2ray'); os.rename('/tmp/v2ray/v2ray', '/usr/local/bin/v2ray'); os.chmod('/usr/local/bin/v2ray', 0o755)" && rm -rf /tmp/v2ray*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/data

CMD ["python", "main.py"]