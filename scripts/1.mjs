
//TODO

'use strict';

const dependRe = /Mod '([\w ]+)' ([a-z0-9_-]+) ([0-9\.+-]+) requires version ([0-9\.+-]+) or later of mod '([\w ]+)' ([a-z0-9_-]+)/

export function onAnalyze(error){
	const lines = error.message.split('\n')
	var deps = []
	if(lines.length > 1){
		var ok = false
		for(let line of lines){
			if(line.trim() === 'Unmet dependency listing:'){
				ok = true
			}else if(ok){
				let matches = dependRe.exec(line)
				if(matches){
					deps.append({
						modName: matches[1],
						modID: matches[2],
						modVersion: matches[3],
						dependentName: matches[5],
						dependentID: matches[6],
						dependentVersion: matches[4],
					})
				}
			}
		}
	}
	return deps.length === 0 ?null :{ dependents: deps }
}
