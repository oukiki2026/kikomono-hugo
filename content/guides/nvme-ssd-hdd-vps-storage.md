---
title: "NVMe, SSD or HDD: what VPS storage changes for a small website"
description: "Storage type shows up in database work, admin pages and restarts more than in static page delivery. Compare the three by workload, then separate disk speed from disk size before choosing a plan."
date: "2026-10-20"
lastmod: "2026-10-20"
weight: 34
guide_category: "hosting"
author: "Rita"
---
<section class="page-hero"><p class="eyebrow">HOSTING GUIDE</p><h1>NVMe, SSD or HDD: what VPS storage changes for a small website</h1><p class="lede">Storage type shows up in database work, admin pages and restarts more than in static page delivery. Compare the three by workload, then separate disk speed from disk size before choosing a plan.</p></section><article class="prose"><h2>Three kinds of storage, one job</h2>
<p>Every VPS plan stores your files, database and system on one of three technologies. An HDD keeps data on spinning magnetic platters and reads it with a moving head, so each request waits for physical movement. A SATA SSD stores data on flash chips with no moving parts, but talks to the computer through an interface designed in the hard-drive era. An NVMe drive also uses flash, but connects through PCI Express with a protocol designed for flash, so it can queue and complete far more small reads and writes at once.</p>
<p>The ranking is consistent: NVMe is fastest, SATA SSD is in the middle and HDD is slowest by a wide margin, especially at the small random reads a database performs. What varies is how much of that gap your particular website can feel.</p>
<h2>Where storage speed shows up — and where it does not</h2>
<p>A static page or image is usually served from memory, a cache or a content delivery network after the first read. For those requests the disk is barely involved, and upgrading storage changes little. Storage speed appears in the work behind the page instead.</p>
<div class="table-wrap"><table><thead><tr><th>Workload</th><th>Storage effect</th><th>What may matter more</th></tr></thead><tbody>
<tr><td>Static pages and images</td><td>Small after caching</td><td>Cache setup, CDN and network region</td></tr>
<tr><td>Database queries and site search</td><td>Large — many small random reads</td><td>Enough memory to hold the working set, indexed queries</td></tr>
<tr><td>Admin pages, logins and checkouts</td><td>Noticeable on busy dynamic sites</td><td>CPU time and application code</td></tr>
<tr><td>Backups, restores and reboots</td><td>Large — bulk reading and writing</td><td>Backup schedule and retention</td></tr>
<tr><td>Uploads and media processing</td><td>Moderate</td><td>CPU for resizing and encoding</td></tr>
</tbody></table></div>
<p>If your site is a generated publication, storage type is a minor line in the plan. If it runs a database-backed application that editors log into all day, storage is part of the daily experience, not a benchmark detail.</p>
<h2>Separate speed from size</h2>
<p>Plan pages put a number in gigabytes next to the storage type, and the two answer different questions. Type is about speed; gigabytes are about capacity. A fast small disk still fills up. A large slow disk is still slow.</p>
<p>Estimate capacity from what grows: the database, uploaded media, logs and the backups you keep on the server. Leave headroom for updates and for the temporary copies made during a restore. Running out of space stops a site as completely as any hardware failure, and it happens on NVMe exactly as it does on HDD.</p>
<h2>Read the plan label carefully</h2>
<p>Storage on a VPS is usually shared hardware, whatever the label says. An "NVMe" plan means the host machine uses NVMe drives; it does not promise you the full speed of a dedicated drive, because neighbours on the same machine read and write too. Peak figures in marketing copy are measured under ideal conditions that a shared plan will not reproduce.</p>
<p>Check what the provider actually documents: whether storage is local to the host or attached over a network, whether extra volumes can be added later, and whether the plan can move to a larger disk without a rebuild. Those operational answers matter more over a year than a one-line speed claim.</p>
<h2>A practical choice</h2>
<p>For most small websites, any SSD is enough and NVMe is a welcome default rather than a requirement. Choose NVMe when the price difference is small, when the site is database-heavy, or when slow admin pages are already a complaint. Accept HDD only for archival or backup roles, or when price is the whole decision and the workload is patient. Do not pay a storage premium while the plan is short of memory: a database that cannot hold its working set in RAM will be slow on any disk.</p>
<p>Finish by comparing the whole plan, not the storage line. Size the server with our <a href="/guides/how-to-choose-first-vps/">first VPS guide</a>, check current plans in the <a href="/compare/">verified offer comparison</a> and read the <a href="/guides/how-to-read-vps-promo-terms/">promotion checklist</a> before paying.</p>
<h2>Current provider records</h2><ul><li><a href="/providers/ionos/">IONOS current source status</a></li><li><a href="/providers/digitalocean/">DigitalOcean current source status</a></li><li><a href="/providers/hetzner/">Hetzner current source status</a></li></ul><h2>Sources</h2><ul><li><a href="https://www.ionos.com/servers/vps" rel="noopener">IONOS VPS features and purchase conditions</a></li><li><a href="https://docs.digitalocean.com/products/droplets/details/pricing/" rel="noopener">DigitalOcean Droplet billing</a></li><li><a href="https://docs.hetzner.com/cloud/servers/faq/" rel="noopener">Hetzner Cloud server FAQ</a></li></ul><p>Source review date: 2026-10-20. Based on the sources above, not a product performance test. Source links are non-affiliate links; check current terms before buying.</p><p><a href="/guides/">← All guides</a> · <a href="/methodology/">How we verify offers</a></p></article>
