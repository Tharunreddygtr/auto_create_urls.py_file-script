import os
import re

apiview_pattern = r'class\s+(\w+)\s*\(\s*APIView\s*\)'
apiview_classes = []
filename = '/home/mphs/OHS/medplus-standalone/MedplusInternal/medplus/leaseagreementtracker/api_views.py'
with open(filename, 'r') as f:
    content = f.read()
    matches = re.findall(apiview_pattern, content)
    apiview_classes.extend(matches)

# Generate path for each APIView class
path_template = 'path(r"{url}", {view}.as_view(), name="{name}"),'
urls = []
files = filename.split('/')
files[-1] = files[-1].split('.')[0]

if len(files) > 1:
    module_path = 'from {module} import {path}'.format(module='.'.join(files[-2:]), path=','.join(apiview_classes))
else:
    module_path = 'from {module} import {path}'.format(module=files[-1], path=','.join(apiview_classes))


def camel_to_snake(string):
    result = re.sub(r'(?<!^)(?=[A-Z])', '_', string).lower()
    return result


for view in apiview_classes:
    url = camel_to_snake(view)
    path = path_template.format(url=url, view=view, name=url)
    urls.append(path)

# Write paths to urls.py file
with open('urls.py', 'w') as f:
    f.write('from django.urls import path\n')
    f.write(module_path)
    f.write('\nurlpatterns = [\n')
    f.write('    ' + '\n    '.join(urls) + '\n')
    f.write(']')

