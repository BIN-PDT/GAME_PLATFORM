from settings import *
from os import walk


def import_image(*path, format="png", alpha=True):
    full_path = f"{join(*path)}.{format}"
    surf = pygame.image.load(full_path)
    return surf.convert_alpha() if alpha else surf.convert()


def import_images(*path):
    frames = []
    for folder_path, _, file_names in walk(join(*path)):
        for file_name in sorted(file_names, key=lambda name: int(name.split(".")[0])):
            full_path = join(folder_path, file_name)
            surf = pygame.image.load(full_path)
            frames.append(surf)
    return frames


def import_sounds(*path):
    sounds = {}
    for folder_path, _, file_names in walk(join(*path)):
        for file_name in file_names:
            sound = pygame.mixer.Sound(join(folder_path, file_name))
            sounds[file_name.split(".")[0]] = sound
    return sounds
