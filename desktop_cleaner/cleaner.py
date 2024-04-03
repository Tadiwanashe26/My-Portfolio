import os
from shutil import move


source_dir = "/mnt/c/Users/Tadiwanashe Ndoziya/Downloads"

imgs_png = "/mnt/c/Users/Tadiwanashe Ndoziya/Pictures/Png"
imgs_jpg = "/mnt/c/Users/Tadiwanashe Ndoziya/Pictures/Jpg"
video = "/mnt/c/Users/Tadiwanashe Ndoziya/Videos"
docs_pdf = "/mnt/c/Users/Tadiwanashe Ndoziya/Documents/Pdf files"
docs_word = "/mnt/c/Users/Tadiwanashe Ndoziya/Documents/word documents"
docs_txt = "/mnt/c/Users/Tadiwanashe Ndoziya/Documents/Txt files"
docs = "/mnt/c/Users/Tadiwanashe Ndoziya/Documents"
exe_files = "/mnt/c/Users/Tadiwanashe Ndoziya/Downloads/Exe Files"
zip_files = "/mnt/c/Users/Tadiwanashe Ndoziya/Downloads/Zip Files"
music = "/mnt/c/Users/Tadiwanashe Ndoziya/Music"

image_extensions = [
    ".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp",
    ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw", ".k25", ".bmp",
    ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf",
    ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"
]

new = 0
document_extensions = [
     ".odt", ".rtf", ".xls", ".xlsx",
    ".csv", ".ppt", ".pptx", ".odp", ".pps", ".odg", ".pub", ".vsd",
    ".md", ".tex"
]


video_extensions = [
    ".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".mpeg", ".mpg",
    ".m4v", ".webm", ".3gp", ".mts", ".m2ts", ".vob", ".ts"
]

music_extensions = [
    ".mp3", ".wav", ".ogg", ".aac", ".wma", ".flac", ".m4a", ".opus"
]

def main():
    with os.scandir(source_dir) as files:
        for file in files:
            if file.is_file():
                dest_path = get_destination(file.name)
                if dest_path:
                    move_file(file.path, dest_path)


def get_destination(filename):
    ext = os.path.splitext(filename)[1].lower()
    if ext in music_extensions:
        return music
    elif ext in image_extensions:
        return imgs_jpg
    elif ext == '.png':
        return imgs_png
    elif ext == '.zip':
        return zip_files
    elif ext == '.exe':
        return exe_files
    elif ext in video_extensions:
        return video
    elif ext == '.pdf':
        return docs_pdf
    elif ext == '.docs' or ext == '.docx':
        return docs_word
    elif ext == '.txt':
        return docs_txt
    elif ext in document_extensions:
        return docs
    else:
        return None

def move_file(src_path, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    dest_path = os.path.join(dest_dir, os.path.basename(src_path))
    move(src_path, dest_path)

if __name__ == "__main__":
    main()



