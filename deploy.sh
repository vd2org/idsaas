#!/usr/bin/env sh

set -e

rsync -rltvv --del -compress-level=9 -e ssh --exclude 'node_modules' --exclude '.git' --exclude '.idea' --exclude '.code' . root@${IDSAAS_HOST}:/opt/idsaas
ssh root@${IDSAAS_HOST} "cd /opt/idsaas && CF_EMAIL=${CF_EMAIL} CF_ZONE_API_TOKEN=${CF_ZONE_API_TOKEN} CF_DNS_API_TOKEN=${CF_DNS_API_TOKEN} docker compose -f compose-master.yml build"
ssh root@${IDSAAS_HOST} "cd /opt/idsaas && CF_EMAIL=${CF_EMAIL} CF_ZONE_API_TOKEN=${CF_ZONE_API_TOKEN} CF_DNS_API_TOKEN=${CF_DNS_API_TOKEN} docker compose -f compose-master.yml up -d"
