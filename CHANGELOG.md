# Changelog

## [Unreleased]

### Fixed

- Include the backend package in non-editable wheels so isolated installed MCP qualification does not import a source checkout (#4318).

### Fixed

- Declare the MCP 1.x dependency imported by the stdio server and freeze it in uv.lock (#4318).
