import subprocess, os, shutil

def copy_files_to_directories(source_dir, dest_parent_dir, num_dirs):
    shutil.rmtree(dest_parent_dir)
    os.makedirs(dest_parent_dir, exist_ok=True)
    # Create N destination directories
    for i in range(num_dirs):
        dest_dir = os.path.join(dest_parent_dir, f'input_{i+1}')
        os.makedirs(dest_dir, exist_ok=True)

    # Get a list of files in the source directory
    files = os.listdir(source_dir)

    # Copy each file to the corresponding destination directory
    for i, file in enumerate(files):
        src_path = os.path.join(source_dir, file)
        dest_dir_index = i % num_dirs  # Calculate destination directory index
        dest_dir = os.path.join(dest_parent_dir, f'input_{dest_dir_index + 1}')
        dest_path = os.path.join(dest_dir, file)
        shutil.copy(src_path, dest_path)
        # print(f"File '{file}' copied to '{dest_dir}'")

source_directory = 'input/'
destination_parent_directory = 'tmp_data/'
os.makedirs(destination_parent_directory, exist_ok=True)

copy_files_to_directories(source_directory, destination_parent_directory, os.cpu_count())


for i in range(os.cpu_count()):
    dockerRun = "docker run"
    mount = " -v ./tmp_data/input_" + f'{i + 1}'
    rest = ":/usr/src/app/input cut"
    subprocess.Popen(dockerRun+mount+rest, shell=True)