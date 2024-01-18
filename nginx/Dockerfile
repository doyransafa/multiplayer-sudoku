FROM nginx:1.25

RUN rm /etc/nginx/conf.d/default.conf
RUN mkdir -p /home/app/web/staticfiles
COPY nginx.conf /etc/nginx/conf.d