import boto3
import traceback

def handler(event, _):
    print("Received event: " + str(event))
    params = event.get('params', {})
    response = {"requestId": event["requestId"], "status": "success"}
    try:
        ssm = boto3.client("ssm")
        ssm_path = params.get('Path', 'not-exists')
        
        parameters = ssm.get_parameters_by_path(Path=ssm_path)['Parameters']
        parameter_values = list(map(lambda param: param['Value'], parameters))

        response["fragment"] = parameter_values

    except Exception as e:
        traceback.print_exc()
        response["status"] = "failure"
        response["errorMessage"] = str(e)
    
    return response