# Salaah Time for Py3status

Shows next salaah time in py3status

## Feature

- Show next salaah time
- Show remaining salaah time (toggled with mouse click)
- Change module color when reached thresholds of remaining time

## Docs

See the docs string

## Examples configuration

Basic:

``` yaml
salaah_time {
   longitude = 32.859741
   latitude = 39.933365
   timezone = 3
   fajr_isha_method = 3
   asr_fiqh = 1
}
```

Advanced:

``` yaml
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

## Sample Output

{'full_text': 'fajr 04:05 AM'}

![image](https://user-images.githubusercontent.com/17734314/68909529-2ddf3580-0781-11ea-8df9-1ae13f3a676d.png)

![image](https://user-images.githubusercontent.com/17734314/68909541-38013400-0781-11ea-8f70-f6815db4dcc1.png)

## Credit:

This module depends on [pyIslam library](https://github.com/abougouffa/pyIslam), make sure it's installed.
