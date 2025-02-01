FROM python:alpine3.21@sha256:f9d772b2b40910ee8de2ac2b15ff740b5f26b37fc811f6ada28fce71a2542b0e

WORKDIR /opt/application

ENV PYTHONPATH="/opt/application:/opt/application/tests:${PYTHONPATH}"

COPY dev.requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY apiutils apiutils

COPY tests tests
COPY .coveragerc ./.coveragerc

ENTRYPOINT pytest --cov-config=.coveragerc --cov --cov-report xml --junitxml=./test_results.xml ./tests
