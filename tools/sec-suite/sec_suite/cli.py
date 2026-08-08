"""sec-suite CLI entrypoint"""
import json
import click
from pathlib import Path
from . import netscan, web_audit, osint, direnum, web_fuzzer, sql_checker, pcap_analyzer, report

OUT_DIR = 'sec-suite-output'

@click.group()
def cli():
    """sec-suite - authorized security toolkit. Use only with permission."""
    pass

@cli.command()
@click.argument('targets', nargs=-1, required=True)
@click.option('--workers', default=50, help='Parallel workers (default 50)')
@click.option('--out', default=OUT_DIR)
def netscan_cmd(targets, workers, out):
    Path(out).mkdir(parents=True, exist_ok=True)
    res = netscan.discover_and_scan(list(targets), workers=workers)
    p = Path(out)/'netscan.json'
    p.write_text(json.dumps(res, indent=2))
    click.echo(f'Wrote {p}')

@cli.command()
@click.argument('urls', nargs=-1, required=True)
@click.option('--out', default=OUT_DIR)
def web_audit_cmd(urls, out):
    Path(out).mkdir(parents=True, exist_ok=True)
    results = [web_audit.audit_url(u) for u in urls]
    p = Path(out)/'web_audit.json'
    p.write_text(json.dumps(results, indent=2))
    click.echo(f'Wrote {p}')

@cli.command()
@click.argument('domains', nargs=-1, required=True)
@click.option('--out', default=OUT_DIR)
def osint_cmd(domains, out):
    Path(out).mkdir(parents=True, exist_ok=True)
    results = [osint.harvest(d) for d in domains]
    p = Path(out)/'osint.json'
    p.write_text(json.dumps(results, indent=2))
    click.echo(f'Wrote {p}')

@cli.command()
@click.argument('base_url')
@click.option('--wordlist', type=click.Path(), default=None)
@click.option('--rate', default=5, help='Requests per second (default 5)')
@click.option('--out', default=OUT_DIR)
def direnum_cmd(base_url, wordlist, rate, out):
    Path(out).mkdir(parents=True, exist_ok=True)
    res = direnum.run_direnum(base_url, wordlist=wordlist, rps=rate)
    p = Path(out)/'direnum.json'
    p.write_text(json.dumps(res, indent=2))
    click.echo(f'Wrote {p}')

@cli.command()
@click.argument('url')
@click.option('--param', default=None, help='Parameter name to fuzz (optional)')
@click.option('--payloads', type=click.Path(), default=None, help='file with payloads (one per line)')
@click.option('--max', default=200, help='Maximum requests (default 200)')
@click.option('--out', default=OUT_DIR)
def web_fuzz_cmd(url, param, payloads, max, out):
    Path(out).mkdir(parents=True, exist_ok=True)
    res = web_fuzzer.fuzz(url, param_name=param, payload_file=payloads, max_requests=max)
    p = Path(out)/'web_fuzz.json'
    p.write_text(json.dumps(res, indent=2))
    click.echo(f'Wrote {p}')

@cli.command()
@click.argument('url')
@click.option('--confirm', is_flag=True, help='Confirm you have permission to run active SQL checks')
@click.option('--out', default=OUT_DIR)
def sql_check_cmd(url, confirm, out):
    if not confirm:
        click.echo('REFUSAL: sql-checker requires --confirm and explicit permission. Aborting.')
        return
    Path(out).mkdir(parents=True, exist_ok=True)
    res = sql_checker.run_checks(url)
    p = Path(out)/'sql_check.json'
    p.write_text(json.dumps(res, indent=2))
    click.echo(f'Wrote {p}')

@cli.command()
@click.argument('pcap_file', type=click.Path(exists=True))
@click.option('--out', default=OUT_DIR)
def pcap_cmd(pcap_file, out):
    Path(out).mkdir(parents=True, exist_ok=True)
    res = pcap_analyzer.analyze(pcap_file)
    p = Path(out)/'pcap.json'
    p.write_text(json.dumps(res, indent=2))
    click.echo(f'Wrote {p}')

@cli.command()
@click.option('--in-dir', default=OUT_DIR)
@click.option('--out-file', default='sec-suite-report.html')
def report_cmd(in_dir, out_file):
    d = report.collect_results(in_dir)
    html = report.render_html(d)
    Path(out_file).write_text(html)
    click.echo(f'Wrote {out_file}')
