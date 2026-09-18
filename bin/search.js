#!/usr/bin/env node
const { spawn } = require('child_process');
const path = require('path');

const scriptPath = path.join(__dirname, '..', 'search');
const child = spawn('python3', [scriptPath, ...process.argv.slice(2)], {
  stdio: 'inherit'
});

child.on('exit', (code) => {
  process.exit(code ?? 0);
});
