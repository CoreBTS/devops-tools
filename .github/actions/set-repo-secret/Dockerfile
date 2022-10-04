FROM python:3.9-slim

RUN pip install pynacl
RUN pip install requests

COPY set-repo-secret.py /set-repo-secret.py

ENTRYPOINT ["python", "/set-repo-secret.py"]