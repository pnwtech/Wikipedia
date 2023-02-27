# Importing required module
import subprocess

# Using system() method to
# execute shell commands
subprocess.Popen(
    "awslocal dynamodb create-table --cli-input-json file://dynamodb/config.json",
    shell=True,
)
subprocess.Popen(
    "awslocal sqs create-queue --queue-name wikipedia",
    shell=True,
)
subprocess.Popen("chalice-local deploy", shell=True, cwd="./grow")
subprocess.Popen("chalice-local deploy", shell=True, cwd="./ingest")
