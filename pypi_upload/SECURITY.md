# Security Policy

## Supported Versions

We release patches for security vulnerabilities. The table below indicates which versions are currently supported:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | ✅ Yes             |
| < 1.0   | ❌ No              |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly by contacting us directly at [shiboshreeroycse@gmail.com](mailto:shiboshreeroycse@gmail.com).

Please do not report security vulnerabilities through public GitHub issues.

When reporting a vulnerability, please include:
- A clear description of the issue
- Steps to reproduce the vulnerability
- Potential impact of the vulnerability
- Any suggested fixes (if known)

## Security Updates

We will publish security advisories for confirmed vulnerabilities through GitHub Security Advisories. We will also update the affected packages on PyPI.

## Best Practices

When using ShiboScript, consider the following security best practices:

- Sanitize all user inputs before processing
- Be cautious when executing external commands
- Validate and sanitize file paths when reading/writing files
- Be careful with network requests and validate URLs
- Keep your ShiboScript installation up to date
