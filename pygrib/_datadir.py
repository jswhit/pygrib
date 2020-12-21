import os

if 'ECCODES_DEFINITION_PATH' in os.environ:
    eccodes_datadir = os.environ['ECCODES_DEFINITION_PATH']
else:
    eccodes_datadir = os.sep.join([os.path.join(os.path.dirname(__file__),'..'),
        'eccodes/definitions'])
    os.environ['ECCODES_DEFINITION_PATH'] = eccodes_datadir
