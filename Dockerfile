FROM python:3.9

WORKDIR /app

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y libgl1-mesa-dev

# Copy the requirements.txt file
COPY . .

# Install packages using pip
RUN pip install -r requirements.txt

# Copy the app.py file
COPY app.py .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]