# joromero.github.io

## Local preview

Opening HTML files with `file://` blocks `fetch()` (e.g. `raw_data.json` on the irregulars page). Use a local server:

```sh
chmod +x scripts/serve-site.sh   # once
./scripts/serve-site.sh
```

Then open [http://127.0.0.1:8080/irregulars/aphorism.html](http://127.0.0.1:8080/irregulars/aphorism.html). Another port: `PORT=3000 ./scripts/serve-site.sh`.
