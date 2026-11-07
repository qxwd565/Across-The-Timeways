#!/usr/bin/env python3
"""Build the Legacy v1-compatible API from the preserved original records."""
import base64
import json
import lzma
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TAGS = {
    32: 'TRIGGER_VISUAL', 189: 'WINDFURY', 190: 'TAUNT',
    191: 'STEALTH', 192: 'SPELLPOWER', 194: 'DIVINE_SHIELD',
    197: 'CHARGE', 208: 'FREEZE', 215: 'OVERLOAD',
    217: 'DEATHRATTLE', 218: 'BATTLECRY', 219: 'SECRET',
    220: 'COMBO', 240: 'IMMUNE', 363: 'POISONOUS',
    415: 'DISCOVER', 443: 'CHOOSE_ONE', 462: 'QUEST',
    685: 'LIFESTEAL', 791: 'RUSH', 968: 'START_OF_GAME',
    1077: 'CASTS_WHEN_DRAWN', 1085: 'REBORN',
    1333: 'OUTCAST', 1518: 'DORMANT', 1720: 'TRADEABLE',
}

def convert(src):
    c = src['card']
    out = {
        'id': c['id'], 'dbfId': c['dbfId'], 'name': c['name'],
        'type': c['type'], 'cardClass': c.get('cardClass') or 'NEUTRAL',
        'rarity': c.get('rarity') or 'FREE',
        'collectible': bool(c['collectible']), 'cost': c['cost'],
        'text': c.get('text') or '', 'attack': c['attack'],
        'health': c['health'], 'durability': c['durability'],
        'armor': c['armor'], 'art': '',
    }
    for field in ('flavor', 'spellSchool', 'classes', 'portrait'):
        if c.get(field):
            out[field] = c[field]
    if c.get('races'):
        out['races'] = c['races']
        out['race'] = c['races'][0]
    out['set'] = c['set']
    out['nativeTags'] = c['nativeTags']
    mechanics = list(dict.fromkeys(
        TAGS[t['id']] for t in c['nativeTags']
        if t.get('value') and t['id'] in TAGS
    ))
    if mechanics:
        out['mechanics'] = mechanics
    if src.get('relatedIds'):
        out['relatedDbfIds'] = src['relatedIds']
    return out

def main():
    encoded = ''.join(p.read_text().strip()
        for p in sorted((ROOT / 'data').glob('part-*.b64')))
    raw = json.loads(lzma.decompress(base64.b64decode(encoded)).decode('utf-8'))
    assert len(raw) == 258, len(raw)
    assert len({r['card']['id'] for r in raw}) == 258
    assert len({r['card']['dbfId'] for r in raw}) == 258
    assert all(r['schemaVersion']==1 and r['expansion']['id']==1957
               and r['card']['set']=='TIME_TRAVEL' for r in raw)
    source = ROOT / 'source' / 'Across The Timeways'
    source.mkdir(parents=True, exist_ok=True)
    art = ROOT / 'art'
    art.mkdir(parents=True, exist_ok=True)
    (art / '.gitkeep').touch()
    (ROOT / '.nojekyll').touch()
    for r in raw:
        (source / (r['card']['id'] + '.json')).write_text(
            json.dumps(r, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    cards = [convert(r) for r in sorted(raw,
        key=lambda x: (x['card']['dbfId'], x['card']['id']))]
    (ROOT / 'cards.json').write_text(
        json.dumps({'schema': 1, 'set': 'Across The Timeways', 'cards': cards},
                   ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    assert len(cards) == 258 and all(c['art'] == '' for c in cards)
    print(f'Built {len(cards)} cards and {len(raw)} source records; no artwork.')

if __name__ == '__main__':
    main()
