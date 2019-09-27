import os
import glob
import platform
import time

menu = 'menu.html'
txt = 'files.txt'


def check():
    if not os.path.exists(txt):
        f = open(txt, "x")
        f.close()

    all_files = []
    with open(txt, "r") as file:
        file = file.read()
        words = file.split(",")
        for i in words:
            all_files.append(i)

    return all_files


def file():
    file_paths = []
    filenames = []
    for file in glob.glob("**/*.php", recursive=True):
        filename = file.split("\\")
        filename = filename[-1].split(".")
        filenames.append(filename[0])
        file_paths.append(file)

    return file_paths, filenames


def get_creation_date(path):
    if platform.system() == 'Windows':
        creation_date = time.strftime('%Y_%m_%d %H:%M',  time.localtime(os.path.getmtime(path)))
        return creation_date
    else:
        stat = os.stat(path)
        try:
            return stat.st_birthtime
        except AttributeError:
            return stat.st_mtime

# [[date, file_path, filename], [], []]


def append():
    file_stats = []
    file_paths, filenames = file()
    existing_files = check()
    for file_path, filename in zip(file_paths, filenames):
        if filename not in existing_files:
            file_stats.append([get_creation_date(file_path), file_path, filename])
    file_stats.sort()
    for row in file_stats:
        template = f'        <a href="{row[1]}" target="main">{row[2].capitalize()}</a><br>\n'
        with open(menu, "a+") as html:
            html.write(template)
        with open(txt, "a+") as files:
            files.write(row[2] + ',')


if __name__ == "__main__":
    append()
