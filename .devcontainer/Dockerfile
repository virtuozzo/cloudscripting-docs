FROM jetpackio/devbox:latest

# Installing your devbox project
WORKDIR /code
USER root:root
RUN mkdir -p /code && chown ${DEVBOX_USER}:${DEVBOX_USER} /code
USER ${DEVBOX_USER}:${DEVBOX_USER}

COPY --chown=${DEVBOX_USER}:${DEVBOX_USER} 3rdparty ./3rdparty
COPY --chown=${DEVBOX_USER}:${DEVBOX_USER} plugins ./plugins

COPY --chown=${DEVBOX_USER}:${DEVBOX_USER} devbox.json devbox.json
COPY --chown=${DEVBOX_USER}:${DEVBOX_USER} devbox.lock devbox.lock
COPY --chown=${DEVBOX_USER}:${DEVBOX_USER} Pipfile Pipfile$
COPY --chown=${DEVBOX_USER}:${DEVBOX_USER} Pipfile.lock Pipfile.lock
COPY --chown=${DEVBOX_USER}:${DEVBOX_USER} Taskfile.yaml Taskfile.yaml

RUN devbox run -- echo "Installed Packages."
RUN devbox shellenv --init-hook >> ~/.profile 
