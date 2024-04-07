# Cloud Scripting Documentation

This repository contains the source files for the Cloud Scripting documentation. The documentation is built using [MkDocs](https://www.mkdocs.org/), a static site generator geared towards project documentation.

Topics submitted here will be published to the [Cloud Scripting portal](https://docs.cloudscripting.com/).

To start editing the documentation on your local machine or in the cloud, follow the instructions below.

## Staging the Docs on Your Local Machine

This guide walks you through the process of staging the documentation locally using either a Devbox or a Dev Container. First, you need to clone the repository:

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

For those seeking greater isolation and portability, the Dev Container method is ideal. Here are the steps to use Dev Container in VS Code:

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

If the repository was cloned using SSH instead of HTTPS, to work with the remote repository from the Dev Container, you need to make sure that your SSH key is added to your local SSH agent. You can follow the instructions [here](https://code.visualstudio.com/remote/advancedcontainers/sharing-git-credentials#_using-ssh-keys) on how to do it. In most cases, executing `ssh-add $HOME/.ssh/path_to_your_ssh_private_key` should be sufficient.

### Developing on Local Machine

MkDocs will incrementally rebuild the site with each file change. Keep your browser open to [http://localhost:8000/](http://localhost:8000/) and refresh to view updates. Use CTRL+C in the terminal to stop the server.

## Developing In The Cloud

When it comes to editing Git-based documentation in the cloud, there are multiple solutions to choose from. For minor changes in a single file, the GitHub interface can be suitable. However, for more extensive modifications, you might prefer a more comprehensive development environment. Some popular alternatives include GitHub Codespaces, github.dev, and Devbox Cloud.

The github.dev is a lightweight web-based editor that offers a quick and convenient way to contribute without the need to start a web server and preview the entire end result.

GitHub Codespaces provides a comprehensive development environment in the cloud, allowing you to easily edit and preview the documentation. It offers a full-featured development environment with a terminal, code editor, and integrated Git support.

Devbox Cloud is a fast alternative to GitHub Codespaces, allowing you to instantly preview changes in the documentation without setting up a local development environment.

The choice of which solution to use depends on your specific needs and preferences. Whether you prioritize a comprehensive development environment, a lightweight web-based editor, or a fast and convenient editing experience, there is a solution available to suit your requirements.

## The github.dev Web-Based Editor

The github.dev editor introduces a lightweight editing experience that runs entirely in your browser. With the github.dev editor, you can navigate files and source code repositories from GitHub, and make and commit code changes. You can open any repository, fork, or pull request in the editor.

The github.dev editor is available to everyone for free on GitHub.com.

### Opening the github.dev editor

You can open any GitHub repository in `github.dev` in either of the following ways:

- To open the repository in the same browser tab, press `.` while browsing the repository or pull request on GitHub.
- To open the repository in a new browser tab, press `>`.
- Change the URL from `github.com` to `github.dev`.
- When viewing a file, select the `▾` dropdown menu and click `github.dev`.

[More info](https://docs.github.com/en/codespaces/the-githubdev-web-based-editor)

## GitHub Codespaces

https://github.com/features/codespaces

## Devbox Cloud

For those who prefer developing in the cloud and wants to instantly preview the end result, the Devbox Cloud is the best option. To use Devbox Cloud, follow these steps:

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
