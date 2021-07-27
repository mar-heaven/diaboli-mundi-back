FROM centos/python-38-centos7
USER root

WORKDIR /tmp
COPY . /tmp
RUN pip3 install -i https://pypi.douban.com/simple -r /tmp/requirements.txt && pip3 install -e .

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "-k", "uvicorn.workers.UvicornWorker", "-w", "2", "diaboli_mundi_back.main:app", "--access-logfile", "-"]
