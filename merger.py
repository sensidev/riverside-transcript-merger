import os.path
import re
import sys
from datetime import timedelta

DEFAULT_TRANSCRIPTS_PATH = 'samples'


# Function to parse timestamp and return timedelta object
def parse_timestamp(timestamp):
    hours = minutes = seconds = 0

    parts = list(map(int, timestamp.split(':')))
    if len(parts) == 2:
        minutes, seconds = parts
        hours = 0
    elif len(parts) == 3:
        hours, minutes, seconds = parts
    return timedelta(hours=hours, minutes=minutes, seconds=seconds)


# Function to format timedelta object back to timestamp
def format_timestamp(timedelta_obj):
    total_seconds = int(timedelta_obj.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"


# Function to adjust the timestamps in a transcript based on offset
def adjust_timestamps(transcript, offset):
    adjusted_transcript = []
    for line in transcript.split('\n'):
        match = re.match(r'^(.*)\((\d+:\d+(?::\d+)?)\)$', line)
        if match:
            person = match.group(1)
            timestamp = match.group(2)
            original_time = parse_timestamp(timestamp)
            new_time = original_time + offset
            adjusted_transcript.append(f"{person}({format_timestamp(new_time)})")
        else:
            adjusted_transcript.append(line)
    return '\n'.join(adjusted_transcript)


# Main function to concatenate transcripts
def concatenate_transcripts(files):
    offset = timedelta()
    concatenated_transcript = ""

    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            transcript = f.read()
            adjusted_transcript = adjust_timestamps(transcript, offset)
            concatenated_transcript += adjusted_transcript + "\n"

            # Update offset for next file
            timestamps = re.findall(r'\((\d+:\d+(?::\d+)?)\)', transcript)
            if timestamps:
                last_timestamp = parse_timestamp(timestamps[-1])
                offset += last_timestamp + timedelta(seconds=1)  # Adding 1 second to avoid overlap

    return concatenated_transcript


def get_sorted_file_list(directory_path):
    # Check if the directory exists
    if not os.path.isdir(directory_path):
        print(f"Error: The directory '{directory_path}' does not exist.")
        return

    try:
        # Get a list of files in the directory
        files = os.listdir(directory_path)

        # Filter out directories, keep only files
        files = [f for f in files if os.path.isfile(os.path.join(directory_path, f))]

        # Sort the list of files
        files.sort()

        # Add the directory path to each file name
        full_file_paths = [os.path.join(directory_path, f) for f in files]

        return full_file_paths

    except Exception as e:
        print(f"An error occurred: {e}")
        return []


if __name__ == "__main__":
    if len(sys.argv) < 2:
        transcript_path = DEFAULT_TRANSCRIPTS_PATH
    else:
        transcript_path = sys.argv[1]

    # List of files to concatenate
    file_list = get_sorted_file_list(transcript_path)

    # Concatenate transcripts
    final_transcript = concatenate_transcripts(file_list)

    # Write the final transcript to a new file
    with open(os.path.join(transcript_path, "merged.txt"), 'w', encoding='utf-8') as output_file:
        output_file.write(final_transcript)

    print(f"Transcripts concatenated successfully {len(file_list)} files!")
