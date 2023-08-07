import os
import dask.bag as db
import pandas as pd
from dask.diagnostics import ProgressBar
from DatasetGeneration.data_extract import DataExtract


class DataCreate:
    def __init__(self, file_path: str):
        self.data_extract = DataExtract()
        self.file_path = file_path
        self.folder_name = None

    def concatenate_paths(self, file_name):
        return os.path.join(self.file_path, file_name)

    def process_file(self, file_name):
        # Process the audio file and extract text and confidence using self.data_extract
        text, confidence = self.data_extract.speech_to_text(file_name)
        return {"text": text, "confidence": confidence}

    def create_dataset(self) -> list:
        """
        Creates the dataset from the file path provided
        :param folder_name: Name of the folder (train, test, validate)
        :return: dataset
        """
        dataset = []

        # List all audio files
        audio_files = list(
            filter(lambda f: not f.startswith(".DS_Store"), os.listdir(self.file_path))
        )

        concatenated_paths = list(map(self.concatenate_paths, audio_files))

        # Use Dask Bag to process the audio files concurrently
        bag = db.from_sequence(concatenated_paths)
        processed_data_bag = bag.map(self.process_file)

        # list all files from the bag

        # Combine the processed data into a single list
        processed_data_list = processed_data_bag.compute()

        for data in processed_data_list:
            dataset.append(data)

        self.folder_name = self.file_path.split("/")[-1]

        return dataset

    def save_dataset(self, dataset: list):
        # Save the dataset to CSV file
        df = pd.DataFrame(dataset, columns=["text", "confidence"])
        df.to_csv(
            f"ResultData/{self.folder_name}.csv", index=False
        )  # Check this where it saves


if __name__ == "__main__":
    file_path = os.listdir("Dataset")

    dataset_folders = list(filter(lambda f: not f.startswith(".DS_Store"), file_path))

    for folders in dataset_folders:
        file_path = os.path.join("Dataset", folders)

        if file_path == "Dataset/validate":
            data_create = DataCreate(file_path)

            with ProgressBar():
                df = data_create.create_dataset()
                data_create.save_dataset(df)
