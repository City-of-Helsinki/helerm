ARG BASE_IMAGE=helsinki/helerm:latest

FROM $BASE_IMAGE

# Change back to root for installing stuff
USER root

RUN pip install --no-cache-dir elastic-apm

# Change back to user
USER helerm

COPY local_settings.py .
