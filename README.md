# Salaah Time for Py3status

## Docs

See the docs string

## Examples configuration

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


## Credit:

This module depends on [pyIslam library](https://github.com/abougouffa/pyIslam), make sure it's installed.
