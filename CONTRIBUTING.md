<!-- Modified for the Odoo Workbench derivative, 2026. Based on the Apache-2.0 upstream project. -->

# Contributing

Bug reports, layout reports and pull requests are welcome. Odoo Workbench is an independent community derivative of [Odoo Dev Panel](https://github.com/SparkDrago05/odoo-dev-panel). Preserve the upstream license and source notices when changing inherited code; see [`NOTICE`](NOTICE).

## Before you start

- **Bugs:** include Ubuntu and Odoo versions, the steps you took, what happened, and sanitized output from `odp --json doctor`. Check for client names you do not want to share first. Do not include passwords, tokens, config files, customer data or database dumps.
- **Security issues:** follow [SECURITY.md](SECURITY.md), not a public issue.
- **A layout that is not discovered:** describe the source, venv, config, filestore, Linux user and PostgreSQL connection layout. Discovery should work across existing setups; provisioning can stay opinionated.
- **Larger changes:** open an issue first so we can agree on a safe approach.
- **Derivative work:** retain Apache-2.0 licensing and add a prominent change notice to modified upstream files in formats that support comments. Do not imply Odoo S.A. endorsement.

## Development setup (Ubuntu 24.04 / 26.04)

Install the native Tauri dependencies:

```sh
sudo apt install build-essential libwebkit2gtk-4.1-dev libsoup-3.0-dev \
    libjavascriptcoregtk-4.1-dev librsvg2-dev libayatana-appindicator3-dev libssl-dev postgresql
```

Install Rust/Cargo, Node.js 22, pnpm 9, Python 3.12 and `uv`, then review `spike/setup-dev-host.sh` before running it. That script configures the local test group and runtime directories.

```sh
sudo spike/setup-dev-host.sh     # optional local privileged-agent test setup
# log out and back in so the odoo-dev group applies
./dev.sh                         # sync the core and start the app with hot reload
./dev.sh test                    # Python-core unit tests
./dev.sh odp agent status        # CLI from the synced copy
./dev.sh shell                   # shell with the odp alias and ODP_* variables
```

`dev.sh` syncs the core into `/opt/odoo-dev-panel/dev` so the run-as users can read it. These runtime paths are retained from the upstream implementation for compatibility.

Build a local package with:

```sh
packaging/build-runtime.sh
cd app && pnpm install && pnpm tauri build
# app/src-tauri/target/release/bundle/deb/
```

## Repository map

| Path | Contents |
|---|---|
| `core/` | Python core and `odp` CLI; standard library runtime |
| `app/` | Tauri 2 + React + TypeScript desktop app; browser preview uses fixtures in `app/src/dev/mock.ts` |
| `packaging/` | Standalone Python runtime, Debian scripts and an APT-repository build scaffold |
| `website/` | Landing page, local visual assets and Markdown-to-HTML docs generator |
| `spike/` | Host setup and container acceptance tests |
| `docs/` | User-facing install and troubleshooting guides |
| `marketing/` | Draft launch copy; verify offers and URLs before publication |

The APT repository scaffold requires a **new Workbench signing key**. The upstream public key has been removed, and the upstream private key must never be reused. The Pages workflow builds the documentation website only.

## Tests

```sh
./dev.sh test
uvx ruff check core/src core/tests --select F
cd app && pnpm exec tsc --noEmit && pnpm test
```

Feature changes also need the relevant container test. The scripts use fresh Ubuntu containers and must be run only on a host configured for the test environment. See the test descriptions in `spike/` before running them.

## Code and safety rules

- Keep the Python core authoritative; the desktop app and CLI should expose the same operations.
- Every mutating action needs a read-only plan with the commands and privilege context visible before execution.
- Never put passwords in command lines, logs, receipts, plans or the registry.
- Never silently delete user data. Move it aside and explain how to restore or remove it.
- Keep discovery read-only and keep Git operations non-destructive.

## Releases and Pages (maintainers)

1. Update the same version in `app/src-tauri/tauri.conf.json`, `app/package.json`, `app/src-tauri/Cargo.toml`, `core/pyproject.toml` and `core/src/odoo_dev_panel/__init__.py`.
2. Push a version tag: `git tag v<version> && git push origin v<version>`.
3. CI verifies the version, runs the tests, builds and smoke-tests the `.deb`, then creates a **draft GitHub release** with the package and `SHA256SUMS`.
4. Review the draft and publish it. The package can then be installed directly from the Releases page.
5. The `Pages` workflow builds the static website from the docs. Configure **Settings → Pages → Build and deployment → GitHub Actions** before enabling deployment.

An independent APT feed, signing key and update pipeline are not configured yet. Add them only after creating and validating a dedicated Workbench key and publishing its public half securely. Do not reuse `packaging/apt/odoo-dev-panel.asc` from upstream; it is not included in this derivative.

The complimentary consultation in the issue template is a maintainer offer, not an automated service. Assign an owner and response process before advertising it.
