from discord.ext import commands, tasks
import datetime
import pytz


class TimerChecker(commands.Cog):
    def __init__(self, data):
        self.data = data
        self.timeZone = pytz.timezone("America/New_York")
        self._timeReset = datetime.datetime(2011, 8, 15, 0, 0, 0, 0, self.timeZone)
        self.timeChecker.start()

    def cog_unload(self):
        self.timeChecker.cancel()

    @tasks.loop(seconds=60)
    async def timeChecker(self):
        now = datetime.datetime.now(tz=self.timeZone)
        if now.hour == self._timeReset.hour and now.minute == self._timeReset.minute:
            self.data.usersID_mapping.clear()
            self.data.saveMapping()

    def getTimeUntilNextReset(self):
        now = datetime.datetime.now(tz=self.timeZone)
        self._timeReset = datetime.datetime(now.year, now.month, now.day + 1,
            self._timeReset.hour,
            self._timeReset.minute,
            self._timeReset.second,
            self._timeReset.microsecond,
            self.timeZone
        )
        return str(self._timeReset - now).split(".")[0]