# -*- coding: UTF-8 -*-

import logging
import os
import shutil
from pygit2 import clone_repository, discover_repository, Repository, Signature

logger = logging.getLogger("satisgit")

satis_bare_repo = 'file:///home/satis/satis-git-repositories/production/satis-git-bare-repository'
satis_working_repo = '/home/satis/tmp'

def update_file(file_path, content):
    dir_path = file_path[:file_path.rfind('/')]
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    with open(file_path, "w") as f:
        f.write(content)

def git_update_file(windtest_id, git_file_path, file_content):
    repo_url = satis_bare_repo + '/' + windtest_id + '.git'
    repo_path = satis_working_repo + '/' + windtest_id
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)

    repo = clone_repository(repo_url, repo_path)
    remote = repo.remotes[0]
    parent = repo.revparse_single('HEAD')
    update_file(repo_path + '/' + git_file_path, file_content)
    index = repo.index
    index.add(git_file_path)
    index.write()
    author = Signature('Ngoc Thach TA', 'ngoc-thach.ta@akka.eu')
    committer = Signature('Ngoc Thach TA', 'ngoc-thach.ta@akka.eu')
    tree = index.write_tree()
    repo.create_commit('refs/heads/master',
            author, committer, 'add toto', tree, [parent.id])
    remote.push('refs/heads/master')

def main():

    logger.info("Starting test satisgit")
    file_content = """
# -*- coding: UTF-8 -*-
from gensatisenv import __package__import *
# --- veuillez conserver ce bandeau intact svp --- #


#@InterpreterUserModule
# Definition des Variables spécifiques
_unit={}

# Cette 2nd entête ne doit toujours pas être modifié. 
#-------------------------------------#
toto = SafinStationnaire.RAW.M1V1 + 5
            """

    git_update_file('Windtest20160623102754', 'calcul/src/user_modules/toto/ismod2.py', file_content)
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    main()    
