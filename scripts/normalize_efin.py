"""Normalize saved, fully paginated Efin history; never infer price adjustment."""
import argparse
import hashlib
import json
import math
import re
from datetime import date, datetime, timezone
from pathlib import Path


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, allow_nan=False).encode()).hexdigest()


def unwrap(payload):
    if not isinstance(payload, dict):
        raise ValueError('Provider payload must be an object')
    if payload.get('isError'):
        raise ValueError('Provider error')
    if isinstance(payload.get('structuredContent'), dict):
        return payload['structuredContent']
    if 'content' in payload:
        blocks = payload['content']
        if not isinstance(blocks, list) or any(not isinstance(b, dict) for b in blocks):
            raise ValueError('Invalid MCP content envelope')
        texts = [b.get('text') for b in blocks if b.get('type') == 'text']
        if len(texts) != 1 or not isinstance(texts[0], str):
            raise ValueError('Ambiguous MCP text envelope')
        parsed = json.loads(texts[0])
        if not isinstance(parsed, dict) or parsed.get('isError'):
            raise ValueError('Invalid provider body')
        return parsed
    return payload


def normalize(pages, symbol):
    if not isinstance(symbol, str) or not symbol.strip():
        raise ValueError('Symbol must be a nonempty string')
    symbol = symbol.strip().upper()
    if isinstance(pages, dict):
        pages = [pages]
    if not isinstance(pages, list) or not pages:
        raise ValueError('Pages must be a nonempty array')
    bars, seen, totals, sources, currencies, cursors = [], set(), set(), set(), set(), set()
    for index, raw in enumerate(pages):
        page = unwrap(raw)
        if page.get('isError'):
            raise ValueError('Provider error')
        meta, body = page.get('meta'), page.get('data')
        if not isinstance(meta, dict) or not isinstance(body, dict):
            raise ValueError('Missing provider metadata/data object')
        if not isinstance(meta.get('symbol'), str) or meta['symbol'].upper() != symbol:
            raise ValueError('Wrong or missing symbol')
        source, currency = meta.get('data_source'), meta.get('currency')
        if not isinstance(source, str) or not source.strip() or 'mock' in source.lower():
            raise ValueError('Missing/mock data source')
        if not isinstance(currency, str) or not re.fullmatch(r'[A-Z]{3}', currency):
            raise ValueError('Missing/invalid currency')
        sources.add(source)
        currencies.add(currency)
        if meta.get('has_more') is not (index < len(pages) - 1):
            raise ValueError('Incomplete/ambiguous pagination')
        if meta['has_more']:
            cursor = meta.get('next_cursor')
            if not isinstance(cursor, str) or not cursor or cursor in cursors:
                raise ValueError('Missing/repeated continuation cursor')
            cursors.add(cursor)
        elif meta.get('next_cursor') not in (None, ''):
            raise ValueError('Final page still has a continuation cursor')
        rows = body.get('data')
        if not isinstance(rows, list) or not rows:
            raise ValueError('No data rows')
        if type(meta.get('result_count')) is not int or meta['result_count'] != len(rows):
            raise ValueError('Page count mismatch')
        total = meta.get('total_count')
        if type(total) is not int or total < len(rows):
            raise ValueError('Invalid total_count')
        totals.add(total)
        for row in rows:
            if not isinstance(row, dict):
                raise ValueError('Invalid history row')
            day = row.get('date')
            if not isinstance(day, str) or date.fromisoformat(day).isoformat() != day:
                raise ValueError('Date must be ISO YYYY-MM-DD')
            if day in seen:
                raise ValueError('Duplicate date; audit/restart pages')
            if 'symbol' in row and row['symbol'] != symbol:
                raise ValueError('Wrong row symbol')
            seen.add(day)
            bar = {'date': day}
            for field in ('open', 'high', 'low', 'close', 'volume_shares'):
                value = row.get(field)
                if isinstance(value, bool) or not isinstance(value, (int, float, str)):
                    raise ValueError('Missing/invalid ' + field)
                value = float(value)
                if not math.isfinite(value) or value < 0 or (field != 'volume_shares' and value == 0):
                    raise ValueError('Invalid ' + field)
                bar['volume' if field == 'volume_shares' else field] = value
            if not bar['low'] <= min(bar['open'], bar['close']) <= max(bar['open'], bar['close']) <= bar['high']:
                raise ValueError('Inconsistent OHLC')
            bars.append(bar)
    if len(totals) != 1 or next(iter(totals)) != len(bars):
        raise ValueError('Total count mismatch')
    if len(sources) != 1 or len(currencies) != 1:
        raise ValueError('Inconsistent provenance')
    bars.sort(key=lambda bar: bar['date'])
    return {'bars': bars, 'provenance': {
        'data_kind': 'efin', 'symbol': symbol, 'source': next(iter(sources)),
        'currency': next(iter(currencies)), 'price_basis': 'unknown',
        'pagination_complete': True, 'calendar_audit': 'not_performed',
        'corporate_actions': 'not_audited', 'actual_start': bars[0]['date'],
        'actual_end': bars[-1]['date'], 'bars': len(bars), 'bars_sha256': digest(bars),
        'raw_pages_sha256': digest(pages), 'page_count': len(pages),
        'retrieved_at': datetime.now(timezone.utc).isoformat(),
        'limitations': [
            'Price adjustment basis is not declared by observed Efin history metadata.',
            'Complete pages do not prove complete exchange-calendar coverage.',
            'Page counts and cursor uniqueness are checked; original request parameters and cursor use require a separate collection audit.',
        ],
    }}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True)
    parser.add_argument('--symbol', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    try:
        result = normalize(json.loads(Path(args.input).read_text()), args.symbol)
        with Path(args.output).open('x') as stream:
            json.dump(result, stream, indent=2, allow_nan=False)
    except (ValueError, TypeError, KeyError, OSError) as exc:
        parser.exit(2, str(exc) + '\n')
