FROM python:3.11-slim

WORKDIR /app

# Копируем файлы requirements (если существует) и остальные файлы
COPY requirements.txt* ./
COPY bot.py .
COPY комплименты.csv .
COPY цитаты.csv .
COPY DATA.csv .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Запускаем бота
CMD ["python", "bot.py"]
