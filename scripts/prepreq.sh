#/bin/sh

# this will produce src/iracelog_service_manager.egg-info
python setup.py egg_info
# src/iracelog_service_manager.egg-info/requires.txt is the file we want to process

# extract package name from "raw" list
# important: awk in the vs container is mawk - no POSIX regex support!
# awk part: awk 'match($0,/(^[a-zA-Z\-_]+)/) { print  substr($1, RSTART,RLENGTH)}'