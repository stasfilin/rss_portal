FROM node:13

WORKDIR /frontend
ADD . /frontend

RUN yarn
RUN yarn build

CMD ["/frontend/setup_container.sh"]