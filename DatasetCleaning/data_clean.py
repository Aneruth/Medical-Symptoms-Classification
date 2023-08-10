import nltk
import os
import string
from helper import read_data


class DataClean:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = read_data(self.file_path)
        nltk.download("stopwords")
        self.stopwords = nltk.corpus.stopwords.words("english")

    def remove_punctuation(self) -> None:
        """
        Remove punctuation from the text
        :return: None
        """
        self.data["text"] = self.data["text"].apply(
            lambda x: "".join([i for i in x if i not in string.punctuation])
        )

    def remove_stopwords(self) -> None:
        """
        Remove stopwords from the text
        :return: None
        """
        self.data["text"] = self.data["text"].apply(
            lambda x: " ".join(
                [word for word in x.split() if word.lower() not in self.stopwords]
            )
        )

    def remove_numbers(self) -> None:
        """
        Remove numbers from the text
        :return: None
        """
        self.data["text"] = self.data["text"].apply(
            lambda x: "".join([i for i in str(x) if not i.isdigit()])
        )

    def remove_whitespace(self) -> None:
        """
        Remove whitespace from the text
        :return: None
        """
        self.data["text"] = self.data["text"].apply(lambda x: " ".join(x.split()))

    def remove_single_characters(self) -> None:
        """
        Remove single characters from the text
        :return: None
        """
        self.data["text"] = self.data["text"].apply(
            lambda x: " ".join([i for i in x.split() if len(i) > 1])
        )

    def lowercase_text(self) -> None:
        """
        Lowercase the text
        :return: None
        """
        self.data["text"] = self.data["text"].apply(lambda x: x.lower())

    def remove_non_ascii(self) -> None:
        """
        Remove non-ascii characters from the text
        :return: None
        """
        self.data["text"] = self.data["text"].apply(
            lambda x: "".join(i for i in x if ord(i) < 128)
        )

    def remove_extra_whitespace_tabs(self) -> None:
        """
        Remove extra whitespace and tabs from the text
        :return: None
        """
        self.data["text"] = self.data["text"].apply(lambda x: " ".join(x.split()))

    def remove_extra_newlines(self) -> None:
        """
        Remove extra newlines from the text
        :return: None
        """
        self.data["text"] = self.data["text"].apply(lambda x: x.replace("\n", ""))

    def remove_empty_string(self) -> None:
        """
        Remove empty strings text from the dataset by checking the confidence value
        if confidence value is 0 then remove the text
        :return: None
        """
        self.data = self.data[self.data["confidence"] != 0]

    def store_clean_data(self, folder_path: str) -> None:
        """
        Store the clean data to the csv file
        :return: None
        """
        root_folder = "/".join(os.path.abspath(__file__).split("/")[:-2])

        if not os.path.exists(root_folder + f"/{folder_path}"):
            os.makedirs(root_folder + f"/{folder_path}")

        datset_name = self.file_path.split("/")[-1].split(".")[0]
        self.data.to_csv(
            root_folder + f"/{folder_path}/clean_{datset_name}_data.csv", index=False
        )

    def consolidate_functions(self, folder_path: str) -> None:
        """
        Consolidate all the functions to clean the data in one function call
        :param folder_path: Path to store the clean data
        :return: None
        """
        self.remove_numbers()
        self.lowercase_text()
        self.remove_stopwords()
        self.remove_whitespace()
        self.remove_single_characters()
        self.remove_non_ascii()
        self.remove_extra_whitespace_tabs()
        self.remove_extra_newlines()
        self.remove_empty_string()
        self.remove_punctuation()
        self.store_clean_data(folder_path)


if __name__ == "__main__":
    for f in os.listdir("Dataset/result"):
        data_path = os.path.join(
            "/".join(os.path.abspath(__file__).split("/")[:-2]), f"Dataset/result/{f}"
        )
        data_clean = DataClean(data_path)
        data_clean.consolidate_functions("Dataset/clean_data")
