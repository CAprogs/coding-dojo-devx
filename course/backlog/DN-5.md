# DN-5: Do not render third-party HTML as is (extension)

**As** the DataNova product owner,
**I want** event descriptions and price details to be displayed safely,
**so that** content published by third parties cannot inject markup or links into our app.

## Context

`description` and `price_detail` come from the Paris Open Data API, which aggregates content written
by event organisers. `src/exposition/main.py` renders both with `st.markdown(..., unsafe_allow_html=True)`.
This is the same trust question as prompt injection: data from outside is data, never code or instructions.

## Acceptance criteria

- Descriptions and price details are rendered without `unsafe_allow_html=True`, or sanitized first
  (for example, HTML tags stripped and entities unescaped with the standard library).
- Line breaks and basic readability are preserved.
- A small pytest test covers the sanitising function, or the PR documents a manual check.

Lab: [extensions](../extensions.md), E3.
