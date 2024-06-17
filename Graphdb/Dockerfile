#FROM openjdk:8-jdk
#FROM azul/zulu-openjdk
FROM adoptopenjdk/openjdk11
 
LABEL maintainer "Johan van Soest <j.vansoest@maastrichtuniversity.nl>"
 
# Build time arguments
ARG download_link=https://go.ontotext.com/cs/c/?cta_guid=3d3cab68-ee83-4dfc-a040-aa707e9a751a&signature=AAH58kET9etoR5C3sbavKQE8N2f_lpQ7fw&placement_guid=ed4ee978-afe2-438d-b2a5-139cf9c665bb&click=f2348df9-5064-44c0-b7cd-f516d365ccf0&hsutk=66064c7cb1c83bb879ea84b3e045d315&canon=https%3A%2F%2Fwww.ontotext.com%2Fthank-you-for-downloading-graphdb%2F%3FsubmissionGuid%3D9aef4612-99d5-4f6f-bb59-8a6dfaf6163b&utm_referrer=https%3A%2F%2Fwww.ontotext.com%2Fproducts%2Fgraphdb%2Fdownload%2F&portal_id=5619976&redirect_url=APefjpF3GTqW2qLJUXRBkBv6FdQiXkuGSIIk2ztRDQCyg-uA-vHlvEyv0WSEblY_adaLcp1qs0Mr6XRHj8SwAPB1ww2sGgswSzael41cSw_kX609s-E65iTSaBSHGMHFHA2aVsj7k1-ITdTBZnU4rkQ3xZSviJVz6Qp5k7oAcMj51YBP4iyeXox_wvxxpm2lsv2ydteLAMKAmLsqnUJ24wQM1iJDBxfBx5zlb7svwXIgJC4Cd9WAeVf9GEoa_Cl44EpOILhVggkjSuT6oSMgvg0QXYHvOBBeAWyDZX56UbMD7d-f1w5zjQfG4lhG7a8ancL8ZmYKPyF6Flg2LYNlejAT1eqiftAI_g&__hstc=95638467.66064c7cb1c83bb879ea84b3e045d315.1676365769953.1676365769953.1676365769953.1&__hssc=95638467.4.1676365769953&__hsfp=1689991152&contentType=standard-page
ARG version=10.1.3
 
# Environment variables, to be used for the docker image
ENV GDB_HEAP_SIZE=8g
ENV GDB_MIN_MEM=8g
ENV GDB_MAX_MEM=8g
 
ENV GRAPHDB_PARENT_DIR=/opt/graphdb
ENV GRAPHDB_HOME=${GRAPHDB_PARENT_DIR}/home
ENV GRAPHDB_INSTALL_DIR=${GRAPHDB_PARENT_DIR}/dist

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y unzip curl

RUN echo 'openssl_conf = default_conf\n' | cat - /etc/ssl/openssl.cnf > /openssl.cnf
RUN echo '[ default_conf ]' >> /openssl.cnf
RUN echo '' >> ./openssl.cnf
RUN echo 'ssl_conf = ssl_sect' >> /openssl.cnf
RUN echo '' >> /openssl.cnf
RUN echo '[ssl_sect]' >> /openssl.cnf
RUN echo '' >> /openssl.cnf
RUN echo 'system_default = system_default_sect' >> /openssl.cnf
RUN echo '' >> /openssl.cnf
RUN echo '[system_default_sect]' >> /openssl.cnf
RUN echo 'MinProtocol = TLSv1.2' >> /openssl.cnf
RUN echo 'CipherString = DEFAULT:@SECLEVEL=1' >> /openssl.cnf
RUN cp /openssl.cnf /etc/ssl/openssl.cnf

# Copy the installation file recieved after registration
#ADD graphdb-${version}-dist.zip /tmp
RUN curl -L -k -o /tmp/graphdb-${version}-dist.zip ${download_link}
 
RUN mkdir -p ${GRAPHDB_PARENT_DIR} && \
    cd ${GRAPHDB_PARENT_DIR} && \
    unzip /tmp/graphdb-${version}-dist.zip && \
    mv graphdb-${version} dist && \
    mkdir -p ${GRAPHDB_HOME} && \
    rm /tmp/graphdb-${version}-dist.zip
 
ENV PATH=${GRAPHDB_INSTALL_DIR}/bin:$PATH
 
CMD ["-Dgraphdb.home=/opt/graphdb/home -Dorg.xml.sax.driver=com.sun.org.apache.xerces.internal.parsers.SAXParser -Djdk.xml.entityExpansionLimit=1000000"]
 
ENTRYPOINT ["/opt/graphdb/dist/bin/graphdb"]
 
EXPOSE 7200