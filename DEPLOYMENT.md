# 🚀 Deployment Guide

This guide covers deploying StudyHub to various platforms.

## Table of Contents
- [Heroku Deployment](#heroku-deployment)
- [DigitalOcean Deployment](#digitalocean-deployment)
- [AWS Deployment](#aws-deployment)
- [Docker Deployment](#docker-deployment)
- [Production Checklist](#production-checklist)

---

## Heroku Deployment

### Prerequisites
- Heroku account
- Heroku CLI installed
- Git repository

### Step-by-Step

1. **Login to Heroku**
```bash
heroku login
```

2. **Create Heroku App**
```bash
heroku create your-app-name
```

3. **Add PostgreSQL Database**
```bash
heroku addons:create heroku-postgresql:mini
```

4. **Set Environment Variables**
```bash
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS="your-app-name.herokuapp.com"
heroku config:set DJANGO_SETTINGS_MODULE="studygroup_platform.settings"
```

5. **Deploy**
```bash
git push heroku main
```

6. **Run Migrations**
```bash
heroku run python manage.py migrate
```

7. **Create Superuser**
```bash
heroku run python manage.py createsuperuser
```

8. **Open App**
```bash
heroku open
```

### Configure Static Files

Add to `settings.py`:
```python
import dj_database_url

# Static files
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Database
DATABASES['default'] = dj_database_url.config(conn_max_age=600)
```

---

## DigitalOcean Deployment

### Using App Platform

1. **Connect GitHub Repository**
   - Login to DigitalOcean
   - Go to App Platform
   - Create New App
   - Connect your GitHub repository

2. **Configure Environment**
   - Select Python environment
   - Set build command: `pip install -r requirements.txt`
   - Set run command: `gunicorn studygroup_platform.wsgi`

3. **Add Database**
   - Add PostgreSQL database component
   - Set environment variables automatically

4. **Configure Domain**
   - Add custom domain in settings
   - Update DNS records

### Using Droplet (Manual)

1. **Create Droplet**
```bash
# Create Ubuntu 22.04 droplet
# SSH into server
ssh root@your-server-ip
```

2. **Install Dependencies**
```bash
apt update
apt install python3-pip python3-venv nginx postgresql postgresql-contrib
```

3. **Setup Project**
```bash
cd /var/www
git clone https://github.com/yourusername/studyhub.git
cd studyhub
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. **Configure PostgreSQL**
```bash
sudo -u postgres psql
CREATE DATABASE studyhub_db;
CREATE USER studyhub_user WITH PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE studyhub_db TO studyhub_user;
\q
```

5. **Configure Nginx**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /static/ {
        alias /var/www/studyhub/staticfiles/;
    }

    location /media/ {
        alias /var/www/studyhub/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

6. **Setup Gunicorn Service**
```bash
sudo nano /etc/systemd/system/gunicorn.service
```

```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/studyhub
ExecStart=/var/www/studyhub/venv/bin/gunicorn \
    --workers 3 \
    --bind 127.0.0.1:8000 \
    studygroup_platform.wsgi:application

[Install]
WantedBy=multi-user.target
```

7. **Start Services**
```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl restart nginx
```

---

## AWS Deployment

### Using Elastic Beanstalk

1. **Install EB CLI**
```bash
pip install awsebcli
```

2. **Initialize EB**
```bash
eb init -p python-3.11 studyhub
```

3. **Create Environment**
```bash
eb create studyhub-env
```

4. **Deploy**
```bash
eb deploy
```

5. **Configure RDS**
```bash
eb create --database
```

### Using EC2

Similar to DigitalOcean Droplet setup but:
- Use Amazon Linux 2 AMI
- Configure Security Groups
- Use RDS for database
- Use S3 for media files
- Configure CloudFront for CDN

---

## Docker Deployment

### Development
```bash
docker-compose up --build
```

### Production

1. **Build Image**
```bash
docker build -t studyhub:latest .
```

2. **Run Container**
```bash
docker run -d \
  -p 8000:8000 \
  --env-file .env.production \
  --name studyhub \
  studyhub:latest
```

3. **With Docker Compose**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

---

## Production Checklist

### Security
- [ ] Set `DEBUG = False`
- [ ] Generate new `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Enable HTTPS/SSL
- [ ] Set secure cookie flags
- [ ] Configure CORS properly
- [ ] Enable CSRF protection
- [ ] Set up firewall rules

### Database
- [ ] Use PostgreSQL (not SQLite)
- [ ] Set up automated backups
- [ ] Configure connection pooling
- [ ] Enable query optimization
- [ ] Set up database replication (optional)

### Static Files
- [ ] Run `collectstatic`
- [ ] Configure WhiteNoise or CDN
- [ ] Enable gzip compression
- [ ] Set cache headers
- [ ] Optimize images

### Performance
- [ ] Enable caching (Redis/Memcached)
- [ ] Configure database indexes
- [ ] Set up query optimization
- [ ] Enable gzip compression
- [ ] Use CDN for static files
- [ ] Configure connection pooling

### Monitoring
- [ ] Set up error tracking (Sentry)
- [ ] Configure logging
- [ ] Set up uptime monitoring
- [ ] Configure performance monitoring
- [ ] Set up alerts

### Backup
- [ ] Database backups (daily)
- [ ] Media files backup
- [ ] Code repository backup
- [ ] Configuration backup
- [ ] Test restore procedures

### Environment Variables
```env
# Production settings
SECRET_KEY=production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_BROWSER_XSS_FILTER=True
SECURE_CONTENT_TYPE_NOSNIFF=True
X_FRAME_OPTIONS=DENY

# AWS S3 (Optional)
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_STORAGE_BUCKET_NAME=your-bucket
AWS_S3_REGION_NAME=us-east-1

# Sentry (Optional)
SENTRY_DSN=your-sentry-dsn
```

### Post-Deployment
- [ ] Test all functionality
- [ ] Check error logs
- [ ] Monitor performance
- [ ] Test email delivery
- [ ] Verify backups
- [ ] Update documentation
- [ ] Announce deployment

---

## Maintenance

### Regular Tasks
- Update dependencies monthly
- Review security advisories
- Check logs weekly
- Monitor disk space
- Optimize database
- Review performance metrics

### Scaling
- Add more workers (gunicorn)
- Enable database replication
- Use load balancer
- Implement caching
- Use CDN
- Optimize queries

---

## Troubleshooting

### Common Issues

**Static files not loading**
```bash
python manage.py collectstatic --noinput
```

**Database connection errors**
- Check DATABASE_URL
- Verify database credentials
- Check network connectivity

**500 Internal Server Error**
- Check error logs
- Verify all environment variables
- Run migrations
- Check file permissions

**Memory issues**
- Increase server resources
- Optimize database queries
- Enable caching
- Reduce worker processes

---

## Support

For deployment issues:
- Check logs: `heroku logs --tail` or `tail -f /var/log/nginx/error.log`
- Email: mohmmadfahad53408@gmail.com
- GitHub Issues: [Report Issue](https://github.com/Fahad13-jpg/studyhub/issues)

---

Made with ❤️ for seamless deployment