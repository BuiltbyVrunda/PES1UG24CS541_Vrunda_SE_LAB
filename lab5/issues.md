# Lab 5 — Static Code Analysis Issues

| Issue | Type | Line(s) in Original Code | Description | Fix Approach / Status |
|---|---|---:|---|---|
| Shell command execution | Security — High | 58 | `os.system()` executed a shell command using a filename, creating a potential command-injection risk. | **Fixed:** Replaced shell execution with `print()` to display the export path. |
| Weak MD5 hash | Security — High | 47 | `hashlib.md5()` is weak for security-sensitive hashing. | **Fixed:** Replaced MD5 with SHA-256 for a stronger general-purpose hash. |
| Unsafe `eval()` | Security — Medium | 42 | `eval(discount_expr)` could execute arbitrary Python expressions. | **Fixed:** Replaced `eval()` with validated numeric discount calculations. |
| Bare exception handler | Bug / Code quality | 26 | A bare `except:` silently ignored errors during membership cancellation. | **Fixed:** Check whether the member exists before deleting the record and return a Boolean result. |
| Mutable default argument | Code quality / Bug | 15 | `registerMember()` used a list as a default argument, which could be shared across calls. | **Fixed:** Changed the default to `None` and initialized the log only when a list is provided. |
| Hardcoded portal secret | Security | 70 | A portal secret was embedded in the source code and printed to the terminal. | **Fixed:** Removed the unused hardcoded secret and its output statement. |
| Insecure random number generation | Security | 51 | `random.randint()` was not suitable for security-sensitive PIN generation. | **Fixed:** Used `secrets.randbelow()` to generate a four-digit PIN. |
| Unused import and variables | Code quality | 6, 31, 41 | The `math` import and `locker_deposit` were unused; `base_fee` was also flagged as unused in the original implementation. | **Fixed:** Removed unused code and used `base_fee` in the renewal calculation. |
| Incorrect comparison with `None` | Style / Code quality | 32 | The code used `== None` instead of Python's recommended identity comparison. | **Fixed:** Used `is not None`. |
| Missing docstrings and naming conventions | Style / Maintainability | Multiple lines | Functions lacked docstrings and used camelCase names. | **Fixed:** Added docstrings and renamed functions to snake_case. |
| File handling and encoding | Code quality | 55–56 | The file was opened without an explicit encoding and closed manually. | **Fixed:** Used a context manager with `encoding="utf-8"`. |
| Formatting violations | Style | Multiple lines | The original file contained long lines and a missing final newline. | **Fixed:** Reformatted the code and added the final newline. |

## Initial Analysis Summary

- **Pylint:** 4.81/10.
- **Bandit:** 6 findings — 2 high, 1 medium, and 3 low severity.
- **Flake8:** Multiple style and code-quality violations.

## Final Analysis Summary

- **Pylint:** 10.00/10.
- **Bandit:** No issues identified.
- **Flake8:** Confirm the final report contains no violations.

## Conclusion

The original code was analyzed using Pylint, Bandit, and Flake8. The identified security, code-quality, and style issues were addressed, and the tools were rerun to verify the improvements. The final program was also executed to confirm that its main functionality remained operational.
