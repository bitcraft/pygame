# package trackmod
# For Python 2.4 and up.

"""A package for tracking module use

Exports:
    begin(repfile=None) ==> None
    end() ==> None
    get_previous_imports() ==> List of names
    get_my_imports() ==> List of names
    get_imports() ==> List of names
    get_unaccessed_modules() ==> List of names
    get_accessed_modules() ==> List of names
    get_accesses() ==> Dictionary of attribute names by module name
    write_report(repfile) ==> None

"""

from trackmod import reporter  # Keep this first.
import sys
import atexit

from trackmod import importer

try:
    installed
except NameError:
    installed = False
else:
    # reloaded; reload submodules.
    reload(importer)  # implicit reporter reload.

def print_(*args, **kwds):
    stream = kwds.get('file', sys.stdout)
    sep = kwds.get('sep', ' ')
    end = kwds.get('end', '\n')

    if args:
        stream.write(sep.join([str(arg) for arg in args]))
    if end:
        stream.write(end)

def _write_report(repfile):
    def report(*args, **kwds):
        print_(file=repfile, *args, **kwds)

    report("=== module usage report ===")
    report("\n-- modules already imported (ignored) --")
    for name in get_previous_imports():
        report(name)
    report("\n-- modules added by", __name__.split('.')[0], "(ignored) --")
    for name in get_my_imports():
        report(name)
    report("\n-- modules imported but not accessed --")
    for name in get_unaccessed_modules():
        report(name)
    report("\n-- modules accessed --")
    accesses = sorted(get_accesses().iteritems())
    for name, attrs in accesses:
        report(name, " (", ', '.join(attrs), ")", sep='')
    report("\n=== end of report ===")

def get_previous_imports():
    """Return a new sorted name list of previously imported modules"""
    return reporter.get_previous_imports()

def get_my_imports():
    """Return a new sorted name list of module imported by this package"""
    return reporter.get_my_imports()

def get_imports():
    """Return a new sorted name list of imported modules"""
    return reporter.get_imports()

def get_unaccessed_modules():
    """Return a new sorted name list of unaccessed imported modules"""
    return reporter.get_unaccessed_modules()
    
def get_accessed_modules():
    """Return a new sorted name list of accessed modules"""
    return reporter.get_accessed_modules()

def get_accesses():
    """Return a new dictionary of lists of attributes by module name"""
    return reporter.get_accesses()

def write_report(repfile=None):
    """Write a module import and access report to repfile

    repfile may be an open file object of a file path. If not previded
    then writes to standard output. Data collection is terminated if not
    already stopped by an end() call. If no data is collected, begin() not
    called, then a runtime error is raised.

    """
    try:
        if collecting:
            end()
    except NameError:
        raise RuntimeError("No import data was collected")
    if repfile is None:
        _write_report(sys.stdout)
    else:
        try:
            repfile.write
        except AttributeError:
            rf = open(repfile, 'w')
            try:
                _write_report(rf)
            finally:
                rf.close()
        else:
            _write_report(repfile)

def begin(repfile=None):
    """Start collecting import and module access information

    repfile, if provided, is the destination for an end-of-run module import
    and access report. It can be either a file path or an open file object.

    """
    global installed, collecting

    if not installed:
        sys.meta_path.insert(0, importer)
        installed = True
        if repfile is not None:
            atexit.register(write_report, repfile)
    try:
        if collecting:
            return
    except NameError:
        collecting = True

def end():
    global collecting
    collecting = False
    reporter.end()
    importer.end()

reporter.begin()  # Keep this last.



