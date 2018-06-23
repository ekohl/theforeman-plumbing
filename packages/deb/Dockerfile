FROM debian:stretch

EXPOSE 5000/tcp
HEALTHCHECK --interval=5m --timeout=3s \
  CMD curl -f http://localhost:5000/ || exit 1

RUN useradd app
RUN apt update && apt upgrade -y && apt install -y dctrl-tools python3-flask python3-requests && apt clean

COPY application.py /application.py

USER app:app
ENTRYPOINT ["python3"]
CMD ["/application.py"]
