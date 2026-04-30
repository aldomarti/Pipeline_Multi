# person-stream Lambda - Transformación

## Descripción
Lambda de transformación de datos de persona. Lee datos crudos de S3 y los transforma
al formato destino en S3 staging. Orquestada por Step Function `sfwrdppersonprocessprd01`.

## Desarrollo local
```bash
docker build -t person-stream .
docker run -p 9000:8080 person-stream
curl -X POST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'
```
