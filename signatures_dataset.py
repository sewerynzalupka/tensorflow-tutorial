import numpy as np
import os
import shutil
from cache import cache
import re

forgery_filename_pattern = r"(?P<forger>\d{{4}})(?P<signer>\d{{3}})_(?P<i>\d{{2}})({exts})$"
genuine_filename_pattern = r"(?P<signer>\d{{3}})_(?P<i>\d{{2}})({exts})$"

class SignaturesDataset:
    def __init__(self, train_dir, test_dir, exts=['.png']):
        """
        Create a data-set consisting of the filenames in the given directory
        and sub-dirs that match the given filename-extensions.

        :param train_dir:
            Root-dir for the files in the data-set.
            
        :param test_dir:
            Root-dir for the files in the data-set.

        :param exts:
            String or tuple of strings with valid filename-extensions.
            Not case-sensitive.

        :return:
            Object instance.
        """

        # Extend input directories to the full path.
        train_dir = os.path.abspath(train_dir)
        test_dir = os.path.abspath(test_dir)

        # Input directories.
        self.train_dir = train_dir
        self.test_dir = test_dir

        # Convert all file-extensions to lower-case.
        self.exts = tuple(ext.lower() for ext in exts)

        # Train set
        signatures = {}
        for filename in self._get_filenames(self.train_dir):
            forgery_match = re.search(forgery_filename_pattern.format(exts='|'.join(self.exts)), filename.lower())
            if forgery_match:
                forged_signer = forgery_match.group('signer')
                if forged_signer not in signatures:
                    signatures[forged_signer] = { 'genuine': [], 'forgeries': [] }
                signatures[forged_signer]['forgeries'].append(filename)
                continue
            genuine_match = re.search(genuine_filename_pattern.format(exts='|'.join(self.exts)), filename.lower())
            if genuine_match:
                signer = genuine_match.group('signer')
                if signer not in signatures:
                    signatures[signer] = { 'genuine': [], 'forgeries': [] }
                signatures[signer]['genuine'].append(filename)
        
        authors = list(signatures.keys())
        
        self.signatures_dict = signatures
        
        self.genuine_classes = ['{author}_genuine'.format(author=author) for author in authors]
        self.forged_classes = ['{author}_forged'.format(author=author) for author in authors]
        self.class_names = self.genuine_classes + self.forged_classes
        
        self.num_classes = len(self.class_names)
                
    def _get_filenames(self, dir):
        """
        Create and return a list of filenames with matching extensions in the given directory.

        :param dir:
            Directory to scan for files. Sub-dirs are not scanned.

        :return:
            List of filenames. Only filenames. Does not include the directory.
        """
        filenames = []
        for root, dirs, files in os.walk(dir):
            for file in files:
                if file.lower().endswith(self.exts):
                    filenames.append(os.path.join(root, file))
        return filenames

def load_cached(cache_path, train_dir, test_dir):
    """
    Wrapper-function for creating a DataSet-object, which will be
    loaded from a cache-file if it already exists, otherwise a new
    object will be created and saved to the cache-file.

    This is useful if you need to ensure the ordering of the
    filenames is consistent every time you load the data-set,
    for example if you use the DataSet-object in combination
    with Transfer Values saved to another cache-file, see e.g.
    Tutorial #09 for an example of this.

    :param cache_path:
        File-path for the cache-file.

    :param in_dir:
        Root-dir for the files in the data-set.
        This is an argument for the DataSet-init function.

    :return:
        The DataSet-object.
    """

    print("Creating dataset from the training files in " + train_dir + " and the testing files in " + test_dir)

    # If the object-instance for SignaturesDataset already
    # exists in the cache-file then reload it, otherwise create
    # an object instance and save it to the cache-file for next time.
    dataset = cache(cache_path=cache_path,
                    fn=SignaturesDataset,
                    train_dir=train_dir,
                    test_dir=test_dir)

    return dataset