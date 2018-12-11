import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qqrobot.settings")

'''
Django 版本大于等于1.7的时候，需要加上下面两句
import django
django.setup()
否则会抛出错误 django.core.exceptions.AppRegistryNotReady: Models aren't loaded yet.
'''

import django
from handler import util

django.setup()


def main():
    from script.models import PythonScript,Command
    files = os.listdir('python_script')
    print(files)
    for file in files:
        obj = PythonScript(name=file[:-3],path=os.path.join(util.PYTHON_SCRIPT_DIR, file),creator='854865755')
        obj.save()
        ob= Command(inside_name=obj,last_bind_user_id='854865755',external_name=file[:-3])
        ob.save()
    # PythonScript()


if __name__ == "__main__":
    main()
    print('Done!')