import boto3, logging, os
from botocore.exceptions import ClientError

menu_options = {
    1: 'Bucket List',
    2: 'Create a Bucket',
    3: 'Delete a Bucket',
    4: 'Delete a file from a Bucket',
    5: 'Add a file to Bucket',
    6: 'Exit',
}


def print_menu():
    for key in menu_options.keys():
        print(key, '-', menu_options[key])
    print("")

def print_bucket_list():
    print('Handle option \'print_bucket_list\'')

    try:
        s3 = boto3.resource('s3')
        bucket_number = 0

        print('Existing buckets: ')
        for bucket in s3.buckets.all():
            bucket_number += 1
            print(f"{bucket_number}: {bucket.name}")
        print("")

    except ClientError as e:
        logging.error(e)
        return False
    return True

def create_bucket():
    print('Handle option \'create_bucket\'')
    bucket_name = input('Please enter bucket name: ')
    bucket_region = input('Please enter bucket region: ')

    try:
        if bucket_region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=bucket_region)
            location = {'LocationConstraint': bucket_region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def delete_bucket():
    print('Handle option \'delete_bucket\'')

    print_bucket_list()
    try:
        client = boto3.client('s3')

        bucket_for_delete = input('Please enter bucket name for delete: ')
        response = client.delete_bucket(Bucket=bucket_for_delete)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def delete_file():
    try:
        print('Handle option \'delete_file\'')
        
        bucket_name = input('Please enter bucket name: ')
        s3 = boto3.resource('s3')

        my_bucket = s3.Bucket(bucket_name)
        file_number= 0
        for file in my_bucket.objects.all():
            file_number += 1
            print(f"{file_number}: {file.key}")

        file_name = input('Please enter file name for delete: ')

        s3.Object(bucket_name, file_name).delete()
    except ClientError as e:
        logging.error(e)
        return False
    return True

def add_file():
    print('Handle option \'add_file\'')
    
    print_bucket_list()

    bucket_name = input('Please enter bucket name: ')
    file_name = input('Please enter file name with path: ')
    object_name = input('Please enter AWS file display name: ')

    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket_name, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def Exit():
    print('Handle option \'Exit\'')

if __name__=='__main__':
    while(True):
        print_menu()
        option = ''
        try:
            option = int(input('Enter your choice: '))
        except:
            print('Worng input, Please enter a number')
        
        if option == 1:
            print_bucket_list()
        elif option == 2:
            create_bucket()
        elif option == 3:
            delete_bucket()
        elif option == 4:
            delete_file()
        elif option == 5:
            add_file()
        elif option == 6:
            print('Thanks message before exiting')
            Exit()
            break
        else:
            print('Invalid option. Please enter a number between 1 and 6.')