# SSL/TLS Configuration Guide for Production Deployment

## SSL Certificate Setup

1. Obtain an SSL Certificate
   - Purchase an SSL certificate from a trusted Certificate Authority (CA)
   - OR use Let's Encrypt for a free SSL certificate
   - Generate a CSR (Certificate Signing Request) if required by your CA

2. Install SSL Certificate
   For Nginx:
   ```nginx
   server {
       listen 443 ssl;
       server_name your_domain.com;
       
       ssl_certificate /path/to/your/certificate.crt;
       ssl_certificate_key /path/to/your/private.key;
       
       # Strong SSL Security Settings
       ssl_protocols TLSv1.2 TLSv1.3;
       ssl_prefer_server_ciphers on;
       ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
       
       # HSTS Settings
       add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
   }
   
   # Redirect HTTP to HTTPS
   server {
       listen 80;
       server_name your_domain.com;
       return 301 https://$server_name$request_uri;
   }
   ```

   For Apache:
   ```apache
   <VirtualHost *:443>
       ServerName your_domain.com
       
       SSLEngine on
       SSLCertificateFile /path/to/your/certificate.crt
       SSLCertificateKeyFile /path/to/your/private.key
       
       # Strong SSL Settings
       SSLProtocol all -SSLv3 -TLSv1 -TLSv1.1
       SSLCipherSuite ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384
       SSLHonorCipherOrder on
       
       # HSTS Settings
       Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
   </VirtualHost>
   
   # Redirect HTTP to HTTPS
   <VirtualHost *:80>
       ServerName your_domain.com
       Redirect permanent / https://your_domain.com/
   </VirtualHost>
   ```

3. Production Checklist
   - Set DEBUG = False in Django settings
   - Update ALLOWED_HOSTS with your domain
   - Ensure all static and media files are served over HTTPS
   - Test SSL configuration using SSL Labs (https://www.ssllabs.com/ssltest/)
   - Monitor SSL certificate expiration dates
   - Keep web server and SSL libraries up to date

4. Environment Variables
   Consider storing sensitive settings as environment variables:
   ```python
   SECURE_SSL_REDIRECT = os.environ.get('DJANGO_SECURE_SSL_REDIRECT', 'True') == 'True'
   SECURE_HSTS_SECONDS = int(os.environ.get('DJANGO_SECURE_HSTS_SECONDS', '31536000'))
   ```

5. Regular Maintenance
   - Monitor SSL certificate expiration
   - Regularly update SSL configuration based on security best practices
   - Keep Django and all dependencies updated
   - Regularly review security headers and settings