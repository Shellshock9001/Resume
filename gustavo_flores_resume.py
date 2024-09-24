import random
import base64
from colorama import init, Fore, Style
import subprocess
import time

"""
Dependencies:
- Python 3.x: Ensure Python 3 is installed.
- colorama: Install via pip using 'pip install colorama'
- mpv (media player): Install via your package manager:
    - On Ubuntu/Debian: 'sudo apt install mpv'
    - On Fedora: 'sudo dnf install mpv'
    - On Arch: 'sudo pacman -S mpv'
    - On macOS: 'brew install mpv' (using Homebrew)
"""

# Initialize Colorama for colored grid output
init()

# Riddle
riddle = """Before the unknown, I’m always near,
Offered in kindness, or whispered in fear.
A phrase that’s wished with hope in the air,
To those embarking on journeys rare.
"""

correct_answer_encoded = "Z29vZCBsdWNr"

encoded_message = "aHR0cHM6Ly93d3cubGlua2VkaW4uY29tL2luL2d1c3Rhdm9mbG9yZXM5MDAxL292ZXJsYXkvMTcyNDk3NzMwMTczNC9zaW5nbGUtbWVkaWEtdmlld2Vy"

# MP3 file URL
mp3_url = "https://github.com/Shellshock9001/mp3_files/blob/main/resume/Nirvana%20-%20Something%20In%20The%20Way%20%20The%20Batman%20OST.mp3?raw=true"

# Decode the hidden message and correct answer
correct_answer = base64.b64decode(correct_answer_encoded).decode('utf-8')
decoded_message = base64.b64decode(encoded_message).decode('utf-8')

# Function to play the MP3 using a Bash command in the background
def play_mp3_with_bash():
    try:
        process = subprocess.Popen(
            ['bash', '-c', f'mpv --no-video --quiet {mp3_url}'],
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL
        )
        return process
    except Exception as e:
        print(f"Error playing MP3 with Bash: {e}")
        return None

# Function to stop the MP3 process
def stop_audio(audio_process):
    if audio_process:
        audio_process.terminate()
        audio_process.wait()  # Ensure the process is reaped properly to avoid zombie processes

# Function to generate unique RGB color code strings for each symbol
def rgb_color_code():
    return f"\033[38;2;{random.randint(0,255)};{random.randint(0,255)};{random.randint(0,255)}m"

# Create a grid with random noise and hidden message embedded
def create_grid(grid_size):
    grid = []
    noise_chars = ['⚲', '⧆', '⌂', '◯', 'Ω', '⊗', '⧍', '∑', 'ℓ', '℧']
    for _ in range(grid_size * grid_size):
        grid.append((random.choice(noise_chars), rgb_color_code()))
    return grid

# Function to update grid with the blending effect
def blend_grid(grid, message, step):
    updated_grid = []
    for i, (char, color) in enumerate(grid):
        if i < len(message) and step >= i:
            updated_grid.append((message[i], rgb_color_code()))  # Reveal part of the message
        else:
            updated_grid.append((char, color))  # Keep random noise
    return updated_grid

# Display the grid with a unique color for each character
def display_grid(grid, grid_size):
    grid_width = grid_size
    for i in range(0, len(grid), grid_width):
        row = grid[i:i + grid_width]
        for char, color in row:
            print(color + char, end=" ")
        print(Style.RESET_ALL)

# Function to animate the blending of the message into the grid
def animate_blend(grid, message, grid_size):
    for step in range(len(message) + 1):
        print("\033c", end="")  # Clear terminal
        blended_grid = blend_grid(grid, message, step)
        display_grid(blended_grid, grid_size)
        time.sleep(0.1)  # Small delay to create the blending effect

# Main function to run the interactive puzzle
def main():
    # Play the MP3 file using Bash, in the background
    audio_process = play_mp3_with_bash()

    # Define grid size based on message length (adjust grid size to display message properly)
    grid_size = 40
    
    # Create and display the initial grid with random symbols
    grid = create_grid(grid_size)
    
    try:
        while True:
            print("\033c", end="")  # Clear terminal
            display_grid(grid, grid_size)

            # Ask user for input: letter guess or full answer
            print(Fore.GREEN + riddle + Style.RESET_ALL)
            user_input = input(Fore.GREEN + "\nWhat am I?: " + Style.RESET_ALL).strip().lower()

            # Compare the user input to the decoded correct answer
            if user_input == correct_answer.lower():
                print("\nCorrect! The hidden message is being revealed...\n")
                animate_blend(grid, decoded_message, grid_size)
                break
            else:
                print(Fore.RED + "\nIncorrect answer. Try again!" + Style.RESET_ALL)

            time.sleep(1)  # Pause briefly before refreshing the grid

    finally:
        stop_audio(audio_process)

# Run the main function
if __name__ == "__main__":
    main()
