# my-blog

A personal blog where I write about things I build, learn, and think about.
Topics (will) range from:

- Data Engineering
- Software Engineering
- DevOps and Cloud
- Using AI tools and building custom AI tools
- Things I like
- Projects I've worked on

## Ideas behind it

- Writing as a way to solidify thinking, not just to publish
- Short, focused posts over long comprehensive guides
- Honest about what's in progress or unfinished
- No tracking, no ads, no newsletter prompts

## Deployment

Two deployment targets: `blog-preview.ramseskools.nl` (private preview, accessible via VPN or local network) and `blog.ramseskools.nl` (public, on GitHub Pages).

### Deployment to preview

The preview site at `https://blog-preview.ramseskools.nl` is auto-deployed via a Dagu DAG (`blog-preview-deploy`).
It polls this repo every 5 minutes for new commits and rebuilds with `mkdocs build`.
The built `site/` directory is served by nginx.

The DAG supports three modes via the `MODE` parameter:

| Mode | Trigger | Behavior |
| --- | --- | --- |
| `check` (default) | Scheduled (every 5 min) | Fetch + compare, skip if no new commits |
| `force` | Manual | Fetch + compare, pull and build regardless |
| `deploy` | Manual | Skip fetch/pull, rebuild from current state |

Manual runs with a mode override:

```bash
dagu start /opt/dagu/dags/blog-preview-deploy.yaml -- MODE=force
dagu start /opt/dagu/dags/blog-preview-deploy.yaml -- MODE=deploy
```

### Deployment to GitHub Pages

The public site at `https://blog.ramseskools.nl` is deployed via the GitHub Actions workflow `.github/workflows/deploy-gh-pages.yml`.

**Triggers:**

- **GitHub Release** - automatically deploys the tagged commit when a release is published.
- **Manual (`workflow_dispatch`)** - can be triggered from the Actions tab in GitHub.

**What it does:**

When triggered manually, the workflow first checks whether the current commit already has a tag.
If not, it creates a CalVer release tag (`YYYY.MM.DD`, auto-incrementing on same-day releases) and generates release notes from commits.
It then checks out that tagged commit, builds the site with `uv run mkdocs build`, and deploys the `site/` directory to GitHub Pages.
