import os
import pandas as pd
from DatasetGeneration.data_extract import DataExtract


class DataCreate:
    def __init__(self, file_path: str, batch_size: int):
        self.data_extract = DataExtract()
        self.file_path = file_path
        self.batch_size = batch_size

    def create_dataset(self) -> pd.DataFrame:
        """
        Creates the dataset from the file path provided
        :return: dataset
        """
        # list all audio files
        audio_files = list(
            filter(lambda f: not f.startswith(".DS_Store"), os.listdir(self.file_path))
        )
        print("Total audio files: ", len(audio_files))

        def concatenate_paths(file_name):
            return os.path.join(self.file_path, file_name)

        concatenated_paths = list(map(concatenate_paths, audio_files))
        print("Concatenated paths: ", concatenated_paths)

        # list all files from the concatenated paths
        # TODO: Implement this using dask bag and create a dataframe for
        # train, test and validation


if __name__ == "__main__":
    file_path = "Dataset"
    batch_size = 500
    data_create = DataCreate(file_path, batch_size)
    data_create.create_dataset()
