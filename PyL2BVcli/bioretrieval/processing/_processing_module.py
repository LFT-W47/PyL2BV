"""
This file contains the function to start the retrieval module of BioRetrieval.
This includes making initial tests, creating output folder and running the retrieval function.
"""

import logging
import os
from datetime import datetime
from shutil import copyfile, rmtree

from ..auxiliar._logger_class import Logger
from ._retrieval import Retrieval

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def bio_retrieval_module(
    input_folder_path: str,
    input_type: str,
    model_folder_path: str,
    conversion_factor: float,
    plot: bool = False,
):
    """
    Bio Retrieval module for ARTMO based models:
     LEO-IPL - University of Valencia. June 2024.
     by Mészáros Viktor Ixion

    This function reads all the files in the folder input_folder_path and
    reads the indicated input_type than starts the retrieval process with the models
    specified in model_folder_path.
    Parameters:
    :type conversion_factor: conversion factor for the retrieval
    :param input_folder_path: path to folder containing input files
    :param input_type: type of input files
    :param model_folder_path: path to folder containing model files
    :return: 0 if successful, 1 if not successful
    """

    # __________________________Construct variables___________________________
    # Create output path
    input_path = os.path.abspath(input_folder_path)  # Create a path object
    path_components = input_path.split(os.sep)  # Split the path into its components
    path_components[-1] = "output"  # Replace last part with output
    output_path = os.sep.join(path_components)  # Join the path components back together

    # Create logfile path
    logfile_path = os.path.join(output_path, "logfile.log")

    # __________________________Split processing by file type_________________

    if input_type == "CHIME netCDF":
        logging.info(f"Processing input type: {input_type}")

        # Check input files, log if number of files are not correct
        list_of_files = os.listdir(input_path)
        # Filter files with .nc extension
        nc_files = [file for file in list_of_files if file.endswith(".nc")]
        try:
            if len(nc_files) % 4 != 0 or not list_of_files:
                # If output folder exists, delete it and make a new one
                make_output_folder(output_path)
                raise FileNotFoundError("Missing input nc file.")
        except Exception as e:
            logging.error(f"Error: {e}")
            with open(logfile_path, "w") as fileID:
                fileID.write(
                    "FAIL: Wrong number of inputs or error loading input image."
                    " Consider checking Input Path/File \n"
                )
                fileID.write(f"Input Path: {input_path} \n")
            return 1

        # Counting input files
        pos_img_files = [i for i, name in enumerate(nc_files) if "IMG" in name]
        num_images = len(pos_img_files)  # Number of image files
        input_files = [os.path.join(input_path, nc_files[i]) for i in pos_img_files]
        input_names = [nc_files[i] for i in pos_img_files]

        # Concatenate the name of output files
        l2b_output = os.path.join(output_path, "CHI_E2ES_PRO_L2VIMG_")
        # If output folder exists, delete it and make a new one
        flag_out = make_output_folder(output_path)

        # Generate processing time
        proces_time = datetime.now().strftime("%Y%m%dT%H%M%SZ")
        l2b_output_files = []  # Collecting the output filenames here

        # Process input files, copy GEO, QUA
        for i in range(num_images):
            input_file_name = input_names[i]
            # Configuration works for CHIME image name convention now
            pos = [j for j, char in enumerate(input_file_name) if char == "_"]
            scene_time = input_file_name[pos[3] + 1 : pos[4]]
            tile = input_file_name[pos[5] + 1 :]
            l2b_output_files.append(f"{l2b_output}{scene_time}_{proces_time}_{tile}")

            try:
                input_file_geo = input_files[i].replace("IMG", "GEO")
                l2b_output_file_geo = l2b_output_files[i].replace("IMG", "GEO")
                copyfile(input_file_geo, l2b_output_file_geo)
                input_file_qua = input_files[i].replace("IMG", "QUA")
                l2b_output_file_qua = l2b_output_files[i].replace("IMG", "QUA")
                copyfile(input_file_qua, l2b_output_file_qua)
            except FileNotFoundError as e:
                logging.error(f"Error: {e}")
                with open(logfile_path, "w") as fileID:
                    fileID.write(
                        "FAIL: Missing complementary files for CHIME image."
                        " Consider checking Input Path/File \n"
                    )
                    fileID.write(f"Input Path: {input_path} \n")
                return 1
            except Exception as e:
                logging.error(f"Unexpected error: {e}")
                with open(logfile_path, "w") as fileID:
                    fileID.write(
                        "FAIL: An unexpected error occurred."
                        " Consider checking Input Path/File \n"
                    )
                    fileID.write(f"Input Path: {input_path} \n")
                return 1

    elif input_type == "ENVI Standard":
        logging.info(f"Processing input type: {input_type}")

        # Check input files, log if number of files are not correct
        list_of_files = os.listdir(input_path)
        # Filter files with .hdr extension
        hdr_files = [file for file in list_of_files if file.endswith(".hdr")]
        try:
            if not list_of_files:
                # If output folder exists, delete it and make a new one
                if os.path.exists(output_path):
                    rmtree(output_path)
                    os.makedirs(output_path)
                else:
                    os.makedirs(output_path)
                raise FileNotFoundError("Missing input hdr file.")
        except Exception as e:
            logging.error(f"Error: {e}")
            with open(logfile_path, "w") as fileID:
                fileID.write(
                    "FAIL: Wrong number of inputs or error loading input file."
                    " Consider checking Input Path/File \n"
                )
                fileID.write(f"Input Path: {input_path} \n")
            return 1

        # Counting input files
        num_images = len(hdr_files)  # Number of image files
        input_files = [
            os.path.join(input_path, hdr_files[i]) for i in range(num_images)
        ]
        input_names = [
            os.path.splitext(os.path.basename(hdr_files[i]))[0]
            for i in range(num_images)
        ]

        # Generate processing time
        proces_time = datetime.now().strftime("%Y%m%dT%H%M%SZ")
        # Collecting the output filenames here
        l2b_output_files = [
            os.path.join(output_path, f"{input_names[i]}_{proces_time}")
            for i in range(num_images)
        ]
        # Create output folder
        flag_out = make_output_folder(output_path)
    else:
        logging.error("Invalid input format")
        return 1

    # ____________________________________Retrieval________________________________

    # Biophysical parameters retrieval
    for i in range(num_images):
        img_name = os.path.basename(l2b_output_files[i])
        log_path = os.path.splitext(l2b_output_files[i])[0]
        log_file_id = Logger(log_path)
        if i == 0:
            # Log information to logfile
            if flag_out:
                logging.info("Output folder already exists. Folder was overwritten.")
                log_file_id.log_message(
                    "Output folder already exists. Folder was overwritten.\n"
                )
            else:
                logging.info("Output folder does not exist. Folder was created.")
                log_file_id.log_message(
                    "Output folder does not exist. Folder was created.\n"
                )

        # Log image information
        logging.info(f"Processing tile: {img_name}")
        log_file_id.log_message(f"Tile: {img_name}\n")
        log_file_id.close()

        # Creating Retrieval object and call function
        retrieval_object = Retrieval(
            log_file_id,
            input_files[i],
            input_type,
            l2b_output_files[i],
            model_folder_path,
            conversion_factor,
            plot,
        )

        return_value = retrieval_object.bio_retrieval
        if return_value == 1:  # There was an error
            logging.error(f"Error during retrieval of {img_name}")
            return 1
        else:
            export_value = retrieval_object.export_retrieval()
            if export_value == 1:  # There was an error
                logging.error(f"Error during export of {img_name}")
                return 1

        logging.info(f"Retrieval of {img_name} successful.")
        with open(f"{log_path}_logfile.log", "a") as log_file_id:
            log_file_id.write(f"Retrieval of {img_name} successful.\n")
    return 0


def make_output_folder(output_path: str) -> bool:
    """
    Create output folder
    :param output_path: path of output folder
    :return: flag: 1 if overwritten, 0 if not
    """
    if os.path.exists(output_path):
        rmtree(output_path)
        os.makedirs(output_path)
        logging.info(
            f"Output folder {output_path} already existed and was overwritten."
        )
        return True
    else:
        os.makedirs(output_path)
        logging.info(f"Output folder {output_path} was created.")
        return False
