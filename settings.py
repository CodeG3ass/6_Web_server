PORT = 80
REQUEST_LENGTH = 16384
ALLOWED_FORMATS = ['html','css','js','txt','png', 'gif']

TYPES = {'html': 'text/html; charset=UTF-8',
             'css': 'text/css',
            'gif': 'image/gif',
            'png': 'image/png',
            'js': 'text/javascript'}

CODES = {'200': 'OK',
         '403': 'Forbidden',
         '404': 'Not found'}