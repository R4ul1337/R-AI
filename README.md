# R AI

R AI is a command-line interface (CLI) application that interacts with the Hugging Face API to provide AI-generated responses to user prompts.

## Version

BETA 0.1.5 (release)

## Features

- Login with Hugging Face API key
- Send user prompts to the AI model and display responses

## Requirements

- Python 3.x
- Hugging Face Hub
- Colorama
- Cryptography, Fernet

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


# Future Updates
- Web APP
- More improved login system
- Better interface
- More AI Models added


# CHANGELOGS

## BETA 0.1.5 (release) Changelog
- New interface + logo/banner;
- Better Login system;
- Added a Changelog option to see the changelog of the version;
- Added a function that stores and encrypts users HF token, so you don't have to login every single time you open the app;
- Added a Logout feature that automatically deletes the saved token and logs you out of the app.

## BETA 0.1.4 Changelog
- New list of both Providers & AI Models. (NOTE: Not all the models currently work!!!);
- New design of input format + general text formatting & colors;
- Now the program will display your Hugging Face username in both title & in the input txt;
- When your chatting with a model, now you can see it's name above the response.
