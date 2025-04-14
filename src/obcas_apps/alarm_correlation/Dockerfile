FROM broadbandforum/obcas-sdk:latest
RUN mkdir -p /obcas_alarm_correlation
COPY . /obcas_alarm_correlation
ENV PYTHONPATH=/obcas_alarm_correlation
WORKDIR /obcas_alarm_correlation/correlator
CMD ["python3", "main.py"]
