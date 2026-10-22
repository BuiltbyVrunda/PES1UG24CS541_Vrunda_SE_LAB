# Lab 5: Static Code Analysis — Reflection

## 1. What is static code analysis?

Static code analysis is the process of examining source code without executing the program to identify potential bugs, security vulnerabilities, and coding-style violations. In this lab, static analysis was used to evaluate the gym membership system and improve its quality, security, and maintainability.

## 2. What is the difference between Pylint, Bandit, and Flake8?

Pylint focuses on overall code quality, naming conventions, missing docstrings, unused variables, and potential programming mistakes. Bandit identifies common security vulnerabilities, such as unsafe use of `eval()`, weak hashing algorithms, and insecure random-number generation. Flake8 checks Python coding style, whitespace, line length, unused imports, and other formatting problems. Using all three tools provides a more comprehensive analysis than relying on just one.

## 3. What issues did you identify, and how did you fix them?

The initial analysis identified multiple issues in the gym membership system. These included unsafe use of `eval()`, shell command execution using `os.system()`, weak MD5 hashing, insecure random-number generation, a hardcoded secret, a mutable default argument, and a bare exception handler. Pylint and Flake8 also reported unused variables, inconsistent function naming, missing docstrings, and formatting violations.

I replaced `eval()` with validated numeric discount calculations, changed MD5 to SHA-256, used Python's `secrets` module for locker PIN generation, removed shell execution, and removed the hardcoded secret. I also corrected the mutable default argument, improved exception handling, cleaned up unused code, renamed functions using snake_case, and improved file handling. After making the changes, I reran the tools and obtained a Pylint score of 10.00/10 and a Bandit report with zero findings.

## 4. How does static analysis improve software quality, and what are its limitations?

Static analysis helps detect potential problems early, encourages consistent coding practices, improves maintainability, and highlights security risks before deployment. It also provides measurable feedback, such as a Pylint score, which can be used to track improvements.

However, static analysis cannot detect every runtime error or guarantee that a program's logic is correct. A clean report does not prove that the application is completely secure. Therefore, static analysis should be combined with manual code review and functional testing. In this lab, running the gym membership program again was important to check that membership status, renewal fee calculation, PIN generation, and roster export continued to work after the fixes.

## Conclusion

This lab demonstrated how Pylint, Bandit, and Flake8 can be used together to improve Python code. By reviewing their findings, applying appropriate fixes, and rerunning the tools, I improved the code quality and addressed the identified security concerns. I learned that static analysis is an important part of software development, but it must be supported by testing and careful review.
