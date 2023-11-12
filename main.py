import os
from typing import Optional, Set, Tuple, List

from send2trash import send2trash

raw_extensions_lower = {'arw', 'cr2', 'cr3', 'nef', 'arw', 'raf', 'orf', 'rw2', 'dng', 'pef'}

jpeg_extensions = {'jpg', 'jpeg', 'JPG', 'JPEG'}
raw_extensions = raw_extensions_lower.union({ext.upper() for ext in raw_extensions_lower})
raw_folders = {'raw', 'RAW', 'Raw'}
default_raw_folder = 'raw'

assert default_raw_folder in raw_folders


def find_raw_sub_folder_path(path) -> Optional[str]:
    folders = {file for file in os.listdir(path) if os.path.isdir(os.path.join(path, file))}
    potential_raw_folders = folders.intersection(raw_folders)
    assert len(potential_raw_folders) < 2, f'Multiple potential raw folders has been found: {potential_raw_folders}'
    return os.path.join(path, next(iter(potential_raw_folders))) if potential_raw_folders else None


def find_raw_folder_path(path) -> Optional[str]:
    return find_raw_sub_folder_path(path) or find_raw_sub_folder_path(os.path.dirname(path))


def has_extension(path, extensions: Set) -> bool:
    file_parts = os.path.splitext(path)
    return file_parts[1].replace('.', '') in extensions if len(file_parts) > 1 else False


def is_jpeg(path) -> bool:
    return has_extension(path, jpeg_extensions)


def find_pairless_raws_and_jpegs(jpeg_files, raw_files) -> Tuple[List[str], List[str]]:
    jpeg_key_to_file = {os.path.splitext(file)[0]: file for file in jpeg_files}
    raw_key_to_file = {os.path.splitext(file)[0]: file for file in raw_files}
    pairless_raw = set(raw_key_to_file.keys()).difference(set(jpeg_key_to_file.keys()))
    pairless_jpeg = set(jpeg_key_to_file.keys()).difference(set(raw_key_to_file.keys()))
    return list(raw_key_to_file[key] for key in pairless_raw), list(jpeg_key_to_file[key] for key in pairless_jpeg)


def raw_sync():
    print('Searching for raw folder...')
    raw_folder = find_raw_sub_folder_path(os.getcwd()) or find_raw_sub_folder_path(os.path.dirname(os.getcwd()))
    assert raw_folder, f'Can not find raw folder in the working directory with any of the next names:  {raw_folders}'
    jpg_folder = os.getcwd()
    print(f'Raw folder: {raw_folder}')
    print(f'JPG folder: {jpg_folder}')

    jpegs = [file for file in os.listdir(jpg_folder) if has_extension(file, jpeg_extensions)]
    raws = [file for file in os.listdir(raw_folder) if has_extension(file, raw_extensions)]

    assert jpegs, f'No jpeg file has been found with any of the {jpeg_extensions} extensions in {jpg_folder} folder.'
    assert raws, f'No raw file has found with any of the {raw_extensions} extensions in {raw_folder} folder.'
    pairless_raws, pairless_jpegs = find_pairless_raws_and_jpegs(jpegs, raws)
    print(f'Pairless raw file(s) (without jpeg pair): {pairless_raws}')
    print(f'Pairless jpeg file(s) (without raw pair): {pairless_jpegs}')

    if pairless_raws:
        if input(f'Do you want to move {len(pairless_raws)} pairless raw file(s) to trash?').lower() in {'y', 'yes'}:
            for file in pairless_raws:
                print(f'Moving {os.path.join(raw_folder, file)} to trash')
                send2trash(os.path.join(raw_folder, file))

    if pairless_jpegs:
        if input(f'Do you want to move {len(pairless_jpegs)} pairless jpeg file(s) to trash?').lower() in {'y', 'yes'}:
            for file in pairless_jpegs:
                print(f'Moving {os.path.join(jpg_folder, file)} to trash')
                send2trash(os.path.join(jpg_folder, file))

    print('All done, exit.')


def raw_pack():
    print('Analizing working directory')
    workdir = os.getcwd()

    jpegs = [file for file in os.listdir(workdir) if has_extension(file, jpeg_extensions)]
    raws = [file for file in os.listdir(workdir) if has_extension(file, raw_extensions)]

    assert jpegs, 'No jpeg files has found, nothing to sort.'
    print(f'Found {len(jpegs)} jpegs and {len(raws)} raw files in the working directory.')

    raw_folder = find_raw_folder_path(workdir)
    print(f'Found the next potential raw folder: {raw_folder}' if raw_folder else
          'No potential raw folder has been found.')

    pairless_raws, pairless_jpegs = find_pairless_raws_and_jpegs(jpegs, raws)
    print(f'Pairless raw file(s) (without jpeg pair): {pairless_raws}')
    print(f'Pairless jpeg file(s) (without raw pair): {pairless_jpegs}')

    raw_folder = raw_folder or default_raw_folder
    if raws:
        if input(f'Do you want to move {len(raws)} raw files to {raw_folder} folder?') in {'y', 'yes'}:
            os.makedirs(raw_folder, exist_ok=True)
            for file in raws:
                source = os.path.join(workdir, file)
                target = os.path.join(raw_folder, file)
                print(f'Moving {source} to {raw_folder}')
                os.replace(source, target)

    print('All done, exit.')
