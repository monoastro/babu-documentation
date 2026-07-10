from datalab_sdk import DatalabClient

client = DatalabClient()

execution = client.run_pipeline( "pl_e0lrR7w92R3c", file_path="data/aditya.png")

execution = client.get_pipeline_execution( execution.execution_id, max_polls=300, poll_interval=2)
result = client.get_step_result(execution.execution_id, step_index=1)
print(f"{result}")
