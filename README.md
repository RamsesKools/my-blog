# my-blog

A personal blog where I write about things I build, learn, and think about.
Topics are ranging from:

- Data-Engineering, Software-Engineering

## Ideas behind it

- Writing as a way to solidify thinking, not just to publish
- Short, focused posts over long comprehensive guides
- Honest about what's in progress or unfinished
- No tracking, no ads, no newsletter prompts

## Deployment

The preview site at `https://blog-preview.ramseskools.nl` is auto-deployed via a Dagu DAG (`blog-preview-deploy`). It polls this repo every 5 minutes for new commits and rebuilds with `mkdocs build`. The built `site/` directory is served by nginx.

The DAG supports three modes via the `MODE` parameter:

| Mode | Trigger | Behavior |
|---|---|---|
| `check` (default) | Scheduled (every 5 min) | Fetch + compare, skip if no new commits |
| `force` | Manual | Fetch + compare, pull and build regardless |
| `deploy` | Manual | Skip fetch/pull, rebuild from current state |

Manual runs with a mode override:

```bash
dagu start /opt/dagu/dags/blog-preview-deploy.yaml -- MODE=force
dagu start /opt/dagu/dags/blog-preview-deploy.yaml -- MODE=deploy
```
