# Cloud Scripting Documentation

This repository contains the source files for the Cloud Scripting documentation. The documentation is built using [MkDocs](https://www.mkdocs.org/), a static site generator geared towards project documentation.

Topics submitted here will be published to the [Cloud Scripting portal](https://docs.cloudscripting.com/).

To start editing the documentation in the cloud or on your local machine, follow the instructions below.

## Developing In The Cloud

When it comes to editing Git-based documentation in the cloud, there are multiple solutions to choose from. For minor changes in a single file, the GitHub interface can be suitable. However, for more extensive modifications, you might prefer a more comprehensive development environment. Some popular alternatives include GitHub Codespaces, github.dev and Devbox Cloud.

The choice of which solution to use depends on your specific needs and preferences. Whether you prioritize a comprehensive development environment, a lightweight web-based editor, or a fast and convenient editing experience, there is a solution available to suit your requirements.

### GitHub Codespaces

GitHub Codespaces provides a comprehensive development environment in the cloud, allowing you to easily edit and preview the documentation. It offers a full-featured development environment with a terminal, code editor, and integrated Git support. When you open the repository in GitHub Codespaces, the Dev Container with Devbox inside and the [VS Code extensions](#vs-code-preinstalled-extensions) will be automatically built and started.

To use GitHub Codespaces, follow these steps:

1. Fork the repository to your GitHub account.
2. Follow to [GitHub Codespaces](https://github.com/codespaces) and click on the `New codespace` button.
3. Select the forked repository from the list of repositories.
4. Select your region and machine type (the 2-core machine would be enough for this repository).
5. Wait for the Codespace to be created. The Dev Container will be automatically built and started.
6. After the Codespace is ready, execute the following commands in the integrated terminal to start the docs web server:

    ```bash
    task serve
    ```

   Alternatively, you can run the `Start the Docs web server` task in VS Code. To do this, select `Terminal -> Run Task...` in the main menu and choose `Start the Docs web server`.
7. After the web server is started, click on the `Open in browser` button to preview the documentation.
8. Make some changes in the documentation and see that changes are reflected in the browser.
9. Create a pull request to contribute the changes.

[More info](https://docs.github.com/en/codespaces) about GitHub Codespaces.

### The github.dev Web-Based Editor

The github.dev editor introduces a lightweight editing experience that runs entirely in your browser. With the github.dev editor, you can navigate files and source code repositories from GitHub, and make and commit code changes. You can open any repository, fork, or pull request in the editor.

#### Opening the github.dev editor

You can open the GitHub repository in `github.dev` in either of the following ways:

- To open the repository in the same browser tab, press `.` while browsing the repository or pull request on GitHub.
- To open the repository in a new browser tab, press `>`.
- Change the URL from `github.com` to `github.dev`.
- When viewing a file, select the `▾` dropdown menu and click `github.dev`.

The drawback of the github.dev editor is that it doesn't provide a built-in terminal to start the web server. Therefore, you can only preview the changes in real-time, file by file, as a rendered Markdown. However, it's a great option for quick edits and minor contributions.

Also, if you need more advanced features, you can navigate to Run and Debug section in the left sidebar and click on the `Continue Working On...` button to open the repository in GitHub Codespaces.

[More info](https://docs.github.com/en/codespaces/the-githubdev-web-based-editor) about the github.dev editor.

### Devbox Cloud

Devbox Cloud is a fast alternative to GitHub Codespaces, allowing you to instantly preview changes in the documentation without setting up a local development environment. However, it doesn't provide a full-featured development environment with VS Code extensions like GitHub Codespaces.

To use Devbox Cloud, follow these steps:

1. Fork the repository to your GitHub account.
2. Open [devbox.sh](https://devbox.sh/) in your browser.
3. Paste the forked repository URL in the input field and click **Go**.
4. After the integrated terminal is ready, execute the following command to start the docs web server:

    ```bash
    task serve
    ```

5. Open a new tab in your browser and paste your current Devbox project link in the address bar. Then, add `/port/8000` at the end of the link. For example, if your Devbox project link is `https://devbox.sh/app/projects/proj_your_project_id`, the new link should be `https://devbox.sh/app/projects/proj_your_project_id/port/8000`.
6. Make some changes in the documentation and see that changes are reflected in the browser.
7. To contribute the changes, add Devbox Cloud GitHub App to your forked repository and create a pull request.

[More info](https://www.jetpack.io/devbox/docs/devbox_cloud/) about Devbox Cloud.

## Staging the Docs on Your Local Machine

This guide is intended for those who prefer to develop locally. Please note that setting up the local development environment may require additional effort.

To get started, you need to clone the repository:

```bash
git clone git@github.com:virtuozzo/cloudscripting-docs.git
cd cloudscripting-docs
```

After cloning the repository, you have two options to run the docs web server: using a Devbox isolated shell or a Dev Container.

**Devbox** provides a faster alternative by installing all dependencies into an isolated shell without an extra layer of virtualization slowing down your file system or every command. On the other hand, **Dev Container** offers more isolation and provides greater portability, allowing you to easily share and replicate your development environment across different machines. The Dev Container in this repository uses **Devbox** inside to provide a consistent shell for everyone who uses it.

### Using Devbox

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

### Using a Dev Container

For those seeking greater isolation and portability, the Dev Container method is a better choice. It provides a consistent environment for everyone who uses it, ensuring that the documentation is built and served in the same way across different machines. The Dev Container in this repository is configured to use the Devbox inside, so you can use either method to run the docs web server.

Here are the steps to use Dev Container in VS Code:

1. Install [Docker Engine](https://docs.docker.com/engine/install/) if you don't already have it installed.
2. Install the **Dev Containers** extension in VS Code.
3. Open the `cloudscripting-docs` repository in VS Code.
4. Use the command palette (Ctrl+Shift+P or Cmd+Shift+P), type `Dev Containers: Reopen in Container`, and select it.
5. VS Code will rebuild the container using the `.devcontainer` folder's configuration.
6. Once the container is ready, you're set to work within the Dev Container environment.
7. To start the docs, issue this command in the integrated terminal:

    ```bash
    task serve
    ```

8. Open your browser and navigate to [http://localhost:8000/](http://localhost:8000/) to preview the documentation. MkDocs will incrementally rebuild the site with each file change and those changes will be reflected in the browser.
9. To contribute the changes, create a pull request.

> **Note:**
> If the repository was cloned using SSH instead of HTTPS, to work with the remote repository from the Dev Container, you need to make sure that your SSH key is added to your local SSH agent. You can follow the instructions [here](https://code.visualstudio.com/remote/advancedcontainers/sharing-git-credentials#_using-ssh-keys) on how to do it. In most cases, executing `ssh-add $HOME/.ssh/path_to_your_ssh_private_key` should be sufficient.
>

#### VS Code Preinstalled Extensions

In addition, the Dev Container in this repository is configured to install necessary VS Code extensions automatically. Here are the extensions that will be installed:

- [devbox by jetpack.io](https://marketplace.visualstudio.com/items?itemName=jetpack-io.devbox)
- [Markdown All in One](https://marketplace.visualstudio.com/items?itemName=yzhang.markdown-all-in-one)
- [Code Spell Checker](https://marketplace.visualstudio.com/items?itemName=streetsidesoftware.code-spell-checker)
- [markdownlint](https://marketplace.visualstudio.com/items?itemName=DavidAnson.vscode-markdownlint)
- [Markdown Preview Enhanced](https://marketplace.visualstudio.com/items?itemName=shd101wyy.markdown-preview-enhanced)
- [GitHub Copilot](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) with enabled Markdown support. This extension is optional but highly recommended for long-term use. It requires an active GitHub Copilot subscription.
- [GitHub Copilot Chat](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat). This extension is also optional but highly recommended for long-term use. It also requires an active GitHub Copilot subscription.
