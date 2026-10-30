# Search window

<p class="ss-meta">Watch the search · refreshes by itself · counts only</p>

!!! plain "In plain words"
    This page shows the search while it runs: how many stars are done, how many dips each safety check stopped, how many were kept, and a self-test that pastes fake planets into every star. It does **not** show pictures of real dips, and it never will without your yes: real events stay on the computer, only counts are published. I do not look at each star by eye. Every star goes through exactly the same checks, which is what makes the result fair, and this page lets you watch those checks work.

<div id="ss-watch" class="sw">Loading...</div>

<style>
.sw { max-width: 760px; }
.sw-head { display: flex; justify-content: space-between; gap: 12px; align-items: center; flex-wrap: wrap; }
.sw-pill { background: var(--ss-raised); border: 1px solid var(--ss-line); border-radius: 999px; padding: 6px 14px; font-weight: 600; }
.sw-pill.sw-finished { border-color: var(--ss-accent); }
.sw-upd, .sw-small { color: var(--ss-text-2); font-size: 14px; }
.sw-label { margin: .6em 0; color: var(--ss-text-2); }
.sw-blind { background: var(--ss-surface); border-left: 4px solid var(--ss-accent); padding: 10px 14px; border-radius: var(--ss-radius); }
.sw h3 { margin-top: 1.6em; }
.sw-row, .sw-flag { margin: 10px 0; }
.sw-lab { display: flex; justify-content: space-between; gap: 12px; font-size: 15px; }
.sw-bar { background: var(--ss-surface); border: 1px solid var(--ss-line); border-radius: 4px; height: 12px; overflow: hidden; }
.sw-bar i { display: block; height: 100%; background: var(--ss-text-3); transition: width .6s; }
.sw-bar.sw-keep i, .sw-row .sw-bar i { background: var(--ss-accent); }
.sw-tick { width: 100%; font-size: 14px; border-collapse: collapse; }
.sw-tick th, .sw-tick td { text-align: left; padding: 4px 8px; border-bottom: 1px solid var(--ss-line); }
</style>

## How to read it

- **The three bars** are the three passes: the light curves, their raw-light twins, and a second look at any dip that only the raw light shows.
- **The checks** are the safety filters, in the order they are asked. A dip stopped by the first one never gets to the next. Most dips are stopped by the spacecraft-settling check, which is normal: that is where TESS data is worst.
- **Tier 1** is the only group that is kept for study. It is a list of dips with no known innocent cause, not a list of planets.
- **The self-test** pastes fake planets into every star-sector and checks that the machine still sees them. It is how we know the search is awake.
- **Blind mode** is used for the sealed stars: real and upside-down dips are pooled, so nobody sees the answer early.

*What this page cannot show:* a picture of why a particular dip was stopped. That would mean opening real events, which needs your explicit yes. For a picture of how each check works, use the chapters on the [detector](book/08-our-detector.md) and [vetting](book/10-vetting.md).
