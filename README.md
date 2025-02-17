# R AI

R AI is a simple command-line interface (CLI) application that interacts with the Hugging Face API to provide AI-generated responses to user prompts.

## Version

BETA 0.1.3

## Features

- Login with Hugging Face API key
- Send user prompts to the AI model and display responses

## Requirements

- Python 3.x
- Hugging Face Hub
- Colorama

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/rai.git
    cd rai
    ```

2. Install the required packages:
    ```sh
    pip install huggingface_hub colorama
    ```

## Usage

1. Run the application:
    ```sh
    python main.py
    ```

2. Enter your Hugging Face API key when prompted.

3. Interact with the AI by typing your prompts. Type `exit` or `quit` to exit the application.

## File Structure

- [main.py](http://_vscodecontentref_/0): The main script that contains the logic for logging in and interacting with the AI.

## License

This project is licensed under the MIT License.