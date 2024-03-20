FROM public.ecr.aws/lambda/python:3.10


# ENV PATH="${PATH}:/tmp"

COPY requirements.txt ./
RUN pip install -r requirements.txt -t /opt/python


COPY app.py config.py model.py ./


CMD yum install libgomp1

# CMD python3.8 -m pip install -r requirements.txt -t .



# RUN pip install model -t model.py

# RUN pip install --no-cache-dir --upgrade pip \
#   && pip install --no-cache-dir -r requirements.txt

# Set the CMD to zip the installed packages into a layer
# change the `requests-layer` to the LAYER_NAME variable as per create_layer.sh file
# CMD cd /opt && zip -r9 /app/dependency-layer.zip .

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambda_handler"]

