For run client, need write you RCON credentials:
- RCON_ADDR
- RCON_PORT (maybe leave default 27015)
- RCON_PASS
to docker-compose.yml:factorio_rcon:environment

and exec command:

```
docker-compose up -d --build
```

