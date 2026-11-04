import hashlib,json
from html.parser import HTMLParser
import markdown
from markdown import preprocessors
from pathlib import Path
raw = '# Example\n\n```text\n \t \na\tb\nab\tc\nabc\td\nabcd\te\n\tindent\n    \nvalue: ${token}  \n\n```\n'
expected = '\na   b\nab  c\nabc d\nabcd    e\n    indent\n\nvalue: ${token}  \n\n'
md=markdown.Markdown(extensions=['markdown.extensions.fenced_code'])
class Capture(HTMLParser):
 def __init__(self): super().__init__();self.active=False;self.code=''
 def handle_starttag(self,tag,attrs):
  if tag=='pre':self.active=True
 def handle_endtag(self,tag):
  if tag=='pre':self.active=False
 def handle_data(self,text):
  if self.active:self.code+=text
capture=Capture();capture.feed(md.convert(raw));assert capture.code==expected
container='# Example\n\n!!! note\n    ```text\n    \tkey:\tvalue\n    ```\n'
normalized='\n'.join(md.preprocessors['normalize_whitespace'].run(container.split('\n')))
assert '        key:    value\n' in normalized
report=dict(schema_version=1,status='pass',inputs=dict(markdown_version=str(markdown.version),module=markdown.__file__,normalizer_path=preprocessors.__file__,normalizer_sha256=hashlib.sha256(Path(preprocessors.__file__).read_bytes()).hexdigest(),tab_length=md.tab_length),checks=[dict(id='independent-root-fence-literal',source_sha256=hashlib.sha256(raw.encode()).hexdigest(),captured_sha256=hashlib.sha256(capture.code.encode()).hexdigest(),captured=capture.code,expected=expected),dict(id='container-absolute-tab-stops',observed_line='        key:    value',after_four_column_container='    key:    value')],issues=[])
print(json.dumps(report,indent=2))
