# -*- coding: utf-8 -*-
"""
Salaah Time.

Configuration parameters:
    longitude: longitude of your city
    latitude: latitude of your city
    timezone: timezone of your country (GMT+n)
    fajr_isha_method:  Fajr and Ishaa reference (default 3)
    asr_fiqh: Asr madhab (default 1)
    format_time: The format for time-related placeholders. May use any Python strftime directives for times. (default ‘%I:%M %p’)
    cache_timeout: refresh interval for this module, default 15 minutes (default 900)
    thresholds = change module color to urgent when remaining time reached the threshold, default 30 minutes (default 1800)

Notes:
   the Fajr and Ishaa reference:
   1 = University of Islamic Sciences, Karachi
   2 = Muslim World League
   3 = Egyptian General Authority of Survey
   4 = Umm al-Qura University, Makkah
   5 = Islamic Society of North America

   the Asr Madhab:
   1 = Shafii
   2 = Hanafi

Format placeholders:
    {format} format for salaah_time

Examples:
```
salaah_time {
   format = "{salaah_name} {salaah_time}"
   format_time = "%I:%M %p"
   longitude = 32.859741
   latitude = 39.933365
   timezone = 3
   fajr_isha_method = 3
   asr_fiqh = 1
}
```

@author azzamsa <https://github.com/azzamsa>
@license GPLv3 <https://www.gnu.org/licenses/gpl-3.0.txt>

SAMPLE OUTPUT
{'full_text': 'fajr 04:05 AM'}
"""

from datetime import date, datetime
from pyIslam.praytimes import PrayerConf, Prayer


def dt_combine(time_):
    dt_time = datetime.combine(date.today(), time_)
    return dt_time


def get_higher_times(salaahs_time):
    higher_times = []
    dt_now = dt_combine(datetime.now().time())

    for salaah in salaahs_time:
        time_ = salaahs_time[salaah]
        dt_time = datetime.combine(date.today(), time_)

        if dt_time > dt_now:
            higher_times.append(time_)

    return higher_times


def get_closest_time(higher_times):
    closest_time = None
    dt_now = dt_combine(datetime.now().time())

    if higher_times:
        closest_time = min(
            higher_times, key=lambda x: abs(datetime.combine(date.today(), x) - dt_now)
        )
    return closest_time


def get_salaahs_time(longitude, latitude, timezone, fajr_isha_method, asr_fiqh):
    pconf = PrayerConf(longitude, latitude, timezone, fajr_isha_method, asr_fiqh)
    pt = Prayer(pconf, date.today())

    salaahs_time = {
        "fajr": pt.fajr_time(),
        "sherook": pt.sherook_time(),
        "dohr": pt.dohr_time(),
        "asr": pt.asr_time(),
        "maghreb": pt.maghreb_time(),
        "ishaa": pt.ishaa_time(),
    }
    return salaahs_time


def get_upcoming_salaah(salaahs_time, time_key):
    # if time_key == None, it's more than isya
    if not time_key:
        upcoming_salaah = "fajr", salaahs_time["fajr"]
        return upcoming_salaah

    # find the salaah name according to given key
    salaah_name = list(salaahs_time.keys())[list(salaahs_time.values()).index(time_key)]
    upcoming_salaah = salaah_name, salaahs_time[salaah_name]

    return upcoming_salaah


def get_remaining_time(upcoming_salaah_time):
    dt_now = dt_combine(datetime.now().time())
    dt_upcoming_salaah = dt_combine(upcoming_salaah_time)
    remaining_time = dt_upcoming_salaah - dt_now

    return remaining_time


def _main(longitude, latitude, timezone, fajr_isha_method, asr_fiqh):
    salaahs_time = get_salaahs_time(
        longitude, latitude, timezone, fajr_isha_method, asr_fiqh
    )
    higher_times = get_higher_times(salaahs_time)
    closest_time = get_closest_time(higher_times)

    upcoming_salaah = get_upcoming_salaah(salaahs_time, closest_time)
    return upcoming_salaah


class Py3status:
    format = "{salaah_name}:{salaah_time}"
    format_time = "%I:%M %p"
    longitude = 106.834091
    latitude = -6.186486
    timezone = 7
    fajr_isha_method = 3
    asr_fiqh = 1
    cache_timeout = 900
    thresholds = 1800
    button = 1

    def _check_urgency(self, thresholds, upcoming_salaah_time):
        urgency = False
        dt_now = dt_combine(datetime.now().time())
        dt_upcoming_salaah = dt_combine(upcoming_salaah_time)
        time_delta = dt_upcoming_salaah - dt_now

        if time_delta.total_seconds() < thresholds:
            urgency = True

        return urgency

    def _format_remaining_time(self, remaining):
        remaining_hour = remaining.seconds // 3600
        remaining_minutes = (remaining.seconds // 60) % 60
        remaining_fmt = f"{remaining_hour}h"
        if remaining_hour < 1:
            remaining_fmt = f"{remaining_minutes}m"
        print(remaining_fmt)
        return remaining_fmt

    def salaah_time(self):
        upcoming_salaah = _main(
            self.longitude,
            self.latitude,
            self.timezone,
            self.fajr_isha_method,
            self.asr_fiqh,
        )
        salaah_name = upcoming_salaah[0]
        salaah_time_ = upcoming_salaah[1]

        if self.button == 1:
            remaining = get_remaining_time(salaah_time_)
            remaining_fmt = self._format_remaining_time(remaining)
            salaah_time_fmt = remaining_fmt
        if self.button == 0:
            salaah_time_fmt = salaah_time_.strftime(self.format_time)

        salaah_data = {"salaah_name": salaah_name, "salaah_time": salaah_time_fmt}
        salaah = self.py3.safe_format(self.format, salaah_data)
        # urgency = self._check_urgency(self.thresholds, salaah_time_)

        color = None
        # if urgency:
        #     color = self.py3.COLOR_BAD

        return {
            "full_text": salaah,
            "color": color,
            "cached_until": self.py3.time_in(self.cache_timeout),
        }

    def on_click(self, event):
        if self.button == 0:
            self.button = 1
        else:
            self.button = 0


if __name__ == "__main__":
    """
    Run module in test mode.
    """
    from py3status.module_test import module_test

    module_test(Py3status)
