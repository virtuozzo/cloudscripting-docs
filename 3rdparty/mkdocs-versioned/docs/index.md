# MkDocs Versioned

The `mkdocs-versioned` project adds the ability to build multiple versions of
MkDocs documentation projects. This is a popular requirement, if, for example
you want to set both development docs and those for the stable release. Or, you
may still support an old release and have users using it.


!!! warning

    This work is experimental and should be viewed as a very early alpha, that
    sortof works.


## Usage

Simply install with pip, `pip install mkdocs-versioned` and then use the command
`mkdocs_versioned`. This command is similar to `mkdocs build`, view the `--help`
output to see some of the configuration options.

By default, it will attempt to build all versions, and it will build the latest
docs to both / and /latest. To show a specific version at the root, use
`mkdocs_versioned --default=0.13.0`. Replacing 0.13.0 with the version you want
to use.


!!! warning

    For mkdocs-versioned to work, it assumes that each of the branches can be
    built with the installed version of Mkdocs.


## TODO

- We currently use private mkdocs API's because there isn't a way to hook in
yet. This work is partly helping in providing input on what hooks are needed
for plugins to work well with MkDocs

- Provide a version switcher, like Django has. Currently the only way to switch
version is by hacking the URL and knowing what to look for.

- Build each version to a tmp directory and then move it over. This helps us
avoid the issue of docs having one version fail and being partly built

- How can we better handle changes in MkDocs config in different versions?
For example, an old version of the docs may require an old MkDocs due to an
old setting or maybe a out of date custom theme. I think we probably need to
just say that the branch needs to be buildable with the latest MkDocs. If they
want to render the docs, they should be happy enough doing minor updates to
make sure it builds old versions.

- Versioned URL's like /v1/ could clash with potential internationalisation
URLs, so we may wan to try something like /en/v1/ etc.

- Add plugin support upstream in MkDocs. We need the following entry points.

    1. A way to register extra commands, `mkdocs build-versioned` maybe?
    2. Something to add or modify the config being used. Possibly also adding
       our own config options.
    3, A way to trigger the build multiple times.
