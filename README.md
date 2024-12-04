# Requirements Processor

This repository contains a script that reads content from all files in the `requirements` directory, sends the content to an Azure AI model for processing, and writes the model's response to corresponding output files.

## Features

- Reads content from all files in the `requirements` directory.
- Sends the content to an Azure AI model for processing.
- Writes the model's response to output files named after the original files with `_response.txt` appended.

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/ryano0oceros/ghmodels-demo.git
    cd ghmodels-demo
    ```

2. Set your GitHub personal access token as an environment variable:
    ```sh
    export GITHUB_TOKEN=your_personal_access_token
    ```

## Usage

1. Place your requirement files in the `requirements` directory.

2. Run the script:
    ```sh
    python3 prompt.py
    ```

3. The responses will be written to the `outputs` directory with filenames corresponding to the original files, appended with `_response.txt`.
