import numpy as np
import pandas as pd


class DatasetGenerator:
    """Generates sample datasets with different distributions."""

    @staticmethod
    def generate_normal_distribution(size: int, mean: float = 0, std: float = 1) -> pd.DataFrame:
        """
        Generate a dataset with a normal distribution.

        Args:
            size (int): Number of samples.
            mean (float): Mean of the distribution. Defaults to 0.
            std (float): Standard deviation of the distribution. Defaults to 1.

        Returns:
            pd.DataFrame: A DataFrame containing the generated data.
        """
        data = np.random.normal(loc=mean, scale=std, size=size)
        return pd.DataFrame({"Normal Distribution": data})

    @staticmethod
    def generate_uniform_distribution(size: int, low: float = 0, high: float = 1) -> pd.DataFrame:
        """
        Generate a dataset with a uniform distribution.

        Args:
            size (int): Number of samples.
            low (float): Lower bound of the distribution. Defaults to 0.
            high (float): Upper bound of the distribution. Defaults to 1.

        Returns:
            pd.DataFrame: A DataFrame containing the generated data.
        """
        data = np.random.uniform(low=low, high=high, size=size)
        return pd.DataFrame({"Uniform Distribution": data})

    @staticmethod
    def generate_random_integers(size: int, low: int = 0, high: int = 100) -> pd.DataFrame:
        """
        Generate a dataset with random integers.

        Args:
            size (int): Number of samples.
            low (int): Lower bound of the integers. Defaults to 0.
            high (int): Upper bound of the integers. Defaults to 100.

        Returns:
            pd.DataFrame: A DataFrame containing the generated data.
        """
        data = np.random.randint(low=low, high=high, size=size)
        return pd.DataFrame({"Random Integers": data})
