import { chromium } from "playwright";
import fs from "node:fs";
import path from "node:path";
import readline from "node:readline";

const taskDir = path.resolve(process.argv[2] || "");
const configPath = path.resolve(process.argv[3] || "gui/config.json");
const instructionPath = path.join(taskDir, "instruction.md");
const probePath = path.join(taskDir, "inputs", "probe.py");

if (!fs.existsSync(instructionPath)) {
  console.error("用法: node gui/send-task.mjs tasks/sb-tool-calls");
  process.exit(1);
}
if (!fs.existsSync(configPath)) {
  console.error("先复制 gui/config.example.json 为 gui/config.json，填上你的界面地址和按钮位置。");
  process.exit(1);
}

const config = JSON.parse(fs.readFileSync(configPath, "utf8"));
const instruction = fs.readFileSync(instructionPath, "utf8");
const taskName = path.basename(taskDir);
const runDir = path.resolve("runs", taskName, "output");
fs.mkdirSync(runDir, { recursive: true });

const browser = await chromium.launch({ headless: false });
const page = await browser.newPage();
await page.goto(config.url);

if (config.fileSelector && fs.existsSync(probePath)) {
  await page.setInputFiles(config.fileSelector, probePath);
}
await page.fill(config.inputSelector, instruction);

const startedAt = new Date();
await page.click(config.sendSelector);
console.log(`已发送 ${taskName}。开始时间 ${startedAt.toISOString()}`);

let endedAt;
if (config.doneSelector) {
  await page.waitForSelector(config.doneSelector);
  endedAt = new Date();
} else {
  await new Promise((resolve) => {
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    rl.question("界面上做完之后，回到这里按回车。\n", () => {
      rl.close();
      resolve();
    });
  });
  endedAt = new Date();
}

const timing = {
  task: taskName,
  started_at: startedAt.toISOString(),
  ended_at: endedAt.toISOString(),
  elapsed_seconds: (endedAt - startedAt) / 1000,
};
const timingPath = path.join(runDir, "timing.json");
fs.writeFileSync(timingPath, JSON.stringify(timing, null, 2) + "\n");
console.log(`用时 ${timing.elapsed_seconds.toFixed(1)} 秒。把 ${timingPath} 放进这一题的 output/，和产物放在一起，再交给核对的模型。`);
await browser.close();
