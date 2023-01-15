FROM postgres:13.3

# COPY ./compose/production/postgres/maintenance /usr/local/bin/maintenance
# RUN chmod +x /usr/local/bin/maintenance/*
# RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
#     && rmdir /usr/local/bin/maintenance

# COPY ./restore_db.sh /docker-entrypoint-initdb.d/

# ADD ./nrgx.sql.gz ./nrgx_sql

# RUN chown -R root:root ./nrgx_sql

# RUN chmod -R 777 ./nrgx_sql