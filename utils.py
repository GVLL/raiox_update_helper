from fuzzywuzzy import fuzz
import os, zipfile
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

SHEETS_PATH = 'sheets'
# cred = credentials.RefreshToken('/Users/hallpaz/Workspace/qt_env/raiox_upload/raiox-do-orcamento-firebase-adminsdk-d9lx9-5e5939ab53.json')
default_app = firebase_admin.initialize_app()

def test_upload_sheet(filepath, year):
    bucket_name = '{0}.appspot.com'.format(default_app.project_id)
    bucket = storage.bucket(bucket_name)
    blob = bucket.blob('tests/{}/{}'.format(year, os.path.basename(filepath)))
    blob.upload_from_filename(filepath)

def nearest(source, candidates):
    ratio_list = [(fuzz.ratio(source, c), c) for c in candidates]
    ratio_list.sort()
    return ratio_list[-1][1]

def compressfile(filename, compressed_name):
    jungle_zip = zipfile.ZipFile(compressed_name, 'w')
    jungle_zip.write(filename, compress_type=zipfile.ZIP_DEFLATED)
    jungle_zip.close()
    return compressed_name

def upload_sheet(filepath, year):
    bucket_name = '{0}.appspot.com'.format(default_app.project_id)
    bucket = storage.bucket(bucket_name)
    filename = os.path.basename(filepath)
    blob = bucket.blob('{}/{}/{}'.format(SHEETS_PATH,year, filename))
    blob.upload_from_filename(filepath)

if __name__ == "__main__":
    print(default_app.project_id)
    test_upload_sheet('/Users/hallpaz/Downloads/Raio-X upload Junho/Gabinete_do_Prefeito2019.zip', '2019')
    print("upload concluido")


from enum import Enum

class Status(Enum):
    NEUTRAL = 0
    SENT = 1
    ERROR = -1