FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf 

RUN mkdir -p  /app/log/d_blog/nginx /app/d_blog/ 
RUN chown -R www-data:www-data /app/d_blog/ /app/log/d_blog/nginx \
&& chmod -R 775 /app/d_blog/ /app/log/d_blog/nginx

ADD ./d_blog.conf /etc/nginx/conf.d/
RUN sed -i 's/default.conf/d_blog.conf/g' /etc/nginx/nginx.conf

# 关闭守护模式
CMD ["nginx", "-g", "daemon off;"]