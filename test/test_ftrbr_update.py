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

def test_ftrbr_pull_nointbr():
    oriR, cloR = utils.clone_makebr_edit_commit_repo(utils.DIR_REPO_CLONE_FTRBR_UPDATE)

    so,se,rc = cloR.exe_cmd_succ('git intbr-unset')
    so,se,rc = cloR.exe_cmd_deny('git ftrbr-update-merge')
    nt.eq_(so, "")
    nt.eq_(se, "Integration branch not set")

def test_ftrbr_pull_uptodate():
    oriR, cloR = utils.clone_makebr_edit_commit_repo(utils.DIR_REPO_CLONE_FTRBR_UPDATE)

    so,se,rc = cloR.exe_cmd_succ('git ftrbr-update-merge')
    nt.assert_in("Switched to branch 'master'",      se)
    nt.assert_in("Pulling 'master'",                 so)
    nt.assert_in("Merging 'master' into 'ftr/work'", so)

def test_ftrbr_pull_uptodate_local():
    oriR, cloR = utils.clone_makebr_edit_commit_repo(utils.DIR_REPO_CLONE_FTRBR_UPDATE)

    so,se,rc = cloR.exe_cmd_succ('git checkout -b another master')
    so,se,rc = cloR.exe_cmd_succ('git intbr another')
    utils.makebr_edit_commit(cloR, brname='side_of_another')

    so,se,rc = cloR.exe_cmd_succ('git ftrbr-update-merge')
    nt.assert_in("Intbr 'another' not tracked, jump pull.", so)
    nt.assert_in("Merging 'another' into 'ftr/side_of_another'", so)

def test_ftrbr_pull_onintbr():
    oriR, cloR = utils.clone_makebr_edit_commit_repo(utils.DIR_REPO_CLONE_FTRBR_UPDATE)

    so,se,rc = cloR.exe_cmd_succ('git checkout master')

    so,se,rc = cloR.exe_cmd_succ('git ftrbr-update-merge')
    nt.assert_in("Already on 'master'",            se)
    nt.assert_in("Pulling 'master'",               so)
    nt.assert_in("Merging 'master' into 'master'", so)

def test_ftrbr_pull():
    oriR, cloR = utils.clone_makebr_edit_commit_repo(utils.DIR_REPO_CLONE_FTRBR_UPDATE)

    utils.edit_commit(oriR, 'on origin', 'b.txt')

    so,se,rc = cloR.exe_cmd_succ('git ftrbr-update-merge')
    nt.assert_in("Pulling 'master'",               so)
    nt.assert_in("create mode 100644 b.txt",       so)
    nt.assert_in("Merging 'master' into 'ftr/work'", so)

def test_ftrbr_pull_conflict_on_mergeftrbr():
    oriR, cloR = utils.clone_makebr_edit_commit_repo(utils.DIR_REPO_CLONE_FTRBR_UPDATE)

    utils.edit_commit(oriR, 'on origin')

    so,se,rc = cloR.exe_cmd_deny('git ftrbr-update-merge')
    nt.assert_in("Pulling 'master'",                 so)
    nt.assert_in("Fast-forward",                     so)
    nt.assert_in("Merging 'master' into 'ftr/work'", so)
    nt.assert_in("CONFLICT (content): Merge conflict in a.txt", so)
    nt.assert_in("Automatic merge failed; fix conflicts and then commit the result.", so)

def test_ftrbr_pull_conflict_on_pullintbr():
    oriR, cloR = utils.clone_makebr_edit_commit_repo(utils.DIR_REPO_CLONE_FTRBR_UPDATE)
    utils.edit_commit(oriR, 'on origin')
    so,se,rc = cloR.exe_cmd_succ('git checkout master')
    utils.edit_commit(cloR, 'on clone')

    so,se,rc = cloR.exe_cmd_deny('git ftrbr-update-merge')
    nt.assert_in("Pulling 'master'",                 so)
    nt.assert_in("CONFLICT (content): Merge conflict in a.txt", so)
    nt.assert_in("Automatic merge failed; fix conflicts and then commit the result.", so)
    nt.assert_not_in("Merging 'master' into 'ftr/work'", so)


def test_ftrbr_rebase_nointbr():
    oriR, cloR = utils.clone_makebr_edit_commit_repo(utils.DIR_REPO_CLONE_FTRBR_UPDATE)

    so,se,rc = cloR.exe_cmd_succ('git intbr-unset')
    so,se,rc = cloR.exe_cmd_deny('git ftrbr-update-rebase')
    nt.eq_(so, "")
    nt.eq_(se, "Integration branch not set")

def test_ftrbr_rebase_uptodate():
    oriR, cloR = utils.clone_makebr_edit_commit_repo(utils.DIR_REPO_CLONE_FTRBR_UPDATE)

    so,se,rc = cloR.exe_cmd_succ('git ftrbr-update-rebase')
    nt.assert_in("Switched to branch 'master'",      se)
    nt.assert_in("Pulling 'master'",                 so)
    nt.assert_in("Rebasing 'ftr/work' onto 'master", so)

def test_ftrbr_rebase_uptodate_local():
    oriR, cloR = utils.clone_makebr_edit_commit_repo(utils.DIR_REPO_CLONE_FTRBR_UPDATE)

    so,se,rc = cloR.exe_cmd_succ('git checkout -b another master')
    so,se,rc = cloR.exe_cmd_succ('git intbr another')
    utils.makebr_edit_commit(cloR, brname='side_of_another')

    so,se,rc = cloR.exe_cmd_succ('git ftrbr-update-rebase')
    nt.assert_in("Intbr 'another' not tracked, jump pull.", so)
    nt.assert_in("Rebasing 'ftr/side_of_another' onto 'another'", so)

def test_ftrbr_rebase_onintbr():
    oriR, cloR = utils.clone_makebr_edit_commit_repo(utils.DIR_REPO_CLONE_FTRBR_UPDATE)

    so,se,rc = cloR.exe_cmd_succ('git checkout master')

    so,se,rc = cloR.exe_cmd_succ('git ftrbr-update-rebase')
    nt.assert_in("Already on 'master'",             se)
    nt.assert_in("Pulling 'master'",                so)
    nt.assert_in("Rebasing 'master' onto 'master'", so)

def test_ftrbr_rebase():
    oriR, cloR = utils.clone_makebr_edit_commit_repo(utils.DIR_REPO_CLONE_FTRBR_UPDATE)

    utils.edit_commit(oriR, 'on origin', 'b.txt')

    so,se,rc = cloR.exe_cmd_succ('git ftrbr-update-rebase')
    nt.assert_in("Pulling 'master'",                  so)
    nt.assert_in("Fast-forward",                      so)
    nt.assert_in("Rebasing 'ftr/work' onto 'master'", so)

def test_ftrbr_rebase_conflict_on_mergeftrbr():
    oriR, cloR = utils.clone_makebr_edit_commit_repo(utils.DIR_REPO_CLONE_FTRBR_UPDATE)

    utils.edit_commit(oriR, 'on origin')

    so,se,rc = cloR.exe_cmd_deny('git ftrbr-update-rebase')
    nt.assert_in("Pulling 'master'",                            so)
    nt.assert_in("Fast-forward",                                so)
    nt.assert_in("Rebasing 'ftr/work' onto 'master'",           so)
    nt.assert_in("CONFLICT (content): Merge conflict in a.txt", so)
    nt.assert_in("Patch failed at 0001 modified file",          so)
    nt.assert_in('When you have resolved this problem run "git rebase --continue"', so)

def test_ftrbr_rebase_conflict_on_pullintbr():
    oriR, cloR = utils.clone_makebr_edit_commit_repo(utils.DIR_REPO_CLONE_FTRBR_UPDATE)
    utils.edit_commit(oriR, 'on origin')
    so,se,rc = cloR.exe_cmd_succ('git checkout master')
    utils.edit_commit(cloR, 'on clone')

    so,se,rc = cloR.exe_cmd_deny('git ftrbr-update-rebase')
    nt.assert_in("Pulling 'master'",                                                  so)
    nt.assert_in("CONFLICT (content): Merge conflict in a.txt",                       so)
    nt.assert_in("Automatic merge failed; fix conflicts and then commit the result.", so)
    nt.assert_not_in("Rebasing 'ftr/work' onto 'master'",                             so)


