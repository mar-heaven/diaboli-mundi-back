FROM conda_py38

WORKDIR /tmp
COPY requirements.txt /tmp
RUN pip3 install -i https://pypi.douban.com/simple -r /tmp/requirements.txt

EXPOSE 5000

