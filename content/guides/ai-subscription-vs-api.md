---
title: "AI subscriptions, APIs and hosting are separate purchases"
description: "Trace who is using the model and where the request is billed before adding another subscription."
date: "2026-10-07"
lastmod: "2026-10-07"
weight: 33
guide_category: "hosting"
---
<section class="page-hero"><p class="eyebrow">AI COST GUIDE</p><h1>AI subscriptions, APIs and hosting are separate purchases</h1><p class="lede">Trace who is using the model and where the request is billed before adding another subscription.</p></section><article class="prose"><h2>Follow the request</h2>
<p>Start with who sends the request. An editor assistant helps you build software. A visitor using your deployed application may trigger a request from your server to an API. The server hosting that application is another service. Before purchasing, identify which account pays for each action instead of assuming a single AI subscription covers the entire project.</p>
<p>Cursor and GitHub Copilot publish their own plan conditions. A supported model inside one tool does not establish API entitlement with the model provider. Likewise, an API key does not automatically include an editor's paid features. Check the agreement for the exact product. This guide does not assert that any subscription grants unlimited model access.</p>
<h2>Make a purchase map</h2>
<div class="table-wrap"><table><thead><tr><th>Purchase</th><th>Who uses it?</th><th>What to verify</th></tr></thead><tbody>
<tr><td>Development assistant</td><td>You while building and reviewing</td><td>Included usage, editor compatibility and extra charges.</td></tr>
<tr><td>Model API</td><td>Your application or automation</td><td>Supported model, usage rates, request limits and data handling.</td></tr>
<tr><td>Hosting</td><td>The running website</td><td>Runtime, traffic, storage, recovery and renewal terms.</td></tr>
</tbody></table></div>
<h2>Do you need both subscriptions?</h2>
<p>Give each subscription a job. If two assistants both serve the same editing task, evaluate whether either has a distinct benefit you actually use. Test within their permitted entry plans when available. Do not buy a bundle simply because a model name is fashionable or because a promotion expires soon. Availability and plan limits can change, so confirm them on the official page at checkout.</p>
<h2>Separate fixed and variable spending</h2>
<p>Subscriptions may have recurring fees as well as variable usage. APIs can include different billing categories, and hosting may add storage or transfer charges. Keep these separate in your budget. If a visitor can trigger model calls, a predictable development subscription does not make your deployed feature's bill predictable.</p>
<p>Watch repeated requests and failed responses. Validate inputs before invoking a paid service, avoid unnecessary retries and decide where usage limits are enforced. Store credentials in a suitable server-side secret mechanism. Never put a private API key into a static page to make integration easier.</p>
<h2>Consider the end of the promotion</h2>
<p>Credits and temporary allowances are useful for evaluation, but they are not ongoing operating income. Decide what the application will cost or stop doing after they end. Record the source and expiry conditions for any credit you rely on. If those details are unknown, do not publish a savings claim or promise users permanent free access.</p>
<p>Connect this decision to the <a href="/ai-tools/ai-app-budget/">AI application budget</a>, <a href="/guides/evaluate-new-ai-model/">model-switch checklist</a> and <a href="/guides/vps-vs-managed-static-hosting/">hosting comparison</a>. Give each purchase a job and a line in the budget. Cancel overlapping tools you do not use.</p><h2>Current provider records</h2><ul><li><a href="/providers/ionos/">IONOS current source status</a></li><li><a href="/providers/digitalocean/">DigitalOcean current source status</a></li><li><a href="/providers/hetzner/">Hetzner current source status</a></li></ul><h2>Sources</h2><ul><li><a href="https://cursor.com/pricing" rel="noopener">Cursor plans</a></li><li><a href="https://github.com/features/copilot/plans" rel="noopener">GitHub Copilot plans</a></li><li><a href="https://ai.google.dev/gemini-api/docs" rel="noopener">Gemini API documentation</a></li></ul><p>Source review date: 2026-10-02. Based on the sources above, not a product performance test. Source links are non-affiliate links; check current terms before buying.</p><p><a href="/guides/">← All guides</a> · <a href="/methodology/">How we verify offers</a></p></article>
