from huggingface_hub import InferenceClient, HfApi
import os
import platform
import time
import colorama

VERSION = "BETA 0.1.4"
username = "Not logged in"
info = f"{colorama.Fore.LIGHTBLUE_EX}[INFO] -> {colorama.Fore.RESET}"
e = f"{colorama.Fore.RED}[ERROR] -> {colorama.Fore.RESET}"

# General functions
def clear():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def title(title):
    global username
    if platform.system() == 'Windows':
        os.system(f'title R AI - {title} - {username} - {VERSION}')
    else:
        print(f"\033]0;R AI - {title} - {username} - {VERSION}\007")

# Main functions
def login():
    global client, username
    global green, blue, light_red, re

    green = colorama.Fore.GREEN
    blue = colorama.Fore.BLUE
    light_red = colorama.Fore.LIGHTRED_EX
    re = colorama.Fore.RESET

    title("Login")
    clear()
    print(f"{info}{green}R AI Successfully Loaded{re}\n\n")
    while True:
        print(f"{info}Please enter your Hugging Face API key to continue.\n")
        api_key = input(f"{blue}HF API Key: {light_red}{re}")
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
    print(f"{info}Logged in as: {light_red}{username}{re}\n")
    
    time.sleep(2)
    print(f"{info}Redirecting...")
    time.sleep(1.5)
    return api_key

def model_select(provider):
    title("Model Selection")
    clear()
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

def provider_select():
    title("Provider Selection")
    clear()
    print("Available Providers:\n")
    providers = ["mistralai", "deepseek", "qwen"]
    for i, provider in enumerate(providers):
        print(f"[{i+1}] {provider}")
    print("[99] Quit")
    while True:
        choice = input(f"\n{info}Select a provider by number: ")
        if choice.isdigit() and 1 <= int(choice) <= len(providers):
            return providers[int(choice) - 1]
        elif choice == '99':
            print(f"{info}Exiting...")
            exit()
        else:
            print(f"{e}Invalid choice, please try again.")

def main():
    global username
    global green, blue, light_red, re

    api_key = login()
    clear()
    title("Main")
    while True:
        provider = provider_select()
        model_name = model_select(provider)
        if model_name is None:
            continue
        clear()
        while True:
            prompt = input(f"--({colorama.Fore.LIGHTMAGENTA_EX}{model_name}{re}) - ({light_red}!{blue}PRESS CTRL + C TO QUIT{light_red}!{re})\n|--({colorama.Fore.RED}{username}{re}) -> ")
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

if __name__ == "__main__":
    main()