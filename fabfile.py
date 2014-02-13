import re
from fabric.api import *
from fabric.contrib.files import *
from fabric.context_managers import *

env.use_ssh_config = True
#env.user = 'uc2-user'
#env.host_string = 'hostname'

def uname():
    return run('uname -a')

def setup_locale():
    run('echo "export LANG=C" | tee -a ~/.bash_profile')
    run('echo "export LC_ALL=C" | tee -a ~/.bash_profile')

def setup_hadoopenv():
    run('echo "export HADOOP_COMMON_HOME=~/hadoop" | tee -a ~/.bash_profile')
    run('echo "export HADOOP_HDFS_HOME=$HADOOP_COMMON_HOME" | tee -a ~/.bash_profile')
    run('echo "export HADOOP_MAPRED_HOME=$HADOOP_COMMON_HOME" | tee -a ~/.bash_profile')
    run('echo "export HADOOP_CONF_DIR=$HADOOP_COMMON_HOME/etc/hadoop" | tee -a ~/.bash_profile')
    run('echo "export TEZ_CONF_DIR=$HADOOP_COMMON_HOME/etc/hadoop" | tee -a ~/.bash_profile')
    run('echo "export TEZ_JARS=~/tez " | tee -a ~/.bash_profile')


def clone_hadooprepo():
    run('git clone git://git.apache.org/hadoop-common.git')

def install_git():
    runcmd('apt-get -y install git-core')

def is_ubuntu():
    return re.match('.*[Uu]buntu.*', uname())

'''
NOTE: install_oracle_java installs Java 7 from unofficial repository(webupd8team).
'''
def install_oracle_java():
    runcmd('sudo apt-get install python-software-properties')
    runcmd('apt-get -y install software-properties-common')

    if is_ubuntu():
        runcmd('add-apt-repository ppa:webupd8team/java')
        runcmd('apt-key adv --keyserver keyserver.ubuntu.com --recv-keys EEA14886')
    else:
        # For debian
        runcmd('echo "deb http://ppa.launchpad.net/webupd8team/java/ubuntu precise main" | tee -a /etc/apt/sources.list.d/webupd8team-java.list')

    runcmd('apt-get -y update')
    runcmd('echo debconf shared/accepted-oracle-license-v1-1 select true |  debconf-set-selections')
    runcmd('echo debconf shared/accepted-oracle-license-v1-1 seen true |  debconf-set-selections')
    runcmd('DEBIAN_FRONTEND=noninteractive apt-get -y --force-yes install oracle-java7-installer')
    runcmd('apt-get -y install oracle-java7-set-default')

def install_maven():
    if is_ubuntu():
        runcmd('apt-get -y install maven')
    else:
        run('wget http://mirror.metrocast.net/apache/maven/maven-3/3.0.5/binaries/apache-maven-3.0.5-bin.tar.gz')
        run('tar xzvf apache-maven-3.0.5-bin.tar.gz')
        run('mv apache-maven-3.0.5 3.0.5')
        runcmd('mkdir /usr/local/maven')
        runcmd('mv 3.0.5 /usr/local/maven/')
        run('echo "export PATH=/usr/local/maven/3.0.5/bin"' + "':$PATH'" + '| tee -a ~/.bash_profile')
        # cleanup
        run('rm -rf apache-maven*')


def install_protobuf():
    runcmd('apt-get build-dep -y protobuf-compiler')
    run('wget https://protobuf.googlecode.com/files/protobuf-2.5.0.tar.bz2')
    run('tar xjvf protobuf-2.5.0.tar.bz2')
    with cd('protobuf-2.5.0'):
        run('./configure')
        run('make -j4')
        runcmd('make install')
    # cleanup
    run('rm -rf protobuf-2.5.0*')
    addenv('export LD_LIBRARY_PATH=/usr/local/lib')
    addenv('export LD_RUN_PATH=/usr/local/lib')

# Helpers
def runcmd(arg):
    if env.user != "root":
        sudo("%s" % arg, pty=True)
    else:
        run("%s" % arg, pty=True)

def addenv(newenv):
    run('echo ' + newenv + ' | tee -a ~/.bash_profile');


# Run entire setup
def setup_hadoopdev():
    setup_locale()
    setup_hadoopenv()
    install_git()
    install_oracle_java()
    install_protobuf()
    install_maven()

