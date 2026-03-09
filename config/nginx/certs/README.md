# Local TLS Certificates

Do not commit TLS private keys or certificates to git.

Generate local cert/key files before running `make deploy`:

```bash
make nginx-certs
```

Expected generated files (local only):
- `config/nginx/certs/nyxera.crt`
- `config/nginx/certs/nyxera.key`
