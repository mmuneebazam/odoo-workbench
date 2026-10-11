<!-- Modified for the Odoo Workbench derivative, 2026. Based on the Apache-2.0 upstream project. -->

# Install and first run

Odoo Workbench is a desktop app and companion CLI for **Ubuntu 24.04 or 26.04 on x86_64**. It can discover installations that already exist on the machine; you do not need to move them into a new directory layout.

> **Derivative release status:** this repository does not yet have its own signed APT feed or update channel. Do not use the upstream project's APT signing key for Workbench. When a Workbench release is published, install the `.deb` artifact from this repository's Releases page.

## Install a published package

Download the `odoo-workbench_<version>_amd64.deb` asset from Releases and install it with APT so dependencies are handled:

```sh
sudo apt install ./odoo-workbench_<version>_amd64.deb
```

Then add your account to the `odoo-dev` group and log out and back in:

```sh
sudo usermod -aG odoo-dev "$USER"
```

Start **Odoo Workbench** from the application menu. The first time an agent is used for a run-as user, Workbench asks you to unlock it once for that boot. See the [security model](../SECURITY.md) and [troubleshooting](troubleshooting.md) if anything is unclear.

## Develop from source

The source build is intended for contributors. The current Tauri app uses a React/TypeScript frontend and the Python core is standard-library based.

1. Use Python 3.12, Node.js 22, pnpm 9, Rust/Cargo, and `uv`.
2. Install the native dependencies needed for Tauri/WebKitGTK on Ubuntu. The [CI workflow](../.github/workflows/ci.yml) lists the current packages.
3. Review `spike/setup-dev-host.sh`; it prepares the local development group, runtime directories and test host. Run it only if you are comfortable with the system changes it makes.
4. From the repository root:

   ```sh
   ./dev.sh       # sync the core and run the desktop app with hot reload
   ./dev.sh test  # run the Python-core unit tests
   ```

The same command-line capabilities are available through `odp`. Add `--json` to CLI commands for machine-readable output.

## First run

- Choose **Scan again** to discover existing installations, configs, databases and processes.
- Use **Doctor** for a read-only health report before attempting repairs.
- Start an instance from a discovered config, or provision a fresh Odoo installation.
- For a database upgrade, review the plan and enable a snapshot before the operation.
- Follow the session logs from **Sessions**; closing the desktop app does not stop Odoo.

## Config permissions

Odoo config files contain database and admin passwords. The recommended local layout is:

| Item | Owner | Group | Mode |
| --- | --- | --- | --- |
| Config file | developer | run-as user's group | `0640` |
| Config file when the developer is the run-as user | developer | developer | `0600` |
| Folder dedicated to one installation | developer | run-as user's group | `2750` |

This lets you edit the config without `sudo`, lets Odoo read it through its group, and keeps other local users from reading passwords. Doctor checks common permission issues. **Fix permissions** uses one reviewed privileged step and keeps a receipt of previous owners/modes; shared folders such as `/etc/odoo` are not changed automatically.

## Compatibility note

The product and repository are named **Odoo Workbench**. The inherited core still uses the `odp` CLI name and retains some `odoo-dev-panel` runtime/config paths to avoid an unsafe in-place migration. These implementation identifiers do not imply an official Odoo product.
