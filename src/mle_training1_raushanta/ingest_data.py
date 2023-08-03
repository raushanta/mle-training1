"""Download data from URL or Load data from a local
csv file and split it into train and test set.
DataLoader can be used as a
base class for different downloading procedures. For a different
downloading procedure,
override the `_download_data` function. If download is set to False,
a raw csv infile must.
be present at 'input_path/infile'. You can either run this script
directly or use DataLoader.
class elsewhere to get train and test splits. When run as script,
train and test splits are.
stored at `output_path/train.csv' and `output_path/test.csv' respectively.
During split, data is .
shuffled and stratified based on `income_range` (see `_split` for more detail)
Run - `python ingest_data.py [-h | --help]`.
to get more information about the accepted arguments.
"""
import tarfile
from pathlib import Path
from typing import Optional, Tuple
from urllib import request
import numpy as np
import pandas as pd
import progressbar
from sklearn.model_selection import train_test_split as tts
class PBar:
    """Utility class to show the file download progress."""

    def __init__(self) -> None:
        self.pbar = None

    def __call__(self, block_num, block_size, total_size):
        if not self.pbar:
            self.pbar = progressbar.ProgressBar(maxval=total_size)
            self.pbar.start()
        downloaded = block_size * block_num
        if downloaded < total_size:
            self.pbar.update(downloaded)
        else:
            self.pbar.finish()
            self.pbar = None


class DataLoader:
    """Download a datafile or Load from disk and split it into train and test.
    This class can be used as a base class
    for loading and splitting other datafiles.
    and it does not provide any public interface.
    Attributes
    ----------
        input_path : str
            Path of the input directory to read infile
        output_path : str
            Path of the output directory to store train.csv and test.csv
        infile : str
            Name of the raw input csv datafile
        download : bool
            Whether file should be downloaded
            or loaded from `input_path/infile (default is False).
        test_size : float
            Portion of data to keep as test
            set - 0 < test_size < 0.5 (default is 0.2).
    """

    def __init__(
        self,
        input_path: str,
        output_path: str,
        infile: str,
        download: bool = False,
        test_size: float = 0.2,
    ) -> None:
        self.input_path = Path(input_path)
        self.output_path = Path(output_path)
        self.infile = infile
        self.download = download
        self.test_size = test_size

    def _download_data(self, url: str) -> None:
        """Download the data from a specified URL

        Download the data from a
        specified URL and if the data is in archive format.
        the archive file
        will be removed subsequently. Often you need override.
        this function
        in a child class to adapt as per your requirement.

        Parameters
        ----------
        url : str
            URL of the datafile as specified in config.ini
        """
        data_dir = self.input_path  # download in data/raw folder
        infile = data_dir / self.infile  # csv data file
        filepath = data_dir / "temp.tgz"  # temporary archive file
        data_dir.mkdir(exist_ok=True)
        logging.warning(
            f"Input directory {data_dir} created if not exists already"
        )

        if not infile.exists():
            request.urlretrieve(url, filepath, PBar())
            logging.info(f"Downloaded file to {filepath}")
            logging.info("Unzipping and removing the archive file")
            # Extract the archive file
            with tarfile.open(filepath, "r") as f:
                f.extractall(data_dir)
            filepath.unlink(missing_ok=True)
        else:
            logging.warning(f"{infile} already exists, file not downloaded")

    def _load_data(self) -> pd.DataFrame:
        """Load data located at input_path

        Returns
        -------
        pd.DataFrame

        Raises
        ------
        FileNotFoundError
            If infile is not located at the input_path
        """
        infile = self.input_path / self.infile
        try:
            df = pd.read_csv(infile)
            return df
        except FileNotFoundError:
            logging.error(
                f"{infile} does not exist, download = {self.download}"
            )
            raise FileNotFoundError(
                f"{infile} does not exist, set 'download = True'"
            )

    def _split(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Load and Split the dataset into Stratified Train and Test

        Data is stratified with respect to the income range,

        Returns
        -------
        Tuple[pd.DataFrame, pd.DataFrame]
            train and test dataframes
        """
        df = self._load_data()
        df["income_range"] = pd.cut(
            df["median_income"],
            [0, 1.5, 3, 4.5, 6, np.inf],
            labels=list(range(5)),
        )

        train, test = tts(
            df,
            test_size=self.test_size,
            random_state=43,
            shuffle=True,
            stratify=df["income_range"],
        )
        logging.info(
            f"Data shapes: original -
            {df.shape}, train - {train.shape}, test - {test.shape}"
        )
        train.drop(["income_range"], axis=1, inplace=True)
        test.drop(["income_range"], axis=1, inplace=True)
        return train, test

    def __call__(
        self, save_to_disk: bool = False, url: str = None
    ) -> Optional[Tuple[pd.DataFrame, pd.DataFrame]]:
        r"""Call the object class to ingest the dataset

        It performs following operations -
        Download the dataset (if `download = True`)
        Load the dataset located at `input_path` with name `infile`
        Split the dataset into train and test, optionally store train
        and test data at `output_path` or return them

        Parameters
        ----------
        save_to_disk : bool, optional
            Whether to save or return the splitted data, by default False
        url : str, optional
            URL of the file to download
            (specify only if `download = True`), by default None

        Returns
        -------
        Optional[Tuple[pd.DataFrame, pd.DataFrame]]
            train and test dataframes
        """
        if self.download:
            self._download_data(url)
        train, test = self._split()
        if save_to_disk:
            train_out = self.output_path / "train.csv"
            test_out = self.output_path / "test.csv"
            train.to_csv(train_out, index=False)
            test.to_csv(test_out, index=False)
            logging.info("train.csv and test.csv saved to disk")
            return

        return train, test


if __name__ == "__main__":
    import argparse
    import configparser
    import logging

    import setup

    # load default cmd arguments from config.ini file
    config = configparser.ConfigParser()
    config.read("config.ini")
    defaults = config["defaults"]

    # Setup Argument Parser
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Data Ingestion script -
        download, load, and split dataset into train and test.",
        epilog="Default arguments are stored in config.ini file.",
        fromfile_prefix_chars="@",
    )

    log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    parser.add_argument(
        "input_path",
        type=str,
        nargs="?",
        help="Path to store downloaded raw data file",
    )
    parser.add_argument(
        "output_path",
        type=str,
        nargs="?",
        help="Path to store processed data files",
    )
    parser.add_argument(
        "-i",
        "--infile",
        metavar="",
        type=str,
        help="Name of the raw data file to process",
    )
    parser.add_argument(
        "-lf", "--log_file", metavar="", type=str, help="Path to the log file"
    )
    parser.add_argument(
        "-ts",
        "--test_size",
        metavar="",
        type=float,
        help="Parameter for train_test_split",
    )
    parser.add_argument(
        "-l", "--level", type=str, choices=log_levels, help="Logging level"
    )
    parser.add_argument(
        "-d",
        "--download",
        action="store_true",
        help="Download the file if not already exists.",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Do not display console logs",
    )

    parser.set_defaults(**defaults)
    args = parser.parse_args()

    # setup logger
    logger = setup.setup_logging(
        args.level, args.quiet, args.log_file, __name__
    )

    # log command line arguments
    for arg, value in vars(args).items():
        logging.info(f"{arg.upper()} - {value}")

    data_loader = DataLoader(
        args.input_path,
        args.output_path,
        args.infile,
        args.download,
        args.test_size,
    )

    url = config["data_url"]["url"]  # load url from config.ini
    data_loader(save_to_disk=True, url=url)
