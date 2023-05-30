FROM python:3.9

WORKDIR /app


RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y libgl1-mesa-dev

# Copy the requirements.txt file
COPY . .

# Install packages using pip
RUN pip install -r requirements.txt

# Set environment variables
ENV FILE_ID_pt=1fGEJ3QQLqCWHUbfmBY7pEOT7Q4nWD5pc
ENV FILE_URL_pt="https://drive.google.com/uc?id=$FILE_ID_pt"
ENV DOWNLOAD_PATH_pt=./weights_folder/best.pt
ENV DOWNLOAD_FILE_pt="wget --no-check-certificate $FILE_URL_pt -O $DOWNLOAD_PATH_pt"

ENV FILE_ID_weights=1CvnoffsL81Z-2gV1HzfJ30P3QBQnjmsG
ENV FILE_URL_weights="https://drive.google.com/uc?id=$FILE_ID_weights"
ENV DOWNLOAD_PATH_weights=./yolo/yolov4.weights
ENV DOWNLOAD_FILE_weights="wget --no-check-certificate $FILE_URL_weights -O $DOWNLOAD_PATH_weights"

# Download files from Google Drive
RUN $DOWNLOAD_FILE_pt
RUN $DOWNLOAD_FILE_weights

# Copy the app.py file
COPY app.py .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]