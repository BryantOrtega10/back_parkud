class Config(object):
    DEBUG=True

class ProductionConfig(Config):
    SECRET_KEY = '075102ad69bff65857ebfe8b03f0e1f54571cd724713c3710653496702ae6e9f'
    JWT_SECRET_KEY = '9bf2f3683315efd31cc3dfc23d1efe30d245575faa27504c7daf113ca07a9ce4'
    MYSQL_HOST = ''
    MYSQL_BD = ''
    MYSQL_USER = ''
    MYSQL_PASS = ''

class DevelopmentConfig(Config):
    SECRET_KEY = '836f57bd4eb7cde5dd6aea4a0d30b14e81aa93c7675dea4067d42ed27ede51c2'
    JWT_SECRET_KEY = '8081907b2886afec69ffb3eeb5a5982d200668b9a6bd0bec65a73f5c6c3e3115'
    MYSQL_HOST = 'localhost'
    MYSQL_BD = 'parkud'
    MYSQL_USER = 'root'
    MYSQL_PASS = ''
    MAIL = 'parkud2023@gmail.com'
    MAIL_PASS = 'ykugdxwzbeadvgom'