#!/usr/bin/env sh
set -e

# Aguardar banco ficar disponível
if [ -n "$DB_HOST" ]; then
  echo "Aguardando Postgres em $DB_HOST:$DB_PORT..."
  until nc -z $DB_HOST ${DB_PORT:-5432}; do
    sleep 1
  done
fi

# Rodar migrações apenas quando habilitado
if [ "${RUN_MIGRATIONS}" = "1" ]; then
  echo "Executando migrações..."
  python manage.py migrate --noinput

  echo "Carregando dados iniciais..."
  python manage.py loaddata core/fixtures/dados.json || echo "Nenhum fixture encontrado."
fi

exec "$@"

