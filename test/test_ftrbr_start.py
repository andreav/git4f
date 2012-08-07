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
    print '> setUpModule test_ftrbr'
    utils.sandbox()

def test_ftrbr_start_nointbr():
    oriR = utils.Repo(utils.DIR_REPO_BASE)
    cloR = utils.Repo(utils.DIR_REPO_CLONE_FTRBR)
    utils.clone_arepo(oriR.dir(), cloR.dir())

    #already tests in another module
    so,se,rc = cloR.exe_cmd_deny('git intbr')

    #when not set, it fails ... no check ret code
    so,se,rc = cloR.exe_cmd('git intbr-unset %s' % utils.CFG_FTR_PREFIX )
    so,se,rc = cloR.exe_cmd_deny('git ftrbr-start aaa')
    nt.eq_(so, '')
    nt.eq_(se, 'Integration branch not set')

    so,se,rc = cloR.exe_cmd_succ('git config --local %s ftr/' % utils.CFG_FTR_PREFIX )
    so,se,rc = cloR.exe_cmd_deny('git ftrbr-start aaa')
    nt.eq_(so, '')
    nt.eq_(se, 'Integration branch not set')
    
def test_ftrbr_start_intbr_tracked_prefix_notset():
    oriR = utils.Repo(utils.DIR_REPO_BASE)
    cloR = utils.Repo(utils.DIR_REPO_CLONE_FTRBR)
    utils.clone_arepo(oriR.dir(), cloR.dir())
    so,se,rc = cloR.exe_cmd_succ('git intbr master')
    so,se,rc = cloR.exe_cmd('git config --local --unset %s' % utils.CFG_FTR_PREFIX )

    so,se,rc = cloR.exe_cmd_succ('git ftrbr-start aaa')
    nt.assert_in("Pulling 'master'", so)
    nt.assert_in("Creating new ftr branch", so)
    nt.assert_in("Switched to a new branch 'aaa'", se)

def test_ftrbr_start_intbr_tracked_prefix_empty():
    oriR = utils.Repo(utils.DIR_REPO_BASE)
    cloR = utils.Repo(utils.DIR_REPO_CLONE_FTRBR)
    utils.clone_arepo(oriR.dir(), cloR.dir())
    so,se,rc = cloR.exe_cmd_succ('git intbr master')
    so,se,rc = cloR.exe_cmd('git config --local %s ""' % utils.CFG_FTR_PREFIX )

    so,se,rc = cloR.exe_cmd_succ('git ftrbr-start aaa')
    nt.assert_in("Pulling 'master'", so)
    nt.assert_in("Creating new ftr branch", so)
    nt.assert_in("Switched to a new branch 'aaa'", se)

def test_ftrbr_start_intbr_tracked_prefix_set():
    oriR = utils.Repo(utils.DIR_REPO_BASE)
    cloR = utils.Repo(utils.DIR_REPO_CLONE_FTRBR)
    utils.clone_arepo(oriR.dir(), cloR.dir())
    so,se,rc = cloR.exe_cmd_succ('git intbr master')
    so,se,rc = cloR.exe_cmd('git config --local %s ftr/' % utils.CFG_FTR_PREFIX )

    so,se,rc = cloR.exe_cmd_succ('git ftrbr-start aaa')
    nt.assert_in("Pulling 'master'", so)
    nt.assert_in("Creating new ftr branch", so)
    nt.assert_in("Switched to a new branch 'ftr/aaa'", se)

def test_ftrbr_start_intbr_onlylocal():
    oriR = utils.Repo(utils.DIR_REPO_BASE)
    cloR = utils.Repo(utils.DIR_REPO_CLONE_FTRBR)
    utils.clone_arepo(oriR.dir(), cloR.dir())
    so,se,rc = cloR.exe_cmd_succ('git checkout -b onlylocal master')
    so,se,rc = cloR.exe_cmd_succ('git intbr onlylocal')

    #should skip pull
    so,se,rc = cloR.exe_cmd_succ('git ftrbr-start aaa')
    nt.assert_in("Intbr 'onlylocal' not tracked, jump pull.", so)
    nt.assert_in("Creating new ftr branch starting from 'onlylocal'", so)
    nt.assert_in("Switched to a new branch 'aaa'", se)

