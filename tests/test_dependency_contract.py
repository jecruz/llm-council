"""The MCP entry point must declare its supported SDK major."""
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib
from packaging.requirements import Requirement


def test_mcp_dependency_is_bounded_to_supported_major():
    """Keep a future incompatible MCP major out of the runtime contract."""
    path = Path(__file__).resolve().parents[1] / 'pyproject.toml'
    project = tomllib.loads(path.read_text())['project']
    requirement = next(Requirement(dep) for dep in project['dependencies'] if Requirement(dep).name == 'mcp')
    assert {(spec.operator,spec.version) for spec in requirement.specifier} == {('>=','1.0.0'),('<','2')}
