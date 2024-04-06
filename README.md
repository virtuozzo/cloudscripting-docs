# Staging the Docs on Your Local Machine

This guide walks you through the process of staging the documentation locally using either a Devbox or a Dev Container. First, you need to clone the repository:

```bash
git clone git@github.com:virtuozzo/cloudscripting-docs.git
cd cloudscripting-docs
```

After cloning the repository, you have two options to run the docs web server: using a Devbox isolated shell or a Dev Container.

**Devbox** provides a faster alternative by installing all dependencies into an isolated shell, while **Dev Container** offers more isolation and could be simpler to install.

## Using Devbox

Devbox is recommended for users who prefer a quick setup with isolated environments. Follow these steps to use Devbox:

1. Install Devbox from [here](https://www.jetpack.io/devbox/docs/installing_devbox/).
2. To start the docs web server, execute one of the following commands:

    ```bash
    devbox run serve
    ```

    or

    ```bash
    devbox shell
    task serve
    ```

Alternatively, in VS Code, you can run the `Start the Docs web server` task, which automatically starts the local server for the documentation. To do this:

- Use the command palette in VS Code (Ctrl+Shift+P or Cmd+Shift+P), type `Tasks: Run Task`, and select `Start the Docs web server`.
- Or, navigate to `Terminal -> Run Task...` and choose `Start the Docs web server`.

## Using a Dev Container

For those preferring VS Code and seeking greater isolation, the Dev Container method is ideal. Follow these steps:

1. Install the **Dev Containers** extension in VS Code.
2. Open the `cloudscripting-docs` repository in VS Code.
3. Use the command palette (Ctrl+Shift+P or Cmd+Shift+P), type `Dev Containers: Reopen in Container`, and select it.
4. VS Code will rebuild the container using the `.devcontainer` folder's configuration.
5. Once the container is ready, you're set to work within the Dev Container environment.
6. To start the docs, issue this command in the integrated terminal:

    ```bash
    task serve
    ```

MkDocs will incrementally rebuild the site with each file change. Keep your browser open to [http://localhost:8000/](http://localhost:8000/) and refresh to view updates. Use CTRL+C in the terminal to stop the server.