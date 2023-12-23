FROM python:3.9 
# Or any preferred Python version.
ADD main.py .
WORKDIR /app
copy . /app
RUN pip install requirements.txt
EXPOSE 27017
EXPOSE 8080
CMD ["python", "./main.py"] 
# Or enter the name of your unique directory and parameter set.