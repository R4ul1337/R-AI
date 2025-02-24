from huggingface_hub import InferenceClient, HfApi
import os
import platform
import time
import colorama
import shutil
import json
from cryptography.fernet import Fernet
import random
import string

VERSION = "BETA 0.1.5 (release)"
username = "Not logged in"
info = f"{colorama.Fore.LIGHTBLUE_EX}[INFO] -> {colorama.Fore.RESET}"
e = f"{colorama.Fore.RED}[ERROR] -> {colorama.Fore.RESET}"

# Define color variables globally
green = colorama.Fore.GREEN
blue = colorama.Fore.BLUE
lred = colorama.Fore.LIGHTRED_EX
re = colorama.Fore.RESET

# Load or generate encryption key
def load_or_generate_key():
    try:
        key_file_path = 'data/encryption_key.key'
        if not os.path.exists('data'):
            os.makedirs('data')
        if os.path.exists(key_file_path):
            with open(key_file_path, 'rb') as key_file:
                key = key_file.read()
        else:
            key = Fernet.generate_key()
            with open(key_file_path, 'wb') as key_file:
                key_file.write(key)
        return key
    except Exception as ex:
        print(f"{e}Failed to load or generate key: {ex}")
        raise

key = load_or_generate_key()
cipher_suite = Fernet(key)

# General functions
def clear():
    try:
        if platform.system() == 'Windows':
            os.system('cls')
        else:
            os.system('clear')
    except Exception as ex:
        print(f"{e}Failed to clear screen: {ex}")

def title(title):
    global username
    try:
        if platform.system() == 'Windows':
            os.system(f'title R AI - {title} - {username} - {VERSION}')
        else:
            print(f"\033]0;R AI - {title} - {username} - {VERSION}\007")
    except Exception as ex:
        print(f"{e}Failed to set title: {ex}")

def save_preferences(remember_user):
    try:
        preferences = {
            "remember_user": remember_user
        }
        with open('data/prefs.json', 'w') as prefs_file:
            encrypted_prefs = cipher_suite.encrypt(json.dumps(preferences).encode())
            prefs_file.write(encrypted_prefs.decode())
    except Exception as ex:
        print(f"{e}Failed to save preferences: {ex}")

def load_preferences():
    try:
        if os.path.exists('data/prefs.json'):
            with open('data/prefs.json', 'r') as prefs_file:
                encrypted_prefs = prefs_file.read().encode()
                decrypted_prefs = cipher_suite.decrypt(encrypted_prefs).decode()
                return json.loads(decrypted_prefs)
        return None
    except Exception as ex:
        print(f"{e}Failed to load preferences: {ex}")
        return None

def save_token(api_key):
    try:
        temp_dir = os.getenv('TEMP')
        random_filename = ''.join(random.choices(string.ascii_letters + string.digits, k=16)) + '.enc'
        token_file_path = os.path.join(temp_dir, random_filename)
        encrypted_token = cipher_suite.encrypt(api_key.encode())
        with open(token_file_path, 'wb') as token_file:
            token_file.write(encrypted_token)
        with open('data/token_filename.txt', 'w') as filename_file:
            filename_file.write(random_filename)
    except Exception as ex:
        print(f"{e}Failed to save token: {ex}")

def load_token():
    try:
        if os.path.exists('data/token_filename.txt'):
            with open('data/token_filename.txt', 'r') as filename_file:
                random_filename = filename_file.read().strip()
            temp_dir = os.getenv('TEMP')
            token_file_path = os.path.join(temp_dir, random_filename)
            if os.path.exists(token_file_path):
                with open(token_file_path, 'rb') as token_file:
                    encrypted_token = token_file.read()
                    decrypted_token = cipher_suite.decrypt(encrypted_token).decode()
                    return decrypted_token
        return None
    except Exception as ex:
        print(f"{e}Failed to load token: {ex}")
        return None

def save_chat_history(model_name, chat_history):
    try:
        if not os.path.exists('data/chat_history'):
            os.makedirs('data/chat_history')
        date_str = time.strftime("%Y-%m-%d")
        file_name = f"{date_str}.json"
        file_path = os.path.join('data/chat_history', file_name)
        chat_data = {
            "model_name": model_name,
            "date": date_str,
            "time": time.strftime("%H:%M:%S"),
            "chat_history": chat_history
        }
        with open(file_path, 'w') as chat_file:
            encrypted_chat_data = cipher_suite.encrypt(json.dumps(chat_data).encode())
            chat_file.write(encrypted_chat_data.decode())
    except Exception as ex:
        print(f"{e}Failed to save chat history: {ex}")

def load_chat_history(file_name):
    try:
        file_path = os.path.join('data/chat_history', file_name)
        if os.path.exists(file_path):
            with open(file_path, 'r') as chat_file:
                encrypted_chat_data = chat_file.read().encode()
                decrypted_chat_data = cipher_suite.decrypt(encrypted_chat_data).decode()
                return json.loads(decrypted_chat_data)
        return None
    except Exception as ex:
        print(f"{e}Failed to load chat history: {ex}")
        return None

# Main functions
def login():
    global client, username

    try:
        title("Login")
        clear()
        api_key = load_token()
        if api_key:
            print(f"{info}Using saved token...\n")
            time.sleep(1.5)
        else:
            while True:
                print(f"{info}Please enter your Hugging Face API key to continue.\n")
                print(f"{info}Read 'HFAPI_FAQ.md' for a step-by-step tutorial!\n")
                api_key = input(f"{blue}HF API Key: {lred}{re}")
                if api_key == "":
                    print(f"{e}Invalid API key, please try again.\n")
                else:
                    break

        clear()
        print(f"{info}Logging in...\n")
        client = InferenceClient(
            provider="hf-inference",
            api_key=api_key
        )
        print(f"{info}{green}Login successful.{re}\n")
        
        # Fetch and store the user's username
        api = HfApi()
        user_info = api.whoami(token=api_key)
        username = user_info['name']
        print(f"{info}Logged in as: {lred}{username}{re}\n")
        time.sleep(2)
        remember_user = input(f"{info}Do you want to be remembered? (BETA, !choosing 'no' won't work!) (yes/no): ").strip().lower()
        if remember_user == 'yes':
            save_token(api_key)
            save_preferences(True)
        else:
            save_preferences(False)

        return api_key
    except Exception as ex:
        print(f"{e}Failed to login: {ex}")
        return None

def model_select(provider, operation):
    try:
        title("Model Selection")
        clear()
        
        def printModels():
            if provider == "mistralai":
                models = [
                    "mistralai/Mistral-7B-Instruct-v0.2",
                    "mistralai/Mistral-Nemo-Instruct-2407",
                    "mistralai/Mistral-Small-24B-Instruct-2501 (This model is not yet implemented.)"
                ]
            elif provider == "deepseek":
                models = [
                    "deepseek-ai/DeepSeek-V3 (This model is not yet implemented.)",
                    "deepseek-ai/deepseek-llm-67b-chat (This model is not yet implemented.)",
                    "deepseek-ai/DeepSeek-R1-Distill-Llama-70B (This model is not yet implemented.)"
                ]
            elif provider == "qwen":
                models = [
                    "Qwen/Qwen2.5-VL-72B-Instruct (This model is not yet implemented.)",
                    "Qwen/Qwen2-VL-72B-Instruct (This model is not yet implemented.)",
                    "Qwen/Qwen2-VL-7B-Instruct (This model is not yet implemented.)"
                ]
            else:
                models = []

            print("Available Models:\n")
            for i, model in enumerate(models):
                print(f"[{i+1}] {model}")
            print("[99] Quit")
            print("[0] Back")

            return models

        models = printModels()
        if operation == "print":
            return
        elif operation == "select":
            while True:
                choice = input(f"\n{info}Select a model by number: ")
                if choice.isdigit() and 1 <= int(choice) <= len(models):
                    selected_model = models[int(choice) - 1]
                    if "This model is not yet implemented." in selected_model:
                        print(f"{e}This model is not yet implemented. Please select another model.{re}")
                    else:
                        return selected_model
                elif choice == '99':
                    print(f"{info}Exiting...")
                    exit()
                elif choice == '0':
                    return None
                else:
                    print(f"{e}Invalid choice, please try again.")
    except Exception as ex:
        print(f"{e}Failed to select model: {ex}")
        return None

def provider_select(operation):
    try:
        title("Provider Selection")
        clear()
        print("Available Providers:\n")
        providers = ["mistralai", "deepseek", "qwen"]
        for i, provider in enumerate(providers):
            print(f"[{i+1}] {provider}")
        print("[99] Quit")
        if operation == "print":
            return
        while True:
            choice = input(f"\n{info}Select a provider by number: ")
            if choice.isdigit() and 1 <= int(choice) <= len(providers):
                return providers[int(choice) - 1]
            elif choice == '99':
                print(f"{info}Exiting...")
                exit()
            else:
                print(f"{e}Invalid choice, please try again.")
    except Exception as ex:
        print(f"{e}Failed to select provider: {ex}")
        return None

def delete_token():
    try:
        if os.path.exists('data/token_filename.txt'):
            with open('data/token_filename.txt', 'r') as filename_file:
                random_filename = filename_file.read().strip()
            temp_dir = os.getenv('TEMP')
            token_file_path = os.path.join(temp_dir, random_filename)
            if os.path.exists(token_file_path):
                os.remove(token_file_path)
            os.remove('data/token_filename.txt')
        print(f"{info}Logged out successfully.")
    except Exception as ex:
        print(f"{e}Failed to delete token: {ex}")

def main():
    global username, client

    try:
        # Create data directory if it doesn't exist
        if not os.path.exists('data'):
            os.makedirs('data')

        while True:
            preferences = load_preferences()
            if preferences and preferences.get("remember_user"):
                api_key = load_token()
                if api_key:
                    client = InferenceClient(
                        provider="hf-inference",
                        api_key=api_key
                    )
                    api = HfApi()
                    user_info = api.whoami(token=api_key)
                    username = user_info['name']
            else:
                api_key = None

            def textCenter(txt):
                terminal_width = shutil.get_terminal_size().columns
                art_lines = txt.splitlines()
                max_length = max(len(line) for line in art_lines)
                padding_left = (terminal_width - max_length) // 2
                for line in art_lines:
                    print(' ' * padding_left + line)

            bannerText = """\n\n██████╗          █████╗ ██╗
██╔══██╗        ██╔══██╗██║
██████╔╝        ███████║██║
██╔══██╗        ██╔══██║██║
██║  ██║        ██║  ██║██║
╚═╝  ╚═╝        ╚═╝  ╚═╝╚═╝\n\n\n"""
            clear()
            title("Main")

            if api_key:
                while True:
                    textCenter(bannerText)
                    print(f"{lred}[1] {re}{blue}Select AI Model{re}")
                    print(f"{lred}[2] {re}{blue}Switch to WEB APP (COMING SOON){re}")
                    print(f"{lred}[!] {re}{blue}Logout{re}")
                    print(f"{lred}[99] {re}{blue}Quit{re}")
                    print(f"{lred}[?] {re}{blue}Changelog{re}")
                    choice = input(f"\n{info}Select an option by number: ")
                    if choice == '1':
                        provider = provider_select(operation="select")
                        model_name = model_select(provider, operation="select")
                        if model_name is None:
                            continue
                        clear()
                        chat_history = []
                        while True:
                            prompt = input(f"--({colorama.Fore.LIGHTMAGENTA_EX}{model_name}{re}) - ({lred}!{blue}PRESS CTRL + C TO QUIT{lred}!{re})\n|--({colorama.Fore.RED}{username}{re}) -> ")
                            if prompt.lower() in ["exit", "quit"]:
                                print("Exiting...")
                                break
                            messages = [
                                {
                                    "role": "user",
                                    "content": f"{prompt}"
                                }
                            ]
                            completion = client.chat.completions.create(
                                model=model_name, 
                                messages=messages, 
                                max_tokens=500,
                            )
                            # Extract and print only the content of the message
                            response_content = completion.choices[0].message.content
                            print(f"\n\n--({colorama.Fore.LIGHTMAGENTA_EX}{model_name}{re})\n|--({colorama.Fore.RED}AI RESPONSE{re}) -> {response_content}\n\n")
                            chat_history.append({"user": prompt, "ai_response": response_content})
                        save_chat_history(model_name, chat_history)
                    elif choice == '2':
                        print(f"{info}A Web APP of R AI is coming soon! :)")
                        input(f"\nPress Enter to continue...")
                        clear()
                        continue
                    elif choice == '!':
                        delete_token()
                        api_key = None
                        clear()
                        break
                    elif choice == '99':
                        print(f"{info}Exiting...")
                        exit()
                    elif choice == '?':
                        print(f"\n{lred}{VERSION} {re}Changelog\n\n{green}- Whole new interface\n- Better login system\n- Added a changelog\n- Added a remember user feature\n- Added a logout feature{re}\n\n{blue}(BETA 0.1.4 ~ 162 lines of code, BETA 0.1.5 ~ 436 lines of code){re}")
                        input(f"\nPress Enter to continue...")
                        clear()
                        continue
                    else:
                        print(f"{e}Invalid choice, please try again.")
                        time.sleep(2)
                        clear()
                        continue
            else:
                while True:
                    textCenter(bannerText)
                    print(f"{lred}[1] {re}{blue}Login{re}(With Hugging Face API Key)")
                    print(f"{lred}[2] {re}{blue}See Providers List{re}")
                    print(f"{lred}[3] {re}{blue}See AI Models List{re}")
                    print(f"{lred}[99] {re}{blue}Quit{re}")
                    choice = input(f"\n{info}Select an option by number: ")
                    if choice == '1':
                        api_key = login()
                        if api_key:
                            client = InferenceClient(
                                provider="hf-inference",
                                api_key=api_key
                            )
                            api = HfApi()
                            user_info = api.whoami(token=api_key)
                            username = user_info['name']
                            clear()
                            break
                    elif choice == '2':
                        provider_select(operation="print")
                        input(f"\nPress Enter to continue...")
                        clear()
                        continue
                    elif choice == '3':
                        provider = provider_select(operation="select")
                        model_select(provider, operation="print")
                        input(f"\nPress Enter to continue...")
                        clear()
                        continue
                    elif choice == '99':
                        print(f"{info}Exiting...")
                        exit()
                    else:
                        print(f"{e}Invalid choice, please try again.")
                        time.sleep(2)
                        clear()
                        continue

    except Exception as ex:
        print(f"{e}An error occurred in the main function: {ex}")

if __name__ == "__main__":
    main()