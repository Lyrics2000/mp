From python:3.8
RUN mkdir -p /usr/src/britam/payments/app
WORKDIR /usr/src/britam/payments/app
COPY . /usr/src/britam/payments/app
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
CMD ["/bin/bash", "./run.sh"]