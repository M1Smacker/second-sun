"""Render counts-only bench evidence. Run after terminal summary and verification."""
import json
from pathlib import Path

ROOT=Path(r'D:\second-sun-astra')
OUT=ROOT/'data/astra/027'
REPORT=ROOT/'research/astra/reports/027-report.md'


def main():
    s=json.loads((OUT/'summary.json').read_text(encoding='utf-8'))
    m=s['metrics']; bg=s['background']; names=s['configs']
    passed=[name for name,r in s['rules'].items() if r['passes']]
    old=REPORT.read_text(encoding='utf-8')
    prereg=old[old.index('## Pass rule recorded BEFORE scoring'):old.index('## Usage')]
    lines=[f'**{"Passes" if passed else "Fails"}: {len(passed)} of 2 c1a configurations passes the prewritten fixed-setting rule.**', '',
        '# 027 c1a tier-level bench', '',
        'Requested model GPT-6-Astra high; runtime model and effort independently unverified. Branch astra/027-c1a-tier-bench. Tree nodes 1.3, 1.5 and 1.6.', '',prereg,
        '## Findings, CONFIRMED as computed', '',
        'P is the mean recovery across five binary-period bins, not the fraction after pooling all trials. A whole-star bootstrap resamples hosts together, preserving dependence among planets placed on the same host. All intervals below are 95% unless marked 99%. Seed 2026111523, 10,000 draws. A count replay and source-copy checks are producer verification, not an independent scientific review.', '',
        '| Configuration | P all 1,098 %, 95% | P possible 968 %, 95% | T156 R %, 95% | Real | Upside-down |',
        '|---|---:|---:|---:|---:|---:|']
    def interval(key,i):
        r=m[key]
        return f"{100*r['rates'][0][i]:.3f} [{100*r['rate95'][0][0][i]:.2f}, {100*r['rate95'][1][0][i]:.2f}]"
    for i,name in enumerate(names):
        lines.append(f"| {name} | {interval('fixed1098',i)} | {interval('possible968',i)} | {interval('T156reference',i)} | {bg[i]['real']} | {bg[i]['flip']} |")
    lines+=['','The reference T156 subset contains 222 Saturn-like trials from the full 2,000. Full-T156 and physically allowed subset intervals are retained in the machine summary and the tables below. M2 was not applied.','',
        '| Population | Configuration | Gain against B, points (95%) | Gain against matching base, points (95%) |',
        '|---|---|---:|---:|']
    for key in ('fixed1098','possible968'):
        for i,name in enumerate(names):
            r=m[key]
            fmt=lambda suffix:f"{100*r['change_'+suffix][i]:+.3f} [{100*r['change_'+suffix+'95'][0][i]:+.3f}, {100*r['change_'+suffix+'95'][1][i]:+.3f}]"
            lines.append(f'| {key} | {name} | {fmt("B")} | {fmt("base")} |')
    lines+=['','## Rule-by-rule outcome','','Rule (c) requires controls on both planet populations. Rule (e) binds against B, following F1 and 023. The comparison against the corresponding c1a-off configuration is also shown as a diagnostic.','',
        '| Candidate | Rule | Number | Pass? |','|---|---|---|---|']
    for i,j in ((1,0),(3,2)):
        rule=s['rules'][names[i]]; p=m['possible968']
        numbers=dict(a=f"gain {100*p['change_base'][i]:+.3f}, lower 95% {100*p['change_base95'][0][i]:+.3f}",
            b=f"real {bg[i]['real']} / 174, upside-down {bg[i]['flip']} / 79",
            c=f"all-bin control: full {m['fixed1098']['paired_pass'][i]}, possible {p['paired_pass'][i]}",
            d=f"reference R {100*m['T156reference']['rates'][0][i]:.3f} vs base {100*m['T156reference']['rates'][0][j]:.3f}",
            e=f"new-real excess vs B {bg[i]['B']['excess']:.1f}, vs base {bg[i]['base']['excess']:.1f}; limit 5")
        for k in 'abcde':
            lines.append(f'| {names[i]} | {k} | {numbers[k]} | {"PASS" if rule[k] else "FAIL"} |')
    lines+=['','## Equal-alarm analysis','']
    eligible=[n for n,r in s['rules'].items() if r['equal_alarm_eligible']]
    equal=OUT/'equal-alarm.json'
    if equal.exists():
        lines.append('See the equal-alarm table below. The floor is chosen on half the stars, a proposal, not a frozen setting.')
        lines.append('```json\n'+equal.read_text(encoding='utf-8')+'\n```')
    elif not eligible:
        lines.append('Not triggered. Neither candidate fails background rule (b) alone. The preregistration therefore does not authorize trying higher SNR floors on these results.')
    else:
        lines.append('NOT TESTED: eligible candidates '+', '.join(eligible)+'. The task remains partial until the authorized ladder is evaluated.')
    lines+=['','## Gains and losses by binary-period bin','',
        'Counts are paired with the same configuration without c1a. A planet with any novel tier-1 crossing counts once. B and K2 use the saved 013/023 novelty definitions; c1a uses its own untouched background for that comparison.', '',
        '| Population | Candidate | Bin (days) | n | Dip gained / lost | Bump gained / lost | Dip-minus-bump 99%, points | Pass? |',
        '|---|---|---|---:|---:|---:|---:|---|']
    bins=('5 to 10','10 to 14','14 to 20','20 to 27.4','27.4 and up')
    for key in ('fixed1098','possible968'):
        r=m[key]
        for i in (1,3):
            for b,label in enumerate(bins):
                lo,hi=[100*r['paired99'][q][b][i] for q in (0,1)]
                moves=r['moves'][b]
                lines.append(f"| {key} | {names[i]} | {label} | {r['n'][b]} | {moves[0][i][0]} / {moves[0][i][1]} | {moves[1][i][0]} / {moves[1][i][1]} | {lo:+.2f}, {hi:+.2f} | {'PASS' if lo<=0<=hi else 'FAIL'} |")
    lines+=['','## Background and blind spots','','New-event matching follows 023: same campaign, host, sector and arm, within 0.1 day plus half the larger box duration. This is a tolerance match, not exact event identity. Every new real event has private dump-distance and eclipse-width evidence in data/astra/027/new-real-events.json. Missing geometry is reported, never treated as clean.', '',
        '| Configuration | Compared with | New real / upside-down | New real within 12 h of dump | Within one catalogue eclipse width | Unknown geometry |',
        '|---|---|---:|---:|---:|---:|']
    for i in (1,2,3):
        for label in ('B','base'):
            r=bg[i][label];g=r['screen']
            lines.append(f"| {names[i]} | {label} | {r['new_real']} / {r['new_flip']} | {g.get('dump12h',0)} | {g.get('eclipse',0)} | {g.get('unknown',0)} |")
    lines+=['','New SNR-7 candidates are matched to all old SNR-7 candidates before counting hold flags. Counts overlap because one event can have several flags; they are not an additive attribution.', '',
        '| Configuration | Campaign | Arm | New candidates | Held at tier 2 | Tier 1 | Dump | Step | Gap edge | Ramp | Repeater | Dominated |',
        '|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for r in s['holds']:
        counts=' | '.join(str(r['flags'].get(f,0)) for f in ('dump','step','gap_edge','ramp','repeater','dominated'))
        lines.append(f"| {r['config']} | {r['campaign']} | {r['arm']} | {r['new_candidates']} | {r['held_tier2']} | {r['tier1']} | {counts} |")
    lines+=['','## T156 supplementary measures','','| Population | n | B % | B+c1a % | K2 % | K2+c1a % |','|---|---:|---:|---:|---:|---:|']
    for key in ('T156all','T156possible','T156reference_possible'):
        lines.append(f"| {key} | {sum(m[key]['n'])} | "+' | '.join(interval(key,i) for i in range(4))+' |')
    lines+=['','## Identity and verification','','B reproduced P 48.105%, R 34.207%, and background 174 / 79. K2 reproduced possible P 51.02% and background 158 / 63. Both arms of every saved B planet/T156 trial and every saved K2 planet trial were compared, with assertions that can fail. K2 T156 is newly scored here, not an archived K2 identity claim. Raw c1a-off replay identity covered 50 untouched star-sectors, not every injected light curve.', '',
        'Runtime rule checks compared 288 synthetic combinations against the extracted pure X10 rule, including 8 detections of a deliberately omitted cap. The access guard rejected three forbidden access events, allowed an authorized write, and checked 12 copy hashes. These hashes establish byte identity only. The copied mask self-test passed. The final verification file records coverage and arithmetic checks actually completed.', '',
        '## What I did NOT check','','No G1 or sealed-star search. No M2 combination, new mask design, quality change, production filter edit, freeze, known-planet replay or external publication. Fresh-seed confirmation is conditional on passing the prewritten rule. The machine data preserve both-arm trial results; this is producer verification, not an independent second key. The origin of any new background event is not established by proximity to a dump or an eclipse.', '',
        '## STOP SIGNS hit','','Usage meter and runtime model identification were unavailable. Any runtime access failure or scientific identity failure is documented in the work log; no bypass of the access guard is authorized.', '',
        '## QUEUE PROPOSALS','','Claude should file the measured c1a result under Tree node 1.3, with background and control evidence under nodes 1.5 and 1.6. No frozen setting is changed.', '',
        '## IDEAS','','None beyond the brief. M2 is a subsequent conditional test only if K2+c1a passes. It was not run.', '',
        '## Disagreements with Claude','','No technical direction was silently changed. Conservative interpretations are recorded in the pre-scoring pass rule.', '',
        '## Questions for Ahmed','','None required for this bench.', '',
        '## Usage','','Predicted 50 five-hour / 8 weekly points; cap 60 five-hour. Actual use and runtime model/effort are unverified because the headless meter is unavailable. Lesson: a detector change must be priced using new detections and new untouched context at the final tier.', '',
        '**Next:** Claude reviews this report and the private verification evidence before deciding whether c1a deserves further work. Review only; no additional Codex compute is requested, and its usage cost is unmeasured.']
    REPORT.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    # Counts-only stratified evidence, separate to keep the main table readable.
    tables=['# 027 background strata','','Counts by campaign, period, product, era and magnitude.','']
    for i,name in enumerate(names):
        tables+=['## '+name,'','| Stratum | Count |','|---|---:|']
        for key,n in sorted({**bg[i]['by_campaign_bin'],**bg[i]['strata']}.items()):
            tables.append(f'| {key} | {n} |')
    (REPORT.parent/'027-tables.md').write_text('\n'.join(tables)+'\n',encoding='utf-8')
    print('Rendered 027 report and count strata.')


if __name__=='__main__':
    main()
