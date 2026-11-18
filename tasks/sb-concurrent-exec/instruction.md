Use the Python already installed in this environment. Do not modify `/app/probe.py`.

Start every command below before any of them finishes. For each integer `i` from 0 through 79, run a separate command:

```
python3 /app/probe.py $i
```

Each command waits 5 seconds, then writes `/app/done/<i>`. That file must contain the index followed by a single newline. `/app/done/0` through `/app/done/79` must all exist.

You have 1800 seconds to complete this task. Do not cheat by using online solutions or hints specific to this task.
