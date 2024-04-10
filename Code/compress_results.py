import sys
sys.path.insert(0,'./utils')
import utils
import objects

utils.create_compressed_file(folders=['details', 'historia', 'litigantes'],
                             years=objects.YEARS,
                             months=objects.MONTHS)

print('Finished creating compressed files.')
