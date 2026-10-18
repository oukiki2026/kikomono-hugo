import unittest
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from prebuild import main as prebuild_main


class AiContentTests(unittest.TestCase):
    def test_config_disables_ai_pages_in_prebuild(self):
        conf = ROOT / 'site-config' / 'site.conf'
        raw = conf.read_text(encoding='utf-8')
        self.assertIn('ai_tools_enabled = true', raw)
        try:
            conf.write_text(raw.replace('ai_tools_enabled = true',
                                        'ai_tools_enabled = false'),
                            encoding='utf-8')
            prebuild_main(ROOT)
            hugo_yaml = (ROOT / 'hugo.yaml').read_text(encoding='utf-8')
            self.assertIn('ai_tools_enabled: "false"', hugo_yaml)
            self.assertIn('ignoreFiles:', hugo_yaml)
            self.assertIn('content/ai-tools/', hugo_yaml)
            sitemap = json.loads((ROOT / 'data' / 'sitemap.json').read_text(encoding='utf-8'))
            locs = [e['loc'] for e in sitemap]
            self.assertFalse(any('/ai-tools/' in loc for loc in locs),
                             'ai-tools URLs must leave the sitemap when disabled')
            self.assertFalse(any(loc.endswith('/start/') or loc.endswith('/free-ai/')
                                 for loc in locs))
        finally:
            conf.write_text(raw, encoding='utf-8')
            prebuild_main(ROOT)  # restore generated files


if __name__ == '__main__':
    unittest.main()
