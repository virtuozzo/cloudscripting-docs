---
draft: false
title: "Deploy an Image from a Custom Registry"
aliases: "/custom-registry/"
seoindex: "index, follow"
seotitle: "Deploy an Image from a Custom Registry"
seokeywords: "cloud scripting, docker registry, private registry, settings, image, manifest example"
seodesc: "Deploy an image from a custom container registry."
menu:
    docs:
        title: "Custom Registry"
        url: "/custom-registry/"
        weight: 7
        parent: "samples"
        identifier: "custom-registry"
---

# Deploy an Image from a Custom Registry

An install manifest that asks the user for a container image and private registry credentials, then provisions a node from that image.

The source is kept in the [basic-examples](https://github.com/jelastic-jps/basic-examples/tree/master/custom-registry) repository on GitHub.

## How it works

- `settings.fields` builds the installation form: image name, registry URL, user and password (the latter with `inputType: password`).
- The node definition reads the answers through `${settings.*}` placeholders and passes the credentials in the `registry` block.

## Manifest

{{< tabs >}}
{{< tabs-item title="YAML" >}}
```yaml
# Define the manifest mandatory option: type.
type: install

# Optional parameter. If id is not specified it will be generated automatically.
id: custom-registry

# Defines the required name parameter
name: Example

homepage: "https://docs.cloudscripting.com/"

description:
  short: Deploy an image from a custom container registry.
  text: |
    Cloud Scripting package that requests image and registry credentials via settings
    and provisions a node using the specified private registry.

# Defines user input parameters including simple and UI-based for a JPS installation/update.
settings:
  fields:
    - name: image
      caption: Image
      type: string
      required: true
    - name: registry
      caption: Registry URL
      type: string
      required: true
    - name: reg_user
      caption: User
      type: string
      required: true
    - name: reg_pass
      caption: Password
      type: string
      inputType: password
      required: true
    - {}

# The infrastructure of the environment.
nodes:
  - image: ${settings.image}
    registry:
      url: ${settings.registry}
      user: ${settings.reg_user}
      password: ${settings.reg_pass}
```
{{< /tabs-item >}}
{{< tabs-item title="JSON" >}}
```json
{
  "type": "install",
  "id": "custom-registry",
  "name": "Example",
  "homepage": "https://docs.cloudscripting.com/",
  "description": {
    "short": "Deploy an image from a custom container registry.",
    "text": "Cloud Scripting package that requests image and registry credentials via settings\nand provisions a node using the specified private registry.\n"
  },
  "settings": {
    "fields": [
      {
        "name": "image",
        "caption": "Image",
        "type": "string",
        "required": true
      },
      {
        "name": "registry",
        "caption": "Registry URL",
        "type": "string",
        "required": true
      },
      {
        "name": "reg_user",
        "caption": "User",
        "type": "string",
        "required": true
      },
      {
        "name": "reg_pass",
        "caption": "Password",
        "type": "string",
        "inputType": "password",
        "required": true
      },
      {}
    ]
  },
  "nodes": [
    {
      "image": "${settings.image}",
      "registry": {
        "url": "${settings.registry}",
        "user": "${settings.reg_user}",
        "password": "${settings.reg_pass}"
      }
    }
  ]
}
```
{{< /tabs-item >}}
{{< /tabs >}}

## Deploy the sample

Import the manifest into your Virtuozzo Application Management dashboard: click **Import**, open the **URL** tab, and paste the raw manifest link.

```text
https://raw.githubusercontent.com/jelastic-jps/basic-examples/master/custom-registry/manifest.yaml
```

The [Quick Start](/quick-start/) guide walks through the import dialog step by step.

## What's next?

- [Visual Settings](/visual-settings/)
- [Placeholders](/placeholders/)
- [Basic Configs](/basic-configs/)
- [Samples](/samples/)
