# use-runway-api

Maintainer direct-API transport for Runway media generation and task polling, with request bodies built from the current model-specific API contract.

**ID:** `runwayml--use-runway-api` · **Tier:** supporting
**Evidence:** path-and-metadata-inspected · **Runtime tested:** no · **Checked:** 2026-10-12
**Portability:** agent-portable · **Provider scope:** runway
**Prerequisites:** node-20-plus, runway-api-key
**Model binding:** live schema; no embedded model list

[Pinned upstream SKILL.md](https://github.com/runwayml/skills/blob/e3dffc15498e9588e7815f37b9ecf10e8bc2c902/skills/use-runway-api/SKILL.md)
Repository revision: `e3dffc15498e9588e7815f37b9ecf10e8bc2c902`
File SHA-256: `53dedb3d19fb0f61966e02ce156630b5151347e5658a7a1ee94c41f2fb18a193`
Repository license: MIT; skill-declared license: not found.

## Before use

- The colocated Node runtime is a generic HTTP transport, not an embedded model catalog. Resolve gen4.5 and aleph2 request fields from current direct Runway API documentation before submission.
- Uses RUNWAY_SKILLS_API_SECRET and the Runway developer API; account availability, cost and generation quality were not tested. Consumer Runway MCP tools are a separate surface.
- The inspected runtime retries all HTTP methods, including generation POST, after some errors without an idempotency key. Audit retry behavior and inspect uncertain jobs before resubmitting a paid request.
- Static source inspection only; dependencies, rendering, listening and paid endpoints were not executed.

Read the whole upstream skill directory and its dependencies. Audit instructions/scripts and licensing before installation. The pinned link is evidence, not an instruction to execute it automatically.
