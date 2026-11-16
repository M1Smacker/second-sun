"""Adapt the reviewed 024 scorer to 025 replay directories and strict coverage."""
from pathlib import Path

ROOT = Path(r'D:\second-sun-astra')
SCRIPTS = ROOT / 'research/astra/scripts'


def main():
    source = (SCRIPTS / '024_score.py').read_text(encoding='utf-8')
    source = source.replace('024_inputs', '025_inputs').replace("brief = '024'", "brief = '025'")
    source = source.replace('Score fresh 024 subtraction replays', 'Score fresh 025 quality-policy replays')
    start = source.index('    extra_folder = H.OUT')
    end = source.index('    for key in changed_keys:', start)
    source = source[:start] + '    def generation_for(key):\n        return generated\n' + source[end:]
    source = source.replace("if path.exists():\n                group = json.loads(path.read_text(encoding='utf-8'))",
                            "if path.exists():\n                group = json.loads(path.read_text(encoding='utf-8'))")
    source = source.replace("group = json.loads(D.read(guard, path, brief))",
                            "group = json.loads(D.read(guard, path, brief))")
    # Require both replay kinds whenever the original development group exists.
    before = "                    if path.is_file():\n                        group = json.loads(D.read(guard, path, brief))"
    after = """                    expected_kind = source / kind / f'{star}_{sec}.json'
                    if (star, sec) in changed_keys and expected_kind.exists():
                        assert path.is_file(), 'Required changed-sector injection replay is missing'
                    if path.is_file():
                        group = json.loads(D.read(guard, path, brief))"""
    assert source.count(before) == 1
    source = source.replace(before, after)
    source = source.replace("'identity verified' if mode == 'V0' else 'scored'",
                            "'historical identity verified' if baseline_run else 'candidate scored'")
    (SCRIPTS / '025_score.py').write_text(source, encoding='utf-8')
    print('Prepared adopted-B scorer with required replay coverage.')


if __name__ == '__main__':
    main()
