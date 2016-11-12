from django import template  
register = template.Library()
import os, re        

STATIC_PATH="/path/to/templates/"                              
version_cache = {}

rx = re.compile(r"^(.*)\.(.*?)$")
def version(path_string):                                                                 
    try:
        if path_string in version_cache:
            mtime = version_cache[path_string]
        else:
            mtime = os.path.getmtime('%s%s' % (STATIC_PATH, path_string,))
            version_cache[path_string] = mtime

        return rx.sub(r"\1.%d.\2" % mtime, path_string)
    except:
        return path_string 

register.simple_tag(version) 