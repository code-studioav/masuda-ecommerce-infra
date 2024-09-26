"Handler lambda code for string array mapping"
import traceback
from enum import Enum

class Operation(Enum):
    ADD_PREFIX = 'ADD_PREFIX'
    ADD_SUFFIX = 'ADD_SUFFIX'
    REPLACE = 'REPLACE'

    @classmethod
    def has_value(cls_, value):
        return value in cls_._value2member_map_
    
    def apply(self, lst, *, prefix='', suffix='', old='', new=''):
        functions = {
            Operation.ADD_PREFIX.value: lambda lst, prefix, suffix, old, new: [f"{prefix}{item}" for item in lst],
            Operation.ADD_SUFFIX.value: lambda lst, prefix, suffix, old, new: [f"{item}{suffix}" for item in lst],
            Operation.REPLACE.value: lambda lst, prefix, suffix, old, new: [str(item).replace(old, new) for item in lst]
        }
        return functions[self.value](lst, prefix, suffix, old, new)


def handler(event, _):
    print("Received event: " + str(event))
    params = event.get('params', {})
    response = {"requestId": event["requestId"], "status": "success"}
    try:
        operation_name = params.get('Operation', 'not-exists')
        if not Operation.has_value(operation_name):
            raise Exception("Operation not found")
        
        operation = Operation(operation_name)
        input_list = params.get('InputArray', [])
        
        prefix = params.get('Prefix', '')
        suffix = params.get('Suffix', '')
        old = params.get('Old', '')
        new = params.get('New', '')

        response["fragment"] = operation.apply(
            input_list,
            prefix=prefix,
            suffix=suffix,
            old=old,
            new=new
        )

    except Exception as e:
        traceback.print_exc()
        response["status"] = "failure"
        response["errorMessage"] = str(e)
    
    return response