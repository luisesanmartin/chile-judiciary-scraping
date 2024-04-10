import subprocess

for _ in range(20):

    subprocess.run(['python', r'.\main_details_data_table.py'])
    try:
        subprocess.run(['python', r'.\detail-tables-progress-report.py'])
    except:
        pass
