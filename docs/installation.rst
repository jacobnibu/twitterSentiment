Installation
===============================================================================

Installation commands/instructions are listed here.

Prerequisite
-------------------------------------------------------------------------------

This is an example of hadoop cluster installation.

* Ansible
* ``inventory.txt`` file
* 10 vm servers with m1.medium

Installation
-------------------------------------------------------------------------------

* Run the playbook::

  ansible-playbook src/installation/hadoop-cluster.yaml -i inventory.txt

* Download Dataset::
  wget http://[domain name]/[filename.tar.gz]

* ...
