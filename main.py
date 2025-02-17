from huggingface_hub import InferenceClient, HfApi
import os
import platform
import time
import colorama

VERSION = "BETA 0.1.3"
username = "Not logged in"

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
    green = colorama.Fore.GREEN
    blue = colorama.Fore.BLUE
    light_red = colorama.Fore.LIGHTRED_EX
    re = colorama.Fore.RESET
    title("Login")
    clear()
    print(f"{green}R AI Successfully Loaded{re}\n\n")
    while True:
        print("Please enter your Hugging Face API key to continue.\n")
        api_key = input(f"{blue}HF API Key: {light_red}{re}")
        if api_key == "":
            print("Invalid API key, please try again.\n")
        else:
            break
    print("Logging in...\n")
    client = InferenceClient(
        provider="hf-inference",
        api_key=api_key
    )
    print(f"{green}Login successful.{re}\n")
    
    # Fetch and store the user's username
    api = HfApi()
    user_info = api.whoami(token=api_key)
    username = user_info['name']
    print(f"Logged in as: {light_red}{username}{re}\n")
    
    time.sleep(2)
    print("Redirecting...")
    time.sleep(1.5)
    return api_key

def fetch_models(api_key):
    api = HfApi()
    models = api.list_models(author=username)
    return models

def model_select(api_key):
    title("Model Selection")
    clear()
    models = fetch_models(api_key)
    print("Available Models:\n")
    for i, model in enumerate(models):
        print(f"[{i+1}] {model.modelId}")
    print("[99] Quit")
    while True:
        choice = input("\nSelect a model by number: ")
        if choice.isdigit() and 1 <= int(choice) <= len(models):
            return models[int(choice) - 1].modelId
        elif choice == '99':
            print("Exiting...")
            exit()
        else:
            print("Invalid choice, please try again.")

def main():
    api_key = login()
    clear()
    title("Main")
    model_name = model_select(api_key)
    while True:
        prompt = input("\nYou: ")
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
        print(f"\n\nAI: {response_content}")

if __name__ == "__main__":
    main()