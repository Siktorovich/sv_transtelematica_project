import logging.config
import logging

logger_config = {
    'version': 1,
    'formatters': {
        'std_format': {
            'format': '{asctime} - {levelname} - {name} - {module}:{funcName}:{lineno} - {message}',
            'style': '{'
        }
    },
    'handlers': {
        'console_handler': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'std_format'
        },
        'console_handler_for_answer': {
            'class': 'logging.StreamHandler',
            'level': 'WARNING'
        }
    },
    'loggers': {
        'autotest_logger': {
            'level': 'DEBUG',
            'handlers': ['console_handler']
            # 'propadate': False
        },
        'answer_logger': {
            'level': 'WARNING',
            'handlers': ['console_handler_for_answer']
        }
    }
}

# Loggers
logging.config.dictConfig(logger_config)
console_logger = logging.getLogger('autotest_logger')
answer_logger = logging.getLogger('answer_logger')
