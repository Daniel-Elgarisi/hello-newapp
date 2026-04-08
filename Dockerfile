FROM nginx:alpine

ARG VERSION=1
LABEL VERSION=${VERSION}

COPY index.html /usr/share/nginx/html/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
