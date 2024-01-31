import os
import sys
sys.path.append(os.getcwd().rstrip('utils'))

from .data_manager import WordDataManager
from .data_processes import ProcessDataGenerator
from .report_merger import MergeReport

