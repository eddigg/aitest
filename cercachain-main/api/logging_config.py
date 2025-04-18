import logging.config
import os

def setup_logging(env):
    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
            'detailed': {
                'format': '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
                'level': 'INFO'
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join('logs', f'{env}.log'),
                'maxBytes': 1024 * 1024 * 5,  # 5 MB
                'backupCount': 5,
                'formatter': 'detailed',
                'level': 'DEBUG' if env == 'development' else 'INFO'
            }
        },
        'loggers': {
            '': {
                'handlers': ['console', 'file'],
                'level': 'DEBUG' if env == 'development' else 'INFO'
            }
        }
    }
    
    os.makedirs('logs', exist_ok=True)
    logging.config.dictConfig(config)