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
        self.dataset = []

    def process_file(self, file_name):
        text, confidence = self.data_extract.speech_to_text(file_name)
        return {"text": text, "confidence": confidence}

    def save_dataset_to_csv(self):
        df = pd.DataFrame(self.dataset, columns=["text", "confidence"])
        csv_filename = f"Dataset/result/{self.folder_name}.csv"
        df.to_csv(csv_filename, index=False)

    def create_and_save_chunk(self, chunk_paths):
        chunk_data_bag = db.from_sequence(chunk_paths)
        chunk_processed_data_bag = chunk_data_bag.map(self.process_file)
        chunk_processed_data_list = chunk_processed_data_bag.compute()
        self.dataset.extend(chunk_processed_data_list)

    def create_dataset(self):
        audio_files = [
            f for f in os.listdir(self.file_path) if not f.startswith(".DS_Store")
        ]

        concatenated_paths = [os.path.join(self.file_path, f) for f in audio_files]
        num_files = len(concatenated_paths)
        chunk_size = 1500  # Adjust as needed
        num_chunks = (num_files + chunk_size - 1) // chunk_size

        self.folder_name = self.file_path.split("/")[-1]

        for chunk_number in range(num_chunks):
            start_idx = chunk_number * chunk_size
            end_idx = min(start_idx + chunk_size, num_files)
            chunk_paths = concatenated_paths[start_idx:end_idx]

            self.create_and_save_chunk(chunk_paths)

        self.save_dataset_to_csv()


if __name__ == "__main__":
    dataset_folders = [
        f for f in os.listdir("Dataset") if not f.startswith(".DS_Store")
    ]

    ProgressBar().register()

    for folder in dataset_folders:
        file_path = os.path.join("Dataset", folder)
        if file_path == "Dataset/train" and file_path != "Dataset/result":
            data_create = DataCreate(file_path)
            df = data_create.create_dataset()
