from idmd.data.generator import DatasetGenerator


def test_generate_normal_distribution_logic():
    """Test that the normal distribution generator creates data with expected properties."""
    df = DatasetGenerator.generate_normal_distribution(size=(1000, 5), mean=5, std=2)
    assert len(df) == 1000, "The generated dataset should have 1000 rows."
    assert "Normal Distribution" in df.columns, "The dataset should contain a column named 'Normal Distribution'."
    assert abs(df["Normal Distribution"].mean() - 5) < 0.5, "The mean should be close to 5."
    assert abs(df["Normal Distribution"].std() - 2) < 0.5, "The standard deviation should be close to 2."


def test_generate_random_integers_logic():
    """Test that the random integer generator creates data within the specified range."""
    df = DatasetGenerator.generate_random_integers(size=(500, 3), low=10, high=20)
    assert len(df) == 500, "The generated dataset should have 500 rows."
    assert "Random Integers" in df.columns, "The dataset should contain a column named 'Random Integers'."
    assert df["Random Integers"].min() >= 10, "All values should be greater than or equal to the lower bound."
    assert df["Random Integers"].max() < 20, "All values should be less than the upper bound."


def test_generate_uniform_distribution_logic():
    """Test that the uniform distribution generator creates data within the specified range."""
    df = DatasetGenerator.generate_uniform_distribution(size=(500, 7), low=0, high=10)
    assert len(df) == 500, "The generated dataset should have 500 rows."
    assert "Uniform Distribution" in df.columns, "The dataset should contain a column named 'Uniform Distribution'."
    assert df["Uniform Distribution"].min() >= 0, "All values should be greater than or equal to the lower bound."
    assert df["Uniform Distribution"].max() < 10, "All values should be less than the upper bound."
