from os import system, listdir

import re
import zipfile

def multiple_replacer(*key_values):
    replace_dict = dict(key_values)
    replacement_function = lambda match: replace_dict[match.group(0)]
    pattern = re.compile("|".join([re.escape(k) for k, v in key_values]), re.M)
    return lambda string: pattern.sub(replacement_function, string)

def multiple_replace(string, *key_values):
    return multiple_replacer(*key_values)(string)

def normalize_name(filename:str):
    replacements = (' ', '_'), ('-', ''), (',', ' ')
    return multiple_replace(filename, *replacements)

def compressfile(filename, sufix):
    dot_index = filename.rfind(".")
    nosufix = filename[:dot_index] + str(sufix)
    system("zip {}.zip '{}'".format(normalize_name(nosufix), filename))

    jungle_zip = zipfile.ZipFile(normalize_name(nosufix), 'w')
    jungle_zip.write(filename, compress_type=zipfile.ZIP_DEFLATED)
    jungle_zip.close()
    return nosufix + ".zip"

def compressallfiles(dirname):
    filenames = listdir(dirname)
    for name in filenames:
        print(compressfile(name), "comprimido com sucesso")

if __name__ == "__main__":
    filenames = listdir('.')
    valid_names = [n for n in filenames if n.endswith('.xlsm')]
    for name in valid_names:
        print(compressfile(name, 2019), "comprimido com sucesso")
       
