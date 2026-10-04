# Security Policy

## Supported Versions

Commit Critter is distributed as a GitHub Action. Security fixes ship as new patch releases, and the major-version tag (`v1`) is moved to point at them, so workflows using `@v1` get fixes automatically.

| Version | Supported          |
| ------- | ------------------ |
| 1.x (`@v1`) | :white_check_mark: |
| unreleased `main` | :x: (use a tagged release) |

## Reporting a Vulnerability

**Please don't open a public issue for security problems.**

Report privately through GitHub instead:

1. Go to this repository's **Security** tab.
2. Click **Report a vulnerability**.
3. Describe the issue, how to reproduce it, and what an attacker could do with it.

What to expect:

- **Acknowledgement within 7 days.** Commit Critter is maintained by one person in their spare time, so please allow for that.
- **Progress updates at least every 14 days** until the report is resolved.
- **If the report is accepted:** I'll work on a fix in a private security advisory, release a patched version, move the `v1` tag, and publish the advisory. You'll be credited unless you'd rather stay anonymous.
- **If it's declined:** I'll explain why, for example because it's out of scope (see below) or isn't exploitable in practice.

Please give me a reasonable chance to release a fix before disclosing publicly. 90 days is the default, or sooner once a fix is out.

## Scope

Commit Critter runs inside **your own** GitHub Actions workflow, with the token you give it. It needs `contents: write` to commit to your repo. It reads only your **public** GitHub events and profile, and it sends no data anywhere except GitHub's API.

**In scope**, for example:

- Anything that lets a third party run code in, or push to, a repo that uses the action
- The action leaking or misusing the workflow token
- Inputs or API responses that can break out of the shell steps (script injection)
- The action writing outside the configured README and `.critter/` folder

**Out of scope:**

- Content you put into your own README through your own inputs (for example, Markdown or HTML in `pet-name`)
- Vulnerabilities in GitHub Actions itself, the runner images, or `actions/checkout`. Please report those to GitHub.
- Contribution-graph or streak behaviour. That's a feature question, so open a normal issue.

## Hardening Tips for Users

- **Pin to a commit SHA** for maximum supply-chain safety, e.g. `uses: Diacod-I/commit-critter@<full-commit-sha>  # v1.0.0`. Dependabot can keep it updated.
- **Keep permissions minimal.** The workflow only needs `permissions: contents: write`.
- **Use the default `GITHUB_TOKEN`.** Don't pass a personal access token unless you have a specific reason to. The default token is scoped to the one repo and expires when the job ends.
