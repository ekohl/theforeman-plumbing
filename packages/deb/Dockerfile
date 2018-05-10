FROM debian:stretch
RUN apt update && apt upgrade -y && apt install -y dctrl-tools python3-flask python3-requests && apt clean
COPY application.py /application.py
ENTRYPOINT ["python3"]
CMD ["application.py"]
