import boto3


def connect_to_s3():
    s3 = boto3.resource(service_name = 's3',
                        aws_access_key_id = 'AKIAJGAAVB3G43YM54SQ',
                        aws_secret_access_key = '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')
    return s3
