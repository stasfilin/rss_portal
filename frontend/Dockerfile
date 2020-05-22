FROM node:latest

RUN mkdir -p /home/node/app/node_modules && chown -R node:node /home/node/app

WORKDIR /home/node/app

USER node
COPY --chown=node:node . .

RUN yarn
RUN yarn global add @vue/cli


CMD ["/frontend/setup_container.sh"]