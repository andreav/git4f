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
    print '> setUpModule test_ftrbr_push'
    utils.sandbox()

def test_ftrbr_push_nointbr():
    oriR, cloR = utils.clone_makebr_edit_commit_repo(utils.DIR_REPO_CLONE_FTRBR_PUSH)

    so,se,rc = cloR.exe_cmd_succ('git intbr-unset')
    so,se,rc = cloR.exe_cmd_deny('git ftrbr-push')
    nt.eq_(so, "")
    nt.eq_(se, "Integration branch not set\nCannot push.")
    nt.assert_not_in("Pulling 'master'", so)
    nt.assert_not_in("Merging", so)

def test_ftrbr_push_onintbr_local():
    oriR, cloR = utils.clone_makebr_edit_commit_repo(utils.DIR_REPO_CLONE_FTRBR_PUSH)

    so,se,rc = cloR.exe_cmd_succ('git checkout -b another master')
    so,se,rc = cloR.exe_cmd_succ('git intbr another')

    so,se,rc = cloR.exe_cmd_deny('git ftrbr-push')
    nt.eq_("", so)
    nt.assert_in("Integration branch 'another' not tracked", se)
    nt.assert_in("Cannot push.", se)
    nt.assert_not_in("Pushing", so)

def test_ftrbr_push_intbr_local():
    oriR, cloR = utils.clone_makebr_edit_commit_repo(utils.DIR_REPO_CLONE_FTRBR_PUSH)

    so,se,rc = cloR.exe_cmd_succ('git checkout -b another master')
    so,se,rc = cloR.exe_cmd_succ('git intbr another')
    utils.makebr_edit_commit(cloR, brname='side_of_another')

    so,se,rc = cloR.exe_cmd_deny('git ftrbr-push')
    nt.eq_("", so)
    nt.assert_in("Integration branch 'another' not tracked", se)
    nt.assert_in("Cannot push.", se)
    nt.assert_not_in("Pushing", so)

def test_ftrbr_push():
    oriR, cloR = utils.clone_makebr_edit_commit_repo(utils.DIR_REPO_CLONE_FTRBR_PUSH)

    so,se,rc = cloR.exe_cmd_succ('git ftrbr-push')
    nt.assert_in("Pulling 'master'",               so)
    nt.assert_in("Merging 'ftr/work' into 'master'", so)
    nt.assert_in("Pushing 'master' to 'origin'",   so)

def test_ftrbr_push_onintbr():
    oriR, cloR = utils.clone_makebr_edit_commit_repo(utils.DIR_REPO_CLONE_FTRBR_PUSH)

    so,se,rc = cloR.exe_cmd_succ('git checkout master')
    so,se,rc = cloR.exe_cmd_succ('git ftrbr-push')
    nt.assert_in("Pulling 'master'",               so)
    nt.assert_in("Merging 'master' into 'master'", so)
    nt.assert_in("Pushing 'master' to 'origin'",   so)

def test_ftrbr_push_conflict_on_mergeftrbr():
    oriR, cloR = utils.clone_makebr_edit_commit_repo(utils.DIR_REPO_CLONE_FTRBR_PUSH)

    utils.edit_commit(oriR, 'on origin')

    so,se,rc = cloR.exe_cmd_deny('git ftrbr-push')
    nt.assert_in("Pulling 'master'",                 so)
    nt.assert_in("Fast-forward",                     so)
    nt.assert_in("Merging 'ftr/work' into 'master'", so)
    nt.assert_in("CONFLICT (content): Merge conflict in a.txt", so)
    nt.assert_in("Automatic merge failed; fix conflicts and then commit the result.", so)

def test_ftrbr_push_conflict_on_pullintbr():
    oriR, cloR = utils.clone_makebr_edit_commit_repo(utils.DIR_REPO_CLONE_FTRBR_PUSH)
    utils.edit_commit(oriR, 'on origin')
    so,se,rc = cloR.exe_cmd_succ('git checkout master')
    utils.edit_commit(cloR, 'on clone')

    so,se,rc = cloR.exe_cmd_deny('git ftrbr-push')
    nt.assert_in("Pulling 'master'",                 so)
    nt.assert_not_in("Fast-forward",                 so)
    nt.assert_not_in("Merging 'ftr/work' into 'master'", so)
    nt.assert_in("CONFLICT (content): Merge conflict in a.txt", so)
    nt.assert_in("Automatic merge failed; fix conflicts and then commit the result.", so)

def test_ftrbr_push_rebase_nointbr():
    oriR, cloR = utils.clone_makebr_edit_commit_repo(utils.DIR_REPO_CLONE_FTRBR_PUSH)

    so,se,rc = cloR.exe_cmd_succ('git intbr-unset')
    so,se,rc = cloR.exe_cmd_deny('git ftrbr-push-rebase')
    nt.eq_(so, "")
    nt.eq_(se, "Integration branch not set\nCannot push.")
    nt.assert_not_in("Pulling 'master'", so)
    nt.assert_not_in("Rebasing", so)

def test_ftrbr_push_rebase_onintbr_local():
    oriR, cloR = utils.clone_makebr_edit_commit_repo(utils.DIR_REPO_CLONE_FTRBR_PUSH)

    so,se,rc = cloR.exe_cmd_succ('git checkout -b another master')
    so,se,rc = cloR.exe_cmd_succ('git intbr another')

    so,se,rc = cloR.exe_cmd_deny('git ftrbr-push-rebase')
    nt.eq_("", so)
    nt.assert_in("Integration branch 'another' not tracked", se)
    nt.assert_in("Cannot push.", se)
    nt.assert_not_in("Pushing", so)

def test_ftrbr_push_rebase_intbr_local():
    oriR, cloR = utils.clone_makebr_edit_commit_repo(utils.DIR_REPO_CLONE_FTRBR_PUSH)

    so,se,rc = cloR.exe_cmd_succ('git checkout -b another master')
    so,se,rc = cloR.exe_cmd_succ('git intbr another')
    utils.makebr_edit_commit(cloR, brname='side_of_another')

    so,se,rc = cloR.exe_cmd_deny('git ftrbr-push-rebase')
    nt.eq_("", so)
    nt.assert_in("Integration branch 'another' not tracked", se)
    nt.assert_in("Cannot push.", se)
    nt.assert_not_in("Pushing", so)

def test_ftrbr_push_rebase():
    oriR, cloR = utils.clone_makebr_edit_commit_repo(utils.DIR_REPO_CLONE_FTRBR_PUSH)

    so,se,rc = cloR.exe_cmd_succ('git ftrbr-push-rebase')
    nt.assert_in("Pulling 'master'",               so)
    nt.assert_in("Rebasing 'ftr/work' onto 'master'", so)
    nt.assert_in("Merging 'ftr/work' into 'master'", so)
    nt.assert_in("Pushing 'master' to 'origin'",   so)

def test_ftrbr_push_rebase_onintbr():
    oriR, cloR = utils.clone_makebr_edit_commit_repo(utils.DIR_REPO_CLONE_FTRBR_PUSH)

    so,se,rc = cloR.exe_cmd_succ('git checkout master')
    so,se,rc = cloR.exe_cmd_succ('git ftrbr-push-rebase')
    nt.assert_in("Pulling 'master'",               so)
    nt.assert_in("Rebasing 'master' onto 'master'",so)
    nt.assert_in("Merging 'master' into 'master'", so)
    nt.assert_in("Pushing 'master' to 'origin'",   so)

def test_ftrbr_push_rebase_conflict_on_mergeftrbr():
    oriR, cloR = utils.clone_makebr_edit_commit_repo(utils.DIR_REPO_CLONE_FTRBR_PUSH)

    utils.edit_commit(oriR, 'on origin')

    so,se,rc = cloR.exe_cmd_deny('git ftrbr-push-rebase')
    nt.assert_in("Pulling 'master'",                 so)
    nt.assert_in("Fast-forward",                     so)
    nt.assert_in("Rebasing 'ftr/work' onto 'master'",so)
    nt.assert_in("CONFLICT (content): Merge conflict in a.txt", so)
    nt.assert_in("Patch failed at 0001 modified file", so)
    nt.assert_in('When you have resolved this problem run "git rebase --continue"', so)

def test_ftrbr_push_rebase_conflict_on_pullintbr():
    oriR, cloR = utils.clone_makebr_edit_commit_repo(utils.DIR_REPO_CLONE_FTRBR_PUSH)
    utils.edit_commit(oriR, 'on origin')
    so,se,rc = cloR.exe_cmd_succ('git checkout master')
    utils.edit_commit(cloR, 'on clone')

    so,se,rc = cloR.exe_cmd_deny('git ftrbr-push-rebase')
    nt.assert_in("Pulling 'master'",                 so)
    nt.assert_not_in("Fast-forward",                 so)
    nt.assert_not_in("Rebasing 'ftr/work' onto 'master'", so)
    nt.assert_in("CONFLICT (content): Merge conflict in a.txt", so)
    nt.assert_in("Automatic merge failed; fix conflicts and then commit the result.", so)
    nt.assert_not_in("Rebasing 'ftr/work' onto 'master'",                             so)

def test_ftrbr_push_detachedhead():
    oriR, cloR = utils.clone_makebr_edit_commit_repo(utils.DIR_REPO_CLONE_FTRBR_PUSH)

    so,se,rc = cloR.exe_cmd_succ('git checkout HEAD~1')
    so,se,rc = cloR.exe_cmd_deny('git ftrbr-push')
    nt.eq_(se, "detached-head\nCannot integrate.")
    nt.eq_(so, '')

def test_ftrbr_push_rebase_detachedhead():
    oriR, cloR = utils.clone_makebr_edit_commit_repo(utils.DIR_REPO_CLONE_FTRBR_PUSH)

    so,se,rc = cloR.exe_cmd_succ('git checkout HEAD~1')
    so,se,rc = cloR.exe_cmd_deny('git ftrbr-push-rebase')
    nt.eq_(se, "detached-head\nCannot integrate.")
    nt.eq_(so, '')



