from pandas import DataFrame


class Dataset:
    """
    This class represents a dataset

    Attributes
    ----------
    name : str | None
        an optional name given by the user
    dataset : DataFrame
        the actual dataset as a pandas DataFrame
    """

    def __init__(self, name: str | None, dataset: DataFrame):
        self.name = name
        self.dataset = dataset
