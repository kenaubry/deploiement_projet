# deploiement_projet

'''
- hosts: all
  become: yes
  tasks:
    - name: Update and upgrade packages
      apt:
        upgrade: yes
        update_cache: yes
        cache_valid_time: 86400

    - name: Install required packages
      apt:
        name:
          - python3-pip
          - python3-venv
          - nginx
          - git
      state: present

    - name: Clone git repository
      git:
        repo: https://github.com/yourusername/yourproject.git
        dest: /home/vagrant/yourproject

    - name: Create virtualenv
      pip:
        chdir: /home/vagrant/yourproject
        virtualenv: /home/vagrant/yourproject/venv
        virtualenv_python: python3

    - name: Install Django requirements
      pip:
        chdir: /home/vagrant/yourproject
        requirements: /home/vagrant/yourproject/requirements.txt
        virtualenv: /home/vagrant/yourproject/venv

    - name: Configure Gunicorn
      template:
        src: gunicorn.service.j2
        dest: /etc/systemd/system/gunicorn.service
      notify: reload systemd

    - name: Configure Nginx
      template:
        src: nginx-site.conf.j2
        dest: /etc/nginx/sites-available/yourproject.conf
      notify: reload nginx

    - name: Enable Nginx site
      file:
        src: /etc/nginx/sites-available/yourproject.conf
        dest: /etc/nginx/sites-enabled/yourproject.conf
        state: link
      notify: reload nginx

  handlers:
    - name: reload nginx
      systemd:
        name: nginx
        state: reloaded

    - name: reload systemd
      systemd:
        daemon_reload: yes

'''
