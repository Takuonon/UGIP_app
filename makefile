.ONESHELL:

# Google Drive file ID
FILE_ID = 1fGEJ3QQLqCWHUbfmBY7pEOT7Q4nWD5pc

FILE_NAME = ./weights_folder/best.pt
PREDOWNLOAD_FILE = curl -sc /tmp/cookie "https://drive.google.com/uc?export=download&id=${FILE_ID}" > /dev/null
CODE="$(awk '/_warning_/ {print $NF}' /tmp/cookie)"
DOWNLOAD_FILE = curl -Lb /tmp/cookie "https://drive.google.com/uc?export=download&confirm=${CODE}&id=${FILE_ID}" -o ${FILE_NAME}

download:
	$(PREDOWNLOAD_FILE)
	$(DOWNLOAD_FILE)