#!/usr/bin/python3

import json
import os
import re

jerror_matcher = re.compile(r'^(\*\.[\w\d$_]+|[\w\d$_]+(?:\.[\w\d$_]+)*):\s+(.*)$')

version_info: dict = {}

def read_json(path: str) -> dict:
	with open(path, 'r') as fd:
		return json.load(fd)

def check_and_update_version(new_version: dict):
	global version_info
	with open('version.json', 'r+') as fd:
		version_info_2 = json.load(fd)
		if version_info != version_info_2:
			print('Error: version changed during create error and solution files')
			exit(1)
		fd.truncate(0)
		fd.seek(0)
		version_info.update(new_version)
		json.dump(version_info, fd, indent='\t')

def main():
	global version_info
	with open('version.json', 'r') as fd:
		version_info = json.load(fd)

	jerrors: dict[int, dict] = {}
	while True:
		try:
			jerror = input('Error class and message: ')
		except KeyboardInterrupt:
			jerror = ''
		if len(jerror) == 0:
			if len(jerrors) == 0:
				ids = input('The target error IDs: ')
				if len(ids) == 0:
					return
				jerrors = dict(map(lambda id: (int(id), read_json(os.path.join('errors', f'{id}.json'))), ids.split(',')))
			break
		gp = jerror_matcher.match(jerror)
		if gp is None:
			jerr_cls = ''
			jerr_msg = jerror
		else:
			jerr_cls = gp[1]
			jerr_msg = gp[2]
		error_file_id: int = version_info['errorIncId'] + 1
		check_and_update_version({
			'patch': version_info['patch'] + 1,
			'errorIncId': error_file_id,
		})
		jerrors[error_file_id] = {
			'error': jerr_cls,
			'message': jerr_msg,
			'solutions': [],
		}

	while True:
		try:
			tags_str = input('Add solution tags: ')
		except KeyboardInterrupt:
			print()
			break
		if len(tags_str) == 0:
			break
		try:
			tags: list[str] = list(map(lambda s: s.strip(), tags_str.split(',')))
			sol_desc = input('Solution description: ')
			sol_link = input('Solution link to: ')

			sol_file = json.dumps({
				'tags': tags,
				'description': sol_desc,
				'link_to': sol_link,
			}, indent='\t', ensure_ascii=False)
			print(f'saving as `solutions/*.json`:')
			print(sol_file)
			if input('Continue? (Y/n) ') not in ['', 'y', 'Y']:
				print('aborted')
				continue

			solution_file_id: int = version_info['solutionIncId'] + 1
			check_and_update_version({
				'patch': version_info['patch'] + 1,
				'solutionIncId': solution_file_id,
			})
			for je in jerrors.values():
				je['solutions'].append(solution_file_id)
			with open(os.path.join('solutions', f'{solution_file_id}.json'), 'w', encoding='utf-8') as fd:
				fd.write(sol_file)
			print('saved')
		except KeyboardInterrupt:
			print()

	for fid, je in jerrors.items():
		with open(os.path.join('errors', f'{fid}.json'), 'w') as fd:
			json.dump(je, fd, indent='\t')

if __name__ == '__main__':
	main()
