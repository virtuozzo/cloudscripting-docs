import markdown
import re

from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern
from markdown.preprocessors import Preprocessor

TABS_START = ur'^@@@\s*$'
TABS_END = ur'^@@!\s*$'
TABS_START_REGEX = re.compile(TABS_START)
TABS_END_REGEX = re.compile(TABS_END)

class TabsPreprocessor(Preprocessor):
    def run(self, lines):
        new_lines = []
        skip_empty_line = False

        for line in lines:
            start = TABS_START_REGEX.match(line)

            if start:
                new_lines.append('<ul class="c-tabs">')
                skip_empty_line = True
                continue

            end = TABS_END_REGEX.match(line)

            if end:
                new_lines.append('</ul>')
                skip_empty_line = False
                continue

            if not line and skip_empty_line:
                continue

            new_lines.append(line)

        return new_lines

class TabsExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.registerExtension(self)
        md.preprocessors["tabs"] = TabsPreprocessor()
        pass


def makeExtension(*args, **kwargs):
    return TabsExtension(*args, **kwargs)
