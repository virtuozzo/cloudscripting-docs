import markdown
import re

from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern
from markdown.preprocessors import Preprocessor

TABS_START = r'^@@@\s*$'
TABS_END = r'^@@!\s*$'
TABS_START_REGEX = re.compile(TABS_START)
TABS_END_REGEX = re.compile(TABS_END)


class TabsPreprocessor(Preprocessor):
    def __init__(self, md):
        # Markdown 3.x expects the Markdown instance here
        super(TabsPreprocessor, self).__init__(md)

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
    # Compatible with Markdown 2.x (md, md_globals) and 3.x (md) signatures
    def extendMarkdown(self, md, md_globals=None):
        md.registerExtension(self)
        # Use the modern registry API; this works across Markdown 3.x
        md.preprocessors.register(TabsPreprocessor(md), 'tabs', 25)


def makeExtension(*args, **kwargs):
    return TabsExtension(*args, **kwargs)
