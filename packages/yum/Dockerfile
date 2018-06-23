FROM centos:7

EXPOSE 5000/tcp
HEALTHCHECK --interval=5m --timeout=3s \
  CMD curl -f http://localhost:5000/ || exit 1

RUN useradd app
RUN yum -y install epel-release && yum -y install python-flask curl && yum clean all

COPY application.py /application.py

USER app:app
ENTRYPOINT ["python"]
CMD ["/application.py"]
