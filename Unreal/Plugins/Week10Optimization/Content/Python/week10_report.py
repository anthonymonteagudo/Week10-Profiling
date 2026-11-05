"""Portable report writer and explicit CSV-window analysis; no Unreal dependency."""
from pathlib import Path
import json,csv,math,statistics,hashlib


def summarize_capture(path,start,stop):
    path=Path(path)
    if not 0 <= start < stop:
        raise ValueError('Require 0 <= start < stop; use a documented steady data-row window.')
    with path.open(encoding='utf-8-sig',newline='') as source:
        rows=list(csv.DictReader(source))
    window=rows[start:stop]
    if len(window)!=stop-start:
        raise ValueError(f'{path.name}: incomplete capture window [{start}:{stop}]')
    metrics={}
    for name in ['FrameTime','GameThreadTime','RenderThreadTime','GPUTime','RHIThreadTime','RHI/DrawCalls']:
        if name not in window[0]:
            continue
        try: values=[float(row[name]) for row in window]
        except (TypeError,ValueError) as error: raise ValueError(f'{path.name}: invalid {name}') from error
        if not all(math.isfinite(x) and x>=0 for x in values):
            raise ValueError(f'{path.name}: nonfinite or negative {name}')
        ordered=sorted(values)
        metrics[name]={'unit':'calls' if 'DrawCalls' in name else 'ms','median':statistics.median(values),'p95':ordered[math.ceil(.95*len(ordered))-1],'min':min(values),'max':max(values)}
    if 'FrameTime' not in metrics: raise ValueError('Missing FrameTime column')
    return {'file':path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'window':[start,stop],'samples':len(window),'metrics':metrics,'budget_ms':1000/60,'frames_over_budget':sum(float(r['FrameTime'])>1000/60 for r in window),'conditions':'Historical capture: match camera, settings, build, hardware and warm-up separately. Not current audit timings.'}


def write_dashboard(report,folder):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    raw=json.dumps(report,indent=2,ensure_ascii=False)
    (folder/'report.json').write_text(raw,encoding='utf-8')
    # JSON is data, never interpolated into executable JavaScript or HTML nodes.
    embedded=raw.replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    template=(Path(__file__).parent/'dashboard.html').read_text(encoding='utf-8')
    (folder/'index.html').write_text(template.replace('<!--REPORT_JSON-->',embedded),encoding='utf-8')
    return folder/'index.html'
