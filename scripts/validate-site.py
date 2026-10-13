"""Check a built documentation site without network access or third-party modules."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else 'site').resolve()
base = 'https://salireza111.github.io/RoTab_Doc/'
files = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
assert 'index.html' in files, 'Missing website entry point'
assert 'help/index.html' in files and 'policies/privacy.html' in files
assert 'search/search_index.json' in files, 'Missing search index'
assert not any(p.endswith(('.wasm', '.data', '.pdb', '.ent', '.pem', '.key', '.zip', '.tgz')) for p in files), 'Unexpected binary/scientific payload'
class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.ids=set(); self.refs=[]; self.feed(text)
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if attrs.get('id'): self.ids.add(attrs['id'])
        key='href' if tag in ('a','link') else 'src' if tag in ('img','script') else None
        if key and attrs.get(key): self.refs.append(attrs[key])
pages={p:Page((root/p).read_text()) for p in files if p.endswith('.html')}
failures=[]
for name,page in pages.items():
    for ref in page.refs:
        url=urlparse(urljoin(base+name,ref))
        if url.scheme not in ('http','https') or url.netloc!=urlparse(base).netloc: continue
        prefix=urlparse(base).path
        if not url.path.startswith(prefix): continue
        target=unquote(url.path[len(prefix):]) or 'index.html'
        if target.endswith('/'): target+='index.html'
        if target not in files: failures.append(f'{name}: missing {target}')
        elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
            failures.append(f'{name}: missing anchor {target}#{url.fragment}')
assert not failures, '\n'.join(failures)
print(f'Validated {len(pages)} pages, local links/anchors and static-site scope.')
