from dataset import load_cached
import download
import os

data_dir = "data/sigComp2011/"
train_dir = os.path.join(data_dir, "train/")
test_dir = os.path.join(data_dir, "test/")

train_data_url = "http://www.iapr-tc11.org/dataset/ICDAR_SignatureVerification/SigComp2011/sigComp2011-trainingSet.zip"
test_data_url = "http://www.iapr-tc11.org/dataset/ICDAR_SignatureVerification/SigComp2011/sigComp2011-test.zip"


def maybe_download_and_extract():
    print("Downloading train data from", train_data_url, "...")
    download.maybe_download_and_extract(url=train_data_url, download_dir=data_dir, pwd=b'I hereby accept the SigComp 2011 disclaimer.')
    print("Downloading test data from", test_data_url, "...")
    download.maybe_download_and_extract(url=test_data_url, download_dir=data_dir, pwd=b'I hereby accept the SigComp 2011 disclaimer.')

def load():
    """
    Load the dataset into memory.

    This uses a cache-file which is reloaded if it already exists,
    otherwise the dataset is created and saved to
    the cache-file. The reason for using a cache-file is that it
    ensure the files are ordered consistently each time the dataset
    is loaded. This is important when the dataset is used in
    combination with Transfer Learning.

    :return:
        A DataSet-object.
    """

    # # Path for the cache-file.
    # cache_path = os.path.join(data_dir, "knifey-spoony.pkl")

    # # If the DataSet-object already exists in a cache-file
    # # then load it, otherwise create a new object and save
    # # it to the cache-file so it can be loaded the next time.
    # dataset = load_cached(cache_path=cache_path,
    #                       in_dir=data_dir)

    # return dataset

def copy_files():
    """
    Copy all the files in the training-set to train_dir
    and copy all the files in the test-set to test_dir.

    This creates the directories if they don't already exist,
    and it overwrites the images if they already exist.

    The images are originally stored in a directory-structure
    that is incompatible with e.g. the Keras API. This function
    copies the files to a dir-structure that works with e.g. Keras.
    """

    # # Load the Knifey-Spoony dataset.
    # # This is very fast as it only gathers lists of the files
    # # and does not actually load the images into memory.
    # dataset = load()

    # # Copy the files to separate training- and test-dirs.
    # dataset.copy_files(train_dir=train_dir, test_dir=test_dir)