import pygame
import threading

# Initialize Pygame Mixer
pygame.mixer.init()

# Define a function to play a sound in a separate thread
def play_sound(sound_file):
    global sound_thread

    # Check if a sound is already playing and if a thread exists
    if pygame.mixer.get_busy() and sound_thread is not None:
        # Stop the current sound
        pygame.mixer.stop()
        # Wait for the thread to finish
        sound_thread.join()

    # Define a target function for the thread that plays the sound
    def target():
        # Load and play the sound
        sound_effect = pygame.mixer.Sound(sound_file)
        sound_effect.play()
        # Wait for the sound to finish playing
        while pygame.mixer.get_busy():
            pygame.time.Clock().tick(10)

    # Create a new thread to play the sound
    sound_thread = threading.Thread(target=target)
    sound_thread.start()

# Initialize the sound thread variable
sound_thread = None

# Example usage: Play a sound
play_sound('guide_1.mp3')

# Function to check if the sound thread is running
def is_sound_thread_running():
    return sound_thread.is_alive() if sound_thread else False

# Wait for some event or condition in your main program...
# For demonstration purposes, we use sleep
import time
if is_sound_thread_running:
    time.sleep(1)
    sound_thread.join()

# Play another sound, stopping the first if it's still playing
play_sound('guide_2.mp3')

if is_sound_thread_running:
    time.sleep(1)
    sound_thread.join()

play_sound('cam-click.wav')
