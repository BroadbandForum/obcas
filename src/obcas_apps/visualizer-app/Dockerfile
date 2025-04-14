FROM node:20-alpine

WORKDIR /alarms-correlation/

COPY ./condor-utils-1.0.3.tgz /alarms-correlation/
COPY ./src/ /alarms-correlation/src/
COPY ./public/ /alarms-correlation/public/
COPY ./package.json /alarms-correlation/
COPY ./config-overrides.js /alarms-correlation/
COPY ./.env /alarms-correlation/.env
COPY ./package-lock.json /alarms-correlation/
COPY ./node_modules/ /alarms-correlation/node_modules/

EXPOSE 3000/tcp

ENV REACT_APP_INGRESS_HOST=http://localhost
ENV REACT_APP_CONDOR_URL=https://www.google.com.ar

RUN npm install
CMD ["npm", "start"]


