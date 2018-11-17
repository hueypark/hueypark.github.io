---
title: Visual Studio Code debug speed up on Windows
date: 2018-05-14
tags: ["go", "vscode", "windows"]
---

On `Visual Studio Code`, `Go` debugging is very slow because that always rebuild everything.

If you set following settings on your `.vscode` folder `Visual Studio Code` will only build when changed.

<!--more-->

#### launch.json
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Launch",
            "type": "go",
            "request": "launch",
            "mode": "exec",
            "port": 2345,
            "host": "127.0.0.1",
            "program": "${workspaceRoot}/main.exe",
            "preLaunchTask": "build-debug",
            "env": {},
            "args": [],
            "showLog": true
        }
    ]
}
```

---

#### tasks.json
```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "build-debug",
            "type": "shell",
            "command": "vgo",
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "never",
                "focus": false,
                "panel": "shared"
            },
            "args": [
                "build",
                "-i",
                "-gcflags",
                "'-N -l'"
            ],
            "windows": {
                "args": [
                    "-o",
                    "main.exe",
                    "\"${workspaceRoot}\\main.go\""
                ]
            },
            "problemMatcher": [
                "$go"
            ]
        }
    ]
}
```
