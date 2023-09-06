import datetime

def format_seconds(seconds):
    tdelta = datetime.timedelta(seconds=seconds)
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    fmt = "{days} dias {hours}h {minutes}m {seconds}s"
    return fmt.format(**d)