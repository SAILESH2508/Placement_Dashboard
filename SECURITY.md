# Security Policy

## Supported Versions

Currently supported versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please follow these steps:

1. **DO NOT** open a public issue
2. Email the security team at: security@placementportal.com
3. Include detailed information about the vulnerability:
   - Type of vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

## Security Best Practices

### For Developers

1. **Never commit sensitive data**
   - API keys
   - Passwords
   - Secret keys
   - Database credentials

2. **Use environment variables**
   - Store all sensitive configuration in `.env` files
   - Never commit `.env` files to version control
   - Use `.env.example` as a template

3. **Keep dependencies updated**
   ```bash
   pip list --outdated
   npm outdated
   ```

4. **Run security checks**
   ```bash
   # Python
   pip install safety
   safety check
   
   # Node.js
   npm audit
   ```

### For Deployment

1. **Set DEBUG=False in production**
2. **Use strong SECRET_KEY**
3. **Configure ALLOWED_HOSTS properly**
4. **Use HTTPS/SSL certificates**
5. **Enable security headers**
6. **Use a production database (PostgreSQL)**
7. **Regular backups**
8. **Monitor logs for suspicious activity**

## Known Security Considerations

### Current Implementation

1. **JWT Tokens**
   - Access tokens expire in 60 minutes
   - Refresh tokens expire in 7 days
   - Tokens are stored in localStorage (consider httpOnly cookies for production)

2. **Password Requirements**
   - Minimum 8 characters
   - Django's built-in password validators

3. **CORS**
   - Currently allows all origins in development
   - Must be restricted in production

4. **Rate Limiting**
   - Not currently implemented
   - Should be added for production

### Recommendations for Production

1. **Implement rate limiting**
   ```python
   # Install django-ratelimit
   pip install django-ratelimit
   ```

2. **Add CAPTCHA for registration/login**
   ```python
   # Install django-recaptcha
   pip install django-recaptcha
   ```

3. **Enable Django security middleware**
   - Already configured in settings.py for production

4. **Use httpOnly cookies for tokens**
   - More secure than localStorage
   - Prevents XSS attacks

5. **Implement 2FA (Two-Factor Authentication)**
   - Consider django-otp or similar

6. **Add API request logging**
   - Monitor for suspicious patterns
   - Already configured basic logging

7. **Regular security audits**
   - Code reviews
   - Penetration testing
   - Dependency scanning

## Security Checklist for Production

- [ ] DEBUG=False
- [ ] Strong SECRET_KEY (50+ random characters)
- [ ] ALLOWED_HOSTS configured
- [ ] HTTPS enabled
- [ ] Security headers enabled
- [ ] CORS properly configured
- [ ] Database credentials secured
- [ ] Email credentials secured
- [ ] API keys in environment variables
- [ ] Rate limiting enabled
- [ ] CAPTCHA on auth endpoints
- [ ] Regular backups configured
- [ ] Logging and monitoring enabled
- [ ] Dependencies updated
- [ ] Security audit completed

## Incident Response

In case of a security incident:

1. **Immediate Actions**
   - Isolate affected systems
   - Change all credentials
   - Notify users if data breach occurred

2. **Investigation**
   - Review logs
   - Identify attack vector
   - Assess damage

3. **Remediation**
   - Patch vulnerabilities
   - Update security measures
   - Document incident

4. **Prevention**
   - Implement additional security measures
   - Update security policies
   - Train team members

## Contact

For security concerns, contact:
- Email: security@placementportal.com
- Emergency: [Emergency contact number]

---

**Last Updated**: November 2025
