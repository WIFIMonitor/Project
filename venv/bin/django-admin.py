#!/media/tiagoadonis/Disco Dados/Ubuntu/Universidade/4_ano/2_Semestre/PEI/***REMOVED***/rep/Project/venv/bin/python
# When the django-***REMOVED***.py deprecation ends, remove this script.
import warnings

from django.core import management

try:
    from django.utils.deprecation import RemovedInDjango40Warning
except ImportError:
    raise ImportError(
        'django-***REMOVED***.py was deprecated in Django 3.1 and removed in Django '
        '4.0. Please manually remove this script from your virtual environment '
        'and use django-***REMOVED*** instead.'
    )

if __name__ == "__main__":
    warnings.warn(
        'django-***REMOVED***.py is deprecated in favor of django-***REMOVED***.',
        RemovedInDjango40Warning,
    )
    management.execute_from_command_line()
