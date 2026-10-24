/* Load with controller.cjs inside functions.exec. Uses only supported tools. */
'use strict';
module.exports = function adapter(tools, repoPath, journalPath) {
  const quote = value => "'" + String(value).replace(/'/g, "'\\''") + "'";
  const script = repoPath + '/.claude/skills/_shared/video-rounds/journal.py';
  async function journal(action, payload) {
    const result = await tools.exec_command({
      cmd:'python3 ' + quote(script) + ' ' + action + ' --path ' + quote(journalPath) + ' --json ' + quote(JSON.stringify(payload || {})),
      workdir:repoPath, max_output_tokens:20000
    });
    if (result.exit_code !== 0 || result.session_id) throw new Error('Journal operation not confirmed: ' + result.output);
    return JSON.parse(result.output);
  }
  return {
    call: async (name,args) => {
      if (!name.startsWith('mcp__codex_app__') || typeof tools[name] !== 'function') throw new Error('Native capability missing: ' + name);
      return tools[name](args);
    },
    store:{load:() => journal('read'),cas:(expected,state) => journal('cas',{expected,state})},
    verifyLocks:(files,decisions) => journal('verify',{files,decisions}),
    verifyRepoPath:async(a,b) => {
      const code = 'import os,sys,json; print(json.dumps(os.path.samefile(sys.argv[1],sys.argv[2])))';
      const r = await tools.exec_command({cmd:'python3 -c ' + quote(code) + ' ' + quote(a) + ' ' + quote(b), workdir:repoPath, max_output_tokens:1000});
      if (r.exit_code !== 0 || r.session_id) return false;
      return r.output.trim() === 'true';
    }
  };
};
