---
name: <folder-name>
description: "<What it does and when to use it, in this repository's terms. The agent decides from this line alone.>"
---

# <Title>

## Steps

1. ...

## Template

```yaml
unit_tests:
  - name: ...
    model: ...
    given:
      - input: ref('...')
        rows:
          - {id: ..., ...}
    expect:
      rows:
        - {id: ..., ...}
```

## Pitfalls in this project

- ...
