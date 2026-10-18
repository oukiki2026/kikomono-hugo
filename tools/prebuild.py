#!/usr/bin/env python3
"""Build-time data preparation for the Hugo site.

Reads site-config/site.conf, data/offers.json and content/ front matter, then
generates (all git-ignored build artifacts):
  hugo.yaml                 site configuration (baseURL, params, markup)
  data/active_offers.json   verified offers enriched with provider names
  data/ai_tools.json        hub card/table data (from ai_content.TOOLS etc.)
  data/schemas.json         per-path JSON-LD, byte-identical to build.py output
  data/sitemap.json         ordered [{loc, lastmod}] replicating build order
  content/providers/{id}.md per-provider pages (front matter only)
  content/deals/{id}.md     per-offer pages (front matter only; none when empty)
  static/data/offers.json   public offer subset (same bytes as build.py)
  static/_headers            CSP/security headers (same bytes as build.py)

Run:  python tools/prebuild.py && hugo -d site
Stdlib only. Business logic (active_offers, offer_schema) is reused from the
frozen build.py so the 48h freshness rule and schema shapes stay identical.
"""
import sys
import json
import re
import hashlib
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from config import load_config
from build import active_offers, offer_schema


def parse_front_matter(path):
    """Minimal parser for the front matter written by tools/convert_content.py."""
    text = Path(path).read_text(encoding='utf-8')
    assert text.startswith('---\n'), path
    end = text.index('\n---', 4)
    fm = {}
    for line in text[4:end].splitlines():
        if not line.strip() or ':' not in line:
            continue
        k, v = line.split(':', 1)
        v = v.strip()
        if v.startswith('"') and v.endswith('"'):
            v = v[1:-1].replace('\\"', '"').replace('\\\\', '\\')
        elif re.fullmatch(r'-?\d+', v):
            v = int(v)
        fm[k.strip()] = v
    return fm


def content_path_to_url(rel):
    """content/ai-tools/x.md -> /ai-tools/x/ ; content/_index.md -> / ."""
    rel = rel.replace('\\', '/')
    if rel == '_index.md':
        return '/'
    if rel.endswith('/_index.md'):
        return '/' + rel[:-len('/_index.md')] + '/'
    return '/' + rel[:-len('.md')] + '/'


def main(root=ROOT):
    cfg = load_config(root / 'site-config' / 'site.conf')
    base = cfg['base_url'].rstrip('/')
    if not re.fullmatch(r'https://[A-Za-z0-9.-]+', base):
        raise ValueError('base_url must be an HTTPS origin')
    data = json.loads((root / 'data' / 'offers.json').read_text(encoding='utf-8'))
    offers = active_offers(cfg, data)
    providers = {p['id']: p for p in cfg['providers']}
    statuses = {p['provider_id']: p for p in data['providers']}
    fetched_at = data['fetched_at']
    month = datetime.fromisoformat(fetched_at).strftime('%B %Y')
    style_version = hashlib.sha256((root / 'static' / 'assets' / 'style.css').read_bytes()).hexdigest()[:12]
    measurement_id = cfg.get('ga4_measurement_id', '')
    if measurement_id and not re.fullmatch(r'G-[A-Z0-9]+', measurement_id):
        raise ValueError('Invalid GA4 measurement ID')

    def url(path):
        return base + path

    def schema_json(path, title, extra):
        bread = {'@context': 'https://schema.org', '@type': 'BreadcrumbList',
                 'itemListElement': [
                     {'@type': 'ListItem', 'position': 1, 'name': cfg['brand'], 'item': url('/')}]}
        if path != '/':
            bread['itemListElement'].append(
                {'@type': 'ListItem', 'position': 2, 'name': title, 'item': url(path)})
        return json.dumps((extra or []) + [bread], ensure_ascii=False).replace('<', '\\u003c')

    def itemlist(items):
        return {'@context': 'https://schema.org', '@type': 'ItemList',
                'itemListElement': [
                    {'@type': 'ListItem', 'position': i + 1,
                     'url': url('/deals/' + o['id'] + '/'), 'name': o['title']}
                    for i, o in enumerate(items)]}

    # ---- content inventory (committed Markdown) ----
    pages = []  # dicts: path, title, description, lastmod, weight
    for md in sorted((root / 'content').rglob('*.md')):
        rel = md.relative_to(root / 'content').as_posix()
        if rel.startswith('providers/') or rel.startswith('deals/'):
            continue  # generated below, not committed
        fm = parse_front_matter(md)
        if 'lastmod' not in fm:
            continue  # non-page stub (e.g. section suppression)
        pages.append({'path': content_path_to_url(rel), 'title': fm['title'],
                      'description': fm.get('description', ''), 'lastmod': fm['lastmod'],
                      'weight': fm.get('weight', 10 ** 6)})

    # ---- generated provider/deal pages ----
    gen_pages = []
    prov_dir = root / 'content' / 'providers'
    prov_dir.mkdir(parents=True, exist_ok=True)
    for md in prov_dir.glob('*.md'):
        md.unlink()
    (prov_dir / '_index.md').write_text(
        '---\ntitle: "Providers"\nbuild:\n  render: false\n  list: false\n---\n',
        encoding='utf-8')
    deal_dir = root / 'content' / 'deals'
    deal_dir.mkdir(parents=True, exist_ok=True)
    for md in deal_dir.glob('*.md'):
        md.unlink()
    for p in cfg['providers']:
        st = statuses.get(p['id'], {})
        fm = {'title': f'{p["name"]} VPS offers & source status \u00b7 {month}',
              'description': f'Official-source {p["name"]} plans, current verification status and billing terms.',
              'date': fetched_at, 'lastmod': fetched_at, 'weight': 10 ** 6,
              'type': 'provider', 'provider_id': p['id'], 'provider_name': p['name'],
              'source_url': p['source'], 'status': st.get('status', 'not-checked'),
              'checked_at': st.get('checked_at', 'Not checked yet')}
        (prov_dir / (p['id'] + '.md')).write_text(
            '---\n' + ''.join(f'{k}: "{v}"\n' for k, v in fm.items()
                              if k not in ('weight',)) +
            f'weight: {fm["weight"]}\n---\n', encoding='utf-8')
        gen_pages.append({'path': f'/providers/{p["id"]}/', 'title': fm['title'],
                          'description': fm['description'], 'lastmod': fetched_at,
                          'kind': 'provider', 'provider': p})
    for o in offers:
        p = providers[o['provider_id']]
        target = p['affiliate'] or o['offer_url']
        affiliate = bool(p['affiliate'])
        fm = {'title': f'{o["title"]} \u2014 {o["currency"]} {o["price"]}/{o["period"]} \u00b7 {month}',
              'description': f'{o["title"]}: {o["currency"]} {o["price"]}/{o["period"]}. {o["terms"]}',
              'date': o['fetched_at'], 'lastmod': o['fetched_at'], 'weight': 10 ** 6,
              'type': 'deal', 'offer_id': o['id'],
              'offer_title': o['title'], 'price': o['price'], 'currency': o['currency'],
              'period': o['period'], 'specs': o.get('specs', ''), 'terms': o['terms'],
              'evidence': o['evidence'], 'source_url': o['source_url'],
              'fetched_at': o['fetched_at'], 'source_sha256': o['source_sha256'],
              'target': target, 'rel': 'sponsored noopener' if affiliate else 'noopener',
              'disclosure': ('Affiliate link: we may earn a commission if you buy.'
                             if affiliate else
                             'Direct official link. No affiliate commission is configured.')}
        (deal_dir / (o['id'] + '.md')).write_text(
            '---\n' + ''.join(f'{k}: "{str(v).replace(chr(34), chr(92) + chr(34))}"\n'
                              for k, v in fm.items() if k != 'weight') +
            f'weight: {fm["weight"]}\n---\n', encoding='utf-8')
        gen_pages.append({'path': f'/deals/{o["id"]}/', 'title': fm['title'],
                          'description': fm['description'], 'lastmod': o['fetched_at'],
                          'kind': 'deal', 'offer': o, 'provider': p})

    # ---- schemas (byte-identical to build.py) ----
    schemas = {}
    for pg in pages:
        path = pg['path']
        extra = None
        if path in ('/hosting/', '/offers/', '/compare/'):
            extra = [itemlist(offers)]
        schemas[path] = schema_json(path, pg['title'], extra)
    for gp in gen_pages:
        if gp['kind'] == 'provider':
            p, items = gp['provider'], [o for o in offers if o['provider_id'] == gp['provider']['id']]
            extra = [{'@context': 'https://schema.org', '@type': 'Service',
                      'name': o['title'],
                      'provider': {'@type': 'Organization', 'name': p['name']},
                      'offers': offer_schema(o)} for o in items]
        else:
            o, p = gp['offer'], gp['provider']
            s = offer_schema(o)
            s.update({'@context': 'https://schema.org', 'name': o['title'],
                      'seller': {'@type': 'Organization', 'name': p['name']}})
            extra = [s]
        schemas[gp['path']] = schema_json(gp['path'], gp['title'], extra)
    (root / 'data' / 'schemas.json').write_text(json.dumps(schemas, indent=2), encoding='utf-8')

    # ---- sitemap order: content by weight, providers/deals after /guides/ ----
    by_weight = sorted(pages, key=lambda p: (p['weight'], p['path']))
    idx = next(i for i, p in enumerate(by_weight) if p['path'] == '/guides/')
    ordered = (by_weight[:idx + 1]
               + [{'path': g['path'], 'lastmod': g['lastmod']} for g in gen_pages]
               + by_weight[idx + 1:])
    if cfg.get('ai_tools_enabled') != 'true':
        ordered = [p for p in ordered
                   if not (p['path'].startswith('/ai-tools/') or p['path'] in ('/start/', '/free-ai/'))]
    sitemap = [{'loc': url(p['path']), 'lastmod': p['lastmod']} for p in ordered]
    (root / 'data' / 'sitemap.json').write_text(json.dumps(sitemap, indent=2), encoding='utf-8')

    # ---- data files for templates ----
    enriched = [dict(o, provider_name=providers[o['provider_id']]['name']) for o in offers]
    (root / 'data' / 'active_offers.json').write_text(json.dumps(enriched, indent=2), encoding='utf-8')
    import ai_content
    (root / 'data' / 'ai_tools.json').write_text(json.dumps(
        {'tools': ai_content.TOOLS,
         'meeting_guides': [list(g) for g in ai_content.MEETING_GUIDES],
         'muse_card': ai_content.MUSE_CARD,
         'review_date': cfg.get('ai_content_updated', '2026-10-02'),
         'hub_date': '2026-10-11'}, indent=2), encoding='utf-8')

    # ---- hugo.yaml ----
    hugo_yaml = f"""baseURL: {base}/
title: {cfg['brand']}
disableKinds: [RSS, taxonomy, term]
enableGitInfo: false
disableHugoGeneratorInject: true
markup:
  goldmark:
    renderer:
      unsafe: true
params:
  base_url: "{base}"
  brand: "{cfg['brand']}"
  tagline: "{cfg['tagline']}"
  repository: "{cfg['repository']}"
  ga4_measurement_id: "{measurement_id}"
  ai_tools_enabled: "{cfg.get('ai_tools_enabled', 'true')}"
  style_version: "{style_version}"
  operator_name: "{cfg.get('operator_name', '')}"
  contact_email: "{cfg.get('contact_email', '')}"
  domain: "{cfg['domain']}"
  month: "{month}"
  updated: "{fetched_at}"
  providers:"""
    for p in cfg['providers']:
        hugo_yaml += f'\n    - id: "{p["id"]}"\n      name: "{p["name"]}"'
    hugo_yaml += '\n'
    if cfg.get('ai_tools_enabled') != 'true':
        hugo_yaml += 'ignoreFiles: ["content/ai-tools/.*"]\n'
    (root / 'hugo.yaml').write_text(hugo_yaml, encoding='utf-8')

    # ---- static/data/offers.json (public subset, same bytes as build.py) ----
    public_data = dict(data, offers=offers,
                       providers=[p for p in data['providers']
                                  if p['provider_id'] in {x['id'] for x in cfg['providers']}])
    static_data = root / 'static' / 'data'
    static_data.mkdir(parents=True, exist_ok=True)
    (static_data / 'offers.json').write_text(json.dumps(public_data, indent=2), encoding='utf-8')

    # ---- static/_headers (same bytes as build.py) ----
    analytics_scripts = " https://www.googletagmanager.com" if measurement_id else ""
    analytics_connections = (" https://www.googletagmanager.com https://*.google-analytics.com"
                             " https://*.google.com") if measurement_id else ""
    analytics_images = (" https://www.googletagmanager.com https://*.google-analytics.com"
                        ) if measurement_id else ""
    (root / 'static' / '_headers').write_text(
        "/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n"
        "  Content-Security-Policy: default-src 'self'; style-src 'self'; img-src 'self'"
        + analytics_images + "; script-src 'self' https://static.cloudflareinsights.com"
        + analytics_scripts + "; connect-src 'self' https://cloudflareinsights.com"
        + analytics_connections + "; frame-ancestors 'none'\n", encoding='utf-8')
    (root / 'static' / 'robots.txt').write_text(
        f'User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n', encoding='utf-8')

    print(json.dumps({'pages': len(sitemap), 'offers': len(offers),
                      'style_version': style_version}, indent=2))


if __name__ == '__main__':
    main()
