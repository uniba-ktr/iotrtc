FROM docker:dind AS dind

FROM node:current-bullseye-slim

# add support for gpio library
RUN apt update && apt install -y python3-pip wget
RUN pip install RPi.GPIO

# Home directory for Node-RED application source code and user data directory.
RUN mkdir -p /usr/src/node-red && mkdir /data
WORKDIR /usr/src/node-red

# package.json contains Node-RED NPM module and node dependencies
COPY package.json /usr/src/node-red/
RUN npm install

# Copy Docker CLI
COPY --from=dind /usr/local/bin/docker /usr/local/bin/docker

# User configuration directory volume
EXPOSE 1880

# Environment variable holding file path for flows configuration
ENV FLOWS=flows.json
ENV NODE_PATH=/usr/src/node-red/node_modules:/data/node_modules

ENTRYPOINT ["npm"]
CMD ["start", "--", "--userDir", "/data"]
