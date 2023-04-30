# Path to the requirement.txt file
REQUIREMENTS_FILE = requirements.txt

# Command to install packages using pip
CONDA_INSTALL_PACKAGES = pip install -r $(REQUIREMENTS_FILE)

# Google Drive file ID and URL
FILE_ID_pt = 1fGEJ3QQLqCWHUbfmBY7pEOT7Q4nWD5pc
FILE_URL_pt = "https://drive.google.com/uc?id=$(FILE_ID_pt)"
# Path to save the downloaded file
DOWNLOAD_PATH_pt = weights_folder/best.pt
# Command to download file from Google Drive and save it to specified path
DOWNLOAD_FILE_pt = wget --no-check-certificate $(FILE_URL_pt) -O $(DOWNLOAD_PATH_pt)

# Google Drive file ID and URL
FILE_ID_weights = 1CvnoffsL81Z-2gV1HzfJ30P3QBQnjmsG
FILE_URL_weights = "https://drive.google.com/uc?id=$(FILE_ID_weights)"
# Path to save the downloaded file
DOWNLOAD_PATH_weights = yolo/yolov4.weights
# Command to download file from Google Drive and save it to specified path
DOWNLOAD_FILE_weights = wget --no-check-certificate $(FILE_URL_weights) -O $(DOWNLOAD_PATH_weights)

# Rule for setting up the conda environment and installing required packages
install:
	$(CONDA_INSTALL_PACKAGES)

download:
	$(DOWNLOAD_FILE_pt)
	$(DOWNLOAD_FILE_weights)	

start:
	streamlit run app.py