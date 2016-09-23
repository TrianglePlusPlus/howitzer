This project links Square to our internal systems

## Configuring cronjobs

### half_hour_cron.sh

```bash
*/30 * * * * /home/thecorp/django/howitzer/square_connect/square_connect/half_hour_cron.sh >> /tmp/howitzer_cron.log
```
