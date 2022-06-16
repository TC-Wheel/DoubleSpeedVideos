import os, subprocess


"""program structure:
we'll walk along- using OS- 
and for each video we find, 
we'll use subprocess to call ffmpeg 
command to speed it up 2x."""


def find_video_paths(video_filetype):
    top_dir = "C:\\Users\\guy\\Desktop\\ffmpeg-work\\"
    video_paths = []
    for dirpath, dirnames, filenames in os.walk(top_dir):
        for filename in filenames:
            if filename[-4:] == video_filetype:
                video_paths.append(os.path.join(dirpath, filename))
    return video_paths


def speed_up_video(video_paths, speed_factor=2, video_filetype=".mp4"):
    # error_check = (0, 0, 0)  # no errors
    for video_path in video_paths:
        # if error_check[0] != 0:
        #     print(
        #         f"Error '{error_check[0]}' with command: '{error_check[1]}'. Console Output: '{error_check[2]}'"
        #     )
        #     error_check = (0, 0, 0)
        #     continue
        video_filename = os.path.basename(video_path)
        print(f"{video_filename = }")
        output = subprocess.run(
            f'ffmpeg -i "{video_path}" -filter_complex "[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]" -map "[v]" -map "[a]" "{os.path.join(os.path.dirname(video_path), video_filename[:-4] + "_2x" + video_filetype)}"'
        )
        # error_check = (output.returncode, output.args, output.stdout)


def replace_old_vids(video_filetype):
    """deletes old slow mp4s & renames fast mp4s to the old name"""
    video_paths = find_video_paths(video_filetype)
    for path_name in video_paths:
        if os.path.basename(path_name)[0] == ".":
            print(f"Skip Hidden file: {os.path.basename(path_name)}")
            continue
        if os.path.basename(path_name)[-7:] != f"_2x{video_filetype}":
            print(f"Remove File: {os.path.basename(path_name)}")
            os.remove(path_name)
        else:
            os.rename(path_name, path_name[:-7] + path_name[-4:])
            print(f"Rename This File: {os.path.basename(path_name)}")


def main():
    # I'm speeding up .mp4 and .m4v files
    mp4_paths = find_video_paths(".mp4")
    print(mp4_paths)
    speed_up_video(mp4_paths)
    replace_old_vids(".mp4")

    m4v_paths = find_video_paths(".m4v")
    print(m4v_paths)
    speed_up_video(m4v_paths, video_filetype=".m4v")
    replace_old_vids(".m4v")


if __name__ == "__main__":
    main()
