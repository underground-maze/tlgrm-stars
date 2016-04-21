# vi: syntax=python
import os
import fabric

from fabric.api import run, sudo, cd

fabric.state.env.colorize_errors = True
fabric.state.output['stdout'] = False

# task const variables
VARS = dict(
    current_user=fabric.state.env.user,

    # project settings
    project_name='starreditemsbot',
    user_data=dict(
        username='root',
        email='root@e.co',
        password='123123'
    ),

    # dirs configs
    templates_dir='./provision/templates',
    root_dir='/home/vagrant/proj',
    venv_path='/home/vagrant/venv',
    base_dir='/home/vagrant',

    # nginx config
    http_host='10.1.1.77',
    http_port='80',

    # database config
    db_name='starreditemsbot',
    db_password='r4HdZEoyJ',
    db_user='starreditemsbot_user',

    # locale conf
    locale='ru_RU',
    encoding='UTF-8',
)


def sentinel(sentinel_name):
    def sentinel_wrapp(function):
        def wrapped():
            sentinel_path = '/usr/sentinel_{}'.format(sentinel_name)
            if fabric.contrib.files.exists(sentinel_path):
                fabric.utils.warn('skip {}'.format(sentinel_name))
                return
            function()
            sudo('touch {}'.format(sentinel_path))
        return wrapped
    return sentinel_wrapp


def common():
    """ Common tasks """
    locale()
    apt_packages()
    python_packages()


def nginx():
    """ Install nginx tasks """
    # install nginx
    sudo('apt-get -y install nginx')
    # create nginx config file for project
    fabric.contrib.files.upload_template(
        'nginx-host.j2', '/etc/nginx/sites-available/{project_name}'.format(**VARS),
        context=VARS, use_jinja=True, backup=False, use_sudo=True, template_dir=VARS['templates_dir'])
    # make s-link to enabled sites
    sudo('ln -sf /etc/nginx/sites-available/{project_name} /etc/nginx/sites-enabled/{project_name}'.format(**VARS))
    # restart nginx
    sudo('service nginx restart')


@sentinel('database')
def database():
    """ Install database """
    pass


@sentinel('locale')
def locale():
    """ Set locale to enviroment """
    fabric.contrib.files.upload_template(
        'environment.j2', '/etc/environment',
        context=VARS, use_jinja=True, backup=False, use_sudo=True, template_dir=VARS['templates_dir'])
    sudo('localedef {locale}.{encoding} -i {locale} -f{encoding}'.format(**VARS))
    # sudo('locale-gen')


@sentinel('apt_packages')
def apt_packages():
    """ Install common packages """
    sudo('apt-get -y update')
    sudo('apt-get -y install libcurl4-gnutls-dev libexpat1-dev gettext libz-dev libssl-dev git')


@sentinel('python')
def python_packages():
    """ Install python components """

    sudo(
        'apt-get -y install python-dev python-pip python-virtualenv build-essential '
        'libncurses5-dev libncursesw5-dev libreadline6-dev libgdbm-dev libsqlite3-dev '
        'libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libxml2-dev libxslt1-dev')

    with cd('/tmp'):
        # download python source code
        run('wget -O python.tgz https://www.python.org/ftp/python/3.5.1/Python-3.5.1.tgz')
        # extract python tarball
        run('tar -xf python.tgz')
        run('mv Python-3.5.1 python')

    with cd('/tmp/python'):
        # configuring python 3.4 Makefile
        run('./configure --prefix=/usr/local/python-3.5.1')
        # compiling the python 3.4 source code and install
        sudo('make && make altinstall #')
    sudo('rm /tmp/* -rf')
    # make link to python
    sudo('ln -sf /usr/local/python-3.5.1/bin/* /usr/local/bin/')


def app():
    """ Run application tasks """
    with cd(VARS['root_dir']):
        # Create venv and install requirements
        run('pyvenv-3.5 {venv_path}'.format(**VARS))
        # Install required python packages with pip from wheels archive
        run('make wheel_install')
        # run app tasks for devserver start
        # Copy settings local
        # run('cd {project_name} && cp settings_local.py.example settings_local.py'.format(**VARS))
        run('make start', pty=False)
