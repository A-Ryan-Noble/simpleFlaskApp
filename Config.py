import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-key'

    IMAGE_UPLOAD_FOLDER = '/Users/ryann/Desktop/Python Stuff/Flask Fun/static/images'
    MAX_CONTENT_LENGTH = 1024 * 1024
    UPLOAD_EXTENSIONS = ['.jpg', '.png']
