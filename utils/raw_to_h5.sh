#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

# this is version 1.4.0 of ThermoRawFileParser:
raw_image='quay.io/biocontainers/thermorawfileparser@sha256:76c17e3124b723f271bc3d5cf0555650288676bb1a827bd1bae9bb684444a404'

if [ "$#" -ne 1 ]; then
    >&2 echo "Usage $0: raw_ms_file"
    exit 128
fi

raw_file="$(realpath "$1")"

validation="\
import logging
from pathlib import Path
from metatlas.tools.validate_filenames import validate_file_name
logging.basicConfig(format='%(levelname)s, %(message)s', level=logging.INFO)
assert validate_file_name(Path('${raw_file}'), minimal=True)"
# the above "minimal=True" should be set to False once raw file names are expected to
# be fully in agreement with the SOP

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

shifter "--env=PYTHONPATH=/src" "--image=doejgi/metatlas_shifter:latest" \
        python -c "$validation" 2>&1 | \
	"${SCRIPT_DIR}/ts.py"

# ThermoRawFileParser.sh should return non-zero exit code on error, but it doesn't
# https://github.com/compomics/ThermoRawFileParser/issues/140
# But the mzML to h5 conversion will fail nicely if the mzML files does not exist
shifter "--image=${raw_image}" ThermoRawFileParser.sh \
	"-i=${raw_file}" "-o=$(dirname "$raw_file")" -f=1 2>&1 | \
	sed 's%^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} INFO%INFO ThermoRawFileParser:%' | \
	"${SCRIPT_DIR}/ts.py"

mzml_file="${raw_file%.raw}.mzML"

mzml_to_h5="\
from metatlas.io.file_converter import mzml_to_h5_and_add_to_db
mzml_to_h5_and_add_to_db('${mzml_file}')"

shifter "--env=PYTHONPATH=/src" "--image=doejgi/metatlas_shifter:latest" \
        python -c "$mzml_to_h5" | \
	"${SCRIPT_DIR}/ts.py"
