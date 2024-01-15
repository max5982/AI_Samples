"""Demo based on ModelAPI."""
# Copyright (C) 2021-2022 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
#

import os
import sys
import cv2
import numpy as np
import importlib
import json

from argparse import SUPPRESS, ArgumentParser
from pathlib import Path

from openvino.model_api.adapters import OpenvinoAdapter, create_core
from openvino.model_api.models import ImageModel, Model

from otx.api.entities.model_template import TaskType
from otx.api.serialization.label_mapper import LabelSchemaMapper
from otx.api.utils.detection_utils import detection2array
from otx.api.usecases.exportable_code.demo.demo_package import SyncExecutor
from otx.api.usecases.exportable_code.demo.demo_package.utils import create_output_converter
from utils import get_model_path, get_parameters


def build_argparser():
    """Parses command line arguments."""
    parser = ArgumentParser(add_help=False)
    args = parser.add_argument_group("Options")
    args.add_argument(
        "-h",
        "--help",
        action="help",
        default=SUPPRESS,
        help="Show this help message and exit.",
    )
    args.add_argument(
        "-m",
        "--models",
        help="Optional. Path to directory with trained model and configuration file. "
        "If you provide several models you will start the task chain pipeline with "
        "the provided models in the order in which they were specified. Default value "
        "points to deployed model folder '../model'.",
        nargs="+",
        default=[Path("../model")],
        type=Path,
    )
    args.add_argument(
        "-d",
        "--device",
        help="Optional. Device to infer the model.",
        choices=["CPU", "GPU"],
        default="CPU",
        type=str,
    )

    return parser



def main():
    """Main function that is used to run demo."""
    args = build_argparser().parse_args()

    # create a model
    model_dir=args.models[0]
    model_adapter = OpenvinoAdapter(create_core(), get_model_path(model_dir / "model.xml"), device=args.device)
    parameters = get_parameters(model_dir / "config.json")
    labels = LabelSchemaMapper.backward(parameters["model_parameters"]["labels"])
    task_type = TaskType[parameters["converter_type"]]
    model_parameters = parameters["model_parameters"]
    model_parameters["labels"] = []
    confidence = model_parameters["confidence_threshold"]
    importlib.import_module("model_wrappers")

    core_model = Model.create_model(
        model_adapter,
        parameters["type_of_model"],
        model_parameters,
        preload=True,
    )

    inferencer = SyncExecutor
    converter = create_output_converter(task_type, labels, model_parameters)


    # Load image
    img = cv2.imread("sample.jpg", cv2.IMREAD_COLOR)
    if img is None:
        print(f"Can't read the image!")
        exit


    # Inference
    predictions = core_model(img)


    # Post Processing
    predictions = detection2array(predictions.objects)
    frame_meta = {"original_shape": img.shape}

    results = converter.convert_to_annotation(predictions, frame_meta)
    for annotation in results.annotations:
        probability = annotation.get_labels()[0].probability
        if probability > confidence:
            entity = annotation.shape
            name = annotation.get_labels()[0].name
            c = annotation.get_labels()[0].color
            print(f"name = {name}")
            print(f"entity = {entity}")

            x1, y1 = int(entity.x1 * img.shape[1]), int(entity.y1 * img.shape[0])
            x2, y2 = int(entity.x2 * img.shape[1]), int(entity.y2 * img.shape[0])
            img = cv2.rectangle(img=img, pt1=(x1, y1), pt2=(x2, y2), color=(c.red, c.green, c.blue, c.alpha), thickness=2)

    cv2.imshow("ret", img)
    cv2.waitKey(0)


if __name__ == "__main__":
    sys.exit(main() or 0)
