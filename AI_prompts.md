# AI Prompt Log — Homework 5

This file records the prompts actually used while completing Homework 5. It will be updated as each problem is completed. Do not add prompts that were not actually entered.

## Homework 5 setup instruction

**Prompt actually entered:**

> for each problem, record its number, titile, my actual prompt, any follow up prompt and waht was missig from the first attempt. keep the file updaete as we work through each problem

This instruction establishes the documentation format. Problem-specific prompts will be added to the corresponding sections below as they are entered.

## Problem 1 — Vibe Coder Prompts

**Prompt 1 (actually entered):**

> for each problem, record its number, titile, my actual prompt, any follow up prompt and waht was missig from the first attempt. keep the file updaete as we work through each problem.
>
> this is the problem1

**Follow-up prompt(s):** None yet.

**What was missing from the first attempt:** Not applicable yet.


## Problem 2 — Study the Campus Customs database

**Prompt 1 (actually entered):**

> here is problem 2 , and title is Study the Campus Customs database. extract data.zip in the homework 5 folder and inspect all tables and columms in campus_customs.db. create data/campus_customs_new.db wihtout changing the original. examine the three open tickets and how they relate to other tables. create output/harness.md listing each table, its columns, and why it matters for the agents.

**Follow-up prompt(s):** None yet.

**Follow-up prompt 2 (actually entered):**

> do the actual database inspection

**What was missing from the first attempt:** The initial prompt described the required database inspection and deliverables, but the actual extraction, schema inspection, open-ticket relationship analysis, copied database creation, and verification still needed to be performed.

## Problem 3 — Build the MCP server

**Prompt 1 (actually entered):**

> here is problem 3, Build the MCP server, create an MCP server using FastMCP in mcp_server/ with data/campus_customs_new.db. build three clearly named tools based on the actual database records to help reslove tickets 101, 102 and 103. do not invent data or modify the original database. update output/harness.md with each tool's name,tables used, related ticket and a specific explanaation of why if help. create mcp_server/README.md explaing the server,database and tools

**Follow-up prompt(s):** None yet.

**What was missing from the first attempt:** Not applicable yet; the MCP server implementation and verification have now been completed.

**Follow-up prompt 2 (actually entered):**

> review problem 3 and meke sure the three MCP tools have descriptive names based on their actual function not just ticket number. verify that each tool uses the correct database tables and that output/harness.md expalin how eash tool help it specific ticket

**What was missing from the first attempt:** The first implementation used ticket-number-only names. The review required descriptive function-based names and clearer documentation of each tool's exact tables and ticket-specific purpose.

## Problem 4 — Add the MCP server to Vibe Coder and test each tool

**Prompt 1 (actually entered):**

> for problem4 , Add the MCP server to vibe coder and test each tool, connect the MCP sever from probelm 3 to code using .mcp.json i. the homework5 project root. install any missing dependence and verify the connection. then actually invoke all three mcp tools through the connected mcp server and save the test prompts, tool name and real outputs in output/mcp_smoke.json. verfy every output against data/campus_customs_new.db.

**Follow-up prompt(s):** None yet.

**What was missing from the first attempt:** The requested MCP root configuration, compatible dependency, connected invocation of all three tools, real output capture, and database verification have now been completed.

## Problem 5 — Build the agent team and grow the MCP tools

**Prompt 1 (actually entered):**

> for probmle 5, Build the agent team and grow the MCP tools. create five pydanticai agent (Boss, inventory, accounting, facilities, cutsomer service) with detailed role-specific prompts. models, loops and full mutual delegation. use only gpt-6-luna via portley.
> extend mcp tools for all three open tickets, using only data/campus_customs_new.db through mcp. enfore all shol rules, expecially human payment approval and cash limits.
> append detailed logs to output/audit_trail.json.updata backend/prompts/, backend/model.py, output/harness.md(agent, tools, tables,safety. token limits), mcp_server/README.md and AI_prompts

**Follow-up prompt(s):** None yet.

**What was missing from the first attempt:** The request required a new five-agent backend, role prompts, bounded mutual delegation, Portkey model configuration, MCP-only evidence access, payment/cash safety rules, audit logging, and cross-file documentation; these have now been added.

**Follow-up prompt 2 (actually entered):**

> review problem5 and ensure there is one separate promptfile for each fo the five agents in backend/prompts/. also ensure the data type are in backend/models.py as required. preseve all existingncunctionally.

**What was missing from the first attempt:** The initial implementation had one shared prompt file and no `backend/models.py` data contracts. Separate role prompts and typed shared models were required while preserving the existing MCP and delegation behavior.

## Problem 6 — Plan the three tickets

**Prompt 1 (actually entered):**

> here is problem 6. the title is Plan the three tickets.
>
> create output/desk_tickets.html with separate tabs for tickets 101, 102 and 103 plus empty Cash and Reflection tabs.
>
> for each ticket, use the actual database information to write a detailed Expected section explaining;
>
> 1. which agent Boss should call first and why,
> 2. the complete expected delegation sequence between relevandt agents.
> 3. which MCP tools should be used and why.
>
> make each plan specific to its ticket, donot invlove unnsecessary agents or invent data. leave the actul sections empty for later comparison.

**Follow-up prompt(s):** None yet.

**What was missing from the first attempt:** Not applicable; the ticket plans and empty comparison sections were created from the verified database and MCP records.

## Problem 7 — Backend routes

**Prompt 1 (actually entered):**

> here is problem7. the title is Backend routes.
> implement all six required FastAPI routes in backend/main.py follwing panel A and B. use the existing agents and mcp tools, require human approval for payments and preserve the original database. test the routes, document them in output/harness.md

**Follow-up prompt 2 (actually entered):**

> complete the remainging problme 7 requiments. add endpoints for agent evet history, human-approved payment execution, checking balance, and database reset. preserve exisiting functionality, test every route.

**Follow-up prompt 3 (actually entered):**

> verify that the homework 5 backend actully runs on port 8000 and that all problme 7 endpoints work over HTTP. fix any issue and report the test results

**Follow-up prompt 4 (actually entered):**

> investiage and fix the portkey connection issue causing /agent to return 503. veify a successful end to end agent run without bypassing the actual model

**Follow-up prompt 5 (actually entered):**

> stop the unrelated lecture 7 server on port 8000, then start the homework 5 backend on port 8000. veify that /agent and all required api routes work. donot modify kecture 7 files

**Follow-up prompt(s):** None yet.

**What was missing from the first attempt:** The Portkey request used an incompatible reasoning setting for function tools, causing the live agent call to fail. The provider-specific setting is now corrected, and a genuine Portkey → PydanticAI → MCP end-to-end run succeeds. Port 8000 was then freed by stopping only the unrelated Lecture 7 process; the Homework 5 backend now serves that port.

## Problem 8 — React + Vite + TypeScript operations dashboard

**Prompt 1 (actually entered):**

> i want a polished React + Vite + TypeScript dashboard in frontend/ that lists all three tickets, runs agents on a selected tickets, shows live agent activity and summaries, marks tickets resolved, supports human payment approval and displays the checking balance. connect it to localhost:8000, configure CORS for localhost:5173, and create output/design.md. run and test the dashbord.

**Follow-up prompt(s):** None yet.

**What was missing from the first attempt:** Not applicable; the dashboard, CORS configuration, resolution endpoint, live agent activity, payment controls, design documentation, and build verification were added.

**Follow-up prompt 2 (actually entered):**

> the dashboard at localhost:5173 shows a blank white page. find and fix the frontend error, then verify the dashboard actually renders and works

**What was missing from the first attempt:** The React app defined `App` but never mounted it with `createRoot`, and the backend CORS list did not include the `127.0.0.1:5173` loopback origin used during the browser test. Both issues were fixed and verified with Chromium.

**Follow-up prompt 3 (actually entered):**

> show each agent's individual activity and summary inthe dashboard, not just agent started and complted. verify the display works without breaking exisiting features

**What was missing from the first attempt:** The audit trail only recorded high-level agent lifecycle events. Agent delegation, MCP lookup/evidence, and specialist summary events are now appended with agent names and displayed in the selected-ticket activity panel.

## Problem 9 — Resolve the Tickets

**Prompt 1 (actually entered):**

> here is problem 9. the title is Resolve the Tickets.
> iwanna reset the working database, resolove teickets 101,102and 103 using real agents and doucment the results. track agents contributions, tools, human approval and exact cash changes. update desk_tickets.html, resolved_tickets.json, resolved_board.html with screenshots, audit_trail.json and harness.md. verify the ending balance against cash_accouts

**Follow-up prompt(s):** None yet.

**What was missing from the first attempt:** Not applicable; the working copy was reset, all three real agent analyses were captured before resolution, ticket statuses were updated, no unapproved payment was executed, cash was verified at $3,400, and all requested reports/screenshots were created.

## Problem 10 — Reflection

**Prompt 1 (actually entered):**

> here is problem10. the title is Reflection. complete all five reflection questions in output/desk_tickets.html useing my view.
> 101:the agents identified zero inventory, supplier lead time, and an unpaid $840 invoice but did not restock the shirt.
> 102:accouting checks were useful, and withholding payment without human approval was appropriate.
> 103: cross-department checks helped but discount require margin and approval-authority checks.
> expected VS actual : i expected concreate soultions, but agents mainly gathered evidence and made recommendations. all tickets were marked resloved although business isuues may remain.
> one agent could handle simple inventory or invoice lookups;cross-department issues benefit from mutiple agents.
> three solvable problme:inventory inquires, unpaid invoice checks and order inquires. three requring new tools:automatic purchasing (supplier api), customer notification(email tool), and discount approval (margin calculation and approval workflow).
> verify each claim against actual logs, explain any discrepancies and preserve my opionn

**Follow-up prompt(s):** None yet.

**What was missing from the first attempt:** Not applicable; all five reflection questions were completed in the desk, cross-checked against the audit and resolution records, and the user’s conclusions were preserved with discrepancies explained.

## Problem 11 — GitHub Submission

**Prompt 1 (actually entered):**

> here is problem 11. the title is GitHub Submission.
> prepare homework5 for submission to a public GitHub repsository. verify the required file stracture, create a safe .gitignore and .env.example and complete README.md with setup , startup, and database reset instrauction. include both database files and all required output. never expose api keys or the real .env. check everything before publishing, then help me publish the repository and save its URL to output/github_url.txt.

**Follow-up prompt(s):** None yet.

**What was missing from the first attempt:** The submission metadata, safe environment template, README, and final public-repository verification were not yet prepared. The package is now prepared; publishing and saving a URL still require the destination GitHub repository URL and user authorization to push.
