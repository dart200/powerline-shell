import re
import subprocess
import signal

class Alarm(Exception):
    pass

def alrmHandler(signum, frame):
    raise Alarm

def get_git_status():
    has_pending_commits = True
    has_untracked_files = False
    origin_position = ""
    failed = False

    # Set the signal handler and a 5-second alarm
    signal.signal(signal.SIGALRM, alrmHandler)
    signal.alarm(3)

    try:
        p = subprocess.Popen(['git', 'status', '--ignore-submodules'], stdout=subprocess.PIPE)
        output = p.communicate()[0]
        signal.alarm(0)
    except Alarm:
        p.kill()
        return False, False, "", True

    for line in output.split('\n'):
        origin_status = re.findall(
                r"Your branch is (ahead|behind).*?(\d+) comm", line)
        if origin_status:
            origin_position = " %d" % int(origin_status[0][1])
            if origin_status[0][0] == 'behind':
                origin_position += u'\u21E3'
            if origin_status[0][0] == 'ahead':
                origin_position += u'\u21E1'

        if line.find('nothing to commit') >= 0:
            has_pending_commits = False
        if line.find('Untracked files') >= 0:
            has_untracked_files = True
    return has_pending_commits, has_untracked_files, origin_position, failed

def add_git_segment():
    #cmd = "git branch 2> /dev/null | grep -e '\\*'"
    p1 = subprocess.Popen(['git', 'branch', '--no-color'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p2 = subprocess.Popen(['grep', '-e', '\\*'], stdin=p1.stdout, stdout=subprocess.PIPE)
    output = p2.communicate()[0].strip()
    if not output:
        return

    branch = output.rstrip()[2:]
    bg = Color.REPO_CLEAN_BG
    fg = Color.REPO_CLEAN_FG

    has_pending_commits, has_untracked_files, origin_position, failed = get_git_status()
    branch += origin_position
    if has_untracked_files:
        branch += ' +'
    if has_pending_commits:
        bg = Color.REPO_DIRTY_BG
        fg = Color.REPO_DIRTY_FG
    if failed:
        bg = Color.REPO_FAIL_BG
        fg = Color.REPO_FAIL_FG


    powerline.append(' %s ' % branch, fg, bg)

try:
    add_git_segment()
except OSError:
    pass
except subprocess.CalledProcessError:
    pass
