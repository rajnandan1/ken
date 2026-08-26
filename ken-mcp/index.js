#!/usr/bin/env node
// Ken MCP server: serves the Thompson-mode ruleset over stdio as a prompt
// (user-invoked) and a tool (for hosts that pull context via tools). It does
// NOT replace the always-on adapters; it's the clean option for hosts whose
// only injection point is the prompt menu.
import fs from "node:fs";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

import { MODES, buildInstructions, resolveMode } from "./instructions.js";

const { version } = JSON.parse(
  await fs.promises.readFile(new URL("../package.json", import.meta.url), "utf8")
);
const server = new McpServer({ name: "ken", version });

const modeArg = z
  .enum(MODES)
  .optional()
  .describe("Ken intensity: lite, full, or ultra. Omit for the configured default.");

server.registerPrompt(
  "ken",
  {
    title: "Ken mode",
    description: "Thompson-mode instructions: think first, build bottom-up, brute force until measured, rewrite over patch.",
    argsSchema: { mode: modeArg },
  },
  ({ mode }) => ({
    messages: [{ role: "user", content: { type: "text", text: buildInstructions(mode) } }],
  }),
);

server.registerTool(
  "ken_instructions",
  {
    title: "Ken instructions",
    description: "Return the Ken ruleset for the given intensity (lite, full, or ultra).",
    inputSchema: { mode: modeArg },
    outputSchema: { mode: z.string(), instructions: z.string() },
    annotations: { readOnlyHint: true, openWorldHint: false },
  },
  ({ mode }) => {
    const resolvedMode = resolveMode(mode);
    const instructions = buildInstructions(resolvedMode);
    const structuredContent = { mode: resolvedMode, instructions };
    return { content: [{ type: "text", text: instructions }], structuredContent };
  },
);

await server.connect(new StdioServerTransport());
