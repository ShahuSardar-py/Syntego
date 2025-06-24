#!/bin/bash
CRON_COMMAND="php $(pwd)/cron.php >/dev/null 2>&1"
CRON_JOB="0 9 * * * $CRON_COMMAND"
(crontab -l | grep -v -F "$CRON_COMMAND" ; echo "$CRON_JOB") | crontab -
echo "CRON job scheduled to run every 24 hours."
