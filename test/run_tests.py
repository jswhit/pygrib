# run all matplotlib based tests
import glob
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams.update(matplotlib.rcParamsDefault)
# Find all test files.
test_files = glob.glob('test_*.py')
test_files.remove('test_spectral.py') # skip spectral transform test
for f in test_files:
    print('running %s...' % f)
    exec(open(f).read())
