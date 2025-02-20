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

2. Set your environment variables:
    ```sh
    export AZURE_ENDPOINT=your_azure_ai_inference_endpoint
    export AZURE_KEY=azure_foundry_api_key_1
    ```

## Usage

1. Place your requirement files in the `requirements` directory.

2. Update the standard prompt in the root directory, feed specific prompts into the requirements directory.

2. Run the script:
    ```sh
    python3 prompt.py
    ```

3. The responses will be written to the `outputs` directory with filenames corresponding to the original files, appended with `_response.txt`.
