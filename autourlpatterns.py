import os
import re

apiview_pattern = r'class\s+(\w+)\s*\(\s*APIView\s*\)'
apiview_classes = []
filename = '/home/mphs/OHS/medplus-standalone/MedplusInternal/medplus/leaseagreementtracker/api_views.py'

urlpatterns = []
if os.path.exists('urls.py'):
    with open('urls.py', 'r') as f:
        content = f.read()
        pattern = r'path\(r"([^"]+)", ([^,]+)\)'
        matches = re.findall(pattern, content)
        for match in matches:
            urlpatterns.append(match[1].split('.')[0])
with open(filename, 'r') as f:
    content = f.read()
    matches = re.findall(apiview_pattern, content)
    for match in matches:
        if match not in urlpatterns:
            apiview_classes.append(match)
# Generate path for each APIView class
path_template = 'path(r"{url}", {view}.as_view(), name="{name}"),'
urls = []
files = filename.split('/')
files[-1] = files[-1].split('.')[0]

# if len(files) > 1:
#     module_path = 'from {module} import {path}'.format(module='.'.join(files[-2:]), path=','.join(apiview_classes))
# else:
#     module_path = 'from {module} import {path}'.format(module=files[-1], path=','.join(apiview_classes))

module_path = 'from {module} import *'.format(module=files[-1])


def camel_to_snake(string):
    result = re.sub(r'(?<!^)(?=[A-Z])', '_', string).lower()
    return result


for view in apiview_classes:
    url = camel_to_snake(view)
    path = path_template.format(url=url, view=view, name=url)
    urls.append(path)

# Write paths to urls.py file
if urlpatterns:
    if urls:
        with open('urls.py', 'a') as f:
            f.write('\nurlpatterns += [\n')
            f.write('    ' + '\n    '.join(urls) + '\n')
            f.write(']')

else:
    with open('urls.py', 'w') as f:
        f.write('from django.urls import path\n')
        f.write(module_path)
        f.write('\nurlpatterns = [\n')
        f.write('    ' + '\n    '.join(urls) + '\n')
        f.write(']')


