import epicbox

epicbox.configure(
    profiles=[
        epicbox.Profile('python', '3.11-alpine3.19')
    ]
)

limits = {
    # CPU time in seconds, None for unlimited
    'cputime': 2,
    # Real time in seconds, None for unlimited
    'realtime': 10,
    # Memory in megabytes, None for unlimited
    'memory': 128,
    # Limit the max processes the sandbox can have, -1 or None for unlimited(default)
    'processes': 5,
}

