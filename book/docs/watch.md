# Search window

<p class="ss-meta">Watch the search · updates by itself · counts only</p>

<div id="ss-watch" class="sw">Loading...</div>

<style>
.sw { max-width: 760px; }
.sw-light { display: flex; gap: 14px; align-items: center; padding: 14px 16px; border-radius: var(--ss-radius); border: 1px solid var(--ss-line); background: var(--ss-surface); font-size: 17px; }
.sw-light small { color: var(--ss-text-2); font-size: 14px; }
.sw-dot { width: 18px; height: 18px; border-radius: 50%; flex: none; background: var(--ss-text-3); }
.sw-l-live .sw-dot { background: #3ecf6e; animation: sw-pulse 1.6s infinite; }
.sw-l-warn .sw-dot { background: #eebf6a; }
.sw-l-stale .sw-dot { background: #e5584f; }
.sw-l-done .sw-dot { background: var(--ss-accent); }
@keyframes sw-pulse { 0% { box-shadow: 0 0 0 0 rgba(62, 207, 110, .6); } 70% { box-shadow: 0 0 0 12px rgba(62, 207, 110, 0); } 100% { box-shadow: 0 0 0 0 rgba(62, 207, 110, 0); } }
.sw-upd, .sw-small { color: var(--ss-text-2); font-size: 14px; }
.sw-now { font-size: 17px; margin: .4em 0; }
.sw-note { background: var(--ss-surface); border-left: 4px solid var(--ss-accent); padding: 8px 14px; border-radius: var(--ss-radius); }
.sw-blind { background: var(--ss-surface); border-left: 4px solid var(--ss-accent); padding: 10px 14px; border-radius: var(--ss-radius); }
.sw h3 { margin-top: 1.6em; }
.sw-row, .sw-flag { margin: 10px 0; }
.sw-lab { display: flex; justify-content: space-between; gap: 12px; font-size: 15px; }
.sw-bar { background: var(--ss-surface); border: 1px solid var(--ss-line); border-radius: 4px; height: 12px; overflow: hidden; }
.sw-bar i { display: block; height: 100%; background: var(--ss-text-3); transition: width .6s; }
.sw-bar.sw-keep i, .sw-row .sw-bar i { background: var(--ss-accent); }
.sw-flow { display: flex; flex-direction: column; align-items: stretch; gap: 4px; }
.sw-stage { border: 1px solid var(--ss-line); border-radius: var(--ss-radius); padding: 10px 14px; background: var(--ss-surface); display: grid; gap: 2px; }
.sw-stage small { color: var(--ss-text-3); }
.sw-stage span { color: var(--ss-text-2); font-size: 14px; }
.sw-stage.sw-active { border-color: var(--ss-accent); animation: sw-glow 2s infinite; }
.sw-arrow { text-align: center; color: var(--ss-text-3); line-height: 1; }
@keyframes sw-glow { 0%, 100% { box-shadow: 0 0 0 0 transparent; } 50% { box-shadow: 0 0 10px 1px var(--ss-accent); } }
.sw-chart { width: 100%; max-width: 420px; height: auto; display: block; background: var(--ss-surface); border: 1px solid var(--ss-line); border-radius: 4px; }
.sw-tick { width: 100%; font-size: 14px; border-collapse: collapse; }
.sw-tick th, .sw-tick td { text-align: left; padding: 4px 8px; border-bottom: 1px solid var(--ss-line); }
.sw-tech { margin-top: 1.6em; border: 1px solid var(--ss-line); border-radius: var(--ss-radius); padding: 8px 14px; }
.sw-tech summary { cursor: pointer; font-weight: 600; min-height: var(--ss-tap); display: flex; align-items: center; }
@media (prefers-reduced-motion: reduce) { .sw-l-live .sw-dot, .sw-stage.sw-active { animation: none; } }
</style>

## How to read it

- **The light at the top** says whether the search is running right now. Green and pulsing means numbers arrived in the last few minutes and the computer has search processes working. Amber means something is off. Red means no new numbers for a while: paused, the computer asleep, or an old snapshot. It checks by itself every minute; you never tap anything.
- **The path every star takes** is the same for every star. The step that is working right now glows.
- **The nine safety checks** are asked in order. A dip stopped by the first one never reaches the next. Most dips are stopped by the spacecraft-settling check, which is normal: that is where TESS data is worst.
- **Tier 1** is the only group kept for study. It is a list of dips with no known innocent cause, not a list of planets.
- **The self-test** pastes fake planets into every star-sector and checks that the machine still sees them. It is how we know the search is awake.
- **Blind mode** is used for the sealed stars: real and upside-down dips are pooled, so nobody sees the answer early.

What you will **not** see here: pictures of real dips or of why a particular star was stopped. That would mean opening real events, which needs your explicit yes. Charts of counts and speed are drawn from the numbers above.

!!! plain "In plain words"
    This page shows the search while it runs: how many stars are done, how many dips each safety check stopped, how many were kept, and a self-test that pastes fake planets into every star. It does **not** show pictures of real dips: real events stay on the computer, only counts are published. I do not look at each star by eye. Every star goes through exactly the same checks, which is what makes the result fair, and this page lets you watch those checks work. The page asks GitHub for new numbers every minute, so it changes by itself while you stay on it. The numbers can be about one to two minutes behind the computer.
