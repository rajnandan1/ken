# Ken for Hermes installed

Enable it if you did not install with `--enable`:

```bash
hermes plugins enable ken
```

Restart Hermes or the gateway after enabling.

In shared gateways, restrict `/ken` to trusted users with Hermes slash-command access controls; runtime mode is process-local.

Commands:

- `/ken [lite|full|ultra|off]`
- `/ken-review [target]`
- `/ken-audit [target]`
- `/ken-debt`
- `/ken-gain`
- `/ken-help`

Bundled skills are available as `ken:ken`, `ken:ken-review`, `ken:ken-audit`, `ken:ken-debt`, `ken:ken-gain`, and `ken:ken-help`.
