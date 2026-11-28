import {pathToFileURL} from 'node:url';
import {runFourRole} from './server.mjs';
export const ROLE='mediator';
if(process.argv[1]&&pathToFileURL(process.argv[1]).href===import.meta.url)
 await runFourRole(ROLE);
