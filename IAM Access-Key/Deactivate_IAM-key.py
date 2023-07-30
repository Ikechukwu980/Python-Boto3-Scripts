import boto3
from datetime import datetime, timezone

client = boto3.client("iam")

paginator = client.get_paginator("list_users")

current_date = datetime.now(timezone.utc)

maximum_key_age = 28

for response in paginator.paginate():
    for user in response["Users"]:
        username = user["UserName"]

        list_key = client.list_access_keys(UserName = username)
        for accesskey in list_key["AccessKeyMetadata"]:
            access_key_id = accesskey["AccessKeyId"]
            key_creation_date = accesskey["CreateDate"]
            age = (current_date - key_creation_date).days
            if age > maximum_key_age:
                print("Deactivate key for the following user:", username)
                client.update_access_key(
                    UserName =username,
                    AccessKeyId = access_key_id,
                    Status = "Inactive"
                )

