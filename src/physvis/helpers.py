from pathlib import Path
import pandas as pd

naming_columns = ['participant','physicalisation','orientation','condition','cube', 'h', 'o', 'g', 'x', 'y']

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

def get_large_csv(input_path: str, delimiter: str = ";", index_col: list = naming_columns[:5]) -> pd.DataFrame:
    """Get the large .csv as a DataFrame (must have created it first using collect())
    Args:
        path: the path from user in any format (relative, absolute, etc.)
    Returns:
        A pandas dataframe
    """
    frame = pd.read_csv(input_path, index_col=index_col, header=0, delimiter=delimiter, keep_default_na=False)
    frame.sort_index()
    frame = frame.apply(pd.to_numeric, errors='ignore')
    return frame

def get_heatmap_csv(input_path: str, delimiter: str = ";", index_col: list = ['physicalisation']) -> pd.DataFrame:
    """Get the large .csv as a DataFrame (must have created it first using collect())
    Args:
        path: the path from user in any format (relative, absolute, etc.)
    Returns:
        A pandas dataframe
    """
    frame = pd.read_csv(input_path, index_col=index_col, header=0, delimiter=delimiter)
    frame = frame.apply(pd.to_numeric, errors='ignore')
    return frame
