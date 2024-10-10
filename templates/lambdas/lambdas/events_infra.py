import boto3
import botocore
import traceback

def handler(event, context):
    print("Received event: " + str(event))
    ecs_cluster = event['ECSClusterName']
    ecs_service = event['ECSServiceName']
    response = {"requestId": context.aws_request_id, "status": "success"}
    
    try:
        ecs = boto3.client('ecs')
        ecs_response = ecs.update_service(
            cluster=ecs_cluster,
            service=ecs_service,
            forceNewDeployment=True
        )
        print(ecs_response)
    except botocore.exceptions.ClientError as e:
        traceback.print_exc()
        response["status"] = "failure"
        response["errorDetails"] = "Failed to update ecs service by client error"
        response["errorMessage"] = str(e)

    except Exception as e:
        traceback.print_exc()
        response["status"] = "failure"
        response["errorDetails"] = "General Fail"
        response["errorMessage"] = str(e)
    
    print(response)
    return response