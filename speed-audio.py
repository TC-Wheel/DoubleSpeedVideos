import os, subprocess


"""program structure:
we'll walk along- using OS- 
and for each video we find, 
we'll use subprocess to call ffmpeg 
command to speed it up 2x."""


def find_audio_paths(file_type):
    top_dir = "C:\\Users\\guy\\Desktop\\ffmpeg-work\\"
    audio_paths = []
    for dirpath, dirnames, filenames in os.walk(top_dir):
        for filename in filenames:
            if filename[-4:] == file_type:
                audio_paths.append(os.path.join(dirpath, filename))
    return audio_paths


def convert_and_2x(audio_paths, end_file_type, speed_factor=2):
    error_check = (0, 0, 0)  # no errors
    for audio_path in audio_paths:
        if error_check[0] != 0:
            print(
                f"Error '{error_check[0]}' with command: '{error_check[1]}'. Console Output: '{error_check[2]}'"
            )
            error_check = (0, 0, 0)
            continue
        audio_filename = os.path.basename(audio_path)
        output = subprocess.run(
            f'ffmpeg -i "{audio_path}" -filter:a atempo={speed_factor} "{os.path.join(os.path.dirname(audio_path), audio_filename[:-4] + end_file_type)}"'
        )
        error_check = (output.returncode, output.args, output.stdout)


def convert(audio_paths, end_file_type):
    # error_check = (0, 0, 0)  # no errors
    for audio_path in audio_paths:
        # if error_check[0] != 0:
        #     print(
        #         f"Error '{error_check[0]}' with command: '{error_check[1]}'. Console Output: '{error_check[2]}'"
        #     )
        #     error_check = (0, 0, 0)
        #     continue
        audio_filename = os.path.basename(audio_path)
        output = subprocess.run(
            f'ffmpeg -i "{audio_path}" -c:a aac "{os.path.join(os.path.dirname(audio_path), audio_filename[:-4] + end_file_type)}"'
        )
        # error_check = (output.returncode, output.args, output.stdout)


def del_all(audio_paths, file_type):
    for path_name in audio_paths:
        if os.path.basename(path_name)[0] == ".":
            print(f"Skip Hidden File: {os.path.basename(path_name)}")
            continue
        if os.path.basename(path_name)[-4:] == file_type:
            print(f"Remove File: {os.path.basename(path_name)}")
            os.remove(path_name)


def main():
    m4a_paths = find_audio_paths(".m4a")
    convert_and_2x(m4a_paths, ".mp3")
    del_all(m4a_paths, ".m4a")
    mp3_paths = find_audio_paths(".mp3")
    convert(mp3_paths, ".m4a")
    del_all(mp3_paths, ".mp3")


if __name__ == "__main__":
    main()
