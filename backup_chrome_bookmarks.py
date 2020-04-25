#!/usr/bin/env python3

import argparse
import filecmp
import os
from shutil import copyfile
from datetime import datetime

CHROME_BOOKMARKS_FOLDER_PATH_DEFAULT = os.getenv("HOME") + '/Library/Application Support/Google/Chrome/Default'
CHROME_BOOKMARKS_FILE_NAME = 'Bookmarks'
BACKUP_FILE_PREFIX = 'chrome_backup_'
MAX_BACKUP_FILES = 5

def parse_backup_folder(backup_folder):

	existing_files = []

	for file in os.listdir(backup_folder):
		if file.startswith(BACKUP_FILE_PREFIX):
			existing_files.append(file)

	# Sort according to newest file
	existing_files.sort(reverse=True)

	return existing_files

def check_paths(backup_folder, chrome_bookmarks_folder):

	if not os.path.exists(backup_folder):
		raise Exception('Provided backup folder does not exist.')
	if not os.path.exists(chrome_bookmarks_folder):
		raise Exception('Chrome bookmarks folder does not exist.')
	if not os.path.exists(chrome_bookmarks_folder + '/' + CHROME_BOOKMARKS_FILE_NAME):
		raise Exception('Chrome bookmarks file does not exist.')

def main(backup_folder, chrome_bookmarks_folder):

	check_paths(backup_folder, chrome_bookmarks_folder)
	existing_files = parse_backup_folder(backup_folder)

	existing_files_count = len(existing_files)

	if existing_files_count < 1:
		# No backup files found
		existing_files.append('')
	
	# Compare newest backup file with bookmarks file
	if filecmp.cmp(backup_folder + '/' + existing_files[0], 
		CHROME_BOOKMARKS_FOLDER_PATH_DEFAULT + '/' + CHROME_BOOKMARKS_FILE_NAME):
		# No delta; no new bookmarks have been added since last backup
		return

	# Delta exists; need to backup bookmarks
	now = datetime.now()
	backup_file_suffix = now.strftime('%Y_%m_%d_%H_%M_%S')
	copyfile(chrome_bookmarks_folder + '/' + CHROME_BOOKMARKS_FILE_NAME,
		backup_folder + '/' + BACKUP_FILE_PREFIX + backup_file_suffix)

	# Maintain only 5 backup files
	# +1 because number of files in folder is |existing_files| + 1
	if existing_files_count + 1 > MAX_BACKUP_FILES:
		os.remove(backup_folder + '/' + existing_files[existing_files_count - 1])

def argument_parser():

	parser = argparse.ArgumentParser(description='Backup Chrome bookmarks.')
	parser.add_argument('backup_folder', action='store',
		help='Absolute path to backup folder')
	parser.add_argument('--chrome_bookmarks_folder', action='store',
		dest='chrome_bookmarks_folder',
		default=CHROME_BOOKMARKS_FOLDER_PATH_DEFAULT,
		help='Abolute path to Chrome bookmarks folder (default: %(default)s)')

	args = parser.parse_args()

	return(args.backup_folder, args.chrome_bookmarks_folder)

if __name__ == '__main__':

	backup_folder, chrome_bookmarks_folder = argument_parser()

	main(backup_folder, chrome_bookmarks_folder)
