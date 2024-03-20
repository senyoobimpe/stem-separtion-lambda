FROM public.ecr.aws/lambda/python:3.10


# ENV PATH="${PATH}:/tmp"

COPY requirements.txt ./
RUN pip install -r requirements.txt -t /opt/python


COPY app.py ./



CMD ["app.lambda_handler"]

