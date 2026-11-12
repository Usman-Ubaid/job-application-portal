FROM node:22-alpine AS base

WORKDIR /app

COPY package.json package-lock.json ./

# ───────────────────────────────────────────
# Development stage
# ───────────────────────────────────────────
FROM base AS dev

RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]

# ───────────────────────────────────────────
# Builder stage — compiles the Next.js app
# (only used on the path to prod)
# ───────────────────────────────────────────
FROM base AS builder

RUN npm ci

COPY . .

RUN npm run build

# ───────────────────────────────────────────
# Production stage — lean final image
# ───────────────────────────────────────────
FROM node:22-alpine AS prod

WORKDIR /app

ENV NODE_ENV=production

COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000

CMD ["node", "server.js"]