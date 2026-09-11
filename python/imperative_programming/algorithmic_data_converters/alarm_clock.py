import datetime
import os
import time

# Import Pygame with fallback error handling to verify library availability before proceeding
try:
    import pygame

except (ImportError, ModuleNotFoundError):
    print("Error: 'pygame' module is not installed. Please run 'pip install pygame-ce'.")
    raise SystemExit


# Layout Constant: Standard 40-character width for main header banners
TOTAL_WIDTH = 40


def display_tui_banner(title):

    """
    Renders a structured ASCII box banner with heading text centred across 40 characters.
    """

    print("\n" + "=" * TOTAL_WIDTH)
    print(title.center(TOTAL_WIDTH))
    print("=" * TOTAL_WIDTH)


def display_info_box(lines):

    """
    Renders a dynamically bordered panel fitted to the longest string in the lines list.
    The total border width equals max string length + 4 characters for '| ' and ' |'.
    """

    max_len = max(len(line) for line in lines)
    border = "-" * (max_len + 4)

    print(border) # Top border

    for line in lines:
        print(f"| {line.ljust(max_len)} |")

    print(border + "\n") # bottom border with newline for spacing


def valid_alarm_time():

    """
    Prompts user for format selection via a match-case menu structure, validates input
    against strict datetime rules, and converts input into a standard 24-hour 'HH:MM:SS' string.
    """

    display_tui_banner("ALARM CLOCK")

    while True:
        print("\nSelect Time Format Mode:")
        print("[1] 12-Hour Format (e.g. 02:30:00 PM)")
        print("[2] 24-Hour Format (e.g. 14:30:00)")

        choice = input("\nEnter choice (1 or 2): ").strip()

        match choice:

            case "1":
                while True:
                    time_input = input("\nEnter Alarm Time (HH:MM:SS): ").strip()
                    period = input("Enter period (AM/PM): ").strip().upper()

                    if period not in ("AM", "PM"):
                        print("\n[X] Error: Period must strictly be 'AM' or 'PM'.")
                        continue

                    try:
                        full_time_str = f"{time_input} {period}"
                        parsed_time = datetime.datetime.strptime(full_time_str, "%I:%M:%S %p")
                        target_24h = parsed_time.strftime("%H:%M:%S")

                        print()
                        display_info_box([
                            f"Mode        : 12-Hour Format ({period})",
                            f"Target Time : {parsed_time.strftime('%I:%M:%S %p')} (Internal: {target_24h})"
                        ])

                        return target_24h

                    except ValueError:
                        print("\n[X] Error: Invalid 12-hour time format!")
                        print("Please use format 'HH:MM:SS' with valid ranges.")
                        print("(Hours: 01-12, Minutes: 00-59, Seconds: 00-59)")
                        print("Example: '08:05:00' with 'AM' or '02:30:00' with 'PM'")

            case "2":
                while True:
                    time_input = input("\nEnter 24-hour time (HH:MM:SS): ").strip()

                    try:
                        parsed_time = datetime.datetime.strptime(time_input, "%H:%M:%S")
                        target_24h = parsed_time.strftime("%H:%M:%S")

                        print()
                        display_info_box([
                            "Mode        : 24-Hour Format",
                            f"Target Time : {target_24h}"
                        ])

                        return target_24h

                    except ValueError:
                        print("\n[X] Error: Invalid 24-hour time format!")
                        print("Please use format 'HH:MM:SS' with valid ranges.")
                        print("(Hours: 00-23, Minutes: 00-59, Seconds: 00-59)")
                        print("Example: '08:05:00' or '14:30:00'")

            case _:
                print("\n[X] Invalid selection! Please enter choice '1' or '2'.")

def set_alarm(alarm_time):

    """
    Monitors system clock against target time, handling Pygame audio initialisation,
    file validation, and sound playback loops.
    """

    sound_file = r"C:\Users\A.I.M\C.S\WAV\Ummati Qad Laha Fajrun.wav" # WAV and MP3 formats supported by Pygame mixer module

    # Pre-check target file path existence on system drive to prevent runtime crashes
    if not os.path.exists(sound_file):
        print(f"\n[X] FileNotFoundError: Audio file missing at path:\n{sound_file}")
        return

    # ============================================================================
    # PYGAME AUDIO ENGINE INITIALISATION
    # ============================================================================
    # 1. pygame.mixer.init(): 
    # Initialises Pygame's internal sound engine and opens system audio channels.
    # ============================================================================
    # 2. pygame.mixer.music.load(): 
    # Loads the WAV / MP3 track into the streaming music buffer.
    # ============================================================================
    
    try:
        pygame.mixer.init()  # Initialise sound subsystem
        pygame.mixer.music.load(sound_file)  # Prepare audio stream buffer

    except FileNotFoundError:
        print(f"\n[X] Error: Sound file '{sound_file}' was not found.")
        return

    except pygame.error as e:
        print(f"\n[X] Pygame Engine Error: Failed to initialise or load track ({e}).")
        return

    display_tui_banner("ALARM MONITOR")
    display_info_box([
        f"Target Time : {alarm_time}",
        "Status      : Polling clock... (Press Ctrl+C to cancel)"
    ])

    is_running = True

    # Continuous clock polling loop
    while is_running:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"Current Clock: {current_time} | Target: {alarm_time}".center(TOTAL_WIDTH), end = "\r")

        if current_time == alarm_time:
            file_name = os.path.basename(sound_file)

            print("\n\n" + "=" * TOTAL_WIDTH) # Double newline due to carriage return overwrite
            print("TIMES UP!".center(TOTAL_WIDTH))
            print("=" * TOTAL_WIDTH)

            print(f"Alarm Time Reached: {alarm_time}".center(TOTAL_WIDTH))
            print(f"Playing {file_name}...".center(TOTAL_WIDTH))
            print("=" * TOTAL_WIDTH)

            try:

                # =============================================================================
                # PYGAME PLAYBACK & STREAMING CONTROL
                # =============================================================================
                # 1. pygame.mixer.music.play(): 
                # Begins non-blocking asynchronous audio playback.
                # =============================================================================
                # 2. pygame.mixer.music.get_busy(): 
                # Returns True while audio channel streams sound,
                # allowing a blocking wait loop to sustain the process until track completion.
                # =============================================================================

                pygame.mixer.music.play()

                # Keep script alive while Pygame active playback channel is busy
                while pygame.mixer.music.get_busy():
                    time.sleep(1)

            except pygame.error as e:
                print(f"[X] Playback Exception: {e}")

            is_running = False

        time.sleep(1)

    print("\n" + "=" * TOTAL_WIDTH)
    print("Alarm session completed successfully.".center(TOTAL_WIDTH))
    print("=" * TOTAL_WIDTH)


if __name__ == "__main__":
    try:
        alarm_time = valid_alarm_time()
        set_alarm(alarm_time)

    except KeyboardInterrupt:
        print("\n\n" + "=" * TOTAL_WIDTH)
        print("[!] Alarm session cancelled by user.".center(TOTAL_WIDTH))
        print("Have a great day!".center(TOTAL_WIDTH))
        print("=" * TOTAL_WIDTH)

