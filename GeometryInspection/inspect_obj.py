"""Count source records in the supplied positive-index, triangulated OBJ examples.

This does not predict Unreal's imported/render vertex count or GPU memory.
"""
from pathlib import Path
import json

def inspect(path):
    counts = {'v': 0, 'vt': 0, 'vn': 0, 'f': 0}
    tuples = set()
    for line in path.read_text(encoding='utf8').splitlines():
        parts = line.split()
        if not parts or parts[0].startswith('#'):
            continue
        if parts[0] in counts:
            counts[parts[0]] += 1
        if parts[0] == 'f':
            if len(parts) != 4:
                raise ValueError('These exercises require triangulated faces.')
            for ref in parts[1:]:
                fields = ref.split('/')
                if len(fields) != 3 or any(int(v) <= 0 for v in fields if v):
                    raise ValueError('Expected positive v/vt/vn or v//vn references.')
                vertex, uv, normal = fields
                if int(vertex) > counts['v'] or int(normal) > counts['vn']:
                    raise ValueError('Reference outside declared records.')
                if uv and int(uv) > counts['vt']:
                    raise ValueError('UV reference outside declared records.')
                tuples.add((int(vertex), int(uv) if uv else None, int(normal)))
    return {'file': path.name, 'positions': counts['v'], 'texture_coordinates': counts['vt'],
            'normals': counts['vn'], 'triangles': counts['f'], 'referenced_attribute_tuples': len(tuples)}

if __name__ == '__main__':
    print(json.dumps([inspect(Path(__file__).with_name(name + '.obj'))
                      for name in ('smooth', 'hard', 'hard_uv')], indent=2))
