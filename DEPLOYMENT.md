# Deployment Guide

## Docker Compose Deployment (Recommended for Phase 1)

### Prerequisites
- Docker 20.10+
- docker-compose 2.0+
- 2GB RAM minimum
- 10GB disk space

### Production Deployment

1. **Clone repository**
```bash
git clone <repository-url>
cd instant-integrity-mvp
```

2. **Configure environment**
```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env`:
```bash
# Required
DATABASE_URL=postgresql://user:STRONG_PASSWORD@postgres:5432/integrity
REDIS_URL=redis://redis:6379/0
JWT_SECRET=GENERATE_STRONG_RANDOM_SECRET_HERE
JWT_ALGORITHM=HS256

# Email (choose one)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
# OR
SENDGRID_API_KEY=SG.xxx

FROM_EMAIL=noreply@yourdomain.com

# Optional
SENTRY_DSN=https://xxx@sentry.io/xxx
SENTRY_ENVIRONMENT=production
```

3. **Start services**
```bash
docker-compose up -d
```

4. **Run migrations**
```bash
docker-compose exec backend alembic upgrade head
```

5. **Verify health**
```bash
curl http://localhost:8000/health
```

### Security Checklist

- [ ] Change default database password
- [ ] Generate strong JWT_SECRET (32+ characters)
- [ ] Configure real email service
- [ ] Enable HTTPS (use reverse proxy like Nginx)
- [ ] Set up firewall rules
- [ ] Configure CORS_ORIGINS for your domain
- [ ] Enable Sentry for error tracking
- [ ] Set up database backups
- [ ] Review rate limiting settings

### Monitoring

**Health Check**
```bash
curl http://localhost:8000/health
```

**View Logs**
```bash
docker-compose logs -f backend
docker-compose logs -f postgres
docker-compose logs -f redis
```

**Database Backup**
```bash
docker-compose exec postgres pg_dump -U user integrity > backup.sql
```

### Scaling

For production scaling, consider:
1. Kubernetes deployment (Phase 4)
2. Managed PostgreSQL (AWS RDS, Google Cloud SQL)
3. Managed Redis (AWS ElastiCache, Redis Cloud)
4. Load balancer for multiple backend instances
5. CDN for static assets

### Troubleshooting

**Container won't start**
```bash
docker-compose down
docker-compose up -d
docker-compose logs backend
```

**Database connection failed**
```bash
docker-compose exec postgres psql -U user -d integrity
```

**Reset database**
```bash
docker-compose down -v
docker-compose up -d
docker-compose exec backend alembic upgrade head
```

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| DATABASE_URL | Yes | - | PostgreSQL connection string |
| REDIS_URL | Yes | - | Redis connection string |
| JWT_SECRET | Yes | - | Secret for JWT signing |
| JWT_ALGORITHM | No | HS256 | JWT algorithm |
| JWT_EXPIRATION_MINUTES | No | 60 | Token expiration |
| SMTP_HOST | No | - | SMTP server host |
| SMTP_PORT | No | - | SMTP server port |
| SMTP_USER | No | - | SMTP username |
| SMTP_PASSWORD | No | - | SMTP password |
| SENDGRID_API_KEY | No | - | SendGrid API key |
| FROM_EMAIL | No | noreply@instantintegrity.com | Sender email |
| VERIFICATION_TOKEN_EXPIRY_HOURS | No | 24 | Email token expiry |
| RATE_LIMIT_ENABLED | No | true | Enable rate limiting |
| SENTRY_DSN | No | - | Sentry error tracking |
| SENTRY_ENVIRONMENT | No | development | Sentry environment |
| CORS_ORIGINS | No | * | Allowed CORS origins |
| APP_ENV | No | development | Application environment |
| DEBUG | No | false | Debug mode |
