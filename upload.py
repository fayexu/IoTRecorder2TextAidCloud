import time
import boto3


def upload_to_aws(local_file, bucket, s3_file):
	s3 = boto3.client('s3',region_name='us-west-2')
	try:
		s3.upload_file(local_file, bucket, s3_file)
		print("Upload Successful")
		return True
	except FileNotFoundError:
		print("The file was not found")
		return False
	except NoCredentialsError:
		print("Credentials not available")
		return False


def main():
	bucket_name = 'cc2021project'
	is_uploaded = upload_to_aws('audio-1.m4a', bucket_name, 'audio_1.m4a')
	print (is_uploaded)


if __name__ == '__main__':
	main()
