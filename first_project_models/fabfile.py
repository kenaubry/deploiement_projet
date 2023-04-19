from fabric import Connection, task

@task
def deploy(ctx):
    # Remplacez user@host par vos informations d'identification Vagrant
    conn = Connection("vagrant@127.0.0.1")

    # Clonez le projet ou mettez-le à jour s'il existe déjà
    conn.run("if [ ! -d my_site ]; then git clone https://github.com/yourusername/my_site.git; else cd my_site && git pull; fi")

    # Changez le répertoire vers votre projet
    with conn.cd("my_site"):
        # Installez les dépendances
        conn.run("pip install -r requirements.txt")

        # Exécutez les migrations de la base de données
        conn.run("python manage.py migrate")

        # Exécutez Gunicorn pour servir votre application
        conn.run("gunicorn my_site.wsgi:application --bind 0.0.0.0:8000 --daemon")

    # Redémarrez Nginx
    conn.sudo("service nginx restart")