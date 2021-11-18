
# write some code to build your image
FROM python:3.8.12-bullseye
COPY api /api
COPY TaxiFareModel /TaxiFareModel
COPY model.joblib /model.joblib
COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install Cython
RUN pip install -r requirements.txt
CMD uvicorn api.fast:app --host 0.0.0.0
