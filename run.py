import subprocess

subprocess.run(["python", "app/scripts/extractCsvFromXlsx.py"])
subprocess.run(["python", "app/scripts/combineCSVFiles.py"])
