# For example, you can run a backup of all your user accounts
# at 5 a.m every week with:
# 0 5 * * 1 tar -zcf /var/backups/home.tgz /home/
# m h  dom mon dow   command
*/7* * * * * export PYTHONPATH=$PYTHONPATH:/project_dir_path/ &&  ~/.virtualenvs/venv_name/python /project_dir_path/../withdraw_and_stake.py >> /cron_job/cron.log 2>&1
