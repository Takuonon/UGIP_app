# Makefile for setting up a new conda environment and installing required packages

# Name of the conda environment
ENV_NAME = env_railway

# Path to the requirement.txt file
REQUIREMENTS_FILE = requirements.txt

# Command to create a new conda environment
CONDA_CREATE_ENV = conda create --name $(ENV_NAME) python=3.8

# Command to install packages using pip
CONDA_INSTALL_PACKAGES = conda install --name $(ENV_NAME) --file $(REQUIREMENTS_FILE)

# Command to activate the conda environment
CONDA_ACTIVATE_ENV = conda activate $(ENV_NAME)

# Google Drive file ID and URL
FILE_ID_pt = https://drive.google.com/drive/folders/1MheAP7o6INpj1pKUrp8CCwCZXJecN9ZQ/best.pt
FILE_URL_pt = "https://drive.google.com/uc?id=$(FILE_ID_pt)"
# Path to save the downloaded file
DOWNLOAD_PATH_pt = weights_folder/best.pt
# Command to download file from Google Drive and save it to specified path
DOWNLOAD_FILE_pt = wget --no-check-certificate $(FILE_URL_pt) -O $(DOWNLOAD_PATH_pt)

# Google Drive file ID and URL
FILE_ID_weights = https://drive.google.com/drive/folders/1MheAP7o6INpj1pKUrp8CCwCZXJecN9ZQ/yolov4.weights
FILE_URL_weights = "https://drive.google.com/uc?id=$(FILE_ID_weights)"
# Path to save the downloaded file
DOWNLOAD_PATH_weights = yolo/yolov4.weights
# Command to download file from Google Drive and save it to specified path
DOWNLOAD_FILE_weights = wget --no-check-certificate $(FILE_URL_weights) -O $(DOWNLOAD_PATH_weights)

# Rule for setting up the conda environment and installing required packages
set-up:
    $(CONDA_CREATE_ENV)
    $(CONDA_INSTALL_PACKAGES)
	$(DOWNLOAD_FILE_pt)
	$(DOWNLOAD_FILE_weights)	
	$(CONDA_ACTIVATE_ENV)

