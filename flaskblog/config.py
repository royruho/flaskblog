import os


class Config:
    """flaskblog configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY')  # should be random
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')

    @classmethod
    def __printConfig__(cls):
        class_attributes = [i for i in cls.__dict__.keys() if i[:1] != '_']
        for att in class_attributes:
            print(f'{att} : {cls.__dict__.get(att)}')
