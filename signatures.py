from dataset import load_cached
import download
import os

data_dir = "data/sigComp2011/"
train_dir = os.path.join(data_dir, "train/")
test_dir = os.path.join(data_dir, "test/")

train_data_url = "http://www.iapr-tc11.org/dataset/ICDAR_SignatureVerification/SigComp2011/sigComp2011-trainingSet.zip"
test_data_url = "http://www.iapr-tc11.org/dataset/ICDAR_SignatureVerification/SigComp2011/sigComp2011-test.zip"


def maybe_download_and_extract():
    download.maybe_download_and_extract(url=train_data_url, download_dir=data_dir, pwd=b'I hereby accept the SigComp 2011 disclaimer.')
    download.maybe_download_and_extract(url=test_data_url, download_dir=data_dir, pwd=b'I hereby accept the SigComp 2011 disclaimer.')
