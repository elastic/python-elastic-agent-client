FROM docker.elastic.co/elastic-agent/elastic-agent:sha256-fff74ac535403af9307ed6f93aad71ec95866bf6f1ec2da1bd7966e6bc17ae72
USER root
# Install dependencies
RUN apt update
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install python3.10 python3.10-venv make -y

# TEMPORARY STUFF
# I need vim to edit some fields
# Git is needed to pull connectors repo
# yq is needed to append our input to elastic-agent.yml
RUN add-apt-repository ppa:rmescandon/yq
RUN apt install vim git yq -y

# Pull connectors
# TODO: when we're ready, figure out packaging and distribution of
# connectors - we might have them zipped or distributed via pip
WORKDIR /usr/share
RUN git clone https://github.com/elastic/connectors.git && \
  cd connectors && \
  git checkout connectors-in-agentless-poc

# Copy and install python agent client
# TODO: also package this with revision and everything
COPY ./ /usr/share/python-elastic-agent
WORKDIR /usr/share/python-elastic-agent
RUN make clean install
# TODO: think of properly installing this
RUN /usr/share/python-elastic-agent/bin/pip install -r /usr/share/connectors/requirements/x86_64.txt

# Add component
# Agent directory name is dynamic and based on build hash, so we need to move in two steps
COPY ./elastic-package/python-elastic-agent-client /tmp/python-elastic-agent-client
COPY ./elastic-package/python-elastic-agent-client.spec.yml /tmp/python-elastic-agent-client.spec.yml
RUN mv /tmp/python-elastic-agent-client /usr/share/elastic-agent/data/elastic-agent-$(cat /usr/share/elastic-agent/.build_hash.txt| cut -c 1-6)/components/python-elastic-agent-client
RUN mv /tmp/python-elastic-agent-client.spec.yml /usr/share/elastic-agent/data/elastic-agent-$(cat /usr/share/elastic-agent/.build_hash.txt| cut -c 1-6)/components/python-elastic-agent-client.spec.yml

# add input to the elastic-agent.yml
RUN yq eval --inplace '.inputs += { "type": "connectors-py", "id": "connectors-py", "use_output": "default"}' /usr/share/elastic-agent/elastic-agent.yml

WORKDIR /usr/share/elastic-agent
