# Grafana docker image

This container builds a container with the
latest master build of Grafana and datasource configuration via environment variables.

## Running your Grafana image
--------------------------

Start your image binding the external port `3000`.

   docker run -i -p 3000:3000 qapps/grafana-docker

Try it out, default admin user is admin/admin.


## Configuring your Grafana container

Datasource configuration via environment variables, example:

```
docker run -d -p 3000:3000 \
    -e "DS_NAME=datasource_name" \
    -e "DS_TYPE=datasource type (CloudWatch, Graphite, InfluxDB, etc...)" \
    -e "DS_ACCESS=proxy or direct" \
    -e "DS_URL=datasource url" \
    -e "DS_PASS=pass" \
    -e "DS_USER=user" \
    -e "DS_DB=dbname" \
    -e "DS_AUTH=false" \
    -e "DS_AUTH_USER=" \
    -e "AUTH_PASS=" \
    -e "DS_IS_DEFAULT=false" \
    -e "DS_JSON_DATA=null" \
    qapps/grafana-docker
```

All options defined in conf/grafana.ini can be overriden using environment variables, for example:

```
docker run -i -p 3000:3000 \
  -e "GF_SERVER_ROOT_URL=http://grafana.server.name"  \
  -e "GF_SECURITY_ADMIN_PASSWORD=secret"  \
  grafana/grafana
```
## Additional env

```
GF_HOST - default: localhost
GF_PORT - default: 3000
GF_USER - default: admin
GF_PASS - default: admin
```

## Docker compose yml example

```
grafana:
    image: qapps/grafana-docker
    ports:
	- "3000:3000"
    environment:
	- DS_NAME=InfluxDB
	- DS_TYPE=influxdb
	- DS_ACCESS=proxy
	- DS_URL=http://localhost:8086
	- DS_PASS=root
	- DS_USER=root
	- DS_DB=dbname
```