FROM public.ecr.aws/lambda/python:3.11
 
# Solo dependencias base — los scripts vienen de S3
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
 
COPY handler.py ${LAMBDA_TASK_ROOT}/
 
CMD ["handler.lambda_handler"]