import markdown

from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern

import re

BLOCK_RE = r'(@@@)(.*?)(@@!)'

REMOVE_START_ENTER = re.compile(r'')


class AttrTagPattern(Pattern):
    def __init__(self, pattern, tag, attrs):
        Pattern.__init__(self, pattern)

        self.tag = tag
        self.attrs = attrs

    def handleMatch(self, m):
        el = markdown.util.etree.Element(self.tag)
        el.text = m.group(3)

        for (key, val) in self.attrs.items():
            el.set(key, val)
        return el


class TabsExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        block_tag = AttrTagPattern(BLOCK_RE, 'ul', {'class': 'c-tabs'})
        # rem = block_tag.compiled_re.match("@@@1@@!")
        md.inlinePatterns.add('ul', block_tag, '_begin')

        pass


def makeExtension(*args, **kwargs):
    return TabsExtension(*args, **kwargs)
