#!/usr/bin/python

"""
    A wrapper script for containerized bfconvert.
    The shebang used is dependent on the container setup.
"""

import time
import os
import sys
import subprocess
import json


def print_current_time(message=None):
    """
        Prints current time.
    :param message: optional message to show
    :return: none
    """
    current_time = time.strftime('%Y-%m-%d %H:%M:%S %Z', time.localtime(time.time()))
    if message is None:
        print(current_time)
    else:
        print(current_time + " " + message)


def print_check_run_info(run):
    """
        Print and checks run result.
    :param run: subprocess.run object
    """
    print("STDOUT------")
    print(run.stdout)
    print("STDERR------")
    print(run.stderr)
    run.check_returncode()


def sample_convert(inputs, output_dir):
    """
        Given input raw image full paths, convert and write to output_dir.
    :param inputs: input raw image absolute paths, JSON string
    :param output_dir: output directory absolute path
    :return: none
    """
    original_names = [os.path.split(inp)[1] for inp in inputs]
    output_names = [os.path.splitext(original)[0] for original in original_names]
    output_names = [outname + ".ome.tif" for outname in output_names]
    output_paths = [os.path.join(output_dir, outname) for outname in output_names]
    os.mkdir(output_dir)
    for i in range(len(inputs)):
        in_path = inputs[i]
        out_path = output_paths[i]
        print_current_time("Running conversion for " + in_path)
        run = subprocess.run(["bfconvert", "-no-upgrade", in_path, out_path], capture_output=True)
        print_check_run_info(run)
        print_current_time("Done conversion")


if __name__ == "__main__":
    #   First, parse parameters
    arg_total = len(sys.argv)
    if len(sys.argv) != 2:
        raise ValueError("USAGE: bfconvert.py <inputs_list> <output_directory>")
    try:
        inputs = json.loads(sys.argv[0])
    except:
        raise ValueError("<inputs_list> must be JSON string.")
    output_dir = sys.argv[1]
    #   Next, check existence of claimed inputs and output directory
    inputs_check = [os.path.exists(i) for i in inputs]
    outdir_check = os.path.exists(output_dir)
    if outdir_check is False:
        raise ValueError("Output directory does not exist")
    if not all(inputs_check):
        raise ValueError("Not all inputs exist")
    #   Next, call the real work function
    sample_convert(inputs, output_dir)
else:
    raise ValueError("bfconvert wrapper script must be called from shell directly.")
