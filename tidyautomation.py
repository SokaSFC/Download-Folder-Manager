from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move
from time import sleep

import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

source_dir =
dest_dir_screenshots = 
dest_dir_music = 
dest_dir_video = 
dest_dir_image = 
dest_dir_documents = 
dest_dir_data = 
dest_dir_code = 
dest_dir_executing = 
dest_dir_fonts = 



image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw", ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]

video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg", ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]

audio_extensions = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]

document_extensions = [".doc", ".docx", ".odt", ".pdf", ".ppt", ".pptx"]

data_extensions = [".csv", ".xls",".xlsx"]

code_extensions = [".py", ".js", ".ipynb", "html", "css"]

executing_extensions = [".pkg", ".dmg", ".zip"]

fonts_extensions = [".ttf", ".otf"]


def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name


def move_file(dest, entry, name):
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(dest, name)
        oldName = join(dest, name)
        newName = join(dest, unique_name)
        rename(oldName, newName)
    move(entry, dest)


class movingfiles(FileSystemEventHandler):
    def on_modified(self, event):
        with scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                self.check_audio_files(entry, name)
                self.check_video_files(entry, name)
                self.check_image_files(entry, name)
                self.check_document_files(entry, name)
                self.check_data_files(entry, name)
                self.check_code_files(entry, name)
                self.check_executing_files(entry, name)
                self.check_fonts_files(entry, name)

    def check_audio_files(self, entry, name):
        for audio_extension in audio_extensions:
            if name.endswith(audio_extension) or name.endswith(audio_extension.upper()):
                move_file(dest_dir_music, entry, name)
                logging.info(f"Moved audio file: {name}")

    def check_video_files(self, entry, name):
        for video_extension in video_extensions:
            if name.endswith(video_extension) or name.endswith(video_extension.upper()):
                move_file(dest_dir_video, entry, name)
                logging.info(f"Moved video file: {name}")

    def check_image_files(self, entry, name):
        for image_extension in image_extensions:
            if name.endswith(image_extension) or name.endswith(image_extension.upper()):
                if "Capture d'écran" in name:
                    move_file(dest_dir_screenshots, entry, name)
                    logging.info(f"Moved image file: {name}")
                else:
                    move_file(dest_dir_image, entry, name)
                    logging.info(f"Moved image file: {name}")

    def check_document_files(self, entry, name):
        for documents_extension in document_extensions:
            if name.endswith(documents_extension) or name.endswith(documents_extension.upper()):
                move_file(dest_dir_documents, entry, name)
                logging.info(f"Moved document file: {name}")

    def check_data_files(self, entry, name):
        for data_extension in data_extensions:
            if name.endswith(data_extension) or name.endswith(data_extension.upper()):
                move_file(dest_dir_data, entry, name)
                logging.info(f"Moved document file: {name}")

    def check_code_files(self, entry, name):
        for code_extension in code_extensions:
            if name.endswith(code_extension) or name.endswith(code_extension.upper()):
                move_file(dest_dir_code, entry, name)
                logging.info(f"Moved document file: {name}")

    def check_executing_files(self, entry, name):
        for executing_extension in executing_extensions:
            if name.endswith(executing_extension) or name.endswith(executing_extension.upper()):
                move_file(dest_dir_executing, entry, name)
                logging.info(f"Moved document file: {name}")

    def check_fonts_files(self, entry, name):
        for fonts_extension in fonts_extensions:
            if name.endswith(fonts_extension) or name.endswith(fonts_extension.upper()):
                move_file(dest_dir_fonts, entry, name)
                logging.info(f"Moved document file: {name}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir

    event_handler = movingfiles()

    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    print ("Ready to work")
    print ("Start processing by moving a file in the source folder")
    print ("[Control Z] or Kill Terminal to end processing")

    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()