# Rennto

Rent management app built with:
- Expo Go + React Native + TypeScript
- FastAPI
- PostgreSQL
- Docker Compose

## Features
- JWT authentication
- Tenant CRUD
- Rent plan CRUD
- Assign a tenant to a plan
- Monthly rent generation endpoint
- Record multiple payments against a rent
- Discounts/waivers
- Tenant-specific history
- Global history
- Dashboard totals
- WhatsApp reminder using the phone's WhatsApp app with a prefilled message

## Run backend

```bash
cd backend
cp .env.example .env
docker compose up --build
```

API docs: http://localhost:8000/docs

Generate monthly rents manually:

```bash
curl -X POST http://localhost:8000/api/v1/rents/generate-monthly \
  -H "Authorization: Bearer YOUR_TOKEN"
```

The endpoint is idempotent: it won't create the same tenant/month rent twice.

## Run mobile app

Install dependencies:

```bash
cd mobile
npm install
```

Set the API URL in `mobile/.env`:

```env
EXPO_PUBLIC_API_URL=http://YOUR-LAN-IP:8000/api/v1
```

For a physical phone using Expo Go, do NOT use `localhost`; use your computer's LAN IP, e.g. `192.168.1.10`.

Start Expo:

```bash
npx expo start
```

Scan the QR code with Expo Go.

## Production notes

This is a complete functional MVP, not a production deployment. Before production:
- use HTTPS
- use a strong secret key
- add refresh-token rotation
- add automated scheduler/worker for monthly generation
- configure PostgreSQL backups
- add rate limiting
- add tests and CI/CD
- use a managed PostgreSQL service or persistent production volume
