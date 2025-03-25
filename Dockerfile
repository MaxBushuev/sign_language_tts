FROM nvcr.io/nvidia/pytorch:24.07-py3

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY test.py .

ENTRYPOINT ["python3" ,"test.py"]