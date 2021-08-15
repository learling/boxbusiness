import pymysql
pymysql.install_as_MySQLdb()

# settings.py:
# 
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': env('DB_NAME'),
#         'USER': env('DB_USER'),
#         'HOST': env('DB_HOST'),
#         'PORT': env('DB_PORT'),
#         'PASSWORD': env('DB_PASSWORD')
#     }
# }
# 
# terminal:
# 
# python3 manage.py migrate
# python3 manage.py inspectdb > models.py
