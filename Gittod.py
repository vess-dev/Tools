#============================================================================================================================================
# gittod.py : Take a git hash as a commandline argument and modify the history of the current repository to a desired time of day.
#============================================================================================================================================
# Imports

# Local imports.
import os
import subprocess
import sys

# Installed imports.

#============================================================================================================================================
# Constants

# Git command for showing git history.
COM_GIT_HISTORY = """git log --graph --pretty=format:'%C(auto)%H%d (%ci) %s'"""
# Git command for getting a commit's date.
COM_GIT_DATE = """git show --no-patch --no-notes --pretty='%cd'"""
# Git command for changing dates.
COM_GIT_CHANGE = """FILTER_BRANCH_SQUELCH_WARNING=1 git filter-branch --env-filter \ 'if [ $GIT_COMMIT = $1 ] then export GIT_AUTHOR_DATE="$2" export GIT_COMMITTER_DATE="$2" fi'"""

#============================================================================================================================================
# Sanitize the input command.

def clean_command(in_com):
	return in_com.strip()

#============================================================================================================================================
# Show a pretty history of git with hash and date.

def run_command(in_com):
	com_final = clean_command(in_com)
	return os.popen(com_final).read()

#============================================================================================================================================
# Get the history of the repository in a nice format.

def get_history():
	git_history = run_command(COM_GIT_HISTORY)
	print(git_history)
	return

#============================================================================================================================================
# Get the date of a specific git commit by hash.

def get_date(in_hash):
	com_full = f"{COM_GIT_DATE} '{in_hash}'"
	com_result = run_command(com_full)
	return com_result.strip()

#============================================================================================================================================
# Main

def main(in_hash, in_mod):
	msg_start = f"Modifiying date of hash: '{in_hash}', to: '{in_mod}'"
	print(msg_start)
	date_string = get_date(in_hash)
	msg_date = f"Got date of hash: '{date_string}'"
	print(msg_date)
	date_split = date_string.split(" ")
	date_split[3] = in_mod
	date_final = " ".join(date_split)
	msg_change = f"Made changed date of hash: '{date_final}'"
	print(msg_change)
	com_final = COM_GIT_CHANGE
	com_final = com_final.replace("$1", in_hash)
	com_final = com_final.replace("$2", date_final)
	msg_final = f"Prepared final command: '\n{com_final}\n'"
	print(msg_final)
	run_command(com_final)
	return

#============================================================================================================================================
# Run

if __name__ == "__main__":
	if len(sys.argv) == 1:
		get_history()
	else:
		main(sys.argv[1], sys.argv[2])
	sys.exit(0)

#============================================================================================================================================