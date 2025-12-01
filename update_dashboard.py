import subprocess

print("🔄 Running ETL Pipeline...")
subprocess.run(["python", "banks_project.py"])

print("📊 Generating Dashboard...")
subprocess.run(["python", "dashboard.py"])

print("✅ Done! Open dashboard.html to view")