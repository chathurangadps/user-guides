"""Render reviewed, repository-native SVG process diagrams without a CDN."""
from html import escape
from pathlib import Path
import textwrap

COLS = (40, 364, 688)
WIDTH, HEIGHT = 272, 126
PALETTE = {
    'action': ('#f5f1fa', '#74539a', '#352347'),
    'decision': ('#fff5dd', '#a27620', '#614914'),
    'pause': ('#fff8e9', '#ad8433', '#624c20'),
    'success': ('#eaf6f0', '#39765c', '#23513e'),
}


def render(diagram, destination):
    nodes = {node['id']: node for node in diagram['nodes']}
    height = 100 + max(n['row'] for n in nodes.values()) * 200 + HEIGHT + 35
    def box(node):
        return COLS[node['col']], 100 + node['row'] * 200
    def center(node):
        x, y = box(node)
        return x + WIDTH / 2, y + HEIGHT / 2
    def port(node, toward):
        cx, cy = center(node)
        dx, dy = toward[0] - cx, toward[1] - cy
        if abs(dx) > abs(dy):
            return (cx + WIDTH / 2 * (1 if dx >= 0 else -1), cy)
        return (cx, cy + HEIGHT / 2 * (1 if dy >= 0 else -1))
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{height}" viewBox="0 0 1000 {height}" role="img" aria-labelledby="title desc">',
           '<title id="title">' + escape(diagram['title']) + '</title>',
           '<desc id="desc">' + escape(diagram['summary'] + ' ' + ' '.join(diagram['steps'])) + '</desc>',
           '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#65748b"/></marker></defs>',
           '<rect width="100%" height="100%" rx="12" fill="#ffffff"/>',
           '<g fill="none" stroke="#65748b" stroke-width="2" stroke-linejoin="round">']
    labels = []
    for edge in diagram['edges']:
        source, target = nodes[edge['from']], nodes[edge['to']]
        via = edge.get('via', [])
        points = [port(source, via[0] if via else center(target))] + via + [port(target, via[-1] if via else center(source))]
        path = 'M' + ' L'.join(f'{x:g},{y:g}' for x, y in points)
        svg.append(f'<path d="{path}" marker-end="url(#arrow)"/>')
        if edge.get('label'):
            if via:
                x, y = (via[-1][0] + via[-2][0]) / 2, via[-1][1] - 12
            else:
                x, y = (points[0][0] + points[-1][0]) / 2, (points[0][1] + points[-1][1]) / 2 - 10
            labels.append(f'<text x="{x:g}" y="{y:g}" text-anchor="middle" font-size="13" font-weight="600" fill="#46536a" stroke="#fff" stroke-width="6" paint-order="stroke">{escape(edge["label"])}</text>')
    svg.append('</g><g font-family="Arial, Helvetica, sans-serif">')
    for node in nodes.values():
        x, y = box(node)
        fill, border, ink = PALETTE[node['kind']]
        if node['kind'] == 'decision':
            svg.append(f'<path d="M{x+WIDTH/2:g},{y} L{x+WIDTH},{y+HEIGHT/2:g} L{x+WIDTH/2:g},{y+HEIGHT} L{x},{y+HEIGHT/2:g} Z" fill="{fill}" stroke="{border}" stroke-width="2"/>')
            svg.append(f'<text x="{x+WIDTH/2:g}" y="{y+55}" text-anchor="middle" font-weight="700" font-size="18" fill="{ink}">{escape(node["label"])}</text>')
            svg.append(f'<text x="{x+WIDTH/2:g}" y="{y+79}" text-anchor="middle" font-size="13" fill="{ink}">{escape(node["detail"])}</text>')
        else:
            svg.append(f'<rect x="{x}" y="{y}" width="{WIDTH}" height="{HEIGHT}" rx="10" fill="{fill}" stroke="{border}" stroke-width="1.5"/>')
            title_lines = textwrap.wrap(node['label'], 25)
            detail_lines = textwrap.wrap(node['detail'], 33)
            assert len(title_lines) <= 2 and len(detail_lines) <= 3, node
            for i, line in enumerate(title_lines):
                svg.append(f'<text x="{x+18}" y="{y+29+i*23}" font-size="18" font-weight="700" fill="{ink}">{escape(line)}</text>')
            for i, line in enumerate(detail_lines):
                svg.append(f'<text x="{x+18}" y="{y+77+i*18}" font-size="14" fill="#4e5d72">{escape(line)}</text>')
    svg.extend(labels)
    svg.append('</g></svg>')
    Path(destination).write_text('\n'.join(svg) + '\n')
