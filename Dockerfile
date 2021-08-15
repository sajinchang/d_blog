FROM python:3.7

# 设置 python 环境变量
ENV PYTHONUNBUFFERED 1

COPY pip.conf /root/.pip/pip.conf

RUN mkdir -p /apps/code/d_blog

WORKDIR /apps/code/d_blog

# 将当前目录加入到工作目录中（. 表示当前目录）
ADD ./ /apps/code/d_blog

# 更新pip版本
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt

RUN find ./scripts -name "*.sh" -exec sed -i 's/\r//' {} \;

 # 给scripts目录可执行权限
RUN chmod -R 755 scripts