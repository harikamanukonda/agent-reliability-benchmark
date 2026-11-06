"""Generate an offline report from measured trajectories; no model execution."""
import html
import json
from pathlib import Path
ROOT=Path(__file__).parent

def render(source,target):
 data=json.loads(Path(source).read_text());sections=[];summary=[]
 for name,run in data.items():
  if not isinstance(run,dict) or 'rows' not in run:continue
  summary.append(f'<tr><td>{html.escape(name)}</td><td>{run["task_success_rate"]:.0%}</td><td>{run["unauthorized_attempts"]}</td><td>{run["blocked_actions"]}</td><td>{run["simulated_unauthorized_effects"]}</td></tr>')
  episodes=[]
  for row in run['rows']:
   episodes.append('<details><summary>'+html.escape(row['scenario'])+' · '+('PASS' if row['success'] else 'FAIL')+'</summary><pre>'+html.escape(json.dumps(row,indent=2))+'</pre></details>')
  sections.append('<section><h2>'+html.escape(name)+'</h2>'+''.join(episodes)+'</section>')
 Path(target).write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Agent Reliability Benchmark</title><style>body{font:15px system-ui;background:#101b19;color:#e4ede5;max-width:1100px;margin:40px auto;padding:20px}h1{color:#c8f580;font-size:40px}td,th{padding:12px;text-align:left;border-bottom:1px solid #526b5c}table{border-collapse:collapse;width:100%}.scroll{overflow:auto}details{padding:15px;background:#1c3027;margin:12px 0;border-radius:6px}summary{cursor:pointer}pre{white-space:pre-wrap;overflow-wrap:anywhere;line-height:1.6}p{color:#b5c8b9}</style><h1>Agent Reliability Benchmark</h1><p>Measured outcomes from ten synthetic scenarios. Scripted policies and actual model results are identified separately. All tool side effects are simulated.</p><div class="scroll"><table><tr><th>Agent</th><th>Success</th><th>Unauthorized attempts</th><th>Blocked</th><th>Unauthorized effects</th></tr>'+''.join(summary)+'</table></div>'+''.join(sections)+'<h2>Limits</h2><p>'+html.escape(' '.join(data['limitations']))+'</p></html>')
if __name__=='__main__':
 source=ROOT/'reports/local-model.json'
 if not source.exists():source=ROOT/'reports/scripted-baselines.json'
 render(source,ROOT/'reports/benchmark.html')
