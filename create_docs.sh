# svn propset svn:mime-type text/html docs/*html
epydoc -v --no-frames --no-private --introspect-only -o docs pygrib
epydoc -v --no-frames --no-private --introspect-only -o ncepgrib2_docs ncepgrib2
