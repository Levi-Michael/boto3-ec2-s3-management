import boto3, logging
from botocore.exceptions import ClientError

menu_options = {
    1: 'Create a EC2',
    2: 'Delete a EC2',
    3: 'EC2 information',
    4: 'Reboot EC2 instance',
    5: 'Trun off EC2',
    6: 'Exit',
}

ec2 = boto3.resource('ec2')


def print_menu():
    for key in menu_options.keys():
        print(key, '-', menu_options[key])
    print("")

def create_ec2():
    print('Handle option \'create_ec2\'')

    try:
        instances_name = input("Please enter instances name: ")
        instances_owner = input("Please enter instances owner name: ")
        instances_imageid = input("Please enter imageID(e.g.: ami-06c39ed6b42908a36): ")
        instances_mincount = int(input("Please enter numer for minimum count: "))
        instances_maxcount = int(input("Please enter numer for maxnimum count: "))
        instances_instancetype = input("Please enter a instance type(e.g.: t2.micro): ")
        instances_subnetid = input("Please enter a subnetid(e.g.: subnet-02406b0473c39ec2b): ")

        instances = ec2.create_instances(
                ImageId=instances_imageid,
                MinCount=instances_mincount,
                MaxCount=instances_maxcount,
                InstanceType=instances_instancetype,
                SubnetId=instances_subnetid,
                TagSpecifications=[
                    {
                        'ResourceType': 'instance',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': instances_name
                            },
                            {
                                'Key': 'Owner',
                                'Value': instances_owner
                            }
                        ]
                    }
                ]
        )
    except ClientError as e:
        logging.error(e)
        return False
    return True

def delete_ec2():
    print('Handle option \'delete_ec2\'')

    try: 
        list_id = 0

        print('Existing instances: ')
        for i in ec2.instances.all():
            list_id += 1
            print(f"{list_id}: {i.id}")

        ec2_for_terminate = input("Please enter ec2 instances ID: ")

        ids = []
        ids.append(ec2_for_terminate)

        ec2.instances.filter(InstanceIds = ids).terminate()
    except ClientError as e:
        logging.error(e)
        return False
    return True

def ec2_information():
    print('Handle option \'ec2_information\'')
    try: 

        print('Existing instances: ')
        for i in ec2.instances.all():

            print(f"\
                ID: {i.id}\n\
                Stat: {i.state}\n\
                Type: {i.instance_type}\n\
                Public IPv4: {i.public_ip_address}\n\
                AMI: {i.image.id}\n\
                ")
    except ClientError as e:
        logging.error(e)
        return False
    return True

def reboot_ec2():
    print('Handle option \'reboot_ec2\'')

    try:

        ec2_reboot = boto3.client('ec2')   
        ec2_list = boto3.resource('ec2')

        instances = []
        list_id = 0

        print('Existing instances: ')
        for i in ec2_list.instances.all():
            list_id += 1
            print(f"{list_id}: {i.id}")
        
        ec2_for_reboot = input("Please enter ec2 instances ID: ")

        instances.append(ec2_for_reboot)
        ec2_reboot.reboot_instances(InstanceIds=instances)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def stop_ec2():
    print('Handle option \'stop_ec2\'')

    try:

        ec2_stop = boto3.client('ec2')   
        ec2_list = boto3.resource('ec2')

        instances = []
        list_id = 0

        print('Existing instances: ')
        for i in ec2.instances.all():
            list_id += 1
            print(f"{list_id}: {i.id}")
        
        ec2_for_stop = input("Please enter ec2 instances ID: ")

        instances.append(ec2_for_stop)
        ec2_stop.stop_instances(InstanceIds=instances)
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
            create_ec2()
        elif option == 2:
            delete_ec2()
        elif option == 3:
            ec2_information()
        elif option == 4:
            reboot_ec2()
        elif option == 5:
            stop_ec2()
        elif option == 6:
            print('Thanks message before exiting')
            Exit()
            break
        else:
            print('Invalid option. Please enter a number between 1 and 6.')
