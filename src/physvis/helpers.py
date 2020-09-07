def create_output_folder(output_path: str) -> Path:
    """Creates a path to store output data if it does not exists.
    Args:
        path: the path from user in any format (relative, absolute, etc.)
    Returns:
        A path to store output data.
    """
    path = Path(output_path)
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
    return path

def get_large_csv(input_path: str, delimiter: str = ";") -> pd.DataFrame:
    """Get the large .csv as a DataFrame (must have created it first using collect())
    Args:
        path: the path from user in any format (relative, absolute, etc.)
    Returns:
        A pandas dataframe
    """
    frame = pd.read_csv(input_path, index_col=naming_columns[:5], header=0, delimiter=delimiter, keep_default_na=False)
    frame.sort_index()
    return frame
