# !/bin/bash

virtualenv venv
./venv/bin/easy_install Django==1.4 django-annoying django-tinymce
./venv/bin/easy_install http://www.saddi.com/software/flup/dist/flup-1.0.2-py2.6.egg psycopg2