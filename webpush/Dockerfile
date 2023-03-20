FROM arm32v7/node:current-stretch-slim

WORKDIR /usr/src/app

COPY . .

RUN npm install

EXPOSE 3000

ENTRYPOINT [ "node" ]
CMD [ "app" ]
