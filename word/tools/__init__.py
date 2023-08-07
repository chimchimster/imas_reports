import os
import sys
sys.path.append(os.getcwd().rstrip('tools'))

from .data_generators.table_of_contents_data import ContentGenerator
from .data_generators.table_data import TableContentGenerator
from .data_generators.tags_data import TagsGenerator
from .data_generators.base_data import BasePageDataGenerator
from .styles_generators.table_style import TableStylesGenerator
from .styles_generators.schedule_style import SchedulerStylesGenerator

