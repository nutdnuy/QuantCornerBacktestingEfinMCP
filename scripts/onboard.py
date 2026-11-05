"""Check the local runtime and initialize a private draft without claiming MCP access."""
import argparse,json,sys
from pathlib import Path

def setup(workspace):
    if sys.version_info < (3,9):raise ValueError('Python 3.9+ required')
    root=Path(__file__).resolve().parents[1]
    if not (root/'assets/quantcorner-mark-light.svg').is_file():raise ValueError('Missing authentic logo')
    w=Path(workspace).expanduser().resolve();w.mkdir(parents=True,exist_ok=True)
    state={'schema_version':1,'local_runtime':'ready','efin_connection':'not_checked','capabilities':{},'grill_me':'discover_in_host','secrets_stored':False}
    plan={'approved':False,'question':None,'symbol':None,'phase':'development','data_audit_passed':False,'price_only_diagnostic_acknowledged':False,'engine':{'strategy':'sma','fast':20,'slow':200,'initial_cash':None,'fee_bps':None,'slippage_bps':None,'lot_size':None,'annual_rf':0,'annual_mar':0,'terminal_liquidation':False,'currency':'THB'},'benchmark':'same-asset buy-and-hold','limitations':[]}
    for name,obj in [('onboarding.json',state),('plan.json',plan)]:
        path=w/name
        if not path.exists():path.write_text(json.dumps(obj,indent=2)+'\n')
    if not (w/'.gitignore').exists():(w/'.gitignore').write_text('*\n')
    return {'workspace':str(w),'local_runtime':'ready','efin_connection':'not_checked','next':'Discover host Efin tools, run smoke test, then grill-me interview; complete plan.json.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--workspace',required=True);a=p.parse_args()
    try:print(json.dumps(setup(a.workspace),indent=2))
    except (ValueError,OSError) as e:p.exit(2,str(e)+'\n')
