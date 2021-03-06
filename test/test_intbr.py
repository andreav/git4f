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

import utils
import nose.tools as nt

def setUpModule():
    print '> setUpModule test_intbr'
    utils.sandbox()

def test_intbr_get():
    oriR = utils.Repo(utils.DIR_REPO_BASE)
    cloR = utils.Repo(utils.DIR_REPO_CLONE_INTBR)

    utils.clone_arepo(oriR.dir(), cloR.dir())

    so,se,rc = cloR.exe_cmd_deny('git intbr')
    nt.eq_(so, '')

def test_intbr_set():
    oriR = utils.Repo(utils.DIR_REPO_BASE)
    cloR = utils.Repo(utils.DIR_REPO_CLONE_INTBR)

    utils.clone_arepo(oriR.dir(), cloR.dir())

    so,se,rc = cloR.exe_cmd_succ('git intbr master')
    nt.eq_(so, '')

    so,se,rc = cloR.exe_cmd_succ('git intbr')
    nt.eq_(so, 'master')

    so,se,rc = cloR.exe_cmd_succ('git config --get 4f.intbr')
    nt.eq_(so, 'master')

def test_intbr_set_on_set():
    oriR = utils.Repo(utils.DIR_REPO_BASE)
    cloR = utils.Repo(utils.DIR_REPO_CLONE_INTBR)

    utils.clone_arepo(oriR.dir(), cloR.dir())
    
    #already tested first intbr set
    so,se,rc = cloR.exe_cmd_succ('git intbr master')

    #already tested first intbr set
    so,se,rc = cloR.exe_cmd_succ('git intbr master')
    nt.eq_(so, '')

    so,se,rc = cloR.exe_cmd_succ('git intbr')
    nt.eq_(so, 'master')

    so,se,rc = cloR.exe_cmd_succ('git config --get 4f.intbr')
    nt.eq_(so, 'master')

def test_intbr_set_on_set_different():
    oriR = utils.Repo(utils.DIR_REPO_BASE)
    cloR = utils.Repo(utils.DIR_REPO_CLONE_INTBR)

    utils.clone_arepo(oriR.dir(), cloR.dir())
    
    #already tested first intbr set
    so,se,rc = cloR.exe_cmd_succ('git intbr master')

    #already tested first intbr set
    so,se,rc = cloR.exe_cmd_succ('git checkout -b another')

    so,se,rc = cloR.exe_cmd_succ('git intbr another')
    nt.eq_(so, '')

    so,se,rc = cloR.exe_cmd_succ('git intbr')
    nt.eq_(so, 'another')

    so,se,rc = cloR.exe_cmd_succ('git config --get 4f.intbr')
    nt.eq_(so, 'another')

def test_intbr_unset_different():
    oriR = utils.Repo(utils.DIR_REPO_BASE)
    cloR = utils.Repo(utils.DIR_REPO_CLONE_INTBR)
    utils.clone_arepo(oriR.dir(), cloR.dir())
    so,se,rc = cloR.exe_cmd_succ('git intbr master')

    so,se,rc = cloR.exe_cmd_succ('git intbr-unset')

    so,se,rc = cloR.exe_cmd_deny('git intbr')
    nt.eq_(so, '')
    nt.eq_(se, 'Integration branch not set')

    so,se,rc = cloR.exe_cmd_deny('git config --get 4f.intbr')
    nt.eq_(so, '')
    nt.eq_(se, '')

def test_intbr_unset_different_onearg():
    oriR = utils.Repo(utils.DIR_REPO_BASE)
    cloR = utils.Repo(utils.DIR_REPO_CLONE_INTBR)
    utils.clone_arepo(oriR.dir(), cloR.dir())
    so,se,rc = cloR.exe_cmd_succ('git intbr master')

    #pass one param more
    so,se,rc = cloR.exe_cmd_succ('git intbr-unset master')
    so,se,rc = cloR.exe_cmd_deny('git intbr')
    nt.eq_(so, '')
    nt.eq_(se, 'Integration branch not set')

    so,se,rc = cloR.exe_cmd_deny('git config --get 4f.intbr')
    nt.eq_(so, '')
    nt.eq_(se, '')

def test_intbr_istracked():
    oriR = utils.Repo(utils.DIR_REPO_BASE)
    cloR = utils.Repo(utils.DIR_REPO_CLONE_INTBR)
    utils.clone_arepo(oriR.dir(), cloR.dir())

    #just cloned, no intbr, unset scenario
    so,se,rc = cloR.exe_cmd_deny('git intbr-istracked')
    nt.eq_(so, '')
    nt.eq_(se, 'Integration branch not set')

    #tracked scenario
    so,se,rc = cloR.exe_cmd_succ('git intbr master')

    so,se,rc = cloR.exe_cmd_succ('git intbr-istracked')
    nt.eq_(so, 'master <- origin/master')
    nt.eq_(se, '')

    so,se,rc = cloR.exe_cmd_succ('git intbr-unset')

    so,se,rc = cloR.exe_cmd_deny('git intbr-istracked')
    nt.eq_(so, '')
    nt.eq_(se, 'Integration branch not set')

    #untracked scenario
    so,se,rc = cloR.exe_cmd_succ('git checkout -b another master')
    so,se,rc = cloR.exe_cmd_succ('git intbr another')

    so,se,rc = cloR.exe_cmd_deny('git intbr-istracked')
    nt.eq_(so, '')
    nt.eq_(se, "Integration branch 'another' not tracked")

    #one param more ... ignored
    so,se,rc = cloR.exe_cmd_succ('git intbr master')
    so,se,rc = cloR.exe_cmd_succ('git intbr-istracked aaa')
    nt.eq_(so, 'master <- origin/master')
    nt.eq_(se, '')
