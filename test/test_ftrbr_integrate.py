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
import os

def setUpModule():
    print '> setUpModule test_ftrbr'
    utils.sandbox()

def test_ftrbr_integrate_nointbr():
    oriR, cloR = utils.clone_makebr_edit_commit_repo(utils.DIR_REPO_CLONE_FTRBR_INTEGRATE)

    so,se,rc = cloR.exe_cmd_succ('git intbr-unset')
    so,se,rc = cloR.exe_cmd_deny('git ftrbr-integrate')
    nt.eq_(so, "")
    nt.eq_(se, "Integration branch not set")

def test_ftrbr_integrate():
    oriR, cloR = utils.clone_makebr_edit_commit_repo(utils.DIR_REPO_CLONE_FTRBR_INTEGRATE)

    so,se,rc = cloR.exe_cmd_succ('git ftrbr-integrate')
    nt.assert_in("Switched to branch 'master'",      se)
    nt.assert_in("Pulling 'master'",                 so)
    nt.assert_in("Merging 'ftr/work' into 'master'", so)

def test_ftrbr_integrate_conflict_on_pullintbr():
    oriR, cloR = utils.clone_makebr_edit_commit_repo(utils.DIR_REPO_CLONE_FTRBR_INTEGRATE)
    utils.edit_commit(oriR, 'on origin')
    so,se,rc = cloR.exe_cmd_succ('git checkout master')
    utils.edit_commit(cloR, 'on clone')

    so,se,rc = cloR.exe_cmd_deny('git ftrbr-integrate')
    nt.assert_in("Pulling 'master'",                   so)
    nt.assert_in("CONFLICT (content): Merge conflict", so)
    nt.assert_in("Automatic merge failed; fix conflicts and then commit the result.", so)
    nt.assert_not_in("Merging", so)
    nt.assert_not_in("Merging", se)

def test_ftrbr_integrate_conflict_on_mergeftrbr():
    oriR, cloR = utils.clone_makebr_edit_commit_repo(utils.DIR_REPO_CLONE_FTRBR_INTEGRATE)
    so,se,rc = cloR.exe_cmd_succ('git checkout master')
    utils.edit_commit(cloR, msg = 'from master')
    so,se,rc = cloR.exe_cmd_succ('git chk-back')

    so,se,rc = cloR.exe_cmd_deny('git ftrbr-integrate')
    nt.assert_in("Pulling 'master'",                   so)
    nt.assert_in("CONFLICT (content): Merge conflict", so)
    nt.assert_in("Merging 'ftr/work' into 'master",    so)
    nt.assert_in("Automatic merge failed; fix conflicts and then commit the result.", so)

def test_ftrbr_integrate_local():
    oriR = utils.Repo(utils.DIR_REPO_BASE)
    cloR = utils.Repo(utils.DIR_REPO_CLONE_FTRBR_INTEGRATE)
    utils.clone_arepo(oriR.dir(), cloR.dir())
    so,se,rc = cloR.exe_cmd_succ('git checkout -b another master')
    so,se,rc = cloR.exe_cmd_succ('git intbr another')
    utils.makebr_edit_commit(cloR)

    so,se,rc = cloR.exe_cmd_succ('git ftrbr-integrate')
    nt.assert_in("Switched to branch 'another'",            se)
    nt.assert_in("Intbr 'another' not tracked, jump pull.", so)
    nt.assert_in("Merging 'ftr/work' into 'another'",       so)

def test_ftrbr_integrate_rebase_nointbr():
    oriR, cloR = utils.clone_makebr_edit_commit_repo(utils.DIR_REPO_CLONE_FTRBR_INTEGRATE)

    so,se,rc = cloR.exe_cmd_succ('git intbr-unset')
    so,se,rc = cloR.exe_cmd_deny('git ftrbr-integrate-rebase')
    nt.eq_(so, "")
    nt.eq_(se, "Integration branch not set")

def test_ftrbr_integrate_rebase():
    oriR, cloR = utils.clone_makebr_edit_commit_repo(utils.DIR_REPO_CLONE_FTRBR_INTEGRATE)

    so,se,rc = cloR.exe_cmd_succ('git ftrbr-integrate-rebase')
    nt.assert_in("Switched to branch 'master'",        se)
    nt.assert_in("Pulling 'master'",                   so)
    nt.assert_in("Rebasing 'ftr/work' onto 'master'",  so)
    nt.assert_in("Merging 'ftr/work' into 'master'",   so)


def test_ftrbr_integrate_rebase_local():
    oriR = utils.Repo(utils.DIR_REPO_BASE)
    cloR = utils.Repo(utils.DIR_REPO_CLONE_FTRBR_INTEGRATE)
    utils.clone_arepo(oriR.dir(), cloR.dir())
    so,se,rc = cloR.exe_cmd_succ('git checkout -b another master')
    so,se,rc = cloR.exe_cmd_succ('git intbr another')
    utils.makebr_edit_commit(cloR)

    so,se,rc = cloR.exe_cmd_succ('git ftrbr-integrate-rebase')
    nt.assert_in("Switched to branch 'another'",            se)
    nt.assert_in("Intbr 'another' not tracked, jump pull.", so)
    nt.assert_in("Rebasing 'ftr/work' onto 'another'",      so)
    nt.assert_in("Merging 'ftr/work' into 'another'",       so)

def test_ftrbr_integrate_rebase_conflict_on_pullintbr():
    oriR, cloR = utils.clone_makebr_edit_commit_repo(utils.DIR_REPO_CLONE_FTRBR_INTEGRATE)
    utils.edit_commit(oriR, 'on origin')
    so,se,rc = cloR.exe_cmd_succ('git checkout master')
    utils.edit_commit(cloR, 'on clone')

    so,se,rc = cloR.exe_cmd_deny('git ftrbr-integrate-rebase')
    nt.assert_in("Pulling 'master'",                   so)
    nt.assert_in("CONFLICT (content): Merge conflict", so)
    nt.assert_in("Automatic merge failed; fix conflicts and then commit the result.", so)
    nt.assert_not_in("Merging", so)
    nt.assert_not_in("Merging", se)

def test_ftrbr_integrate_rebase_conflict_on_mergeftrbr():
    oriR, cloR = utils.clone_makebr_edit_commit_repo(utils.DIR_REPO_CLONE_FTRBR_INTEGRATE)
    so,se,rc = cloR.exe_cmd_succ('git checkout master')
    utils.edit_commit(cloR, msg = 'from master')
    so,se,rc = cloR.exe_cmd_succ('git chk-back')

    so,se,rc = cloR.exe_cmd_deny('git ftrbr-integrate')
    nt.assert_in("Pulling 'master'",                   so)
    nt.assert_in("CONFLICT (content): Merge conflict", so)
    nt.assert_in("Merging 'ftr/work' into 'master",    so)
    nt.assert_in("Automatic merge failed; fix conflicts and then commit the result.", so)

