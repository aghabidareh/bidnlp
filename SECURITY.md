# Security Policy

## Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1   | :x:                |

## Reporting a Vulnerability

We take the security of BidNLP seriously. If you believe you have found a security vulnerability, please report it to us as described below.

### Please Do Not

* **Do not** open a public GitHub issue for security vulnerabilities
* **Do not** disclose the vulnerability publicly until we've had a chance to address it

### Please Do

1. **Email** your findings to the maintainers (create a security advisory on GitHub)
2. **Provide** detailed steps to reproduce the vulnerability
3. **Include** the version of BidNLP you're using
4. **Wait** for a response - we aim to respond within 48 hours

### What to Report

We're interested in all types of security issues, including:

* **Code injection** vulnerabilities
* **Denial of service** attacks
* **Authentication/authorization** bypasses
* **Data exposure** issues
* **Dependency vulnerabilities**

### What to Expect

1. **Acknowledgment**: We'll acknowledge your email within 48 hours
2. **Communication**: We'll keep you informed about our progress
3. **Fix**: We'll work on a fix and release it as soon as possible
4. **Credit**: We'll credit you in the release notes (unless you prefer to remain anonymous)

## Security Best Practices

When using BidNLP in production:

1. **Keep Updated**: Always use the latest version
2. **Validate Input**: Sanitize and validate all user input before processing
3. **Resource Limits**: Set appropriate timeouts and resource limits
4. **Dependencies**: Regularly update dependencies
5. **Monitoring**: Monitor for unusual patterns or performance issues

## Automated Security

We use several automated tools to maintain security:

* **Dependabot**: Automatic dependency updates
* **CodeQL**: Automated code security analysis
* **Bandit**: Python security linter
* **Safety**: Dependency vulnerability scanner

## Security Updates

Security updates will be released as:

* **Patch releases** for supported versions
* **Security advisories** on GitHub
* **Announcements** in release notes

## Contact

For security-related questions or concerns:

* Create a **Security Advisory** on GitHub
* Email the maintainers (check GitHub profile)

## Acknowledgments

We thank the security researchers and community members who help keep BidNLP secure.

---

**Thank you for helping keep BidNLP and its users safe!** 🔒
