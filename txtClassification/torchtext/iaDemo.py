# Copyright (c) Facebook, Inc. and its affiliates.
import os
from functools import partial

# we import HttpReader from _download_hooks so we can swap out public URLs
# with interal URLs when the dataset is used within Facebook

from torchtext._internal.module_utils import is_module_available
from torchtext.data.datasets_utils import (
    _create_dataset_directory,
    _wrap_split_argument,
)
from torchdata.datapipes.iter import FileOpener

# Define the path to your local CSV files
_LOCAL_FILE_PATHS = {
    "train": "data/IA-demo/train.tsv",
    "dev": "data/IA-demo/dev.tsv",
    "test": "data/IA-demo/test.tsv",
}

DATASET_NAME = "iaDemo"


def _modify_test_res(t):
    return (t[1].strip(),)

def _modify_res(t):
    return t[0].strip(), int(t[1])

#@_wrap_split_argument(("train", "dev", "test"))
def iaDemo(split):
    """iaDemo Dataset

    Number of lines per split:
        - train: 
        - dev: 
        - test: 

    Args:
        split: split or splits to be returned. Can be a string or tuple of strings. Default: (`train`, `dev`, `test`)

    :returns: DataPipe that yields tuple of text and/or label (1 to 4). The `test` split only returns text.
    :rtype: Union[(int, str), (str,)]
    """
    # TODO Remove this after removing conditional dependency
    if not is_module_available("torchdata"):
        raise ModuleNotFoundError(
            "Package `torchdata` not found. Please install following instructions at https://github.com/pytorch/data"
        )

    # Define file paths for each split
    file_path = _LOCAL_FILE_PATHS[split]

    # Create data pipeline from local file
    data_dp = FileOpener([file_path], encoding="utf-8")

    # Parse CSV files, skipping the header
    if split == "test":
        parsed_data = data_dp.parse_csv(skip_lines=1, delimiter="\t").map(_modify_test_res)
    else:
        parsed_data = data_dp.parse_csv(skip_lines=1, delimiter="\t").map(_modify_res)

    return parsed_data.shuffle().set_shuffle(False).sharding_filter()

