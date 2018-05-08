FROM centos:7
RUN yum -y install epel-release && yum -y install python-flask && yum clean all
COPY application.py /application.py
ENTRYPOINT ["python"]
CMD ["application.py"]
