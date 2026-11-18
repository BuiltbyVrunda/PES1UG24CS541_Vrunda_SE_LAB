# Lab 7: Fuzzing for Input Validation Bugs

**Problem:** L6_L7_48 - Daycare Fees (`daycare_fees.py`)
**Tools:** Python 3.13, [Hypothesis](https://hypothesis.readthedocs.io/), pytest

Fuzz testing with Hypothesis was used to find input-validation bugs in three functions
(`parse_enrolment`, `hours_average`, `payable_fee`), and the module was then hardened.

| Result | Tests passing |
|--------|---------------|
| Original code | **5 / 66** (61 fail) |
| Fixed code | **66 / 66** |

## Files

| File | Description |
|------|-------------|
| `SE_LAB_7_PES1UG24CS541.pdf` | Report with the screenshots for Steps 1-6 |
| `daycare_fees.py` | **Fixed** application script |
| `test_daycare_fees.py` | Completed Hypothesis tests (66 test cases) |
| `original/daycare_fees_original.py` | The original buggy script, kept so Steps 2 and 4 can be reproduced |
| `screenshots/` | The individual screenshot images used in the PDF |

## How to run

```bash
pip install hypothesis pytest

python daycare_fees.py                 # interactive app
pytest test_daycare_fees.py            # or: python -m pytest test_daycare_fees.py
```

To see the tests fail, copy `original/daycare_fees_original.py` over `daycare_fees.py` in a scratch folder and run pytest there.

## Bugs found by fuzzing

| Function | Input | Original behaviour | Fix |
|----------|-------|--------------------|-----|
| `parse_enrolment` | `None`, non-strings | `AttributeError` / `TypeError` | Only `str` accepted |
| | `""`, `toddler`, `a:b:c` | `ValueError` (unpacking) | Exactly one `:` required |
| | `toddler:abc`, `toddler:` | `ValueError` | Strict decimal parsing |
| | `toddler:nan`, `:inf`, `:-3`, `:1_0` | Accepted | Finite, 0-168 hours, ASCII digits only |
| | `:5`, control characters | Accepted | Name must be non-empty and printable |
| `hours_average` | `None`, `""`, `1,,3`, `one,two` | `AttributeError` / `ValueError` | Every token validated |
| | `20.5,21` | `ValueError` | Decimals allowed |
| | `1,2` | Returned `1` (floor division) | True division -> `1.5` |
| | `-5,5`, `170,10` | Accepted | 0-168 range |
| `payable_fee` | `None`, `3000`, `1\|2\|3`, `abc\|1` | `AttributeError` / `ValueError` | Type check, exactly one `\|` |
| | `nan\|1`, `inf\|1`, `1e999\|1` | Returned `nan` / `inf` | Non-finite rejected |
| | `3000\|-9999` | Negative discount **raised** the bill to 13539.0 | Negative values rejected |
| `main()` | Ctrl-D / Ctrl-C | Traceback | Handled, prints "Input cancelled." |

**Contract used for the fix:** the functions never raise. Invalid input returns `None`, and `main()` prints a readable message.
