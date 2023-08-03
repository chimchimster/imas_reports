import os
import sys
sys.path.append(os.getcwd().rstrip('tools'))

from .data_generators.content_data import ContentGenerator
from .data_generators.table_data import TableContentGenerator
from .data_generators.tags_data import TagsGenerator
from .styles_generators.table_style import TableStylesGenerator
from .styles_generators.schedule_style import SchedulerStylesGenerator

