import logging
from .bioretrieval.processing._processing_module import bio_retrieval_module


def run_model(
    input_folder_path: str,
    input_type: str,
    model_folder_path: str,
    conversion_factor: float,
    plot: bool = False,
):
    """
    This function runs the retrieval function.
    :param conversion_factor: image conversion factor
    :param input_folder_path: path to the input folder
    :param input_type: type of input file
    :param model_folder_path: path to the model folder
    :return: Shows completion message and is able to run again
    """
    logging.info("Running model.")

    message = bio_retrieval_module(
        input_folder_path,
        input_type,
        model_folder_path,
        conversion_factor,
        plot,
    )

    if message == 1:
        completion_message = "Something went wrong"
        logging.error(completion_message)
    elif message == 0:
        completion_message = "Model ran successfully"

    logging.info(completion_message)

    return completion_message
