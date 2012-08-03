#!/user/bin/python
# Copyright (C) 2012 Andrea Valle
#
# This file is part of git4f.
# 
# git4f is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# git4f is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with git4f.  If not, see <http://www.gnu.org/licenses/>.

import os, shutil, subprocess
import shlex
import nose.tools as nt

DIR_TEST_ROOT = os.path.abspath(os.path.dirname(__file__))
DIR_SANDBOX   = os.path.join(DIR_TEST_ROOT, 'sandbox')
DIR_REPO_BASE = os.path.join(DIR_SANDBOX,'repo')
DIR_REPO_CLONE_INTBR = os.path.join(DIR_SANDBOX,'clone.intbr')
DIR_REPO_CLONE_FTRBR = os.path.join(DIR_SANDBOX,'clone.ftrbr')
FILE_REPO_BASE       = 'a.txt'
CFG_FTR_PREFIX         = '4f.ftrbr-prefix'
CFG_FTR_PULL_MERGE_OPT = '4f.ftrbr-pull-merge-opt'
CFG_FTR_PUSH_MERGE_OPT = '4f.ftrbr-push-merge-opt'

# EXCEPTIONS ##################
class FailedCommand(Exception): pass
class FileNotExists(Exception): pass
class FileNotInSandbox(Exception): pass

# UTILS #######################
def touch(fname, times = None):
    with file(fname, 'a'):
        os.utime(fname, times)

def check_fname(f):
    #if not os.path.exists(f):
    #    raise FileNotExists(f)
    nt.assert_in('/sandbox', f)

# GIT MGT #####################
def exe_cmd(cmd, adir, mustsucc=None):
    print (' -C- (%s)'%os.path.basename(adir)).ljust(18), cmd

    #return subprocess.call(shlex.split(cmd), stdout=None, cwd=adir)
    po = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True, cwd=adir)
    so, se = po.communicate()

    rc = po.returncode
    if mustsucc == True:
        nt.eq_(rc, 0, 'Failed command: cd %s && %s' % (adir, cmd))
    if mustsucc == False:
        nt.assert_not_equal(rc, 0, 'Must fail command: cd %s && %s' % (adir, cmd))

    if so.strip() != '': print ' -SO- ', so.strip()
    if se.strip() != '': print ' -SE- ', se.strip()

    return so.strip(), se.strip(), rc

class Repo:
    def __init__(self, root):
        check_fname(root)
        self._root = root

    def dir(self):
        return self._root

    def exe_cmd(self, cmd, mustsucc=None):
        return exe_cmd(cmd, self._root)
    def exe_cmd_succ(self, cmd):
        return exe_cmd(cmd, self._root, mustsucc=True)
    def exe_cmd_deny(self, cmd):
        return exe_cmd(cmd, self._root, mustsucc=False)


# FUNCTIONS ###################
def sandbox():
    check_fname(DIR_SANDBOX)
    shutil.rmtree(DIR_SANDBOX,ignore_errors=True)
    os.mkdir(DIR_SANDBOX)
    create_arepo(DIR_REPO_BASE,FILE_REPO_BASE)

def create_arepo(adir, afile):
    check_fname(adir)

    #clean old, init bare
    origRepo = Repo(adir)
    shutil.rmtree(adir,ignore_errors=True)
    os.mkdir(adir)
    origRepo.exe_cmd('git init --bare')

    #clone, populate, push, destroy
    tbddir  = adir + '.tbd'
    tbdfile = os.path.join(tbddir, afile)
    tbdRepo = Repo(tbddir)

    clone_arepo(adir, tbddir)
    touch(tbdfile)
    tbdRepo.exe_cmd('git add %s' % afile)
    tbdRepo.exe_cmd('git commit -m "first commit"')
    tbdRepo.exe_cmd('git push origin master')
    shutil.rmtree(tbddir,ignore_errors=True)

def clone_arepo(adir, clonedir):
    check_fname(clonedir)
    shutil.rmtree(clonedir,ignore_errors=True)
    cmd_clone = 'git clone %s %s' % (adir, clonedir)
    exe_cmd( cmd_clone, DIR_SANDBOX, mustsucc=True )
    nt.assert_true(os.path.exists(clonedir), 'Not cloned %s' % clonedir)

